import json
import time
import uuid
from collections.abc import AsyncGenerator, Sequence
from datetime import timedelta
from pathlib import Path
from typing import Any

from agno.agent import Agent, RunEvent
from agno.skills import Skills, LocalSkills
from agno.tools import Toolkit
from agno.tools.mcp import MCPTools
from agno.tools.mcp.params import SSEClientParams, StreamableHTTPClientParams
from agno.tools.shell import ShellTools
from mcp import StdioServerParameters

from app.config.path_conf import AI_SKILLS_DIR, AI_FILE_DIR
from app.core.logger import log
from app.plugin.module_ai.agno.model_map import create_model
from app.plugin.module_ai.ai_knowledge_base.service import FilesService, get_file_dir
from app.plugin.module_ai.ai_tools.service import AIToolsService


class AgnoProvider:
    """
    Agno AI客户端类
    """

    def __init__(
            self,
            provider: str | None = None,
            model: str | None = None,
            api_key: str | None = None,
            base_url: str | None = None,
            temperature: float | None = None,
    ) -> None:
        self.model_id = model or ""
        self.model = create_model(
            provider=provider,
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
        )

    async def agent(
            self,
            query: str | Sequence[dict[str, str]],
            system_prompt: str = "",
            file_markdowns: Sequence[dict[str, str]] | None = None,
            mcp_configs: Sequence[dict[str, Any]] | None = None,
            active_skills: Sequence[str] | None = None,
            internal_tools: Sequence[str] | None = None,
            conversation_id: int | None = None,
            authorization: str | None = None,
            mcp_extra_headers: dict[str, str] | None = None,
            response_schema: dict[str, Any] | None = None,
            auth: Any = None,
    ) -> AsyncGenerator[dict[str, Any], Any]:
        """
        处理查询并返回流式响应

        参数:
        - query (str | Sequence[dict[str, str]]): 用户查询或消息上下文。
        - system_prompt (str): 系统提示词。
        - file_markdowns (Sequence[dict[str, str]] | None): 上传文件Markdown内容。
        - mcp_configs (Sequence[dict[str, Any]] | None): MCP配置列表。
        - authorization (str | None): 授权信息。

        返回:
        - AsyncGenerator[dict[str, Any], Any]: OpenAI Chat Completion流式分片。
        """
        completion_id = f"chatcmpl-{uuid.uuid4().hex}"
        created = int(time.time())
        yield self._format_openai_chunk(
            completion_id=completion_id,
            created=created,
            delta={"role": "assistant"},
            finish_reason=None,
        )
        normalized_query = self._normalize_query(query)
        # output_schema = resolve_output_schema(response_schema)

        mcp_tools = self._get_mcp_tools(mcp_configs, authorization=authorization, extra_headers=mcp_extra_headers)
        requested_internal_tools = list(internal_tools or [])
        log.info(
            f"工具准备中: mcp_configs={len(mcp_configs or [])}, mcp_tools={len(mcp_tools)}, "
            f"internal_tools={requested_internal_tools}"
        )
        tools = mcp_tools + self._get_tools(internal_tools, conversation_id, auth=auth)
        log.info(
            f"工具准备完成: total_tools={len(tools)}, mcp_tools={len(mcp_tools)}, "
            f"internal_toolkits={len(tools) - len(mcp_tools)}"
        )

        agent = Agent(
            model=self.model,
            reasoning=False,
            instructions=self._build_system_prompt(
                system_prompt=system_prompt,
                file_markdowns=file_markdowns,
            ),
            markdown=True,
            tools=tools,
            skills=self._get_skills(active_skills),
            # output_schema=output_schema,
        )
        try:
            async for chunk in agent.arun(normalized_query,
                                          stream_events=True, stream=True, show_full_reasoning=True):
                if chunk.event == RunEvent.run_content and chunk.reasoning_content:
                    content = chunk.reasoning_content or ""
                    if not content:
                        continue

                    yield self._format_openai_chunk(
                        completion_id=completion_id,
                        created=created,
                        delta={"reasoning_content": content},
                        finish_reason=None,
                    )
                    continue

                if chunk.event == RunEvent.run_completed:
                    yield self._format_openai_chunk(
                        completion_id=completion_id,
                        created=created,
                        delta={},
                        finish_reason="stop",
                        usage={
                            "prompt_tokens": chunk.metrics.input_tokens,  # 输入 token 数
                            "completion_tokens": chunk.metrics.output_tokens,  # 模型生成的输出 token 数
                            "total_tokens": chunk.metrics.total_tokens,  # prompt + completion 之和（最常用的计费依据）
                        },
                    )
                    continue

                if chunk.event == RunEvent.tool_call_started:
                    yield self._format_openai_chunk(
                        completion_id=completion_id,
                        created=created,
                        delta={
                            "tool_calls": [
                                {
                                    "index": 0,
                                    "id": chunk.tool.tool_call_id,
                                    "type": "function",
                                    "function": {
                                        "name": chunk.tool.tool_name
                                    },
                                }
                            ]
                        },
                        finish_reason=None,
                    )
                    continue

                if chunk.event == RunEvent.tool_call_completed:
                    yield self._format_openai_chunk(
                        completion_id=completion_id,
                        created=created,
                        delta={
                            "tool_calls": [
                                {
                                    "index": 0,
                                    "id": chunk.tool.tool_call_id,
                                    "type": "function",
                                    "function": {
                                        "name": chunk.tool.tool_name,
                                        "arguments": chunk.tool.tool_args,
                                        "result": chunk.tool.result,
                                    },
                                }
                            ]
                        },
                        finish_reason=None,
                    )
                    continue

                if chunk.event in {RunEvent.run_content, RunEvent.run_intermediate_content}:
                    content = chunk.content or ""
                    if not content:
                        continue

                    if hasattr(content, "model_dump_json"):
                        content = '```json\n' + content.model_dump_json() + '\n```'
                    elif not isinstance(content, str):
                        try:
                            content = json.dumps(content, ensure_ascii=False)
                        except Exception:
                            content = str(content)

                    yield self._format_openai_chunk(
                        completion_id=completion_id,
                        created=created,
                        delta={"content": content},
                        finish_reason=None,
                    )
                    continue

        except Exception as e:
            log.error(f"AI处理查询失败: {e!s}")
            yield self._format_openai_chunk(
                completion_id=completion_id,
                created=created,
                delta={"content": self._friendly_error_message(e)},
                finish_reason="stop",
            )

    @staticmethod
    def _normalize_query(query: str | Sequence[dict[str, str]]) -> str | list[dict[str, str]]:
        if isinstance(query, str):
            return query

        normalized: list[dict[str, str]] = []
        for item in query:
            if not isinstance(item, dict):
                continue
            role = str(item.get("role") or "").strip().lower()
            if role not in {"user", "assistant"}:
                continue

            content = str(item.get("content") or "").strip()
            if not content:
                continue

            if not normalized:
                if role == "assistant":
                    continue
                normalized.append({"role": role, "content": content})
                continue

            previous_role = normalized[-1]["role"]
            if role == previous_role:
                normalized[-1]["content"] = f"{normalized[-1]['content']}\n\n{content}"
                continue

            normalized.append({"role": role, "content": content})

        return normalized

    def _format_openai_chunk(
            self,
            completion_id: str,
            created: int,
            delta: dict[str, Any],
            finish_reason: str | None = None,
            usage: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        result = {
            "id": completion_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": self.model_id,
            "choices": [
                {
                    "index": 0,
                    "delta": delta,
                    "finish_reason": finish_reason,
                }
            ],
        }
        if usage:
            result["usage"] = usage
        return result

    @classmethod
    def _get_mcp_tools(
            cls,
            mcp_configs: Sequence[dict[str, Any]] | None,
            authorization: str | None = None,
            extra_headers: dict[str, str] | None = None,
    ) -> list[MCPTools]:
        if not mcp_configs:
            return []

        tools: list[MCPTools] = []
        seen_server_keys: set[str] = set()
        for item in mcp_configs:
            try:
                config = json.loads(item["config"]) if item.get("config") else {}
                for server_name, server_config in config["mcpServers"].items():
                    if server_config.get("disable"):
                        log.info(f"MCP已禁用，跳过: {server_name}")
                        continue
                    server_key = cls._build_mcp_server_key(item=item, server_config=server_config)
                    if server_key and server_key in seen_server_keys:
                        log.info(f"MCP重复加载已跳过: {server_name}")
                        continue
                    if server_key:
                        seen_server_keys.add(server_key)
                    tools.append(
                        cls._build_single_mcp_tool(
                            item=item,
                            server_name=server_name,
                            server_config=server_config,
                            authorization=authorization,
                            extra_headers=extra_headers,
                        )
                    )
            except Exception as e:
                log.error(f"MCP工具加载失败: {e!s} item={item}")
                return []
        return tools

    @classmethod
    def _build_mcp_server_key(
            cls,
            item: dict[str, Any],
            server_config: dict[str, Any],
    ) -> str:
        item_type = str(item.get("type") or "").strip().lower()

        if item_type in {"http", "streamable-http", "streamable_http", "sse"}:
            base_url = str(server_config.get("baseUrl") or server_config.get("url") or "").strip()
            normalized_url = base_url.rstrip("/").lower()
            normalized_type = "http" if item_type in {"http", "streamable-http", "streamable_http"} else "sse"
            return f"{normalized_type}:{normalized_url}"

        if item_type == "stdio":
            command = str(server_config.get("command") or "").strip()
            args = cls._get_args(server_config.get("args"))
            cwd = str(server_config.get("cwd") or "").strip()
            return f"stdio:{command}|{' '.join(args)}|{cwd}"

        return ""

    @classmethod
    def _build_single_mcp_tool(
            cls,
            item: dict[str, Any],
            server_name: str,
            server_config: dict[str, Any],
            authorization: str | None = None,
            extra_headers: dict[str, str] | None = None,
    ) -> MCPTools:
        headers = cls._get_headers(
            server_config,
            authorization=authorization,
            extra_headers=extra_headers,
        )
        timeout_seconds = int(server_config.get("timeoutSeconds") or 30)
        tool_name_prefix = cls._sanitize_tool_name_prefix(server_name)

        if item["type"] == "sse":
            base_url = server_config.get("baseUrl") or server_config.get("url")
            if not base_url:
                raise ValueError(f"MCP配置缺少 baseUrl: {server_name}")
            server_params = SSEClientParams(
                url=str(base_url).strip(),
                headers=headers or None,
                timeout=float(timeout_seconds),
            )
            return MCPTools(
                transport="sse",
                server_params=server_params,
                timeout_seconds=timeout_seconds,
                tool_name_prefix=tool_name_prefix,
            )

        if item["type"] in {"http", "streamable-http", "streamable_http"}:
            base_url = server_config.get("baseUrl") or server_config.get("url")
            if not base_url:
                raise ValueError(f"MCP配置缺少 url: {server_name}")
            server_params = StreamableHTTPClientParams(
                url=base_url.strip(),
                headers=headers or None,
                timeout=timedelta(seconds=timeout_seconds),
            )
            return MCPTools(
                transport="streamable-http",
                server_params=server_params,
                timeout_seconds=timeout_seconds,
                tool_name_prefix=tool_name_prefix,
            )

        if item["type"] == "stdio":
            command = server_config.get("command")
            if not command:
                raise ValueError(f"MCP配置缺少 command: {server_name}")
            args = server_config.get("args")
            env = server_config.get("env")
            cwd = server_config.get("cwd")
            command_text = str(command).strip()
            args_list = cls._get_args(args)
            cwd_path = str(cwd).strip() if cwd else None
            log.info(
                f"初始化MCP(stdio): server={server_name}, command={command_text}, args={args_list}, "
                f"cwd={cwd_path}, timeout={timeout_seconds}s"
            )
            server_params = StdioServerParameters(
                command=command_text,
                args=args_list,
                env=cls._get_env(env),
                cwd=cwd_path,
            )
            return MCPTools(
                transport="stdio",
                server_params=server_params,
                timeout_seconds=timeout_seconds,
                tool_name_prefix=tool_name_prefix,
            )

        raise ValueError(f"MCP类型不支持: {item['type'] or 'unknown'}")

    @classmethod
    def _get_skills(cls, skill_configs: Sequence[str] | None) -> Skills | None:
        if not skill_configs:
            return None

        skill_paths: list[str] = []
        for item in skill_configs:
            try:
                raw_path = str(item).strip()
                if not raw_path:
                    continue
                path_obj = Path(raw_path)
                resolved = path_obj if path_obj.is_absolute() else AI_SKILLS_DIR.joinpath(path_obj)
                resolved = resolved.resolve()
                if resolved.is_dir():
                    skill_paths.append(str(resolved))
                else:
                    log.info(f"技能目录不存在，跳过: {resolved}")
            except Exception as e:
                log.error(f"技能加载失败: {e!s} item={item}")

        if not skill_paths:
            return None

        unique_paths = list(dict.fromkeys(skill_paths))
        loaders = [LocalSkills(path) for path in unique_paths]
        return Skills(loaders=loaders)

    @classmethod
    def _get_tools(cls, tools_configs: Sequence[str] | None, conversation_id, auth: Any = None) -> Toolkit | None:
        if not tools_configs:
            return []
        tools_map = AIToolsService.map_tools()
        requested_tools = list(tools_configs)
        missing_tools = [tool_name for tool_name in requested_tools if tool_name not in tools_map]
        if missing_tools:
            log.warning(f"请求的内部工具不存在，已跳过: {missing_tools}")
        log.info(f"加载内部工具: requested={requested_tools}, available={list(tools_map.keys())}")
        tools = []
        for t in tools_configs:
            if tools_map.get(t):
                tools.append(tools_map[t])
        fs = FilesService(get_file_dir(conversation_id))
        fs._ensure_ai_file_dir()
        metadata = {"auth": auth} if auth else {}
        ai_tools = AIToolsService.create_toolkit_from_openharness_tools(
            tools,
            cwd=fs.FILE_DIR,
            toolkit_name="fast3_tools",
            metadata=metadata
        )
        return [ai_tools]

    @staticmethod
    def _get_headers(
            server_config: dict[str, Any],
            authorization: str | None = None,
            extra_headers: dict[str, str] | None = None,
    ) -> dict[str, str]:
        raw_headers = server_config.get("headers", {})
        if isinstance(raw_headers, dict):
            headers: dict[str, str] = {
                str(key): str(value)
                for key, value in raw_headers.items()
                if key is not None and value is not None
            }
        else:
            headers = {}

        if isinstance(extra_headers, dict):
            for key, value in extra_headers.items():
                if key is None or value is None:
                    continue
                header_name = str(key).strip()
                header_value = str(value).strip()
                if header_name and header_value:
                    headers[header_name] = header_value

        if authorization:
            header_name = next((key for key in headers if str(key).lower() == "authorization"), "Authorization")
            headers[header_name] = str(authorization).strip()

        return headers

    @staticmethod
    def _sanitize_tool_name_prefix(server_name: str) -> str:
        normalized = "".join(
            char if char.isascii() and (char.isalnum() or char == "_") else "_"
            for char in server_name
        ).strip("_")
        return normalized[:24] or "mcp"

    @staticmethod
    def _get_args(args: Any) -> list[str]:
        if isinstance(args, (list, tuple)):
            return [str(arg) for arg in args]
        if args is None or args == "":
            return []
        return [str(args)]

    @staticmethod
    def _get_env(env: Any) -> dict[str, str] | None:
        if not isinstance(env, dict):
            return None
        return {
            str(key): str(value)
            for key, value in env.items()
            if key is not None and value is not None
        }

    @staticmethod
    def _friendly_error_message(e: Exception) -> str:
        """将 OpenAI 或网络异常转换为友好的中文提示。"""
        # 尝试获取状态码与错误体
        status_code = getattr(e, "status_code", None)
        body = getattr(e, "body", None)
        message = getattr(e, "message", None) or None

        if body and isinstance(body, dict):
            message = body.get("message")

        if message:
            return f"请求失败: {message}"

        if status_code == 401:
            return "API Key 无效或过期，请检查配置。"
        elif status_code == 429:
            return "请求过多或额度不足，请稍后再试。"
        elif status_code == 500:
            return "AI 服务端发生错误，请稍后重试。"
        elif status_code == 502:
            return "OpenAI 兼容服务返回 502，请检查服务本身是否兼容 OpenAI SDK 请求格式。"
        elif status_code == 404:
            return "请求的模型或地址不存在。"

        return f"发生未知错误: {e!s}"

    @classmethod
    def _build_system_prompt(
            cls,
            system_prompt: str,
            file_markdowns: Sequence[dict[str, str]] | None = None,
    ) -> list[str]:
        instructions = ["使用中文回答;"]
        if system_prompt:
            instructions.append(system_prompt)

        if file_markdowns:
            file_prompt = build_file_context_prompt(file_markdowns)
            if file_prompt:
                instructions.append(file_prompt)

        return instructions


def build_file_context_prompt(file_markdowns: Sequence[dict[str, str]] | None = None) -> str:
    if not file_markdowns:
        return ""

    sections = ["以下是用户上传文件转换后的 Markdown 内容。回答问题时请优先结合这些文件内容，"
                "若用户问题与文件内容冲突，请明确指出并以文件内容为准。"]
    for index, item in enumerate(file_markdowns, start=1):
        file_name = str(item.get("name") or f"文件{index}")
        markdown = str(item.get("markdown") or "").strip()
        if not markdown:
            markdown = "[无可用内容]"
        sections.append(f"【上传文件{index}】{file_name}\n{markdown}")
    return "\n\n".join(sections)
