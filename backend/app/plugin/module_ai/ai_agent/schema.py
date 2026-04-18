# -*- coding: utf-8 -*-

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr
from app.plugin.module_ai.ai_agent_auth.schema import AiAgentAuthRuleOutSchema, AiAgentAuthRuleSchema


class AiAgentBaseSchema(BaseModel):
    status: str = Field(default="0", description='是否启用(0:启用 1:禁用)')
    name: str = Field(default="", description='智能体名称')
    description: str | None = Field(default="", description='智能体描述')
    type: str = Field(default="", description='智能体类型')
    config: str = Field(default="", description='智能体配置')
    prompt_template: str = Field(default="", description='提示词模板')
    model: str = Field(default="", description='模型配置')
    cover: str = Field(default="", description='封面图片URL')
    order_no: int = Field(default=0, description='排序号')


class AiAgentCreateSchema(AiAgentBaseSchema):
    """
    ai_agent新增模型
    """


class AiAgentUpdateSchema(AiAgentBaseSchema):
    """
    ai_agent更新模型
    """


class AiAgentPersistSchema(AiAgentBaseSchema):
    visibility_scope: str = Field(default="private", description='可见范围(private/public)')
    publish_status: str = Field(default="draft", description='发布状态(draft/published/clone/offline/delete)')
    version_no: int = Field(default=0, description='版本号')
    public_agent_id: int = Field(default=0, description='成功发布的公用智能体ID')
    total_usage: int = Field(default=0, description='使用次数')
    score: int = Field(default=0, description='智能体评分')


class AiAgentPublishSchema(BaseModel):
    name: str = Field(default="", description='发布名称')
    description: str | None = Field(default="", description='发布说明')
    type: str = Field(default="", description='智能体类型')
    auth_rules: list[AiAgentAuthRuleSchema] = Field(default_factory=list, description='授权规则')


class AiAgentManageSchema(AiAgentPublishSchema):
    """
    管理广场智能体模型
    """
    order_no: int | None = Field(default=None, description='排序号')
    score: int | None = Field(default=None, description='智能体评分')
    total_usage: int | None = Field(default=None, description='使用次数')


class AiAgentOutSchema(AiAgentPersistSchema, BaseSchema, UserBySchema):
    """
    ai_agent响应模型
    """

    model_config = ConfigDict(from_attributes=True)

    current_right: int = Field(default=0, description='当前用户权限(0无权限 1可见 2可克隆)')
    can_view: bool = Field(default=False, description='是否可见/可用')
    can_clone: bool = Field(default=False, description='是否可克隆')
    can_manage: bool = Field(default=False, description='是否可管理')
    is_owner: bool = Field(default=False, description='是否创建者')
    is_admin: bool = Field(default=False, description='是否管理员')
    auth_rules: list[AiAgentAuthRuleOutSchema] = Field(default_factory=list, description='授权规则')


class AiAgentKnowledgeDatasetSchema(BaseModel):
    dataset_id: str = Field(default="", description="知识库ID")
    name: str = Field(default="", description="知识库名称")
    description: str | None = Field(default=None, description="知识库描述")
    document_count: int | None = Field(default=None, description="文档数量")


class AiAgentQueryParam:
    """ai_agent查询参数"""

    def __init__(
            self,
            name: str | None = Query(None, description="智能体名称"),
            status: str | None = Query(None, description="是否启用(0:启用 1:禁用)"),
            created_id: int | None = Query(None, description="创建人ID"),
            updated_id: int | None = Query(None, description="更新人ID"),
            type: str | None = Query(None, description="智能体类型"),
            visibility_scope: str | None = Query(None, description="可见范围(private/public)"),
            publish_status: str | None = Query(None, description="发布状态(draft/published/clone/offline/delete)"),
            version_no: int | None = Query(None, description="版本号"),
            public_agent_id: int | None = Query(None, description="成功发布的公用智能体ID"),
            config: str | None = Query(None, description="智能体配置"),
            prompt_template: str | None = Query(None, description="提示词模板"),
            model: str | None = Query(None, description="模型配置"),
            cover: str | None = Query(None, description="封面图片URL"),
            created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围",
                                                           examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
            updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围",
                                                           examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        self.status = status
        self.created_id = created_id
        self.updated_id = updated_id
        self.name = ("like", name)
        self.type = type
        self.visibility_scope = visibility_scope
        self.publish_status = publish_status
        self.version_no = version_no
        self.public_agent_id = public_agent_id
        self.config = config
        self.prompt_template = prompt_template
        self.model = model
        self.cover = cover
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
