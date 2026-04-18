# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class AiChatMsgCreateSchema(BaseModel):
    """
    ai_chat_msg新增模型
    """
    status: str = Field(default="", description='状态')
    description: str = Field(default="", description='备注/描述')
    chat_id: int = Field(default=0, description='会话id')
    role: str = Field(default="", description='role')
    content: str = Field(default="", description='内容')
    order_seq: int = Field(default=0, description='排序序号')
    token_count: int = Field(default=0, description='token数量')
    input_tokens: int = Field(default=0, description='输入token数量')
    output_tokens: int = Field(default=0, description='输出token数量')
    parent_id: int = Field(default=0, description='父消息id')


class AiChatMsgUpdateSchema(AiChatMsgCreateSchema):
    """
    ai_chat_msg更新模型
    """
    ...


class AiChatMsgOutSchema(AiChatMsgCreateSchema, BaseSchema, UserBySchema):
    """
    ai_chat_msg响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class AiChatMsgQueryParam:
    """ai_chat_msg查询参数"""

    def __init__(
        self,
        status: str | None = Query(None, description="状态"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        chat_id: int | None = Query(None, description="会话id"),
        role: str | None = Query(None, description="role"),
        content: str | None = Query(None, description="内容"),
        order_seq: int | None = Query(None, description="排序序号"),
        token_count: int | None = Query(None, description="token数量"),
        input_tokens: int | None = Query(None, description="输入token数量"),
        output_tokens: int | None = Query(None, description="输出token数量"),
        parent_id: int | None = Query(None, description="父消息id"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.status = status
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 精确查询字段
        self.chat_id = chat_id
        # 精确查询字段
        self.role = role
        # 精确查询字段
        self.content = content
        # 精确查询字段
        self.order_seq = order_seq
        # 精确查询字段
        self.token_count = token_count
        # 精确查询字段
        self.input_tokens = input_tokens
        # 精确查询字段
        self.output_tokens = output_tokens
        # 精确查询字段
        self.parent_id = parent_id
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
