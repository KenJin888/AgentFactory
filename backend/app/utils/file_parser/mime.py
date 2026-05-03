# -*- coding: utf-8 -*-
"""
MIME类型检测和适配器映射

提供文件MIME类型检测功能和MIME类型到适配器的映射。
"""

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_adapter import BaseFileAdapter


async def detect_mime_type(file_path: str) -> str:
    """
    检测文件的MIME类型

    首先尝试使用 python-magic 库检测，如果失败则使用文件扩展名推断。

    Args:
        file_path: 文件路径

    Returns:
        str: MIME类型
    """
    import aiofiles

    # 首先尝试使用 magic 检测
    try:
        import magic
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(file_path)
        if mime_type and mime_type != "application/octet-stream":
            return mime_type
    except Exception:
        pass

    # 尝试读取文件头部进行判断
    try:
        async with aiofiles.open(file_path, "rb") as f:
            header = await f.read(8)

        # PDF
        if header.startswith(b"%PDF"):
            return "application/pdf"

        # PNG
        if header.startswith(b"\x89PNG\r\n\x1a\n"):
            return "image/png"

        # JPEG
        if header.startswith(b"\xff\xd8\xff"):
            return "image/jpeg"

        # GIF
        if header.startswith(b"GIF87a") or header.startswith(b"GIF89a"):
            return "image/gif"

        # ZIP (包括 Office 文档)
        if header.startswith(b"PK\x03\x04"):
            # 可能是 Office 文档
            return "application/zip"
    except Exception:
        pass

    # 根据扩展名推断
    ext = Path(file_path).suffix.lower()
    mime_map = {
        ".txt": "text/plain",
        ".md": "text/markdown",
        ".markdown": "text/markdown",
        ".json": "application/json",
        ".yaml": "application/x-yaml",
        ".yml": "application/x-yaml",
        ".xml": "application/xml",
        ".csv": "text/csv",
        ".html": "text/html",
        ".htm": "text/html",
        ".css": "text/css",
        ".js": "application/javascript",
        ".ts": "application/typescript",
        ".py": "text/x-python",
        ".java": "text/x-java",
        ".c": "text/x-c",
        ".cpp": "text/x-cpp",
        ".cc": "text/x-cpp",
        ".h": "text/x-c-header",
        ".hpp": "text/x-c++hdr",
        ".cs": "text/x-csharp",
        ".go": "text/x-go",
        ".rb": "text/x-ruby",
        ".php": "text/x-php",
        ".rs": "text/x-rust",
        ".swift": "text/x-swift",
        ".kt": "text/x-kotlin",
        ".scala": "text/x-scala",
        ".pl": "text/x-perl",
        ".lua": "text/x-lua",
        ".sh": "application/x-sh",
        ".sql": "text/x-sql",
        ".pdf": "application/pdf",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".ppt": "application/vnd.ms-powerpoint",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".xls": "application/vnd.ms-excel",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
        ".tiff": "image/tiff",
        ".tif": "image/tiff",
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".m4a": "audio/mp4",
        ".aac": "audio/aac",
        ".ogg": "audio/ogg",
        ".flac": "audio/flac",
        ".vue": "text/x-vue",
        ".tsx": "text/typescript-jsx",
        ".jsx": "text/jsx",
        ".dart": "text/x-dart",
        ".r": "text/x-r",
        ".m": "text/x-matlab",
        ".sass": "text/x-sass",
        ".scss": "text/x-scss",
        ".less": "text/x-less",
        ".ini": "text/x-ini",
        ".toml": "text/x-toml",
        ".conf": "text/x-config",
        ".cfg": "text/x-config",
        ".properties": "text/x-properties",
        ".env": "text/x-env",
        ".dockerfile": "text/x-dockerfile",
        ".gitignore": "text/x-gitignore",
    }

    if ext in mime_map:
        return mime_map[ext]

    # 尝试文本检测
    if await _is_likely_text_file(file_path):
        return "text/plain"

    return "application/octet-stream"


async def _is_likely_text_file(file_path: str, bytes_to_read: int = 1024) -> bool:
    """
    检查文件是否可能是文本文件

    Args:
        file_path: 文件路径
        bytes_to_read: 读取的字节数

    Returns:
        bool: 是否可能是文本文件
    """
    import aiofiles

    try:
        async with aiofiles.open(file_path, "rb") as f:
            content = await f.read(bytes_to_read)

        if not content:
            return False

        # 检查空字节
        if b"\x00" in content:
            return False

        # 检查可打印字符比例
        non_text_chars = 0
        for byte in content:
            if not (32 <= byte <= 126 or byte in (9, 10, 13)):
                non_text_chars += 1

        non_text_ratio = non_text_chars / len(content) if content else 0
        return non_text_ratio <= 0.1

    except Exception:
        return False


