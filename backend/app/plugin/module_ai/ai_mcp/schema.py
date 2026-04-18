# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class AiMcpCreateSchema(BaseModel):
    """
    ai_mcp新增模型
    """
    status: str = Field(default="0", description='是否启用(0:启用 1:禁用)')
    description: str | None = Field(default="", max_length=255, description='备注/描述')
    name: str = Field(default="", description='mcp名称')
    type: str = Field(default="", description='类型')
    abstract: str = Field(default="", description='摘要')
    category: str = Field(default="", description='分类')
    config: str = Field(default="", description='mcp配置')
    tools: str = Field(default="", description='工具配置')
    cover: str = Field(default="", description='封面图片URL')


class AiMcpUpdateSchema(AiMcpCreateSchema):
    """
    ai_mcp更新模型
    """
    ...


class AiMcpOutSchema(AiMcpCreateSchema, BaseSchema, UserBySchema):
    """
    ai_mcp响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class AiMcpQueryParam:
    """ai_mcp查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="mcp名称"),
        status: str | None = Query(None, description="是否启用(0:启用 1:禁用)"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        type: str | None = Query(None, description="类型"),
        abstract: str | None = Query(None, description="摘要"),
        category: str | None = Query(None, description="分类"),
        config: str | None = Query(None, description="mcp配置"),
        tools: str | None = Query(None, description="工具配置"),
        cover: str | None = Query(None, description="封面图片URL"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.status = status
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 模糊查询字段
        self.name = ("like", name)
        # 精确查询字段
        self.type = type
        # 精确查询字段
        self.abstract = abstract
        # 精确查询字段
        self.category = category
        # 精确查询字段
        self.config = config
        # 精确查询字段
        self.tools = tools
        # 精确查询字段
        self.cover = cover
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
