# -*- coding: utf-8 -*-

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class AiAgentModel(ModelMixin, UserMixin):
    """
    ai_agent表
    """
    __tablename__: str = 'ai_agent'
    __table_args__: dict[str, str] = {'comment': 'ai_agent'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str] = mapped_column(String(100), nullable=False, default='', comment='智能体名称')
    type: Mapped[str] = mapped_column(String(100), nullable=False, default='', comment='智能体类型')
    visibility_scope: Mapped[str] = mapped_column(String(20), nullable=False, default='private',
                                                  comment='可见范围(private/public)')
    publish_status: Mapped[str] = mapped_column(String(20), nullable=False, default='draft',
                                                comment='发布状态(draft/published/clone/offline/delete)')
    version_no: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='版本号')
    public_agent_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='成功发布的公用智能体ID')
    config: Mapped[str] = mapped_column(Text, nullable=False, default='', comment='智能体配置')
    prompt_template: Mapped[str] = mapped_column(Text, nullable=False, default='', comment='提示词模板')
    model: Mapped[str] = mapped_column(Text, nullable=False, default='', comment='模型配置')
    cover: Mapped[str] = mapped_column(String(200), nullable=False, default='', comment='封面图片URL')

    total_usage: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='使用次数')
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='智能体评分')
    order_no: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='排序号')


