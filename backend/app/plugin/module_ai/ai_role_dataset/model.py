# -*- coding: utf-8 -*-

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin


class AiRoleDatasetModel(ModelMixin):
    """
    AIRoleDataset表
    """
    __tablename__: str = 'ai_role_dataset'
    __table_args__: dict[str, str] = {'comment': 'AIRoleDataset'}

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_role.id", ondelete="CASCADE", onupdate="CASCADE"),
        comment="角色ID",
    )
    datasets_id: Mapped[str] = mapped_column(
        String(100),
        comment="知识库ID",
    )
    permission: Mapped[str] = mapped_column(
        String(16),
        comment="权限类型(只读, 读写)",
    )
