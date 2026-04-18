# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AiDatasetAuthCreateSchema(BaseModel):
    dataset_id: str = Field(..., description="知识库ID")
    target_type: str = Field(..., description="授权对象类型(global/role/user)")
    target_value: str | None = Field(default=None, description="授权对象值")
    target_right: int = Field(default=1, description="权限值(1只读 2读写)")
    granted_by: int = Field(..., description="授权人ID")


class AiDatasetAuthRuleSchema(BaseModel):
    target_type: str = Field(..., description="授权对象类型(global/role/user)")
    target_value: str | None = Field(default=None, description="授权对象值")
    target_right: int = Field(default=1, description="权限值(1只读 2读写)")

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


class AiDatasetAuthRuleOutSchema(AiDatasetAuthRuleSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = Field(default=None, description="主键ID")
    target_label: str | None = Field(default=None, description="授权对象名称")
    granted_by: int | None = Field(default=None, description="授权人ID")
    granted_at: str | None = Field(default=None, description="授权时间")
    is_default: bool = Field(default=False, description="是否为默认兼容规则")


class AiDatasetAuthRulesPayload(BaseModel):
    auth_rules: list[AiDatasetAuthRuleSchema] = Field(default_factory=list, description="授权规则")


class AiDatasetAuthRulesResponse(BaseModel):
    code: int = Field(default=0, description="状态码")
    message: str = Field(default="success", description="消息")
    data: list[AiDatasetAuthRuleOutSchema] = Field(default_factory=list, description="授权规则列表")
