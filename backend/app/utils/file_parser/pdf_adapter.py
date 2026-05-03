# -*- coding: utf-8 -*-
"""
PDF文件适配器

支持PDF文件的解析和内容提取。
"""

from pathlib import Path

from .base_adapter import BaseFileAdapter


class PdfFileAdapter(BaseFileAdapter):
    """PDF文件适配器"""

    def __init__(self, file_path: str, max_file_size: int = 30 * 1024 * 1024):
        super().__init__(file_path, max_file_size)
        self._file_content: str | None = None
        self._pdf_data: dict | None = None

    def _get_file_description(self) -> str:
        """获取文件描述"""
        return "PDF Document"

    async def _load_pdf_data(self) -> dict | None:
        """加载PDF数据"""
        if self._pdf_data is not None:
            return self._pdf_data

        from aiofiles import open as aio_open
        import aiofiles

        stat = await aiofiles.os.stat(self.file_path)
        if stat.st_size > self.max_file_size:
            return None

        try:
            async with aio_open(self.file_path, "rb") as f:
                buffer = await f.read()

            # 使用 pypdf 解析 PDF
            from pypdf import PdfReader
            from io import BytesIO

            reader = PdfReader(BytesIO(buffer))
            num_pages = len(reader.pages)

            # 提取每页文本
            page_contents = []
            for page in reader.pages:
                text = page.extract_text() or ""
                page_contents.append(text.strip())

            # 获取PDF信息
            info = reader.metadata or {}

            self._pdf_data = {
                "num_pages": num_pages,
                "info": {
                    "title": info.title if info else None,
                    "author": info.author if info else None,
                    "creator": info.creator if info else None,
                    "producer": info.producer if info else None,
                    "subject": info.subject if info else None,
                },
                "page_contents": page_contents,
            }

            return self._pdf_data

        except Exception as e:
            from app.core.logger import log
            log.error(f"Error parsing PDF: {e}")
            return None

    async def get_content(self) -> str | None:
        """获取文件原始内容"""
        if self._file_content is None:
            pdf_data = await self._load_pdf_data()
            if pdf_data:
                self._file_content = "\n\n--- Page Separator ---\n\n".join(
                    pdf_data["page_contents"]
                )
        return self._file_content

    async def get_llm_content(self) -> str | None:
        """获取适合LLM处理的内容格式"""
        pdf_data = await self._load_pdf_data()
        if not pdf_data:
            return None

        # 构建Markdown格式的内容
        pages_markdown = []
        for i, page_content in enumerate(pdf_data["page_contents"], 1):
            # 转换文本为Markdown格式
            markdown_content = self._convert_text_to_markdown(page_content)
            pages_markdown.append(f"## Page {i}\n\n{markdown_content}")

        all_pages_markdown = "\n\n---\n\n".join(pages_markdown)

        info = pdf_data["info"]
        return f"""# PDF file description

## Basic PDF file information
* **Total pages:** {pdf_data["num_pages"]}
* **PDF title:** {info.get("title") or "Unknown"}
* **PDF author:** {info.get("author") or "Unknown"}
* **PDF creator:** {info.get("creator") or "Unknown"}
* **PDF producer:** {info.get("producer") or "Unknown"}

## PDF content (page by page)
{all_pages_markdown}
"""

    def _convert_text_to_markdown(self, text: str) -> str:
        """将文本转换为Markdown格式"""
        if not text:
            return ""

        lines = text.split("\n")
        paragraphs = []
        current_paragraph = ""

        for line in lines:
            trimmed_line = line.strip()

            if not trimmed_line:
                if current_paragraph:
                    paragraphs.append(current_paragraph)
                    current_paragraph = ""
                continue

            if current_paragraph:
                # 检查是否是新段落
                last_char = current_paragraph[-1] if current_paragraph else ""
                first_char = trimmed_line[0] if trimmed_line else ""

                if (
                    last_char in ".?!"
                    and first_char.isupper()
                    and first_char.isalpha()
                ):
                    paragraphs.append(current_paragraph)
                    current_paragraph = trimmed_line
                else:
                    current_paragraph += " " + trimmed_line
            else:
                current_paragraph = trimmed_line

        if current_paragraph:
            paragraphs.append(current_paragraph)

        # 处理每个段落
        markdown_paragraphs = []
        for paragraph in paragraphs:
            if not paragraph.strip():
                continue

            # 检查是否是标题
            if len(paragraph) < 100:
                # 可能是主标题（全大写，短）
                if paragraph == paragraph.upper() and len(paragraph) < 50:
                    markdown_paragraphs.append(f"# {paragraph}")
                    continue

                # 可能是副标题（以冒号结尾，无句号）
                if paragraph.endswith(":") and "." not in paragraph:
                    markdown_paragraphs.append(f"## {paragraph}")
                    continue

            # 检查是否是编号列表项
            import re
            if re.match(r"^\d+\.?\s", paragraph):
                markdown_paragraphs.append(re.sub(r"^(\d+)\.?\s", r"\1. ", paragraph))
                continue

            # 检查是否是项目符号
            if re.match(r"^[•\-*]\s", paragraph):
                markdown_paragraphs.append(re.sub(r"^[•\-*]\s", "* ", paragraph))
                continue

            # 普通段落
            markdown_paragraphs.append(paragraph)

        return "\n\n".join(markdown_paragraphs)

    async def get_thumbnail(self) -> str | None:
        """获取缩略图"""
        return None
