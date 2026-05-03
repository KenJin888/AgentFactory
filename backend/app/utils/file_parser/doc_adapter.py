# -*- coding: utf-8 -*-
"""
Word文档适配器

支持 .doc 和 .docx 文件的解析。
"""

from pathlib import Path

from .base_adapter import BaseFileAdapter


class DocFileAdapter(BaseFileAdapter):
    """Word文档适配器"""

    def __init__(self, file_path: str, max_file_size: int = 30 * 1024 * 1024):
        super().__init__(file_path, max_file_size)
        self._file_content: str | None = None
        self._html_content: str | None = None

    def _get_file_description(self) -> str:
        """获取文件描述"""
        return "Word Document"

    async def _load_document_content(self) -> str | None:
        """加载文档内容"""
        if self._html_content is not None:
            return self._html_content

        from aiofiles import open as aio_open
        import aiofiles

        stat = await aiofiles.os.stat(self.file_path)
        if stat.st_size > self.max_file_size:
            return None

        try:
            async with aio_open(self.file_path, "rb") as f:
                buffer = await f.read()

            # 使用 mammoth 转换 Word 文档
            import mammoth
            from io import BytesIO

            result = mammoth.convert_to_html(
                BytesIO(buffer),
                convert_image=mammoth.images.img_element(lambda image: {"src": ""}),
            )
            self._html_content = result.value
            return self._html_content

        except Exception as e:
            from app.core.logger import log
            log.error(f"Error parsing Word document: {e}")
            return None

    async def get_content(self) -> str | None:
        """获取文件原始内容"""
        if self._file_content is None:
            html = await self._load_document_content()
            if html:
                # 将HTML转换为纯文本
                from html.parser import HTMLParser

                class HTMLStripper(HTMLParser):
                    def __init__(self):
                        super().__init__()
                        self.text = []

                    def handle_data(self, data):
                        self.text.append(data)

                    def get_text(self):
                        return " ".join(self.text)

                stripper = HTMLStripper()
                stripper.feed(html)
                self._file_content = stripper.get_text()

        return self._file_content

    async def get_llm_content(self) -> str | None:
        """获取适合LLM处理的内容格式"""
        html = await self._load_document_content()
        if not html:
            return None

        # 将HTML转换为Markdown
        try:
            import markdownify
            markdown = markdownify.markdownify(html, heading_style="ATX")
        except ImportError:
            # 如果没有 markdownify，使用简单的HTML到文本转换
            from html.parser import HTMLParser

            class HTMLToTextParser(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.text = []
                    self.in_script = False

                def handle_starttag(self, tag, attrs):
                    if tag in ("script", "style"):
                        self.in_script = True
                    elif tag in ("p", "div", "br", "h1", "h2", "h3", "h4", "h5", "h6"):
                        self.text.append("\n")
                    elif tag in ("li",):
                        self.text.append("\n* ")

                def handle_endtag(self, tag):
                    if tag in ("script", "style"):
                        self.in_script = False
                    elif tag in ("p", "div", "h1", "h2", "h3", "h4", "h5", "h6"):
                        self.text.append("\n")

                def handle_data(self, data):
                    if not self.in_script:
                        self.text.append(data)

            parser = HTMLToTextParser()
            parser.feed(html)
            markdown = "".join(parser.text)

        # 分页处理
        pages = self._paginate_content(markdown)

        file_description = f"""# Word Document Description

## Basic Word Document Information
* **Total Pages:** {len(pages)}

## Document Content
"""

        # 为每页生成预览
        pages_content = []
        for i, page in enumerate(pages, 1):
            pages_content.append(f"""### Page {i}
```
{page}
```
""")

        return file_description + "\n".join(pages_content)

    def _paginate_content(self, markdown: str) -> list[str]:
        """将内容分页"""
        import re

        # 按标题分页
        heading_pattern = re.compile(r"^(#{1,2})\s", re.MULTILINE)
        pages = heading_pattern.split(markdown)

        # 移除第一个空元素（如果存在）
        if pages and not pages[0].strip():
            pages.pop(0)

        # 重新组合页面
        result = []
        for i in range(0, len(pages), 2):
            if i + 1 < len(pages):
                result.append(f"{pages[i]}{pages[i + 1]}")
            else:
                result.append(pages[i])

        return result if result else [markdown]

    async def get_thumbnail(self) -> str | None:
        """获取缩略图"""
        return None
