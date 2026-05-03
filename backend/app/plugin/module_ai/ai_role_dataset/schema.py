# -*- coding: utf-8 -*-

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class AiRoleDatasetCreateSchema(BaseModel):
    """
    AIRoleDataset新增模型
    """
    role_id: int = Field(default=..., description='')
    datasets_id: str = Field(default=..., description='')
    permission: str = Field(default=..., description='')
    status: str = Field(default="0", description='')
    description: str | None = Field(default=None, max_length=255, description='')


class AiRoleDatasetUpdateSchema(AiRoleDatasetCreateSchema):
    """
    AIRoleDataset更新模型
    """
    ...


class AiRoleDatasetOutSchema(AiRoleDatasetCreateSchema, BaseSchema, UserBySchema):
    """
    AIRoleDataset响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class AiRoleDatasetQueryParam:
    """AIRoleDataset查询参数"""

    def __init__(
            self,
            role_id: int | None = Query(None, description=""),
            datasets_id: str | None = Query(None, description=""),
            permission: str | None = Query(None, description=""),
            status: str | None = Query(None, description=""),
            created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围",
                                                           examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
            updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围",
                                                           examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.role_id = role_id
        # 精确查询字段
        self.datasets_id = datasets_id
        # 精确查询字段
        self.permission = permission
        # 精确查询字段
        self.status = status
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
