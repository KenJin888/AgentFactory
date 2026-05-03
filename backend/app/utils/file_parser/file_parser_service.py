# -*- coding: utf-8 -*-
"""
文件解析服务

提供统一的文件解析接口，支持多种文件类型。
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .base_adapter import BaseFileAdapter, FileMetaData


@dataclass
class ParseOptions:
    """解析选项"""
    max_file_size: int = 30 * 1024 * 1024  # 默认30MB
    content_type: str | None = "llm-friendly"  # 'origin', 'llm-friendly', None


@dataclass
class MessageFile:
    """消息文件数据结构"""
    name: str = ""
    path: str = ""
    mime_type: str = ""
    token: int = 0
    content: str = ""
    thumbnail: str | None = None
    metadata: dict = field(default_factory=dict)


class FileParserService:
    """文件解析服务"""

    def __init__(self, max_file_size: int = 30 * 1024 * 1024):
        """
        初始化文件解析服务

        Args:
            max_file_size: 最大文件大小（字节）
        """
        self.max_file_size = max_file_size
        self._adapter_cache: dict[str, BaseFileAdapter] = {}

    def _get_adapter_class(self, mime_type: str) -> type[BaseFileAdapter]:
        """
        根据MIME类型获取适配器类

        Args:
            mime_type: MIME类型

        Returns:
            BaseFileAdapter: 适配器类
        """
        from .mime import get_mime_type_adapter_map
        from .text_adapter import TextFileAdapter
        from .code_adapter import CodeFileAdapter
        from .pdf_adapter import PdfFileAdapter
        from .doc_adapter import DocFileAdapter
        from .excel_adapter import ExcelFileAdapter
        from .csv_adapter import CsvFileAdapter
        from .image_adapter import ImageFileAdapter
        from .ppt_adapter import PptFileAdapter
        from .audio_adapter import AudioFileAdapter
        from .unsupported_adapter import UnsupportedFileAdapter

        adapter_map = {
            "TextFileAdapter": TextFileAdapter,
            "CodeFileAdapter": CodeFileAdapter,
            "PdfFileAdapter": PdfFileAdapter,
            "DocFileAdapter": DocFileAdapter,
            "ExcelFileAdapter": ExcelFileAdapter,
            "CsvFileAdapter": CsvFileAdapter,
            "ImageFileAdapter": ImageFileAdapter,
            "PptFileAdapter": PptFileAdapter,
            "AudioFileAdapter": AudioFileAdapter,
            "UnsupportedFileAdapter": UnsupportedFileAdapter,
        }

        mime_adapter_map = get_mime_type_adapter_map()

        # 首先尝试精确匹配
        adapter_name = mime_adapter_map.get(mime_type)
        if adapter_name and adapter_name in adapter_map:
            return adapter_map[adapter_name]

        # 尝试通配符匹配
        type_prefix = mime_type.split("/")[0] if "/" in mime_type else ""
        wildcard = f"{type_prefix}/*"
        adapter_name = mime_adapter_map.get(wildcard)
        if adapter_name and adapter_name in adapter_map:
            return adapter_map[adapter_name]

        # 默认返回不支持的适配器
        return UnsupportedFileAdapter

    async def create_adapter(self, file_path: str, mime_type: str | None = None) -> BaseFileAdapter:
        """
        创建文件适配器

        Args:
            file_path: 文件路径
            mime_type: MIME类型（可选，如果不提供则自动检测）

        Returns:
            BaseFileAdapter: 文件适配器实例
        """
        if not mime_type:
            from .mime import detect_mime_type
            mime_type = await detect_mime_type(file_path)

        adapter_class = self._get_adapter_class(mime_type)
        return adapter_class(file_path, self.max_file_size)

    async def parse_file(
        self,
        file_path: str,
        mime_type: str | None = None,
        options: ParseOptions | None = None,
    ) -> MessageFile:
        """
        解析文件

        Args:
            file_path: 文件路径
            mime_type: MIME类型（可选）
            options: 解析选项

        Returns:
            MessageFile: 解析后的文件信息
        """
        if options is None:
            options = ParseOptions()

        # 创建适配器
        adapter = await self.create_adapter(file_path, mime_type)

        # 处理文件
        await adapter.process_file()

        # 获取内容
        content = ""
        if options.content_type == "llm-friendly":
            content = await adapter.get_llm_content() or ""
        elif options.content_type == "origin":
            content = await adapter.get_content() or ""

        # 获取缩略图
        thumbnail = await adapter.get_thumbnail()

        # 构建元数据
        metadata = {}
        if adapter.file_meta_data:
            metadata = {
                "fileName": adapter.file_meta_data.file_name,
                "fileSize": adapter.file_meta_data.file_size,
                "fileDescription": adapter.file_meta_data.file_description,
                "fileCreated": adapter.file_meta_data.file_created.isoformat() if adapter.file_meta_data.file_created else None,
                "fileModified": adapter.file_meta_data.file_modified.isoformat() if adapter.file_meta_data.file_modified else None,
            }

        # 计算token数（简单估算）
        token_count = self._estimate_tokens(content, adapter.mime_type or "")

        return MessageFile(
            name=adapter.file_meta_data.file_name if adapter.file_meta_data else Path(file_path).name,
            path=file_path,
            mime_type=adapter.mime_type or "application/octet-stream",
            token=token_count,
            content=content,
            thumbnail=thumbnail,
            metadata=metadata,
        )

    def _estimate_tokens(self, content: str, mime_type: str) -> int:
        """
        估算token数量

        Args:
            content: 内容
            mime_type: MIME类型

        Returns:
            int: 估算的token数
        """
        if not content:
            return 0

        # 图片文件特殊处理
        if mime_type.startswith("image/"):
            # 对于base64图片，估算token数
            if content.startswith("data:image"):
                # base64编码的图片，大约4/3的字符对应1个token
                base64_data = content.split(",")[1] if "," in content else content
                return len(base64_data) // 4
            return 0

        # 音频文件
        if mime_type.startswith("audio/"):
            return len(content) // 4

        # 文本内容：大约4个字符对应1个token
        return len(content) // 4

    async def parse_upload_file(
        self,
        upload_file: Any,  # FastAPI UploadFile
        options: ParseOptions | None = None,
    ) -> MessageFile:
        """
        解析上传的文件

        Args:
            upload_file: FastAPI UploadFile 对象
            options: 解析选项

        Returns:
            MessageFile: 解析后的文件信息
        """
        import aiofiles
        import aiofiles.os
        import tempfile

        if options is None:
            options = ParseOptions()

        # 创建临时文件
        temp_dir = tempfile.gettempdir()
        file_name = upload_file.filename or "unnamed_file"
        temp_path = Path(temp_dir) / file_name

        try:
            # 保存上传的文件到临时目录
            content = await upload_file.read()

            # 检查文件大小
            if len(content) > options.max_file_size:
                raise ValueError(f"File size exceeds maximum allowed size: {options.max_file_size} bytes")

            async with aiofiles.open(temp_path, "wb") as f:
                await f.write(content)

            # 解析文件
            mime_type = upload_file.content_type
            result = await self.parse_file(str(temp_path), mime_type, options)

            return result

        finally:
            # 清理临时文件
            try:
                if await aiofiles.os.path.exists(str(temp_path)):
                    await aiofiles.os.remove(str(temp_path))
            except Exception:
                pass

    async def parse_multiple_files(
        self,
        file_paths: list[str],
        options: ParseOptions | None = None,
    ) -> list[MessageFile]:
        """
        解析多个文件

        Args:
            file_paths: 文件路径列表
            options: 解析选项

        Returns:
            list[MessageFile]: 解析后的文件信息列表
        """
        import asyncio

        tasks = [self.parse_file(file_path, options=options) for file_path in file_paths]
        return await asyncio.gather(*tasks)

    async def validate_file(self, file_path: str) -> dict[str, Any]:
        """
        验证文件是否可解析

        Args:
            file_path: 文件路径

        Returns:
            dict: 验证结果
        """
        try:
            path = Path(file_path)

            if not path.exists():
                return {"valid": False, "error": "File not found"}

            if not path.is_file():
                return {"valid": False, "error": "Path is not a file"}

            import aiofiles
            stat = await aiofiles.os.stat(file_path)

            if stat.st_size > self.max_file_size:
                return {
                    "valid": False,
                    "error": f"File size exceeds maximum allowed size: {self.max_file_size} bytes",
                }

            mime_type = await self.create_adapter(file_path)

            return {
                "valid": True,
                "mime_type": mime_type,
                "size": stat.st_size,
            }

        except Exception as e:
            return {"valid": False, "error": str(e)}

    def get_supported_extensions(self) -> list[str]:
        """
        获取支持的文件扩展名列表

        Returns:
            list[str]: 支持的文件扩展名列表
        """
        return [
            ".txt", ".md", ".markdown", ".json", ".yaml", ".yml", ".xml", ".csv",
            ".html", ".htm", ".css", ".js", ".ts", ".tsx", ".jsx", ".py", ".java",
            ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".cs", ".go", ".rb", ".php",
            ".rs", ".swift", ".kt", ".scala", ".pl", ".lua", ".sh", ".sql",
            ".vue", ".svelte", ".sass", ".scss", ".less",
            ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx",
            ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".tif",
            ".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac",
        ]

    def get_supported_mime_types(self) -> list[str]:
        """
        获取支持的MIME类型列表

        Returns:
            list[str]: 支持的MIME类型列表
        """
        from .mime import get_mime_type_adapter_map
        mime_map = get_mime_type_adapter_map()
        return [mime for mime in mime_map.keys() if "*" not in mime]
