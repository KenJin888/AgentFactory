# -*- coding: utf-8 -*-
"""
文件解析模块

提供多种文件类型的解析功能，支持文本、代码、PDF、Word、Excel、CSV、图片、音频等格式。
参考 mcp_chat2 项目的 filePresenter 实现。
"""

from .base_adapter import BaseFileAdapter, FileMetaData
from .file_parser_service import FileParserService, MessageFile, ParseOptions
from .mime import detect_mime_type, get_mime_type_adapter_map

__all__ = [
    "BaseFileAdapter",
    "FileMetaData",
    "FileParserService",
    "MessageFile",
    "ParseOptions",
    "detect_mime_type",
    "get_mime_type_adapter_map",
]
