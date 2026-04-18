# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AiAgentAuthCreateSchema(BaseModel):
    agent_id: int = Field(..., description="智能体ID")
    target_type: str = Field(..., description="授权对象类型(global/role/user)")
    target_value: str | None = Field(default=None, description="授权对象值")
    target_right: int = Field(default=1, description="权限值(1可见 2可克隆)")
    granted_by: int = Field(..., description="授权人ID")


class AiAgentAuthRuleSchema(BaseModel):
    target_type: str = Field(..., description="授权对象类型(global/role/user)")
    target_value: str | None = Field(default=None, description="授权对象值")
    target_right: int = Field(default=1, description="权限值(1可见 2可克隆)")

    @model_validator(mode="after")
    def validate_rule(self):
        target_type = str(self.target_type or "").strip()
        if target_type not in {"global", "role", "user"}:
            raise ValueError("target_type 必须为 global/role/user")

        if self.target_right not in {1, 2}:
            raise ValueError("target_right 必须为 1 或 2")

        if target_type == "global":
            self.target_value = None
            return self

        target_value = str(self.target_value or "").strip()
        if not target_value:
            raise ValueError("target_value 不能为空")

        self.target_value = str(int(target_value))
        return self


class AiAgentAuthRuleOutSchema(AiAgentAuthRuleSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = Field(default=None, description="主键ID")
    target_label: str | None = Field(default=None, description="授权对象名称")
    granted_by: int | None = Field(default=None, description="授权人ID")
    granted_at: str | None = Field(default=None, description="授权时间")
