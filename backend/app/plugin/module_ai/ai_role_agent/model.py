# -*- coding: utf-8 -*-

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin


class AiRoleAgentModel(ModelMixin):
    """
    AIRoleAgent表
    """
    __tablename__: str = 'ai_role_agent'
    __table_args__: dict[str, str] = {'comment': 'AIRoleAgent'}

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_role.id", ondelete="CASCADE", onupdate="CASCADE"),
        comment="角色ID",
    )
    agent_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ai_agent.id", ondelete="CASCADE", onupdate="CASCADE"),
        comment="智能体ID",
    )
    permission: Mapped[str] = mapped_column(
        String(16),
        comment="权限类型(只读, 读写)",
    )
