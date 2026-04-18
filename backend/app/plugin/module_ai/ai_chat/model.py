# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Integer, DateTime, Text, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class AiChatModel(ModelMixin, UserMixin):
    """
    ai_chat表
    """
    __tablename__: str = 'ai_chat'
    __table_args__: dict[str, str] = {'comment': 'ai_chat'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='用户ID')
    agent_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='智能体ID')
    title: Mapped[str] = mapped_column(String(200), nullable=False, default='', comment='会话标题')
    model_info: Mapped[str] = mapped_column(Text, nullable=False, default='', comment='模型信息')
    tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='耗费token数量')

    model_id: Mapped[str] = mapped_column(String(100), nullable=False, default='', comment='模型ID')
    provider_id: Mapped[str] = mapped_column(String(100), nullable=False, default='', comment='服务商ID')
    parent_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment='父会话ID')

