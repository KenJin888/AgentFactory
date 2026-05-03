# -*- coding: utf-8 -*-
"""
文本文件适配器

支持普通文本文件、Markdown、JSON、YAML、XML等格式的解析。
"""

from pathlib import Path

from .base_adapter import BaseFileAdapter


class TextFileAdapter(BaseFileAdapter):
    """文本文件适配器"""

    def __init__(self, file_path: str, max_file_size: int = 30 * 1024 * 1024):
        super().__init__(file_path, max_file_size)
        self._file_content: str | None = None

    def _get_file_description(self) -> str:
        """获取文件描述"""
        ext = Path(self.file_path).suffix.lower()
        descriptions = {
            ".md": "Markdown Document",
            ".markdown": "Markdown Document",
            ".json": "JSON File",
            ".yaml": "YAML File",
            ".yml": "YAML File",
            ".xml": "XML File",
            ".txt": "Text File",
        }
        return descriptions.get(ext, "Text File")

    async def get_content(self) -> str | None:
        """获取文件原始内容"""
        if self._file_content is None:
            from aiofiles import open as aio_open

            full_path = Path(self.file_path)
            if not full_path.exists():
                return None

            import aiofiles
            stat = await aiofiles.os.stat(self.file_path)
            if stat.st_size > self.max_file_size:
                return None

            async with aio_open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                self._file_content = await f.read()

        return self._file_content

    async def get_llm_content(self) -> str | None:
        """获取适合LLM处理的内容格式"""
        content = await self.get_content()
        if content is None:
            return None

        ext = Path(self.file_path).suffix.lower()
        language_map = {
            ".md": "markdown",
            ".markdown": "markdown",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".xml": "xml",
            ".txt": "",
        }
        language = language_map.get(ext, "")

        if language:
            return f"## File Content\n\n```{language}\n{content}\n```"
        return f"## File Content\n\n```\n{content}\n```"

    async def get_thumbnail(self) -> str | None:
        """获取缩略图"""
        return None