def get_mime_type_adapter_map() -> dict[str, str]:
    """
    获取MIME类型到适配器类名的映射

    Returns:
        dict: MIME类型到适配器类名的映射
    """
    return {
        # 文本格式
        "text/plain": "TextFileAdapter",
        "text/markdown": "TextFileAdapter",
        "text/csv": "CsvFileAdapter",
        "application/json": "TextFileAdapter",
        "application/x-yaml": "TextFileAdapter",
        "application/xml": "TextFileAdapter",
        "text/xml": "TextFileAdapter",
        "text/html": "CodeFileAdapter",
        "text/css": "CodeFileAdapter",

        # 代码格式
        "application/javascript": "CodeFileAdapter",
        "application/typescript": "CodeFileAdapter",
        "text/javascript": "CodeFileAdapter",
        "text/typescript": "CodeFileAdapter",
        "text/x-python": "CodeFileAdapter",
        "text/x-python-script": "CodeFileAdapter",
        "text/x-java": "CodeFileAdapter",
        "text/x-c": "CodeFileAdapter",
        "text/x-cpp": "CodeFileAdapter",
        "text/x-c-header": "CodeFileAdapter",
        "text/x-c++hdr": "CodeFileAdapter",
        "text/x-csharp": "CodeFileAdapter",
        "text/x-go": "CodeFileAdapter",
        "text/x-ruby": "CodeFileAdapter",
        "text/x-php": "CodeFileAdapter",
        "text/x-rust": "CodeFileAdapter",
        "text/x-swift": "CodeFileAdapter",
        "text/x-kotlin": "CodeFileAdapter",
        "text/x-scala": "CodeFileAdapter",
        "text/x-perl": "CodeFileAdapter",
        "text/x-lua": "CodeFileAdapter",
        "application/x-sh": "CodeFileAdapter",
        "text/x-sql": "CodeFileAdapter",
        "text/x-vue": "CodeFileAdapter",
        "text/typescript-jsx": "CodeFileAdapter",
        "text/jsx": "CodeFileAdapter",
        "text/x-dart": "CodeFileAdapter",
        "text/x-r": "CodeFileAdapter",
        "text/x-matlab": "CodeFileAdapter",
        "text/x-sass": "CodeFileAdapter",
        "text/x-scss": "CodeFileAdapter",
        "text/x-less": "CodeFileAdapter",
        "text/x-ini": "CodeFileAdapter",
        "text/x-toml": "CodeFileAdapter",
        "text/x-config": "CodeFileAdapter",
        "text/x-properties": "CodeFileAdapter",
        "text/x-env": "CodeFileAdapter",
        "text/x-dockerfile": "CodeFileAdapter",
        "text/x-gitignore": "CodeFileAdapter",

        # 音频格式
        "audio/mpeg": "AudioFileAdapter",
        "audio/mp3": "AudioFileAdapter",
        "audio/wav": "AudioFileAdapter",
        "audio/x-wav": "AudioFileAdapter",
        "audio/mp4": "AudioFileAdapter",
        "audio/x-m4a": "AudioFileAdapter",
        "audio/m4a": "AudioFileAdapter",
        "audio/aac": "AudioFileAdapter",
        "audio/ogg": "AudioFileAdapter",
        "audio/flac": "AudioFileAdapter",

        # Excel格式
        "application/vnd.ms-excel": "ExcelFileAdapter",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "ExcelFileAdapter",
        "application/vnd.oasis.opendocument.spreadsheet": "ExcelFileAdapter",

        # 图片格式
        "image/jpeg": "ImageFileAdapter",
        "image/jpg": "ImageFileAdapter",
        "image/png": "ImageFileAdapter",
        "image/gif": "ImageFileAdapter",
        "image/webp": "ImageFileAdapter",
        "image/bmp": "ImageFileAdapter",
        "image/tiff": "ImageFileAdapter",

        # PDF格式
        "application/pdf": "PdfFileAdapter",

        # Word文档格式
        "application/msword": "DocFileAdapter",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "DocFileAdapter",

        # PowerPoint格式
        "application/vnd.ms-powerpoint": "PptFileAdapter",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": "PptFileAdapter",
    }
