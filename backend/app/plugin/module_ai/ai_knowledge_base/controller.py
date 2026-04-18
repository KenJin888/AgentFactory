from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Body
from fastapi.responses import JSONResponse, FileResponse

from app.common.response import SuccessResponse
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .service import FilesService
from .schema import (
    CreateDirectoryRequest,
    DeletePathRequest,
    CreateFileRequest,
    ReadFileRequest,
    UpdateFileRequest
)

AIFilesRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/knowledge_base",
    tags=["AI知识库文件管理"]
)


@AIFilesRouter.get(
    "/list",
    summary="列出目录内容",
    description="列出指定目录的内容",
    dependencies=[Depends(AuthPermission(["module_ai:knowledge_base:query"]))],
)
async def list_directory_controller(
    path: Annotated[str, "目录路径，空表示根目录"] = ""
) -> JSONResponse:
    ai_file = FilesService()
    result = ai_file.list_directory(path)
    log.info(f"列出目录内容成功: {path}")
    return SuccessResponse(data=result, msg="列出目录内容成功")


@AIFilesRouter.post(
    "/directory/create",
    summary="创建目录",
    description="创建新目录",
    dependencies=[Depends(AuthPermission(["module_ai:knowledge_base:create"]))],
)
async def create_directory_controller(
    req: CreateDirectoryRequest
) -> JSONResponse:
    ai_file = FilesService()
    result = ai_file.create_directory(req.path, req.name)
    log.info(f"创建目录成功: {req.path}/{req.name}")
    return SuccessResponse(data=result, msg="创建目录成功")


@AIFilesRouter.delete(
    "/delete",
    summary="删除文件或目录",
    description="删除指定的文件或目录",
    dependencies=[Depends(AuthPermission(["module_ai:knowledge_base:delete"]))],
)
async def delete_path_controller(
    req: DeletePathRequest
) -> JSONResponse:
    ai_file = FilesService()
    result = ai_file.delete_path(req.path)
    log.info(f"删除成功: {req.path}")
    return SuccessResponse(data=result, msg="删除成功")


@AIFilesRouter.post(
    "/file/create",
    summary="创建文件",
    description="创建新文件",
    dependencies=[Depends(AuthPermission(["module_ai:knowledge_base:create"]))],
)
async def create_file_controller(
    req: CreateFileRequest
) -> JSONResponse:
    ai_file = FilesService()
    result = ai_file.create_file(req.path, req.name, req.content)
    log.info(f"创建文件成功: {req.path}/{req.name}")
    return SuccessResponse(data=result, msg="创建文件成功")


@AIFilesRouter.post(
    "/file/read",
    summary="读取文件内容",
    description="读取文件内容，仅支持txt、md、json格式",
    dependencies=[Depends(AuthPermission(["module_ai:knowledge_base:query"]))],
)
async def read_file_controller(
    req: ReadFileRequest
) -> JSONResponse:
    ai_file = FilesService()
    result = ai_file.read_file(req.path)
    log.info(f"读取文件成功: {req.path}")
    return SuccessResponse(data=result, msg="读取文件成功")


@AIFilesRouter.put(
    "/file/update",
    summary="更新文件内容",
    description="更新文件内容，仅支持txt、md、json格式",
    dependencies=[Depends(AuthPermission(["module_ai:knowledge_base:update"]))],
)
async def update_file_controller(
    req: UpdateFileRequest
) -> JSONResponse:
    ai_file = FilesService()
    result = ai_file.update_file(req.path, req.content)
    log.info(f"更新文件成功: {req.path}")
    return SuccessResponse(data=result, msg="更新文件成功")


@AIFilesRouter.post(
    "/file/upload",
    summary="上传文件",
    description="上传文件到指定目录",
    dependencies=[Depends(AuthPermission(["module_ai:knowledge_base:create"]))],
)
async def upload_file_controller(
    path: Annotated[str, Body(..., description="目标目录路径")],
    file: Annotated[UploadFile, File(..., description="上传的文件")]
) -> JSONResponse:
    ai_file = FilesService()
    result = await ai_file.upload_file(path, file)
    log.info(f"上传文件成功: {path}/{file.filename}")
    return SuccessResponse(data=result, msg="上传文件成功")


@AIFilesRouter.get(
    "/file/download",
    summary="下载文件",
    description="下载指定文件",
    dependencies=[Depends(AuthPermission(["module_ai:knowledge_base:query"]))],
)
async def download_file_controller(
    path: Annotated[str, "文件路径"]
) -> FileResponse:
    ai_file = FilesService()
    file_path, filename = ai_file.download_file(path)
    log.info(f"下载文件成功: {path}")
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )
