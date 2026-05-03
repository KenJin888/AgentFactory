# -*- coding: utf-8 -*-
"""
CSV文件适配器

支持CSV文件的解析和Markdown表格转换。
"""

import csv
from io import StringIO
from pathlib import Path

from .base_adapter import BaseFileAdapter


class CsvFileAdapter(BaseFileAdapter):
    """CSV文件适配器"""

    def __init__(self, file_path: str, max_file_size: int = 30 * 1024 * 1024):
        super().__init__(file_path, max_file_size)
        self._file_content: str | None = None
        self._parsed_rows: list[list[str]] | None = None

    def _get_file_description(self) -> str:
        """获取文件描述"""
        return "CSV File"

    async def _load_content(self) -> str | None:
        """加载文件内容"""
        if self._file_content is not None:
            return self._file_content

        from aiofiles import open as aio_open
        import aiofiles

        stat = await aiofiles.os.stat(self.file_path)
        if stat.st_size > self.max_file_size:
            return None

        try:
            async with aio_open(self.file_path, "r", encoding="utf-8", errors="ignore") as f:
                self._file_content = await f.read()
            return self._file_content
        except Exception as e:
            from app.core.logger import log
            log.error(f"Error reading CSV file: {e}")
            return None

    def _parse_csv_content(self, content: str) -> list[list[str]]:
        """解析CSV内容"""
        rows = []
        try:
            reader = csv.reader(StringIO(content))
            for row in reader:
                # 清理单元格数据
                cleaned_row = [cell.strip().strip('"').strip("'") for cell in row]
                rows.append(cleaned_row)
        except Exception as e:
            from app.core.logger import log
            log.error(f"Error parsing CSV content: {e}")
            # 尝试简单分割
            rows = [
                [cell.strip().strip('"').strip("'") for cell in line.split(",")]
                for line in content.split("\n")
                if line.strip()
            ]

        # 过滤掉空行
        return [row for row in rows if any(cell for cell in row)]

    def _generate_table_markdown(self, rows: list[list[str]]) -> str:
        """生成Markdown表格"""
        if not rows:
            return ""

        headers = rows[0]
        data = rows[1:]

        # 生成表头
        markdown = "| " + " | ".join(headers) + " |\n"
        markdown += "| " + " | ".join(["---"] * len(headers)) + " |\n"

        # 生成数据行
        for row in data:
            # 确保行长度与表头一致
            padded_row = row + [""] * (len(headers) - len(row))
            padded_row = padded_row[:len(headers)]
            markdown += "| " + " | ".join(padded_row) + " |\n"

        return markdown

    async def get_content(self) -> str | None:
        """获取文件原始内容"""
        return await self._load_content()

    async def get_llm_content(self) -> str | None:
        """获取适合LLM处理的内容格式"""
        content = await self._load_content()
        if not content:
            return None

        rows = self._parse_csv_content(content)
        if not rows:
            return None

        headers = rows[0] if rows else []

        # 限制预览行数
        preview_rows = rows[:11]  # 表头 + 前10行数据

        return f"""# CSV File Description

## Basic CSV File Information
* **Total Rows:** {len(rows)}
* **Total Columns:** {len(headers)}

## Column Headers
{chr(10).join([f"{i + 1}. {header}" for i, header in enumerate(headers)])}

## Data Preview (First 10 Rows)
{self._generate_table_markdown(preview_rows)}
"""

    async def get_thumbnail(self) -> str | None:
        """获取缩略图"""
        return None
