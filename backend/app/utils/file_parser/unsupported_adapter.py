# -*- coding: utf-8 -*-
"""
不支持的文件适配器

用于处理无法识别的文件类型。
"""

from pathlib import Path

from .base_adapter import BaseFileAdapter


class UnsupportedFileAdapter(BaseFileAdapter):
    """不支持的文件适配器"""

    def __init__(self, file_path: str, max_file_size: int = 30 * 1024 * 1024):
        super().__init__(file_path, max_file_size)

    def _get_file_description(self) -> str:
        """获取文件描述"""
        ext = Path(self.file_path).suffix.lower()
        return f"Unsupported File Type ({ext})"

    async def get_content(self) -> str | None:
        """获取文件原始内容"""
        return ""

    async def get_llm_content(self) -> str | None:
        """获取适合LLM处理的内容格式"""
        return ""

    async def get_thumbnail(self) -> str | None:
        """获取缩略图"""
        return None
