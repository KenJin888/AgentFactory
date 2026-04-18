# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Body, Path
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import BatchSetAvailable
from app.core.dependencies import AuthPermission
from app.core.logger import log
from .schema import AiChatMsgCreateSchema, AiChatMsgUpdateSchema, AiChatMsgQueryParam
from .service import AiChatMsgService

AiChatMsgRouter = APIRouter(prefix='/ai_chat_msg', tags=["ai_chat_msg模块"])


@AiChatMsgRouter.get("/detail/{id}", summary="获取ai_chat_msg详情", description="获取ai_chat_msg详情")
async def get_ai_chat_msg_detail_controller(
        id: int = Path(..., description="ID"),
        auth: AuthSchema = Depends(AuthPermission())
) -> JSONResponse:
    """获取ai_chat_msg详情接口"""
    result_dict = await AiChatMsgService.detail_ai_chat_msg_service(auth=auth, id=id)
    log.info(f"获取ai_chat_msg详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取ai_chat_msg详情成功")


@AiChatMsgRouter.get("/list", summary="查询ai_chat_msg列表", description="查询ai_chat_msg列表")
async def get_ai_chat_msg_list_controller(
        page: PaginationQueryParam = Depends(),
        search: AiChatMsgQueryParam = Depends(),
        auth: AuthSchema = Depends(AuthPermission())
) -> JSONResponse:
    """查询ai_chat_msg列表接口（数据库分页）"""
    result_dict = await AiChatMsgService.page_ai_chat_msg_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询ai_chat_msg列表成功")
    return SuccessResponse(data=result_dict, msg="查询ai_chat_msg列表成功")


@AiChatMsgRouter.post("/create", summary="创建ai_chat_msg", description="创建ai_chat_msg")
async def create_ai_chat_msg_controller(
        data: AiChatMsgCreateSchema,
        auth: AuthSchema = Depends(AuthPermission())
) -> JSONResponse:
    """创建ai_chat_msg接口"""
    result_dict = await AiChatMsgService.create_ai_chat_msg_service(auth=auth, data=data)
    log.info("创建ai_chat_msg成功")
    return SuccessResponse(data=result_dict, msg="创建ai_chat_msg成功")


@AiChatMsgRouter.put("/update/{id}", summary="修改ai_chat_msg", description="修改ai_chat_msg")
async def update_ai_chat_msg_controller(
        data: AiChatMsgUpdateSchema,
        id: int = Path(..., description="ID"),
        auth: AuthSchema = Depends(AuthPermission())
) -> JSONResponse:
    """修改ai_chat_msg接口"""
    result_dict = await AiChatMsgService.update_ai_chat_msg_service(auth=auth, id=id, data=data)
    log.info("修改ai_chat_msg成功")
    return SuccessResponse(data=result_dict, msg="修改ai_chat_msg成功")


@AiChatMsgRouter.delete("/delete", summary="删除ai_chat_msg", description="删除ai_chat_msg")
async def delete_ai_chat_msg_controller(
        ids: list[int] = Body(..., description="ID列表"),
        auth: AuthSchema = Depends(AuthPermission())
) -> JSONResponse:
    """删除ai_chat_msg接口"""
    await AiChatMsgService.delete_ai_chat_msg_service(auth=auth, ids=ids)
    log.info(f"删除ai_chat_msg成功: {ids}")
    return SuccessResponse(msg="删除ai_chat_msg成功")


@AiChatMsgRouter.patch("/available/setting", summary="批量修改ai_chat_msg状态", description="批量修改ai_chat_msg状态")
async def batch_set_available_ai_chat_msg_controller(
        data: BatchSetAvailable,
        auth: AuthSchema = Depends(AuthPermission())
) -> JSONResponse:
    """批量修改ai_chat_msg状态接口"""
    await AiChatMsgService.set_available_ai_chat_msg_service(auth=auth, data=data)
    log.info(f"批量修改ai_chat_msg状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改ai_chat_msg状态成功")
