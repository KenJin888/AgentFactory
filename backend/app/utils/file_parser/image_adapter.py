# -*- coding: utf-8 -*-
"""
图片文件适配器

支持多种图片格式的解析，提供缩略图和LLM友好的base64格式。
"""

from pathlib import Path

from .base_adapter import BaseFileAdapter


class ImageFileAdapter(BaseFileAdapter):
    """图片文件适配器"""

    def __init__(self, file_path: str, max_file_size: int = 30 * 1024 * 1024):
        super().__init__(file_path, max_file_size)
        self._image_metadata: dict | None = None

    def _get_file_description(self) -> str:
        """获取文件描述"""
        return "Image File"

    async def _extract_image_metadata(self) -> dict:
        """提取图片元数据"""
        if self._image_metadata is not None:
            return self._image_metadata

        try:
            from PIL import Image

            with Image.open(self.file_path) as img:
                self._image_metadata = {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                    "mode": img.mode,
                }
        except Exception as e:
            from app.core.logger import log
            log.error(f"Error extracting image metadata: {e}")
            # 如果PIL失败，至少获取格式
            ext = Path(self.file_path).suffix.lower()
            format_map = {
                ".jpg": "JPEG",
                ".jpeg": "JPEG",
                ".png": "PNG",
                ".gif": "GIF",
                ".webp": "WEBP",
                ".bmp": "BMP",
                ".tiff": "TIFF",
                ".tif": "TIFF",
            }
            self._image_metadata = {
                "width": None,
                "height": None,
                "format": format_map.get(ext, "Unknown"),
                "mode": None,
            }

        return self._image_metadata

    async def _compress_image(self, max_size: tuple[int, int] = (1200, 1200), quality: int = 70) -> bytes:
        """压缩图片"""
        from PIL import Image
        import io

        with Image.open(self.file_path) as img:
            # 转换为RGB（处理RGBA、P模式等）
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # 调整大小
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # 保存为JPEG
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=quality, optimize=True)
            return buffer.getvalue()

    async def get_content(self) -> str | None:
        """获取文件原始内容（返回空，图片内容不适合文本显示）"""
        return ""

    async def get_llm_content(self) -> str | None:
        """
        获取适合LLM处理的内容格式

        返回压缩后的base64编码图片，适合多模态LLM处理。
        """
        import aiofiles

        stat = await aiofiles.os.stat(self.file_path)
        if stat.st_size > self.max_file_size:
            return None

        try:
            # 压缩图片
            compressed_data = await self._compress_image(max_size=(1200, 1200), quality=70)

            # 转换为base64
            import base64
            base64_string = base64.b64encode(compressed_data).decode("utf-8")

            return f"data:image/jpeg;base64,{base64_string}"

        except Exception as e:
            from app.core.logger import log
            log.error(f"Error processing image for LLM: {e}")
            return None

    async def get_thumbnail(self) -> str | None:
        """
        获取缩略图

        Returns:
            str: base64编码的缩略图
        """
        try:
            # 生成缩略图
            compressed_data = await self._compress_image(max_size=(256, 256), quality=70)

            # 转换为base64
            import base64
            base64_string = base64.b64encode(compressed_data).decode("utf-8")

            return f"data:image/jpeg;base64,{base64_string}"

        except Exception as e:
            from app.core.logger import log
            log.error(f"Error generating thumbnail: {e}")
            return None

    async def get_image_info(self) -> dict:
        """获取图片信息"""
        metadata = await self._extract_image_metadata()
        return {
            "width": metadata.get("width"),
            "height": metadata.get("height"),
            "format": metadata.get("format"),
        }
