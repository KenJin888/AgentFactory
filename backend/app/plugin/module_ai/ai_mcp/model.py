# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Integer, DateTime, Text, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class AiMcpModel(ModelMixin, UserMixin):
    """
    ai_mcp表
    """
    __tablename__: str = 'ai_mcp'
    __table_args__: dict[str, str] = {'comment': 'ai_mcp'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, default='', comment='mcp名称')
    type: Mapped[str] = mapped_column(String(100), nullable=False, default='', comment='类型')
    abstract: Mapped[str] = mapped_column(String(200), nullable=False, default='', comment='摘要')
    category: Mapped[str] = mapped_column(String(200), nullable=False, default='', comment='分类')
    config: Mapped[str] = mapped_column(Text, nullable=False, default='', comment='mcp配置')
    tools: Mapped[str] = mapped_column(Text, nullable=False, default='', comment='工具配置')
    cover: Mapped[str] = mapped_column(String(200), nullable=False, default='', comment='封面图片URL')
