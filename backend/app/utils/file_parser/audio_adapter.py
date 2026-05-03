# -*- coding: utf-8 -*-
"""
音频文件适配器

支持多种音频格式的解析，仅返回文件路径信息。
"""

from pathlib import Path

from .base_adapter import BaseFileAdapter


class AudioFileAdapter(BaseFileAdapter):
    """音频文件适配器"""

    def __init__(self, file_path: str, max_file_size: int = 30 * 1024 * 1024):
        super().__init__(file_path, max_file_size)

    def _get_file_description(self) -> str:
        """获取文件描述"""
        ext = Path(self.file_path).suffix.lower()
        descriptions = {
            ".mp3": "MP3 Audio File",
            ".wav": "WAV Audio File",
            ".m4a": "M4A Audio File",
            ".aac": "AAC Audio File",
            ".ogg": "OGG Audio File",
            ".flac": "FLAC Audio File",
        }
        return descriptions.get(ext, "Audio File")

    async def get_content(self) -> str | None:
        """
        获取文件原始内容

        对于音频文件，仅返回文件路径信息，不读取二进制内容。
        """
        return f"Audio file path: {self.file_path}"

    async def get_llm_content(self) -> str | None:
        """
        获取适合LLM处理的内容格式

        对于音频文件，仅返回文件路径信息。
        """
        return f"Audio file path: {self.file_path}"

    async def get_thumbnail(self) -> str | None:
        """获取缩略图"""
        return None
