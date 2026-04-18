import json
import traceback
from pathlib import Path
from typing import Any

from fastapi import Request, UploadFile, status
from pydantic import ValidationError
from sqlalchemy import func, select, update

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.params.service import ParamsService
from app.config.setting import settings
from app.core.base_schema import BatchSetAvailable
from app.core.database import async_db_session
from app.core.exceptions import CustomException
from app.core.logger import log
from app.plugin.module_ai.ai_agent.service import AiAgentService
from app.plugin.module_ai.ai_chat_msg.crud import AiChatMsgCRUD
from app.plugin.module_ai.ai_chat_msg.model import AiChatMsgModel
from app.plugin.module_ai.ai_chat_msg.schema import AiChatMsgCreateSchema
from app.plugin.module_ai.ai_chat_msg.service import AiChatMsgService
from app.plugin.module_ai.ai_mcp.crud import AiMcpCRUD
from app.plugin.module_ai.ai_mcp.schema import AiMcpOutSchema
from .crud import AiChatCRUD
from .file_markdown import extract_upload_file_markdowns
from .model import AiChatModel
from .schema import (
    AiChatCompletionSchema,
    AiChatCreateSchema,
    AiChatCompletionSaveSchema,
    AiChatOutSchema,
    AiChatQueryParam,
    AiChatUpdateSchema,
)


