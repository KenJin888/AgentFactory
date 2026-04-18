import asyncio
from collections.abc import Sequence
from io import BytesIO
from pathlib import Path

from fastapi import UploadFile
from markitdown import MarkItDown

from app.core.exceptions import CustomException
from app.core.logger import log

_FILE_CONTEXT_INTRO = (
    "以下是用户上传文件转换后的 Markdown 内容。回答问题时请优先结合这些文件内容，"
    "若用户问题与文件内容冲突，请明确指出并以文件内容为准。"
)
_MAX_FILE_CONTENT_CHARS = 20000
_MAX_TOTAL_FILE_CONTEXT_CHARS = 60000


def _convert_upload_file_to_markdown(file_name: str, content: bytes) -> str:
    stream = BytesIO(content)
    extension = Path(file_name or "").suffix or None
    result = MarkItDown().convert_stream(stream, file_extension=extension)
    return (result.text_content or "").strip()


async def extract_upload_file_markdowns(
        files: Sequence[UploadFile] | None,
        max_file_size_bytes: int | None = None,
) -> list[dict[str, str]]:
    if not files:
        return []

    markdown_files: list[dict[str, str]] = []
    total_chars = 0

    for upload_file in files:
        file_name = upload_file.filename or "未命名文件"
        try:
            content = await upload_file.read()
            if max_file_size_bytes is not None and len(content) > max_file_size_bytes:
                raise CustomException(msg=f"文件 {file_name} 超过大小限制")
            markdown = await asyncio.to_thread(
                _convert_upload_file_to_markdown,
                file_name=file_name,
                content=content,
            )
            if not markdown:
                markdown = "[文件可读取，但未提取到可用文本内容]"
        except CustomException:
            raise
        except Exception as exc:
            log.exception(f"上传文件转 Markdown 失败: file={file_name} error={exc!s}")
            markdown = f"[文件解析失败: {exc!s}]"
        finally:
            await upload_file.close()

        remaining_chars = _MAX_TOTAL_FILE_CONTEXT_CHARS - total_chars
        if remaining_chars <= 0:
            markdown_files.append(
                {
                    "name": file_name,
                    "markdown": "[文件内容过长，已超出本轮可注入上下文上限，未继续附加]",
                }
            )
            break

        max_chars = min(_MAX_FILE_CONTENT_CHARS, remaining_chars)
        if len(markdown) > max_chars:
            markdown = f"{markdown[:max_chars]}\n\n[内容过长，已截断]"

        total_chars += len(markdown)
        markdown_files.append({"name": file_name, "markdown": markdown})

    return markdown_files
