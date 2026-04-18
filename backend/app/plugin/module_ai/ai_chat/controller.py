import asyncio
import base64
import hashlib
import json
import math

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from fastapi import APIRouter, Body, Depends, Path, Request
from fastapi.responses import JSONResponse, StreamingResponse
from redis.asyncio.client import Redis

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import SuccessResponse
from app.config.setting import settings
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import BatchSetAvailable
from app.core.dependencies import AuthPermission
from app.core.dependencies import redis_getter
from app.core.logger import log
from app.core.redis_crud import RedisCURD
from app.plugin.module_ai.agno.agno_provider import AgnoProvider
from .schema import (
    AiChatCompletionSchema,
    AiChatCompletionSaveSchema,
    AiChatCompletionStopSchema,
    AiChatCreateSchema,
    AiChatQueryParam,
    AiChatUpdateSchema,
)
from .service import AiChatService
from .stream_manager import AiChatStreamManager

AiChatRouter = APIRouter(prefix="/ai_chat", tags=["ai_chat模块"])


def _evp_bytes_to_key(
        password: bytes, salt: bytes, key_len: int, iv_len: int
) -> tuple[bytes, bytes]:
    derived = b""
    previous = b""
    while len(derived) < key_len + iv_len:
        previous = hashlib.md5(previous + password + salt).digest()
        derived += previous
    return derived[:key_len], derived[key_len: key_len + iv_len]


def decrypt_aisaas_api_key(ciphertext: str | None) -> str:
    if not ciphertext:
        return ""
    try:
        raw = base64.b64decode(ciphertext)
        if raw[:8] != b"Salted__":
            return ciphertext
        salt = raw[8:16]
        key, iv = _evp_bytes_to_key(settings.SASS_SECRET_KEY.encode("utf-8"), salt, 32, 16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(raw[16:]), AES.block_size)
        text = decrypted.decode("utf-8")
        return text or ciphertext
    except Exception:
        return ciphertext


def _get_auth_user_id(auth: AuthSchema) -> int:
    return auth.user.id if auth.user else 0


def _estimate_message_tokens(message: dict[str, str]) -> int:
    content = str(message.get("content") or "")
    if not content:
        return 0

    ascii_count = sum(1 for char in content if ord(char) < 128)
    non_ascii_count = len(content) - ascii_count
    return max(1, non_ascii_count + math.ceil(ascii_count / 4) + 8)


