from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class ExUserPreferenceModel(ModelMixin, UserMixin):
    __tablename__: str = "ex_user_preference"
    __table_args__ = (
        UniqueConstraint("user_id", "pref_key", name="uq_ex_user_preference_user_pref_key"),
        {"comment": "用户偏好表"},
    )
    __loader_options__: list[str] = ["created_by", "updated_by"]

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_user.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
        comment="用户ID",
    )
    pref_key: Mapped[str] = mapped_column(String(100), nullable=False, comment="偏好键")
    pref_value: Mapped[str | None] = mapped_column(Text, nullable=True, comment="偏好值")
