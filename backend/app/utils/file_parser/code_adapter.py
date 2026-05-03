# -*- coding: utf-8 -*-
"""
代码文件适配器

支持多种编程语言代码文件的解析。
"""

from pathlib import Path

from .base_adapter import BaseFileAdapter


class CodeFileAdapter(BaseFileAdapter):
    """代码文件适配器"""

    def __init__(self, file_path: str, max_file_size: int = 30 * 1024 * 1024):
        super().__init__(file_path, max_file_size)
        self._file_content: str | None = None
        self.mime_type = "text/code"

    def _get_file_description(self) -> str:
        """获取文件描述"""
        ext = Path(self.file_path).suffix.lower()
        descriptions = {
            ".js": "JavaScript Source File",
            ".ts": "TypeScript Source File",
            ".tsx": "React TypeScript Component",
            ".jsx": "React JavaScript Component",
            ".py": "Python Source File",
            ".java": "Java Source File",
            ".c": "C Source File",
            ".cpp": "C++ Source File",
            ".cc": "C++ Source File",
            ".cxx": "C++ Source File",
            ".h": "C/C++ Header File",
            ".hpp": "C++ Header File",
            ".hxx": "C++ Header File",
            ".hh": "C++ Header File",
            ".cs": "C# Source File",
            ".go": "Go Source File",
            ".rb": "Ruby Source File",
            ".php": "PHP Source File",
            ".rs": "Rust Source File",
            ".swift": "Swift Source File",
            ".kt": "Kotlin Source File",
            ".scala": "Scala Source File",
            ".pl": "Perl Source File",
            ".lua": "Lua Source File",
            ".sh": "Shell Script",
            ".html": "HTML File",
            ".htm": "HTML File",
            ".css": "CSS File",
            ".vue": "Vue.js Component File",
            ".svelte": "Svelte Component File",
            ".sass": "Sass File",
            ".scss": "SCSS File",
            ".less": "Less File",
            ".sql": "SQL Script",
            ".dart": "Dart Source File",
            ".r": "R Source File",
            ".m": "MATLAB/Objective-C Source File",
            ".json": "JSON File",
            ".yaml": "YAML File",
            ".yml": "YAML File",
            ".xml": "XML File",
            ".md": "Markdown File",
            ".toml": "TOML File",
            ".ini": "INI Configuration File",
            ".env": "Environment Configuration File",
            ".conf": "Configuration File",
            ".config": "Configuration File",
            ".properties": "Properties Configuration File",
            ".lock": "Lock File",
            ".gitignore": "Git Ignore File",
            ".dockerignore": "Docker Ignore File",
            ".dockerfile": "Dockerfile",
            ".editorconfig": "Editor Configuration File",
            ".babelrc": "Babel Configuration File",
            ".eslintrc": "ESLint Configuration File",
            ".prettierrc": "Prettier Configuration File",
        }
        return descriptions.get(ext, "Source Code File")

    def _get_language_from_filename(self) -> str:
        """从文件名获取编程语言标识"""
        ext = Path(self.file_path).suffix.lower()
        filename = Path(self.file_path).name.lower()

        language_map = {
            ".js": "javascript",
            ".ts": "typescript",
            ".tsx": "tsx",
            ".jsx": "jsx",
            ".py": "python",
            ".java": "java",
            ".c": "c",
            ".cpp": "cpp",
            ".cc": "cpp",
            ".cxx": "cpp",
            ".h": "c",
            ".hpp": "cpp",
            ".hxx": "cpp",
            ".hh": "cpp",
            ".cs": "csharp",
            ".go": "go",
            ".rb": "ruby",
            ".php": "php",
            ".rs": "rust",
            ".swift": "swift",
            ".kt": "kotlin",
            ".scala": "scala",
            ".pl": "perl",
            ".lua": "lua",
            ".sh": "bash",
            ".html": "html",
            ".htm": "html",
            ".css": "css",
            ".vue": "vue",
            ".svelte": "svelte",
            ".sass": "sass",
            ".scss": "scss",
            ".less": "less",
            ".sql": "sql",
            ".dart": "dart",
            ".r": "r",
            ".m": "matlab",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".xml": "xml",
            ".md": "markdown",
            ".toml": "toml",
            ".ini": "ini",
        }

        # 特殊文件名处理
        special_files = {
            ".gitignore": "gitignore",
            ".dockerignore": "gitignore",
            "dockerfile": "dockerfile",
            ".env": "env",
            ".babelrc": "json",
            ".eslintrc": "json",
            ".prettierrc": "json",
            ".editorconfig": "ini",
        }

        if filename in special_files:
            return special_files[filename]

        return language_map.get(ext, "")

    async def get_content(self) -> str | None:
        """获取文件原始内容"""
        if self._file_content is None:
            from aiofiles import open as aio_open
            import aiofiles

            full_path = Path(self.file_path)
            if not full_path.exists():
                return None

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

        language = self._get_language_from_filename()
        if language:
            return f"```{language}\n{content}\n```"
        return f"```\n{content}\n```"

    async def get_thumbnail(self) -> str | None:
        """获取缩略图"""
        return None
