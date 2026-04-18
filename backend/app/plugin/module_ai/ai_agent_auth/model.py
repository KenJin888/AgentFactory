# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import MappedBase


class AiAgentAuthModel(MappedBase):
    """
    ai_agent_auth表
    """

    __tablename__: str = "ai_agent_auth"
    __table_args__ = (
        UniqueConstraint("agent_id", "target_type", "target_value", name="uq_ai_agent_auth_target"),
        {"comment": "智能体授权表"},
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="主键ID",
    )
    agent_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ai_agent.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
        comment="关联智能体ID",
    )
    target_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
        comment="授权对象类型(global/role/user)",
    )
    target_value: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        comment="授权对象值(global为空，role/user存ID)",
    )
    target_right: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        comment="权限值(1可见 2可克隆)",
    )
    granted_by: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="授权人ID",
    )
    granted_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
        comment="授权时间",
    )