def _clip_message_context(
        messages: list[dict[str, str]], context_length: int | None
) -> list[dict[str, str]]:
    if not messages:
        return []
    # 未设置，不处理！
    if not context_length:
        return messages

    max_context_length = context_length or 4096
    response_reserve = max(256, min(2048, max_context_length // 4))
    prompt_budget = max(512, max_context_length - response_reserve)

    system_messages = [message for message in messages if message.get("role") == "system"]
    dialogue_messages = [message for message in messages if message.get("role") != "system"]

    selected_system_messages: list[dict[str, str]] = []
    used_tokens = 0
    for message in reversed(system_messages):
        message_tokens = _estimate_message_tokens(message)
        if selected_system_messages and used_tokens + message_tokens > prompt_budget:
            continue
        selected_system_messages.append(message)
        used_tokens += message_tokens
    selected_system_messages.reverse()

    if not dialogue_messages:
        return selected_system_messages

    selected_dialogue_messages: list[dict[str, str]] = []
    latest_message = dialogue_messages[-1]
    latest_tokens = _estimate_message_tokens(latest_message)
    selected_dialogue_messages.append(latest_message)
    used_tokens += latest_tokens

    for message in reversed(dialogue_messages[:-1]):
        message_tokens = _estimate_message_tokens(message)
        if used_tokens + message_tokens > prompt_budget:
            continue
        selected_dialogue_messages.append(message)
        used_tokens += message_tokens

    selected_dialogue_messages.reverse()
    return [*selected_system_messages, *selected_dialogue_messages]


async def _build_message_context(
        auth: AuthSchema, data: AiChatCompletionSchema
) -> list[dict[str, str]]:
    incoming_content = str(data.userMessage.text or "").strip()
    if not incoming_content:
        raw_content = data.userMessage.content
        if isinstance(raw_content, str):
            incoming_content = raw_content.strip()
        elif isinstance(raw_content, list):
            content_parts = [
                str(item.get("text") or "").strip()
                for item in raw_content
                if isinstance(item, dict)
            ]
            incoming_content = "\n".join(part for part in content_parts if part).strip()

    incoming_messages = [{"role": "user", "content": incoming_content}] if incoming_content else []

    if (data.conversation_id or 0) <= 0 or len(incoming_messages) > 1:
        return _clip_message_context(incoming_messages, data.context_length)

    history_messages = await AiChatService.get_conversation_message_context(
        auth=auth,
        conversation_id=data.conversation_id or 0,
    )
    if not incoming_messages:
        return history_messages

    latest_message = incoming_messages[-1]
    if history_messages:
        latest_history = history_messages[-1]
        if latest_history.get("role") == latest_message.get("role") and latest_history.get(
                "content"
        ) == latest_message.get("content"):
            return _clip_message_context(history_messages, data.context_length)

    return _clip_message_context([*history_messages, *incoming_messages], data.context_length)


@AiChatRouter.get("/detail/{id}", summary="获取ai_chat详情", description="获取ai_chat详情")
async def get_ai_chat_detail_controller(
        id: int = Path(..., description="ID"),
        auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """获取ai_chat详情接口"""
    result_dict = await AiChatService.detail_ai_chat_service(auth=auth, id=id)
    log.info(f"获取ai_chat详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取ai_chat详情成功")


@AiChatRouter.get("/list", summary="查询ai_chat列表", description="查询ai_chat列表")
async def get_ai_chat_list_controller(
        page: PaginationQueryParam = Depends(),
        search: AiChatQueryParam = Depends(),
        auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """查询ai_chat列表接口（数据库分页）"""
    if search.status is None:
        search.status = "0"
    result_dict = await AiChatService.page_ai_chat_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询ai_chat列表成功")
    return SuccessResponse(data=result_dict, msg="查询ai_chat列表成功")


@AiChatRouter.post("/create", summary="创建ai_chat", description="创建ai_chat")
async def create_ai_chat_controller(
        data: AiChatCreateSchema,
        auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """创建ai_chat接口"""
    result_dict = await AiChatService.create_ai_chat_service(auth=auth, data=data)
    log.info("创建ai_chat成功")
    return SuccessResponse(data=result_dict, msg="创建ai_chat成功")


@AiChatRouter.post("/chat/completions", summary="AI对话接口", description="AI对话接口")
async def chat_completions(
        request: Request,
        auth: AuthSchema = Depends(AuthPermission(check_data_scope=False)),
) -> StreamingResponse:
    """AI对话接口"""
    data, file_markdowns = await AiChatService.resolve_chat_completion_request_service(request)
    await AiChatService.save_user_message_from_completion_service(
        auth=auth,
        data=data,
        file_markdowns=file_markdowns,
    )
    system_prompt = data.system_prompt or ""
    enabled_mcp_tool_ids: list[int] = []
    active_skills: list[str] = []
    internal_tools: list[str] = []
    knowledge_dataset_ids: list[str] = []
    mcp_extra_headers: dict[str, str] = {}
    agent_detail = await AiChatService.get_agent_by_conversation(
        auth=auth,
        conversation_id=data.conversation_id,
    )
    if agent_detail is not None:
        agent_prompt = agent_detail.get("prompt_template")
        if agent_prompt:
            system_prompt = agent_prompt
        mcp_config = AiChatService.extract_agent_mcp_config(agent_detail)
        enabled_mcp_tool_ids = AiChatService._deduplicate_int_list(mcp_config.get("enabledMcpToolIds"))
        active_skills = AiChatService._deduplicate_str_list(mcp_config.get("activeSkills"))
        internal_tools = AiChatService._deduplicate_str_list(mcp_config.get("internalTools"))
        knowledge_dataset_ids = AiChatService.extract_agent_knowledge_dataset_ids(agent_detail)
    if data.conversation_id:
        mcp_extra_headers["X-AI-Conversation-Id"] = str(data.conversation_id)
    provider_info = await AiChatService.get_provider_model_info(
        auth=auth,
        provider=data.provider,
        model=data.model,
    )
    api_key = decrypt_aisaas_api_key(provider_info.get("apiKey"))
    mcp_configs = await AiChatService.get_enabled_mcp_configs(auth=auth, ids=enabled_mcp_tool_ids)
    mcp_configs = AiChatService.append_builtin_knowledge_mcp_config(
        mcp_configs=mcp_configs,
        knowledge_dataset_ids=knowledge_dataset_ids,
    )

    client = AgnoProvider(
        provider=data.provider,
        model=data.model,
        api_key=api_key,
        base_url=provider_info.get("baseUrl"),
        temperature=data.temperature,
    )

    user_id = _get_auth_user_id(auth)
    message_context = await _build_message_context(auth=auth, data=data)

    async def generate():
        stream_task = asyncio.current_task()
        if stream_task is not None:
            await AiChatStreamManager.register(
                user_id=user_id,
                conversation_id=data.conversation_id,
                task=stream_task,
            )

        try:
            async for payload in client.agent(
                    message_context,
                    system_prompt=system_prompt,
                    file_markdowns=file_markdowns,
                    mcp_configs=mcp_configs,
                    active_skills=active_skills,
                    internal_tools=internal_tools,
                    conversation_id=data.conversation_id,
                    authorization=request.headers.get("Authorization"),
                    mcp_extra_headers=mcp_extra_headers,
                    response_schema=data.response_schema.model_dump(exclude_none=True) if data.response_schema else None,
            ):
                if not payload:
                    continue
                yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
        except asyncio.CancelledError:
            log.info("AI对话已停止: user_id=%s conversation_id=%s", user_id, data.conversation_id)
            return
        finally:
            await AiChatStreamManager.unregister(
                user_id=user_id,
                conversation_id=data.conversation_id,
                task=stream_task,
            )

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@AiChatRouter.post("/chat/completions/save", summary="保存AI对话消息", description="保存AI对话消息")
async def save_chat_completions(
        data: AiChatCompletionSaveSchema,
        auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """保存AI对话消息接口"""
    result_dict = await AiChatService.save_chat_completion_message_service(auth=auth, data=data)
    log.info("保存AI对话消息成功: chat_id=%s", data.conversation_id)
    return SuccessResponse(data=result_dict, msg="保存AI对话消息成功")


@AiChatRouter.post("/chat/completions/stop", summary="停止AI对话", description="停止AI对话")
async def stop_chat_completions(
        data: AiChatCompletionStopSchema,
        auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """停止AI对话接口"""
    stopped = await AiChatStreamManager.cancel(
        user_id=_get_auth_user_id(auth),
        conversation_id=data.conversation_id,
    )
    msg = "停止AI对话成功" if stopped else "当前无进行中的AI对话"
    log.info(
        "%s: user_id=%s conversation_id=%s", msg, _get_auth_user_id(auth), data.conversation_id
    )
    return SuccessResponse(
        data={"conversation_id": data.conversation_id, "stopped": stopped}, msg=msg
    )


@AiChatRouter.put("/update/{id}", summary="修改ai_chat", description="修改ai_chat")
async def update_ai_chat_controller(
        data: AiChatUpdateSchema,
        id: int = Path(..., description="ID"),
        auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """修改ai_chat接口"""
    result_dict = await AiChatService.update_ai_chat_service(auth=auth, id=id, data=data)
    log.info("修改ai_chat成功")
    return SuccessResponse(data=result_dict, msg="修改ai_chat成功")


@AiChatRouter.delete("/delete", summary="删除ai_chat", description="删除ai_chat")
async def delete_ai_chat_controller(
        ids: list[int] = Body(..., description="ID列表"),
        auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """删除ai_chat接口"""
    await AiChatService.delete_ai_chat_service(auth=auth, ids=ids)
    log.info(f"删除ai_chat成功: {ids}")
    return SuccessResponse(msg="删除ai_chat成功")


@AiChatRouter.patch(
    "/available/setting", summary="批量修改ai_chat状态", description="批量修改ai_chat状态"
)
async def batch_set_available_ai_chat_controller(
        data: BatchSetAvailable, auth: AuthSchema = Depends(AuthPermission())
) -> JSONResponse:
    """批量修改ai_chat状态接口"""
    await AiChatService.set_available_ai_chat_service(auth=auth, data=data)
    log.info(f"批量修改ai_chat状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改ai_chat状态成功")


@AiChatRouter.get("/stats", summary="获取统计数据", description="获取AI模块统计数据，支持缓存")
async def get_stats_controller(
        force_refresh: bool = False,
        auth: AuthSchema = Depends(AuthPermission()),
        redis: Redis = Depends(redis_getter),
) -> JSONResponse:
    """获取统计数据接口"""
    cache_key = "ai_stats"
    redis_crud = RedisCURD(redis)

    # 检查缓存是否有效（5分钟内）
    if not force_refresh:
        cached_data = await redis_crud.get(cache_key)
        if cached_data:
            import json
            try:
                result_dict = json.loads(cached_data)
                log.info("使用缓存的统计数据")
                return SuccessResponse(data=result_dict, msg="获取统计数据成功")
            except json.JSONDecodeError:
                log.error("解析缓存数据失败")

    # 获取最新统计数据
    result_dict = await AiChatService.get_stats_service(auth=auth)
    # 更新缓存，设置5分钟过期
    await redis_crud.set(cache_key, result_dict, expire=300)
    log.info("获取最新统计数据成功")
    return SuccessResponse(data=result_dict, msg="获取统计数据成功")
