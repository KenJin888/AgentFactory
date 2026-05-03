from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, Field

from app.core.database import async_db_session
from app.plugin.module_ai.ai_agent.schema import (
    AiAgentCreateSchema,
    AiAgentUpdateSchema,
)
from app.plugin.module_ai.ai_agent.service import AiAgentService
from openharness.tools.base import BaseTool, ToolExecutionContext, ToolResult


class ManageAgentToolInput(BaseModel):
    """Arguments for the manage agent tool."""

    action: str = Field(
        description="要执行的操作类型：create=创建新智能体，update=修改智能体，get=查询单个智能体详情，list=查询智能体列表"
    )
    agent_id: int = Field(default=None, description="智能体ID（update 和 get 操作时必填）")
    name: str = Field(default="", description="智能体名称（create 和 update 时可选）")
    description: str = Field(default="", description="智能体描述")
    system_prompt: str = Field(default="", description="系统提示词（create 和 update 时常用）")
    type: str = Field(default="", description="智能体类型")
    config: str = Field(default="", description='智能体配置(内容从 list_resources 获取,参数格式：{"mcp":{"activeSkills":["my-cli-tool"],"externalTools":["time-mcp"],"internalTools":["manage_agent","list_models","list_resources"],"knowledge":[{"name":"操作说明书","dataset_id":"315c917c396a11f1a2107a2bf96f4c3a"}]},"welcome":"开场白，可以为空"})')
    model: str = Field(default="", description='模型配置(内容从 list_models 获取,参数格式:{"id":"deepseek-chat","name"...)')
    cover: str = Field(default="", description="封面图片URL")


class ManageAgentTool(BaseTool):
    """Manage agents.

    A tool to manage agents: create, update, get, and list agents.
    """
    name = "manage_agent"
    description = "统一管理智能体（Agent）的工具。可用于创建新的智能体、更新已有智能体的信息、或查询智能体的详情。根据传入的操作类型（action）执行对应功能。"
    input_model = ManageAgentToolInput

    async def execute(
            self,
            arguments: ManageAgentToolInput,
            context: ToolExecutionContext,
    ) -> ToolResult:
        auth = context.metadata.get('auth')
        if auth is None:
            return ToolResult(
                output="错误：缺少认证信息，无法执行智能体管理操作",
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

                    if arguments.action == 'create':
                        result = await self._create_agent(save_auth, arguments)
                        return ToolResult(
                            output=f"创建智能体成功：{json.dumps(result, ensure_ascii=False)}"
                        )
                    elif arguments.action == 'update':
                        result = await self._update_agent(save_auth, arguments)
                        return ToolResult(
                            output=f"更新智能体成功：{json.dumps(result, ensure_ascii=False)}"
                        )
                    elif arguments.action == 'get':
                        result = await self._get_agent(save_auth, arguments)
                        return ToolResult(
                            output=f"获取智能体详情成功：{json.dumps(result, ensure_ascii=False)}"
                        )
                    elif arguments.action == 'list':
                        result = await self._list_agents(save_auth, arguments)
                        return ToolResult(
                            output=f"获取智能体列表成功：{json.dumps(result, ensure_ascii=False)}"
                        )
                    else:
                        return ToolResult(
                            output=f"action参数错误: {arguments.action}，仅支持 create/update/get/list",
                            is_error=True
                        )
        except Exception as e:
            return ToolResult(
                output=f"执行操作失败：{str(e)}",
                is_error=True
            )

    async def _create_agent(self, auth, arguments: ManageAgentToolInput) -> dict[str, Any]:
        create_data = AiAgentCreateSchema(
            status="0",
            name=arguments.name or "未命名智能体",
            description=arguments.description,
            type=arguments.type,
            config=arguments.config,
            prompt_template=arguments.system_prompt,
            model=arguments.model,
            cover=arguments.cover,
            order_no=0,
        )
        return await AiAgentService.create_ai_agent_service(auth=auth, data=create_data)

    async def _update_agent(self, auth, arguments: ManageAgentToolInput) -> dict[str, Any]:
        if not arguments.agent_id:
            raise ValueError("agent_id 不能为空")
        update_data = AiAgentUpdateSchema(
            status="0",
            name=arguments.name,
            description=arguments.description,
            type=arguments.type,
            config=arguments.config,
            prompt_template=arguments.system_prompt,
            model=arguments.model,
            cover=arguments.cover,
            order_no=0,
        )
        return await AiAgentService.update_ai_agent_service(auth=auth, id=arguments.agent_id, data=update_data)

    async def _get_agent(self, auth, arguments: ManageAgentToolInput) -> dict[str, Any]:
        if not arguments.agent_id:
            raise ValueError("agent_id 不能为空")
        return await AiAgentService.detail_ai_agent_service(auth=auth, id=arguments.agent_id)

    async def _list_agents(self, auth, arguments: ManageAgentToolInput) -> list[dict[str, Any]]:
        search = type("SearchParam", (), {})()
        search.publish_status = ("!=", "delete")
        search.visibility_scope = "private"
        return await AiAgentService.list_ai_agent_service(auth=auth, search=search)
