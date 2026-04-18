from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import SuccessResponse
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import (
    AllPermissionSummarySchema,
    PluginPermissionSummarySchema,
)
from .service import ExServicesService

ExServicesRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/ex_services",
    tags=["扩展服务模块"],
)


@ExServicesRouter.get(
    "/plugin/permissions",
    summary="获取插件模块权限字",
    description="获取 plugin 目录下所有模块的权限字",
    response_model=PluginPermissionSummarySchema,
)
async def get_plugin_permissions_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission())],
) -> JSONResponse:
    result_dict = ExServicesService.get_plugin_permissions_service().model_dump()
    log.info(f"获取插件模块权限字成功: {auth.user.id if auth.user else 0}")
    return SuccessResponse(data=result_dict, msg="获取插件模块权限字成功")


@ExServicesRouter.get(
    "/all/permissions",
    summary="获取全部权限字",
    description="获取 plugin 与 /api/v1 下所有模块的权限字",
    response_model=AllPermissionSummarySchema,
)
async def get_all_permissions_controller(
    auth: Annotated[AuthSchema, Depends(AuthPermission())],
) -> JSONResponse:
    result_dict = ExServicesService.get_all_permissions_service().model_dump()
    log.info(f"获取全部权限字成功: {auth.user.id if auth.user else 0}")
    return SuccessResponse(data=result_dict, msg="获取全部权限字成功")
