from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission, get_current_user
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import (
    ExUserPreferenceCreateSchema,
    ExUserPreferenceQueryParam,
    ExUserPreferenceSetMySchema,
    ExUserPreferenceUpdateSchema,
)
from .service import ExUserPreferenceService

ExUserPreferenceRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/ex_user_preference",
    tags=["用户偏好模块"],
)


@ExUserPreferenceRouter.get("/detail/{id}", summary="获取用户偏好详情", description="获取用户偏好详情")
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ex:ex_user_preference:detail"]))],
) -> JSONResponse:
    result_dict = await ExUserPreferenceService.detail_service(auth=auth, id=id)
    log.info(f"获取用户偏好详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取用户偏好详情成功")


@ExUserPreferenceRouter.get("/list", summary="查询用户偏好列表", description="查询用户偏好列表")
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[ExUserPreferenceQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ex:ex_user_preference:query"]))],
) -> JSONResponse:
    result_dict = await ExUserPreferenceService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    log.info("查询用户偏好列表成功")
    return SuccessResponse(data=result_dict, msg="查询用户偏好列表成功")


@ExUserPreferenceRouter.post("/create", summary="创建用户偏好", description="创建用户偏好")
async def create_obj_controller(
    data: ExUserPreferenceCreateSchema,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ex:ex_user_preference:create"]))],
) -> JSONResponse:
    result_dict = await ExUserPreferenceService.create_service(auth=auth, data=data)
    log.info(f"创建用户偏好成功: {result_dict.get('id')}")
    return SuccessResponse(data=result_dict, msg="创建用户偏好成功")


@ExUserPreferenceRouter.put("/update/{id}", summary="修改用户偏好", description="修改用户偏好")
async def update_obj_controller(
    data: ExUserPreferenceUpdateSchema,
    id: Annotated[int, Path(description="ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ex:ex_user_preference:update"]))],
) -> JSONResponse:
    result_dict = await ExUserPreferenceService.update_service(auth=auth, id=id, data=data)
    log.info(f"修改用户偏好成功: {id}")
    return SuccessResponse(data=result_dict, msg="修改用户偏好成功")


@ExUserPreferenceRouter.delete("/delete", summary="删除用户偏好", description="删除用户偏好")
async def delete_obj_controller(
    ids: Annotated[list[int], Body(description="ID列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_ex:ex_user_preference:delete"]))],
) -> JSONResponse:
    await ExUserPreferenceService.delete_service(auth=auth, ids=ids)
    log.info(f"删除用户偏好成功: {ids}")
    return SuccessResponse(msg="删除用户偏好成功")


@ExUserPreferenceRouter.get(
    "/my/key/{pref_key}", summary="获取当前用户偏好", description="获取当前用户偏好"
)
async def get_my_preference_controller(
    pref_key: Annotated[str, Path(description="偏好键")],
    auth: Annotated[AuthSchema, Depends(get_current_user)],
) -> JSONResponse:
    result_dict = await ExUserPreferenceService.get_my_preference_service(auth=auth, pref_key=pref_key)
    log.info(f"获取当前用户偏好成功: {pref_key}")
    return SuccessResponse(data=result_dict, msg="获取当前用户偏好成功")


@ExUserPreferenceRouter.put(
    "/my/key/{pref_key}", summary="设置当前用户偏好", description="设置当前用户偏好"
)
async def set_my_preference_controller(
    pref_key: Annotated[str, Path(description="偏好键")],
    data: ExUserPreferenceSetMySchema,
    auth: Annotated[AuthSchema, Depends(get_current_user)],
) -> JSONResponse:
    result_dict = await ExUserPreferenceService.set_my_preference_service(
        auth=auth, pref_key=pref_key, pref_value=data.pref_value
    )
    log.info(f"设置当前用户偏好成功: {pref_key}")
    return SuccessResponse(data=result_dict, msg="设置当前用户偏好成功")
