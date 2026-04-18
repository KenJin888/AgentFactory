# -*- coding: utf-8 -*-

from typing import Any

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class AiChatCreateSchema(BaseModel):
    """
    ai_chat新增模型
    """
    status: str = Field(default="0", description='是否启用(0:启用 1:禁用)')
    description: str | None = Field(default="", max_length=255, description='备注/描述')
    user_id: int = Field(default=0, description='用户ID')
    agent_id: int = Field(default=0, description='智能体ID')
    title: str = Field(default="", description='会话标题')
    model_info: str = Field(default="", description='模型信息')
    tokens: int = Field(default=0, description='耗费token数量')
    model_id: str = Field(default="", max_length=100, description='模型ID')
    provider_id: str = Field(default="", max_length=100, description='服务商ID')
    parent_id: int = Field(default=0, description='父会话ID')


class AiChatUpdateSchema(AiChatCreateSchema):
    """
    ai_chat更新模型
    """
    ...


class AiChatCompletionMessage(BaseModel):
    role: str = Field(..., min_length=1, max_length=20, description="角色")
    content: str = Field(..., min_length=1, max_length=4000, description="内容")


class AiChatResponseSchema(BaseModel):
    schema_key: str | None = Field(default=None, min_length=1, max_length=100, description="预置结构名")
    json_schema: dict[str, Any] | None = Field(default=None, description="用户自定义 JSON Schema")


class UserMessageContent(BaseModel):
    think: bool | None = Field(default=None, description="是否启用深度思考")
    search: bool | None = Field(default=None, description="是否启用联网搜索")
    text: str = Field(..., description="用户输入文本")
    continue_: bool | None = Field(default=None, alias="continue", description="是否继续生成")
    files: list[dict[str, Any]] | None = Field(default=None, description="上传文件列表")
    resources: list[Any] | None = Field(default=None, description="资源列表")
    prompts: list[Any] | None = Field(default=None, description="提示词列表")
    links: list[str] | None = Field(default=None, description="链接列表")
    content: Any = Field(default=None, description="富文本内容")


class AiChatCompletionSchema(BaseModel):
    provider: str | None = Field(default=None, description="模型提供商")
    model: str | None = Field(default=None, min_length=1, max_length=100, description="模型名称")
    userMessage: UserMessageContent = Field(..., description="用户消息")
    # messages?: AiChatCompletionMessage[] = Field(default=None, description="对话消息列表")
    conversation_id: int | None = Field(default=None, description="会话ID")
    system_prompt: str | None = Field(default=None, description="系统提示词")
    context_length: int | None = Field(default=None, ge=512, le=128000, description="上下文长度预算")
    temperature: float | None = Field(default=None, description="温度参数")
    response_schema: AiChatResponseSchema | None = Field(default=None, description="结构化输出约束")


class AiChatCompletionSaveSchema(BaseModel):
    conversation_id: int = Field(..., gt=0, description="会话ID(chat_id)")
    role: str = Field(..., min_length=1, max_length=20, description="角色")
    content: str = Field(..., min_length=1, description="内容")
    token_count: int = Field(default=0, ge=0, description="token数量")
    input_tokens: int = Field(default=0, ge=0, description="输入token数量")
    output_tokens: int = Field(default=0, ge=0, description="输出token数量")


class AiChatCompletionStopSchema(BaseModel):
    conversation_id: int = Field(..., gt=0, description="浼氳瘽ID")


class AiChatOutSchema(AiChatCreateSchema, BaseSchema, UserBySchema):
    """
    ai_chat响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class AiChatQueryParam:
    """ai_chat查询参数"""

    def __init__(
            self,
            status: str | None = Query(None, description="是否启用(0:启用 1:禁用)"),
            created_id: int | None = Query(None, description="创建人ID"),
            updated_id: int | None = Query(None, description="更新人ID"),
            user_id: int | None = Query(None, description="用户ID"),
            agent_id: int | None = Query(None, description="智能体ID"),
            title: str | None = Query(None, description="会话标题"),
            model_info: str | None = Query(None, description="模型信息"),
            tokens: int | None = Query(None, description="耗费token数量"),
            model_id: str | None = Query(None, description="模型ID"),
            provider_id: str | None = Query(None, description="服务商ID"),
            parent_id: int | None = Query(None, description="父会话ID"),
            created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围",
                                                           examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
            updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围",
                                                           examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.status = status
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 精确查询字段
        self.user_id = user_id
        # 精确查询字段
        self.agent_id = agent_id
        # 精确查询字段
        self.title = title
        # 精确查询字段
        self.model_info = model_info
        # 精确查询字段
        self.tokens = tokens
        # 精确查询字段
        self.model_id = model_id
        # 精确查询字段
        self.provider_id = provider_id
        # 精确查询字段
        self.parent_id = parent_id
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
