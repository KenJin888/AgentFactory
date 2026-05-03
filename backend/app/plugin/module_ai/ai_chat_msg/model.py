# -*- coding: utf-8 -*-

from sqlalchemy import Integer, Text, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class AiChatMsgModel(ModelMixin, UserMixin):
    """
    ai_chat_msg表
    """
    __tablename__: str = 'ai_chat_msg'
    __table_args__: dict[str, str] = {'comment': 'ai_chat_msg'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    chat_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='会话id')
    role: Mapped[str] = mapped_column(String(50), nullable=False, default='', comment='role')
    content: Mapped[str] = mapped_column(
        Text().with_variant(LONGTEXT(), "mysql"), nullable=False, default='', comment='内容')
    order_seq: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='排序序号')
    token_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='token数量')
    input_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='输入token数量')
    output_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='输出token数量')
    status: Mapped[str] = mapped_column(String(50), nullable=False, default='', comment='状态')
    parent_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='父消息id')
