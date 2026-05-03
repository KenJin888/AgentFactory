# -*- coding: utf-8 -*-
"""
AI聊天文件处理器

处理用户上传的文件，解析内容并整合到对话消息中。
"""

from collections.abc import Sequence
from typing import Any

from fastapi import UploadFile

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import log
from app.utils.file_parser import FileParserService, MessageFile, ParseOptions


_FILE_CONTEXT_INTRO = (
    "以下是用户上传文件转换后的内容。回答问题时请优先结合这些文件内容，"
    "若用户问题与文件内容冲突，请明确指出并以文件内容为准。"
)

_MAX_FILE_CONTENT_CHARS = 20000
_MAX_TOTAL_FILE_CONTEXT_CHARS = 60000


class AiChatFileProcessor:
    """AI聊天文件处理器"""

    def __init__(self):
        self.parser_service = FileParserService(
            max_file_size=settings.AI_CHAT_UPLOAD_MAX_FILE_SIZE
        )

    async def process_upload_files(
        self,
        files: Sequence[UploadFile] | None,
    ) -> list[dict[str, Any]]:
        """
        处理上传的文件列表

        Args:
            files: 上传的文件列表

        Returns:
            list[dict]: 处理后的文件信息列表
        """
        if not files:
            return []

        processed_files: list[dict[str, Any]] = []
        total_chars = 0

        for upload_file in files:
            file_name = upload_file.filename or "未命名文件"

            try:
                # 验证文件
                self._validate_upload_file(upload_file)

                # 解析文件
                options = ParseOptions(
                    max_file_size=settings.AI_CHAT_UPLOAD_MAX_FILE_SIZE,
                    content_type="llm-friendly",
                )

                message_file = await self.parser_service.parse_upload_file(
                    upload_file,
                    options=options,
                )

                # 处理内容长度限制
                processed_file = self._process_file_content(
                    message_file,
                    file_name,
                    total_chars,
                )

                if processed_file:
                    total_chars += len(processed_file.get("content", ""))
                    processed_files.append(processed_file)

            except CustomException:
                raise
            except Exception as e:
                log.exception(f"处理上传文件失败: file={file_name} error={e!s}")
                processed_files.append({
                    "name": file_name,
                    "content": f"[文件解析失败: {e!s}]",
                    "mime_type": upload_file.content_type or "application/octet-stream",
                })

        return processed_files

    def _validate_upload_file(self, file: UploadFile) -> None:
        """
        验证上传文件

        Args:
            file: 上传的文件

        Raises:
            CustomException: 验证失败时抛出
        """
        file_name = (file.filename or "").strip() or "未命名文件"
        from pathlib import Path
        extension = Path(file_name).suffix.lower()
        content_type = (file.content_type or "").split(";", 1)[0].strip().lower()

        allowed_extensions = {
            item.lower()
            for item in settings.AI_CHAT_UPLOAD_ALLOWED_EXTENSIONS
        }
        allowed_content_types = {
            item.lower()
            for item in settings.AI_CHAT_UPLOAD_ALLOWED_CONTENT_TYPES
        }

        if (
            extension not in allowed_extensions
            and content_type not in allowed_content_types
        ):
            allowed_ext_text = "、".join(sorted(allowed_extensions))
            raise CustomException(
                msg=f"文件 {file_name} 类型不支持，仅支持：{allowed_ext_text}",
                status_code=422,
            )

    def _process_file_content(
        self,
        message_file: MessageFile,
        file_name: str,
        current_total_chars: int,
    ) -> dict[str, Any] | None:
        """
        处理文件内容，应用长度限制

        Args:
            message_file: 解析后的文件信息
            file_name: 文件名
            current_total_chars: 当前总字符数

        Returns:
            dict | None: 处理后的文件信息
        """
        remaining_chars = _MAX_TOTAL_FILE_CONTEXT_CHARS - current_total_chars

        if remaining_chars <= 0:
            return {
                "name": file_name,
                "content": "[文件内容过长，已超出本轮可注入上下文上限，未继续附加]",
                "mime_type": message_file.mime_type,
            }

        content = message_file.content or "[文件可读取，但未提取到可用文本内容]"

        # 应用单文件长度限制
        max_chars = min(_MAX_FILE_CONTENT_CHARS, remaining_chars)
        if len(content) > max_chars:
            content = f"{content[:max_chars]}\n\n[内容过长，已截断]"

        return {
            "name": file_name,
            "content": content,
            "mime_type": message_file.mime_type,
            "token": message_file.token,
            "thumbnail": message_file.thumbnail,
            "metadata": message_file.metadata,
        }

    def build_file_context(self, processed_files: list[dict[str, Any]]) -> str:
        """
        构建文件上下文内容

        Args:
            processed_files: 处理后的文件信息列表

        Returns:
            str: 文件上下文内容
        """
        if not processed_files:
            return ""

        context_parts = [_FILE_CONTEXT_INTRO, ""]

        for i, file_info in enumerate(processed_files, 1):
            file_name = file_info.get("name", f"文件{i}")
            content = file_info.get("content", "")

            context_parts.append(f"### 文件 {i}: {file_name}")
            context_parts.append(content)
            context_parts.append("")

        return "\n".join(context_parts)

    def merge_files_with_message(
        self,
        user_message: dict[str, Any],
        processed_files: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        将文件信息与用户消息合并

        Args:
            user_message: 用户消息
            processed_files: 处理后的文件信息列表

        Returns:
            dict: 合并后的消息
        """
        if not processed_files:
            return user_message

        # 构建文件上下文
        file_context = self.build_file_context(processed_files)

        # 获取原始消息文本
        original_text = user_message.get("text", "")

        # 合并内容
        merged_content = f"{original_text}\n\n{file_context}".strip()

        # 构建包含文件信息的消息
        result = dict(user_message)
        result["text"] = merged_content
        result["files"] = processed_files

        return result

    def format_files_for_storage(
        self,
        processed_files: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        格式化文件信息用于存储

        Args:
            processed_files: 处理后的文件信息列表

        Returns:
            list[dict]: 格式化后的文件信息列表
        """
        if not processed_files:
            return []

        formatted_files = []
        for file_info in processed_files:
            formatted_file = {
                "name": file_info.get("name", ""),
                "content": file_info.get("content", ""),
                "mimeType": file_info.get("mime_type", ""),
                "token": file_info.get("token", 0),
            }

            # 可选字段
            if file_info.get("thumbnail"):
                formatted_file["thumbnail"] = file_info["thumbnail"]

            if file_info.get("metadata"):
                formatted_file["metadata"] = file_info["metadata"]

            formatted_files.append(formatted_file)

        return formatted_files


# 全局文件处理器实例
ai_chat_file_processor = AiChatFileProcessor()
