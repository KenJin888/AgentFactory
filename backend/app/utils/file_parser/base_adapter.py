# -*- coding: utf-8 -*-
"""
文件适配器基类

定义文件解析的通用接口和基础功能。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class FileMetaData:
    """文件元数据"""
    file_name: str = ""
    file_size: int = 0
    file_description: str = ""
    file_created: datetime = field(default_factory=datetime.now)
    file_modified: datetime = field(default_factory=datetime.now)
    file_hash: str = ""


class BaseFileAdapter(ABC):
    """文件适配器基类"""

    def __init__(self, file_path: str, max_file_size: int = 30 * 1024 * 1024):
        """
        初始化文件适配器

        Args:
            file_path: 文件路径
            max_file_size: 最大文件大小（字节），默认30MB
        """
        self.file_path = file_path
        self.max_file_size = max_file_size
        self.mime_type: str | None = None
        self.file_meta_data: FileMetaData | None = None

    async def _read_file(self) -> bytes:
        """读取文件内容"""
        from aiofiles import open as aio_open
        async with aio_open(self.file_path, "rb") as f:
            return await f.read()

    def _calculate_file_hash(self, file_buffer: bytes) -> str:
        """计算文件哈希值"""
        import hashlib
        return hashlib.sha256(file_buffer).hexdigest()

    async def _extract_basic_info(self) -> dict[str, Any]:
        """提取文件基本信息"""
        import aiofiles
        import os

        stat = await aiofiles.os.stat(self.file_path)
        return {
            "file_size": stat.st_size,
            "file_created": datetime.fromtimestamp(stat.st_ctime),
            "file_modified": datetime.fromtimestamp(stat.st_mtime),
        }

    async def _preprocess_file(self) -> None:
        """预处理文件，检测MIME类型"""
        from .mime import detect_mime_type
        self.mime_type = await detect_mime_type(self.file_path)

    async def process_file(self) -> FileMetaData | None:
        """
        处理文件，提取元数据

        Returns:
            FileMetaData: 文件元数据
        """
        if not self.mime_type:
            await self._preprocess_file()

        if not self.file_meta_data:
            try:
                basic_info = await self._extract_basic_info()
                self.file_meta_data = FileMetaData(
                    file_name=Path(self.file_path).name,
                    file_size=basic_info["file_size"],
                    file_description=self._get_file_description(),
                    file_created=basic_info["file_created"],
                    file_modified=basic_info["file_modified"],
                )
            except Exception as e:
                from app.core.logger import log
                log.error(f"Error processing file: {e}")
                return None

        return self.file_meta_data

    @abstractmethod
    def _get_file_description(self) -> str:
        """获取文件描述"""
        pass

    @abstractmethod
    async def get_content(self) -> str | None:
        """
        获取文件原始内容

        Returns:
            str: 文件内容
        """
        pass

    @abstractmethod
    async def get_llm_content(self) -> str | None:
        """
        获取适合LLM处理的内容格式

        Returns:
            str: LLM友好的内容格式
        """
        pass

    async def get_thumbnail(self) -> str | None:
        """
        获取文件缩略图（如适用）

        Returns:
            str: 缩略图数据（base64编码）
        """
        return None
