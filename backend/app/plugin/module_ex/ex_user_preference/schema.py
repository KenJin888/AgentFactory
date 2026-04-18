from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class ExUserPreferenceCreateSchema(BaseModel):
    user_id: int = Field(..., description="用户ID")
    pref_key: str = Field(..., max_length=100, description="偏好键")
    pref_value: str | None = Field(default=None, description="偏好值(JSON字符串)")
    status: str = Field(default="0", description="是否启用(0:启用 1:禁用)")
    description: str | None = Field(default=None, max_length=255, description="备注")

    @field_validator("pref_key")
    @classmethod
    def validate_pref_key(cls, value: str) -> str:
        v = value.strip()
        if not v:
            raise ValueError("偏好键不能为空")
        return v


class ExUserPreferenceUpdateSchema(BaseModel):
    user_id: int | None = Field(default=None, description="用户ID")
    pref_key: str | None = Field(default=None, max_length=100, description="偏好键")
    pref_value: str | None = Field(default=None, description="偏好值(JSON字符串)")
    status: str | None = Field(default=None, description="是否启用(0:启用 1:禁用)")
    description: str | None = Field(default=None, max_length=255, description="备注")

    @field_validator("pref_key")
    @classmethod
    def validate_pref_key(cls, value: str | None) -> str | None:
        if value is None:
            return value
        v = value.strip()
        if not v:
            raise ValueError("偏好键不能为空")
        return v


class ExUserPreferenceSetMySchema(BaseModel):
    pref_value: str | None = Field(default=None, description="偏好值(JSON字符串)")


class ExUserPreferenceOutSchema(ExUserPreferenceCreateSchema, BaseSchema, UserBySchema):
    model_config = ConfigDict(from_attributes=True)


@dataclass
class ExUserPreferenceQueryParam:
    def __init__(
        self,
        user_id: int | None = Query(None, description="用户ID"),
        pref_key: str | None = Query(None, description="偏好键"),
        status: str | None = Query(None, description="是否启用"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围"),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围"),
    ) -> None:
        if user_id is not None:
            self.user_id = ("eq", user_id)
        if pref_key:
            self.pref_key = ("like", pref_key)
        if status:
            self.status = ("eq", status)
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