class AiChatService:
    """
    ai_chat服务层
    """
    _BUILTIN_RAGFLOW_MCP_NAME = "ragflow-knowledge"
    _BUILTIN_RAGFLOW_MCP_URL = "http://127.0.0.1:9024/mcp"

    @classmethod
    async def resolve_chat_completion_request_service(
            cls,
            request: Request,
    ) -> tuple[AiChatCompletionSchema, list[dict[str, str]]]:
        payload, files = await cls._parse_chat_completion_request(request)
        payload = cls._normalize_completion_payload(payload=payload, files=files)

        try:
            data = AiChatCompletionSchema.model_validate(payload)
        except ValidationError as exc:
            raise CustomException(
                msg=f"请求体校验失败: {exc.errors()[0].get('msg') or exc!s}",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=payload,
            ) from exc

        cls._validate_upload_files(files)
        file_markdowns = await extract_upload_file_markdowns(
            files=files,
            max_file_size_bytes=settings.AI_CHAT_UPLOAD_MAX_FILE_SIZE,
        )
        return data, file_markdowns

    @classmethod
    def build_user_message_storage_content(
            cls,
            data: AiChatCompletionSchema,
            file_markdowns: list[dict[str, str]] | None = None,
    ) -> str:
        user_payload = data.userMessage.model_dump(by_alias=True, exclude_none=True)
        raw_files = user_payload.get("files") or []
        if not isinstance(raw_files, list):
            raw_files = []

        normalized_files: list[dict] = []
        markdown_files = file_markdowns or []
        file_count = max(len(raw_files), len(markdown_files))

        for index in range(file_count):
            raw_file = raw_files[index] if index < len(raw_files) and isinstance(raw_files[index], dict) else {}
            markdown_file = markdown_files[index] if index < len(markdown_files) else {}

            file_name = str(
                raw_file.get("name")
                or markdown_file.get("name")
                or f"文件{index + 1}"
            ).strip()
            file_content = str(
                raw_file.get("content")
                or markdown_file.get("markdown")
                or ""
            ).strip()

            normalized_file: dict = {}
            if file_name:
                normalized_file["name"] = file_name
            if file_content:
                normalized_file["content"] = file_content

            for key in ("mimeType", "token", "path", "thumbnail", "metadata"):
                value = raw_file.get(key)
                if value is not None:
                    normalized_file[key] = value

            if normalized_file:
                normalized_files.append(normalized_file)

        if normalized_files:
            user_payload["files"] = normalized_files
        else:
            user_payload.pop("files", None)

        return json.dumps(user_payload, ensure_ascii=False, default=str)

    @staticmethod
    def _deduplicate_str_list(values: list[Any] | None) -> list[str]:
        if not isinstance(values, list):
            return []

        result: list[str] = []
        seen: set[str] = set()
        for item in values:
            value = str(item).strip()
            if not value or value in seen:
                continue
            seen.add(value)
            result.append(value)
        return result

    @staticmethod
    def _deduplicate_int_list(values: list[Any] | None) -> list[int]:
        if not isinstance(values, list):
            return []

        result: list[int] = []
        seen: set[int] = set()
        for item in values:
            try:
                value = int(item)
            except (TypeError, ValueError):
                continue
            if value <= 0 or value in seen:
                continue
            seen.add(value)
            result.append(value)
        return result

    @classmethod
    def parse_agent_config(cls, raw_config: str | dict[str, Any] | None) -> dict[str, Any]:
        if isinstance(raw_config, dict):
            return raw_config

        if not raw_config:
            return {}

        try:
            parsed = json.loads(str(raw_config))
        except Exception as exc:
            log.warning("解析智能体配置失败: %s", exc)
            return {}

        if not isinstance(parsed, dict):
            return {}
        return parsed

    @classmethod
    def extract_agent_mcp_config(cls, agent_detail: dict | None) -> dict[str, Any]:
        if not isinstance(agent_detail, dict):
            return {}

        agent_config = cls.parse_agent_config(agent_detail.get("config"))
        mcp_config = agent_config.get("mcp")
        if not isinstance(mcp_config, dict):
            return {}
        return mcp_config

    @classmethod
    def extract_agent_knowledge_dataset_ids(cls, agent_detail: dict | None) -> list[str]:
        mcp_config = cls.extract_agent_mcp_config(agent_detail)
        knowledge_list = mcp_config.get("knowledge")
        if not isinstance(knowledge_list, list):
            return []

        dataset_ids: list[str] = []
        for item in knowledge_list:
            if not isinstance(item, dict):
                continue
            dataset_id = str(item.get("dataset_id") or "").strip()
            if dataset_id:
                dataset_ids.append(dataset_id)
        return cls._deduplicate_str_list(dataset_ids)

    @classmethod
    async def get_agent_knowledge_dataset_ids_by_conversation(
            cls,
            auth: AuthSchema,
            conversation_id: int,
    ) -> list[str]:
        if not conversation_id:
            raise CustomException(msg="缺少会话ID", status_code=status.HTTP_400_BAD_REQUEST)

        agent_detail = await cls.get_agent_by_conversation(auth=auth, conversation_id=conversation_id)
        if agent_detail is None:
            raise CustomException(msg="当前会话未绑定智能体", status_code=status.HTTP_400_BAD_REQUEST)

        dataset_ids = cls.extract_agent_knowledge_dataset_ids(agent_detail)
        if not dataset_ids:
            raise CustomException(msg="当前智能体未配置知识库", status_code=status.HTTP_400_BAD_REQUEST)

        return dataset_ids

    @classmethod
    async def save_user_message_from_completion_service(
            cls,
            auth: AuthSchema,
            data: AiChatCompletionSchema,
            file_markdowns: list[dict[str, str]] | None = None,
    ) -> dict[str, int | bool] | None:
        chat_id = int(data.conversation_id or 0)
        if chat_id <= 0:
            return None

        content = cls.build_user_message_storage_content(
            data=data,
            file_markdowns=file_markdowns,
        )
        if not content:
            return None

        return await cls.save_chat_completion_message_service(
            auth=auth,
            data=AiChatCompletionSaveSchema(
                conversation_id=chat_id,
                role="user",
                content=content,
                token_count=0,
                input_tokens=0,
                output_tokens=0,
            ),
        )

    @classmethod
    async def _parse_chat_completion_request(
            cls,
            request: Request,
    ) -> tuple[dict, list[UploadFile]]:
        content_type = (request.headers.get("content-type") or "").lower()

        if "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type:
            form = await request.form()
            body = form.get("body")
            files = [
                file
                for file in form.getlist("files")
                if hasattr(file, "read") and hasattr(file, "filename") and (file.filename or "").strip()
            ]
            if body is None or str(body).strip() == "":
                raise CustomException(
                    msg="缺少请求体",
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
            return cls._load_chat_completion_payload(str(body)), files

        raw_body = await request.body()
        if not raw_body:
            raise CustomException(
                msg="缺少请求体",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        return cls._load_chat_completion_payload(raw_body.decode("utf-8")), []

    @classmethod
    def _load_chat_completion_payload(cls, body: str) -> dict:
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            raise CustomException(
                msg=f"请求体 JSON 解析失败: {exc.msg}",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            ) from exc

        if not isinstance(payload, dict):
            raise CustomException(
                msg="请求体格式错误，必须为 JSON 对象",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        return payload

    @classmethod
    def _normalize_completion_payload(
            cls,
            payload: dict,
            files: list[UploadFile] | None = None,
    ) -> dict:
        normalized_payload = dict(payload)
        if not files:
            return normalized_payload

        user_message = normalized_payload.get("userMessage")
        if isinstance(user_message, dict):
            user_message["text"] = (
                str(user_message.get("text") or "").strip() or "请结合我上传的文件内容回答。"
            )
            return normalized_payload

        normalized_messages = normalized_payload.get("messages")
        if isinstance(normalized_messages, list):
            for message in reversed(normalized_messages):
                if not isinstance(message, dict):
                    continue
                if message.get("role") != "user":
                    continue
                message["content"] = (
                    str(message.get("content") or "").strip() or "请结合我上传的文件内容回答。"
                )
                break

        return normalized_payload

    @classmethod
    def _validate_upload_files(cls, files: list[UploadFile] | None) -> None:
        if not files:
            return

        if len(files) > settings.AI_CHAT_UPLOAD_MAX_FILE_COUNT:
            raise CustomException(
                msg=f"上传文件数量不能超过 {settings.AI_CHAT_UPLOAD_MAX_FILE_COUNT} 个",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        for file in files:
            cls._validate_single_upload_file(file)

    @classmethod
    def _validate_single_upload_file(cls, file: UploadFile) -> None:
        file_name = (file.filename or "").strip() or "未命名文件"
        extension = Path(file_name).suffix.lower()
        content_type = (file.content_type or "").split(";", 1)[0].strip().lower()
        file_size = getattr(file, "size", None)
        allowed_extensions = {item.lower() for item in settings.AI_CHAT_UPLOAD_ALLOWED_EXTENSIONS}
        allowed_content_types = {
            item.lower()
            for item in settings.AI_CHAT_UPLOAD_ALLOWED_CONTENT_TYPES
        }

        if extension not in allowed_extensions and content_type not in allowed_content_types:
            allowed_ext_text = "、".join(sorted(allowed_extensions))
            raise CustomException(
                msg=f"文件 {file_name} 类型不支持，仅支持：{allowed_ext_text}",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        if file_size is not None and file_size > settings.AI_CHAT_UPLOAD_MAX_FILE_SIZE:
            raise CustomException(
                msg=f"文件 {file_name} 超过大小限制，单个文件不能超过 {settings.AI_CHAT_UPLOAD_MAX_FILE_SIZE // (1024 * 1024)}MB",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

    @classmethod
    async def detail_ai_chat_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await AiChatCRUD(auth).get_by_id_ai_chat_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return AiChatOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def get_agent_by_conversation(cls, auth: AuthSchema, conversation_id: int) -> dict | None:
        if not conversation_id:
            return None
        chat_detail = await cls.detail_ai_chat_service(
            auth=auth,
            id=conversation_id,
        )
        agent_id = chat_detail.get("agent_id") or 0
        if not agent_id:
            return None
        agent_detail = await AiAgentService.detail_ai_agent_service(
            auth=auth,
            id=agent_id,
        )
        return agent_detail

    @classmethod
    async def get_provider_model_info(
            cls, auth: AuthSchema, provider: str | None, model: str | None
    ) -> dict:
        config_value = await ParamsService.get_config_value_by_key_service(
            config_key="aisaas_models",
            auth=auth,
        )
        if not config_value:
            raise CustomException(msg="aisaas_models 配置为空")
        try:
            aisaas_models = json.loads(config_value)
        except Exception as e:
            raise CustomException(msg=f"aisaas_models 配置解析失败: {e!s}")
        if not isinstance(aisaas_models, list):
            raise CustomException(msg="aisaas_models 配置格式错误")
        provider_map = {
            item.get("id"): item
            for item in aisaas_models
            if isinstance(item, dict) and item.get("id")
        }
        if not provider:
            raise CustomException(msg="模型提供商不能为空")
        if provider not in provider_map:
            raise CustomException(msg=f"模型提供商不存在: {provider}")
        provider_info = provider_map[provider]
        if not provider_info.get("enable"):
            raise CustomException(msg=f"模型提供商未启用: {provider}")
        provider_models = []
        if isinstance(provider_info.get("models"), list):
            provider_models.extend(provider_info.get("models"))
        if isinstance(provider_info.get("customModels"), list):
            provider_models.extend(provider_info.get("customModels"))
        model_info = next(
            (
                item
                for item in provider_models
                if isinstance(item, dict) and item.get("id") == model
            ),
            None,
        )
        if not model_info:
            raise CustomException(msg=f"模型不存在: {model}")
        if not model_info.get("enabled"):
            raise CustomException(msg=f"模型未启用: {model}")
        provider_model_info = dict(provider_info)
        provider_model_info["model_info"] = model_info
        return provider_model_info

    @classmethod
    async def get_conversation_message_context(
            cls, auth: AuthSchema, conversation_id: int
    ) -> list[dict[str, str]]:
        if not conversation_id:
            return []

        message_list = await AiChatMsgCRUD(auth).list_ai_chat_msg_crud(
            search={"chat_id": conversation_id},
            order_by=[{"id": "asc"}],
        )

        context_messages: list[dict[str, str]] = []
        for message in message_list:
            if not message.role:
                continue

            normalized_content = cls._normalize_message_content_for_context(
                role=message.role,
                raw_content=message.content,
            )
            if not normalized_content:
                continue

            context_messages.append({"role": message.role, "content": normalized_content})
        return context_messages

    @classmethod
    def _normalize_message_content_for_context(
            cls, role: str | None, raw_content: str | None
    ) -> str:
        text = str(raw_content or "").strip()
        if not text:
            return ""

        parsed = json.loads(text)
        role_name = str(role or "").lower()

        if role_name == "assistant":
            normalized = cls._extract_assistant_message_text(parsed)
            return normalized or text

        if role_name == "user":
            normalized = cls._extract_user_message_text(parsed)
            return normalized or text

        if isinstance(parsed, str):
            return parsed.strip()

        return text

    @classmethod
    def _extract_user_message_text(cls, payload: object | list | str) -> str:
        if isinstance(payload, dict):
            text = str(payload.get("text") or "").strip()
            file_sections: list[str] = []
            files = payload.get("files")
            if isinstance(files, list):
                for index, item in enumerate(files, start=1):
                    if not isinstance(item, dict):
                        continue
                    file_name = str(item.get("name") or f"文件{index}").strip()
                    if not file_name:
                        continue
                    file_sections.append(f"【用户上传文件{index}】{file_name}")

            content_text = ""
            content = payload.get("content")
            if isinstance(content, str):
                content_text = content.strip()
            elif isinstance(content, list):
                parts = [
                    str(item.get("text") or "").strip()
                    for item in content
                    if isinstance(item, dict)
                ]
                content_text = "\n".join(part for part in parts if part).strip()

            result_parts = [part for part in [text, content_text, "\n\n".join(file_sections)] if part]
            return "\n\n".join(result_parts).strip()

        return ""

    @classmethod
    def _extract_assistant_message_text(cls, payload: object | list | str) -> str:
        if isinstance(payload, str):
            return payload.strip()

        blocks = payload
        if isinstance(payload, dict):
            blocks = payload.get("content")
            if isinstance(blocks, str):
                try:
                    blocks = json.loads(blocks)
                except Exception:
                    return blocks.strip()

        if not isinstance(blocks, list):
            return ""

        text_parts: list[str] = []
        for block in blocks:
            if not isinstance(block, dict):
                continue

            block_type = str(block.get("type") or "")
            content = str(block.get("content") or "").strip()
            if content and block_type in {
                "content",
                "reasoning_content",
                "artifact-thinking",
                "search",
                "plan",
                "error",
                "action",
            }:
                text_parts.append(content)
                continue

            if block_type == "tool_call":
                tool_call = block.get("tool_call")
                if isinstance(tool_call, dict):
                    tool_response = str(tool_call.get("response") or "").strip()
                    if tool_response:
                        text_parts.append(tool_response)

        return "\n".join(part for part in text_parts if part).strip()

    @classmethod
    async def get_enabled_mcp_configs(cls, auth: AuthSchema, ids: list[int] | None) -> list[dict]:
        clean_ids = cls._deduplicate_int_list(ids)
        if not clean_ids:
            return []

        mcp_list = await AiMcpCRUD(auth).list_ai_mcp_crud(
            search={
                "id": ("in", clean_ids),
                "status": "0",
            },
            order_by=[{"id": "asc"}],
        )
        mcp_map = {
            int(item.id): AiMcpOutSchema.model_validate(item).model_dump()
            for item in mcp_list
            if item.id is not None
        }

        missing_ids = [str(mcp_id) for mcp_id in clean_ids if mcp_id not in mcp_map]
        if missing_ids:
            log.warning(f"以下MCP未找到或未启用，已跳过: {','.join(missing_ids)}")

        return [mcp_map[mcp_id] for mcp_id in clean_ids if mcp_id in mcp_map]

    @classmethod
    def build_builtin_ragflow_mcp_config(cls) -> dict[str, Any]:
        return {
            "id": 0,
            "name": cls._BUILTIN_RAGFLOW_MCP_NAME,
            "type": "http",
            "abstract": "Agent knowledge retrieval MCP",
            "config": json.dumps(
                {
                    "mcpServers": {
                        cls._BUILTIN_RAGFLOW_MCP_NAME: {
                            "url": cls._BUILTIN_RAGFLOW_MCP_URL,
                            "timeoutSeconds": 30,
                        }
                    }
                },
                ensure_ascii=False,
            ),
        }

    @classmethod
    def append_builtin_knowledge_mcp_config(
            cls,
            mcp_configs: list[dict] | None,
            knowledge_dataset_ids: list[str] | None,
    ) -> list[dict]:
        result = list(mcp_configs or [])
        if not cls._deduplicate_str_list(knowledge_dataset_ids):
            return result

        result.append(cls.build_builtin_ragflow_mcp_config())
        return result

    @classmethod
    async def save_chat_completion_message_service(
            cls, auth: AuthSchema, data: AiChatCompletionSaveSchema
    ) -> dict[str, int | bool]:
        chat_id = data.conversation_id
        token_increment = max(0, int(data.token_count or 0))
        role_name = str(data.role or "").lower()

        try:
            async with async_db_session() as session:
                async with session.begin():
                    save_auth = AuthSchema(
                        db=session,
                        user=auth.user,
                        check_data_scope=auth.check_data_scope,
                    )
                    max_order_seq_result = await session.execute(
                        select(func.max(AiChatMsgModel.order_seq)).where(AiChatMsgModel.chat_id == chat_id)
                    )
                    next_order_seq = int(max_order_seq_result.scalar() or 0) + 1
                    msg = await AiChatMsgService.create_ai_chat_msg_service(
                        auth=save_auth,
                        data=AiChatMsgCreateSchema(
                            chat_id=chat_id,
                            role=data.role,
                            content=data.content,
                            order_seq=next_order_seq,
                            token_count=data.token_count,
                            input_tokens=data.input_tokens,
                            output_tokens=data.output_tokens,
                        ),
                    )
                    if role_name == "assistant" and token_increment > 0:
                        update_result = await session.execute(
                            update(AiChatModel)
                            .where(AiChatModel.id == chat_id)
                            .values(tokens=AiChatModel.tokens + token_increment)
                        )
                        if (update_result.rowcount or 0) <= 0:
                            raise CustomException(msg=f"会话不存在: {chat_id}")
        except Exception as e:
            log.error(
                "保存 ai_chat_msg 失败: chat_id=%s role=%s content_len=%s token_count=%s input_tokens=%s output_tokens=%s error=%s",
                chat_id,
                data.role,
                len(data.content or ""),
                data.token_count,
                data.input_tokens,
                data.output_tokens,
                e,
            )
            raise CustomException(msg=f"保存AI对话消息失败\n{traceback.format_exc()}")

        log.info("ai_chat_msg 保存成功: chat_id=%s msg_id=%s", chat_id, msg.get("id"))
        return {
            "saved": True,
            "chat_id": chat_id,
            "msg_id": int(msg.get("id") or 0),
        }

    @classmethod
    async def page_ai_chat_service(
            cls,
            auth: AuthSchema,
            page_no: int,
            page_size: int,
            search: AiChatQueryParam | None = None,
            order_by: list[dict] | None = None,
    ) -> dict:
        """分页查询（数据库分页）"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"id": "asc"}]
        offset = (page_no - 1) * page_size
        result = await AiChatCRUD(auth).page_ai_chat_crud(
            offset=offset, limit=page_size, order_by=order_by_list, search=search_dict
        )
        return result

    @classmethod
    async def create_ai_chat_service(cls, auth: AuthSchema, data: AiChatCreateSchema) -> dict:
        """创建"""
        # 检查唯一性约束
        obj = await AiChatCRUD(auth).create_ai_chat_crud(data=data)
        return AiChatOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_ai_chat_service(
            cls, auth: AuthSchema, id: int, data: AiChatUpdateSchema
    ) -> dict:
        """更新"""
        # 检查数据是否存在
        obj = await AiChatCRUD(auth).get_by_id_ai_chat_crud(id=id)
        if not obj:
            raise CustomException(msg="更新失败，该数据不存在")

        # 检查唯一性约束

        obj = await AiChatCRUD(auth).update_ai_chat_crud(id=id, data=data)
        return AiChatOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_ai_chat_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        for id in ids:
            obj = await AiChatCRUD(auth).get_by_id_ai_chat_crud(id=id)
            if not obj:
                raise CustomException(msg=f"删除失败，ID为{id}的数据不存在")
        await AiChatCRUD(auth).set_available_ai_chat_crud(ids=ids, status="1")

    @classmethod
    async def set_available_ai_chat_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await AiChatCRUD(auth).set_available_ai_chat_crud(ids=data.ids, status=data.status)

    @classmethod
    async def get_stats_service(cls, auth: AuthSchema) -> dict:
        """获取统计数据"""
        from app.api.v1.module_system.user.crud import UserCRUD
        from app.api.v1.module_system.dept.crud import DeptCRUD
        from app.api.v1.module_system.role.crud import RoleCRUD
        from app.api.v1.module_system.position.crud import PositionCRUD
        from app.plugin.module_ai.ai_agent.crud import AiAgentCRUD
        from app.plugin.module_ai.ai_chat_msg.crud import AiChatMsgCRUD
        from app.plugin.module_ai.ai_mcp.crud import AiMcpCRUD
        from sqlalchemy import func
        import datetime

        # 获取用户数
        user_list = await UserCRUD(auth).get_list_crud()
        user_count = len(user_list)

        # 获取部门数
        dept_list = await DeptCRUD(auth).get_list_crud()
        dept_count = len(dept_list)

        # 获取角色数
        role_list = await RoleCRUD(auth).get_list_crud()
        role_count = len(role_list)

        # 获取岗位数
        position_list = await PositionCRUD(auth).get_list_crud()
        position_count = len(position_list)

        # 获取智能体数
        agent_list = await AiAgentCRUD(auth).list_ai_agent_crud()
        agent_count = len(agent_list)

        # 获取MCP数量
        mcp_list = await AiMcpCRUD(auth).list_ai_mcp_crud()
        mcp_count = len(mcp_list)

        # 获取对话数
        chat_list = await AiChatCRUD(auth).list_ai_chat_crud()
        chat_count = len(chat_list)

        # 获取消息数量
        msg_list = await AiChatMsgCRUD(auth).list_ai_chat_msg_crud()
        msg_count = len(msg_list)

        # 计算累计token
        from .model import AiChatModel
        async with auth.db as session:
            result = await session.execute(
                func.sum(AiChatModel.tokens)
            )
            total_tokens = result.scalar() or 0

        return {
            "statistical_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_count": user_count,
            "dept_count": dept_count,
            "role_count": role_count,
            "position_count": position_count,
            "agent_count": agent_count,
            "mcp_count": mcp_count,
            "chat_count": chat_count,
            "msg_count": msg_count,
            "total_tokens": int(total_tokens)
        }
