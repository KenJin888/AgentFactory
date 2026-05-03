from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Body
from fastapi.responses import JSONResponse
from redis import Redis

from app.common.response import SuccessResponse
from app.config.path_conf import AI_SKILLS_DIR
from app.core.dependencies import AuthPermission, redis_getter
from app.core.logger import log
from app.core.redis_crud import RedisCURD
from app.core.router_class import OperationLogRoute
from .schema import UpdateSkillRequest
from .service import AISkillsService, get_skills
from ..ai_knowledge_base.schema import ReadFileRequest
from ..ai_knowledge_base.service import FilesService

AISkillsRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/ai_skills",
    tags=["AI技能管理"]
)


@AISkillsRouter.post(
    "/create/{name}",
    summary="创建技能",
    description="创建新技能，支持三种方式：上传文件夹、上传zip压缩包、通过url下载zip",
    dependencies=[Depends(AuthPermission(["module_ai:ai_skills:create"]))],
)
async def create_skill_controller(
        name: Annotated[str, "技能名称"],
        file: Annotated[UploadFile, File(description="上传的文件")] = None,
        url: Annotated[str, Body(description="技能zip包的下载地址")] = None
) -> JSONResponse:
    result = await AISkillsService.create_skill(name, file, url)
    log.info(f"创建技能成功: {name}")
    return SuccessResponse(data=result, msg="创建技能成功")


@AISkillsRouter.delete(
    "/delete/{name}",
    summary="删除技能",
    description="删除指定的技能",
    dependencies=[Depends(AuthPermission(["module_ai:ai_skills:delete"]))],
)
async def delete_skill_controller(
        name: Annotated[str, "技能名称"]
) -> JSONResponse:
    result = AISkillsService.delete_skill(name)
    log.info(f"删除技能成功: {name}")
    return SuccessResponse(data=result, msg="删除技能成功")


@AISkillsRouter.get(
    "/detail/{name}",
    summary="获取技能详情",
    description="获取技能的SKILL.md文件内容",
    dependencies=[Depends(AuthPermission(["module_ai:ai_skills:query"]))],
)
async def get_skill_detail_controller(
        name: Annotated[str, "技能名称"]
) -> JSONResponse:
    result = AISkillsService.get_skill_detail(name)
    log.info(f"获取技能详情成功: {name}")
    return SuccessResponse(data=result, msg="获取技能详情成功")


@AISkillsRouter.put(
    "/update/{name}",
    summary="更新技能",
    description="更新技能的SKILL.md文件内容",
    dependencies=[Depends(AuthPermission(["module_ai:ai_skills:update"]))],
)
async def update_skill_controller(
        name: Annotated[str, "技能名称"],
        req: UpdateSkillRequest,
        redis: Redis = Depends(redis_getter),
) -> JSONResponse:
    result = AISkillsService.update_skill(name, req.content)
    log.info(f"更新技能成功: {name}")
    # 更新技能后强制刷新技能列表
    cache_key = "ai_skills_list"
    redis_crud = RedisCURD(redis)
    ai_skills_list = AISkillsService.list_skills()
    await redis_crud.set(cache_key, ai_skills_list, expire=600)
    return SuccessResponse(data=result, msg="更新技能成功")


@AISkillsRouter.get(
    "/list",
    summary="列出技能列表",
    description="列出所有技能",
    dependencies=[Depends(AuthPermission())],
)
async def list_skills_controller(
        force_refresh: bool = False,
        redis: Redis = Depends(redis_getter),
) -> JSONResponse:
    result = await get_skills(force_refresh, redis)
    return SuccessResponse(data=result, msg="列出技能列表成功")


@AISkillsRouter.get(
    "/file/list",
    summary="列出目录内容",
    description="列出指定目录的内容",
    dependencies=[Depends(AuthPermission(["module_ai:ai_skills:query"]))],
)
async def list_directory_controller(
        path: Annotated[str, "目录路径，空表示根目录"] = ""
) -> JSONResponse:
    skills_file = FilesService(AI_SKILLS_DIR)
    result = skills_file.list_directory(path)
    log.info(f"列出目录内容成功: {path}")
    return SuccessResponse(data=result, msg="列出目录内容成功")


@AISkillsRouter.post(
    "/file/read",
    summary="读取文件内容",
    description="读取文件内容，仅支持txt、md、json格式",
    dependencies=[Depends(AuthPermission(["module_ai:ai_skills:query"]))],
)
async def read_file_controller(
        req: ReadFileRequest
) -> JSONResponse:
    skills_file = FilesService(AI_SKILLS_DIR)
    result = skills_file.read_file(req.path, url_state=True)
    log.info(f"读取文件成功: {req.path}")
    return SuccessResponse(data=result, msg="读取文件成功")
