from pydantic import BaseModel
from typing import List, Optional


class FileItem(BaseModel):
    name: str
    path: str
    is_dir: bool
    size: Optional[int] = None
    modified_time: Optional[str] = None


class ListDirectoryResponse(BaseModel):
    current_path: str
    items: List[FileItem]


class CreateDirectoryRequest(BaseModel):
    path: str
    name: str


class DeletePathRequest(BaseModel):
    path: str


class CreateFileRequest(BaseModel):
    path: str
    name: str
    content: Optional[str] = ""


class ReadFileRequest(BaseModel):
    path: str


class ReadFileResponse(BaseModel):
    path: str
    content: str


class UpdateFileRequest(BaseModel):
    path: str
    content: str
