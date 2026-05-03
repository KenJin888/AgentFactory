from __future__ import annotations

import json
from typing import Any, Awaitable, Callable, Literal

from pydantic import BaseModel, Field

from app.api.v1.module_system.params.schema import ParamsQueryParam
from app.api.v1.module_system.params.service import ParamsService
from app.core.database import async_db_session
from app.core.dependencies import redis_getter
from app.plugin.module_ai.ai_agent.service import AiAgentService
from app.plugin.module_ai.ai_mcp.schema import AiMcpQueryParam
from app.plugin.module_ai.ai_mcp.service import AiMcpService
from app.plugin.module_ai.ai_skills.service import get_skills

from openharness.tools.base import BaseTool, ToolExecutionContext, ToolResult
from app.plugin.module_ai.ai_tools.tool import get_cls_object


class ListResourcesToolInput(BaseModel):
    """Arguments for the list resources tool."""

    resource_type: Literal["skills", "tools", "knowledge_base", "models", "all"] = Field(
        description="要查询的类型：skills=技能，tools=工具，knowledge_base=知识库，models=模型，all=返回所有资源列表"
    )


class ListResourcesTool(BaseTool):
    """List available resources.

    A tool to retrieve the list of available resources (skills, tools, knowledge bases) from the system.
    """
    name = "list_resources"
    description = "获取系统可用的资源列表，支持返回 skills（技能）、tools（工具）、knowledge_base（知识库）、models（模型）的列表。可一次性获取全部或指定类型。"
    input_model = ListResourcesToolInput

    async def execute(
            self,
            arguments: ListResourcesToolInput,
            context: ToolExecutionContext,
    ) -> ToolResult:
        auth = context.metadata.get('auth')
        if auth is None:
            return ToolResult(
                output="错误：缺少认证信息，无法获取资源列表",
                is_error=True
            )

        try:
            async with async_db_session() as session:
                async with session.begin():
                    from app.api.v1.module_system.auth.schema import AuthSchema
                    save_auth = AuthSchema(
                        db=session,
                        user=auth.user,
                        check_data_scope=auth.check_data_scope,
                    )

                    fetchers: dict[str, Callable[[Any], Awaitable[Any]]] = {
                        "skills": lambda _auth: self._get_skills(),
                        "tools": self._get_tools,
                        "knowledge_base": self._get_knowledge_base,
                        "models": self._get_models,
                        "all": self._get_all,
                    }
                    success_messages = {
                        "skills": "获取技能列表成功",
                        "tools": "获取工具列表成功",
                        "knowledge_base": "获取知识库列表成功",
                        "models": "获取模型列表成功",
                        "all": "获取全部列表成功",
                    }
                    result = await fetchers[arguments.resource_type](save_auth)
                    return ToolResult(
                        output=f"{success_messages[arguments.resource_type]}：{json.dumps(result, ensure_ascii=False)}"
                    )

        except Exception as e:
            return ToolResult(
                output=f"执行操作失败：{str(e)}",
                is_error=True
            )

    async def _get_skills(self) -> list[dict[str, Any]]:
        redis = redis_getter
        result = await get_skills(False, redis)
        return result['skills']

    async def _get_tools(self, auth) -> dict[str, Any]:
        from app.plugin.module_ai.ai_tools.service import get_tools
        redis = redis_getter
        page = 1
        page_size = 200
        search = get_cls_object(AiMcpQueryParam, {"status": "0"})
        mcp_list = []
        while True:
            result_dict = await AiMcpService.page_ai_mcp_service(
                auth=auth,
                page_no=page,
                page_size=page_size,
                search=search,
            )
            for d in result_dict['items']:
                data = {
                    'name': d['name'],
                    'description': d['abstract']
                }
                mcp_list.append(data)
            if page * page_size < result_dict['total']:
                page += 1
            else:
                break
        result = await get_tools(False, redis)
        res_data = {
            'external_tools': mcp_list,
            'internal_tools': result['tools']
        }
        return res_data

    async def _get_knowledge_base(self, auth) -> list[dict[str, Any]]:
        try:
            page = 1
            page_size = 200
            knowledge_base_list = []
            while True:
                result_dict = await AiAgentService.list_available_knowledge_datasets_service(
                    auth=auth,
                    page=page,
                    page_size=page_size,
                )
                knowledge_base_list += result_dict
                if len(result_dict) == 200:
                    page += 1
                else:
                    break
            return knowledge_base_list
        except Exception:
            return []

    async def _get_models(self, auth) -> list[dict[str, Any]]:
        search_param = ParamsQueryParam(
            config_key="aisaas_models",
            config_name=None,
            config_type=None,
            description=None,
            status=None,
            created_time=None,
            updated_time=None,
        )
        order_by = [{"updated_time": "desc"}]
        model_list = []
        obj_list = await ParamsService.get_obj_list_service(auth=auth, search=search_param, order_by=order_by)
        for obj in obj_list:
            config_value = json.loads(obj["config_value"])
            for data in config_value:
                if data.get("models"):
                    model_list += data["models"]
        return model_list

    async def _get_all(self, auth) -> dict[str, Any]:
        res_data = await self._get_tools(auth)
        res_data["skills"] = await self._get_skills()
        res_data["knowledge_base"] = await self._get_knowledge_base(auth)
        res_data["models"] = await self._get_models(auth)
        return res_data
