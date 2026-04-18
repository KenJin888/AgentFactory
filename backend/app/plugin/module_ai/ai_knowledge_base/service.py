import os
from pathlib import Path
from datetime import datetime
from typing import List

from app.config.path_conf import AI_FILE_DIR
from app.core.exceptions import CustomException
from .schema import FileItem


class FilesService:
    """
    文件管理服务层
    """

    def __init__(self, file_dir=AI_FILE_DIR):
        self.FILE_DIR = file_dir

    def _ensure_ai_file_dir(self):
        """确保AI目录存在"""
        if not self.FILE_DIR.exists():
            self.FILE_DIR.mkdir(parents=True, exist_ok=True)

    def _validate_path(self, path: str) -> Path:
        """
        验证路径，确保路径在AI目录内
        
        参数:
            path: 需要验证的路径
            
        返回:
            Path对象
            
        异常:
            CustomException: 路径非法时抛出
        """
        self._ensure_ai_file_dir()

        target_path = self.FILE_DIR.joinpath(path).resolve()
        ai_file_dir_absolute = self.FILE_DIR.resolve()

        if ai_file_dir_absolute not in target_path.parents and target_path != ai_file_dir_absolute:
            raise CustomException(msg="非法路径，只能操作AI目录内的文件")

        return target_path

    def list_directory(self, path: str = "") -> dict:
        """
        列出指定目录的内容
        
        参数:
            path: 相对路径，默认为空（根目录）
            
        返回:
            包含当前路径和文件列表的字典
        """
        target_path = self._validate_path(path)

        if not target_path.exists() or not target_path.is_dir():
            raise CustomException(msg="目录不存在")

        items: List[FileItem] = []

        for item in target_path.iterdir():
            rel_path = str(item.relative_to(self.FILE_DIR)).replace("\\", "/")
            stat = item.stat()
            modified_time = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

            items.append(FileItem(
                name=item.name,
                path=rel_path,
                is_dir=item.is_dir(),
                size=stat.st_size if item.is_file() else None,
                modified_time=modified_time
            ))

        items.sort(key=lambda x: (not x.is_dir, x.name.lower()))

        return {
            "current_path": path,
            "items": items
        }

    def create_directory(self, path: str, name: str) -> dict:
        """
        创建目录
        
        参数:
            path: 父目录路径
            name: 新目录名称
            
        返回:
            操作结果
        """
        parent_path = self._validate_path(path)

        if not parent_path.exists() or not parent_path.is_dir():
            raise CustomException(msg="父目录不存在")

        new_dir_path = parent_path.joinpath(name)

        if new_dir_path.exists():
            raise CustomException(msg="目录已存在")

        new_dir_path.mkdir(parents=True, exist_ok=True)

        return {"message": "目录创建成功"}

    def delete_path(self, path: str) -> dict:
        """
        删除文件或目录
        
        参数:
            path: 要删除的路径
            
        返回:
            操作结果
        """
        target_path = self._validate_path(path)

        if not target_path.exists():
            raise CustomException(msg="路径不存在")

        if target_path == self.FILE_DIR.resolve():
            raise CustomException(msg="不能删除根目录")

        if target_path.is_dir():
            for item in target_path.rglob("*"):
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    item.rmdir()
            target_path.rmdir()
        else:
            target_path.unlink()

        return {"message": "删除成功"}

    def create_file(self, path: str, name: str, content: str = "") -> dict:
        """
        创建文件
        
        参数:
            path: 父目录路径
            name: 新文件名称
            content: 文件内容
            
        返回:
            操作结果
        """
        parent_path = self._validate_path(path)

        if not parent_path.exists() or not parent_path.is_dir():
            raise CustomException(msg="父目录不存在")

        new_file_path = parent_path.joinpath(name)

        if new_file_path.exists():
            raise CustomException(msg="文件已存在")

        new_file_path.write_text(content, encoding="utf-8")

        return {"message": "文件创建成功"}

    def read_file(self, path: str, url_state=False) -> dict:
        """
        读取文件内容
        
        参数:
            path: 文件路径
            
        返回:
            文件路径和内容
        """
        target_path = self._validate_path(path)

        if not target_path.exists() or not target_path.is_file():
            raise CustomException(msg="文件不存在")

        if url_state:
            url = str(target_path).replace("\\", "/").split('backend')[1]
            return {
                "path": path,
                "url": url
            }
        else:
            ext = target_path.suffix.lower()
            editable_exts = [".txt", ".md", ".json"]

            if ext not in editable_exts:
                raise CustomException(msg="只能编辑txt、md、json格式的文件")

            content = target_path.read_text(encoding="utf-8")

            return {
                "path": path,
                "content": content
            }

    def update_file(self, path: str, content: str) -> dict:
        """
        更新文件内容
        
        参数:
            path: 文件路径
            content: 新内容
            
        返回:
            操作结果
        """
        target_path = self._validate_path(path)

        if not target_path.exists() or not target_path.is_file():
            raise CustomException(msg="文件不存在")

        ext = target_path.suffix.lower()
        editable_exts = [".txt", ".md", ".json"]

        if ext not in editable_exts:
            raise CustomException(msg="只能编辑txt、md、json格式的文件")

        target_path.write_text(content, encoding="utf-8")

        return {"message": "文件更新成功"}

    async def upload_file(self, path: str, file) -> dict:
        """
        上传文件
        
        参数:
            path: 目标目录路径
            file: 上传的文件对象
            
        返回:
            操作结果
        """
        parent_path = self._validate_path(path)

        if not parent_path.exists() or not parent_path.is_dir():
            raise CustomException(msg="父目录不存在")

        file_path = parent_path.joinpath(file.filename)

        if file_path.exists():
            raise CustomException(msg="文件已存在")

        content = await file.read()
        file_path.write_bytes(content)

        return {"message": "文件上传成功", "filename": file.filename}

    def download_file(self, path: str) -> tuple:
        """
        下载文件
        
        参数:
            path: 文件路径
            
        返回:
            (文件路径, 文件名)
        """
        target_path = self._validate_path(path)

        if not target_path.exists() or not target_path.is_file():
            raise CustomException(msg="文件不存在")

        return str(target_path), target_path.name
