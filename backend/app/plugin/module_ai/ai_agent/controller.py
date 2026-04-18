# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, UploadFile, Body, Path, Query
from fastapi.responses import StreamingResponse, JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import SuccessResponse, StreamResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import BatchSetAvailable
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.utils.common_util import bytes2file_response
from .schema import AiAgentCreateSchema, AiAgentUpdateSchema, AiAgentQueryParam, AiAgentPublishSchema, \
    AiAgentManageSchema
from .service import AiAgentService

AiAgentRouter = APIRouter(prefix='/ai_agent', tags=["ai_agent模块"])


@AiAgentRouter.get("/detail/{id}", summary="获取ai_agent详情", description="获取ai_agent详情")
async def get_ai_agent_detail_controller(
    id: int = Path(..., description="ID"),
        auth: AuthSchema = Depends(AuthPermission(check_data_scope=False))
) -> JSONResponse:
    """获取ai_agent详情接口"""
    result_dict = await AiAgentService.detail_ai_agent_service(auth=auth, id=id)
    log.info(f"获取ai_agent详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取ai_agent详情成功")


@AiAgentRouter.get("/list", summary="查询ai_agent列表", description="查询ai_agent列表")
async def get_ai_agent_list_controller(
    page: PaginationQueryParam = Depends(),
    search: AiAgentQueryParam = Depends(),
        auth: AuthSchema = Depends(AuthPermission(check_data_scope=False))
) -> JSONResponse:
    """查询ai_agent列表接口（数据库分页）"""
    result_dict = await AiAgentService.page_ai_agent_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询ai_agent列表成功")
    return SuccessResponse(data=result_dict, msg="查询ai_agent列表成功")


@AiAgentRouter.get("/my/list", summary="查询我的私有ai_agent列表", description="查询我的私有ai_agent列表")
async def get_my_ai_agent_list_controller(
    page: PaginationQueryParam = Depends(),
    search: AiAgentQueryParam = Depends(),
        auth: AuthSchema = Depends(AuthPermission(check_data_scope=False))
) -> JSONResponse:
    result_dict = await AiAgentService.my_page_ai_agent_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询我的私有ai_agent列表成功")
    return SuccessResponse(data=result_dict, msg="查询我的私有ai_agent列表成功")


@AiAgentRouter.get("/square/list", summary="查询企业广场ai_agent列表", description="查询企业广场ai_agent列表")
async def get_square_ai_agent_list_controller(
    page: PaginationQueryParam = Depends(),
    search: AiAgentQueryParam = Depends(),
        auth: AuthSchema = Depends(AuthPermission(check_data_scope=False))
) -> JSONResponse:
    result_dict = await AiAgentService.square_page_ai_agent_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询企业广场ai_agent列表成功")
    return SuccessResponse(data=result_dict, msg="查询企业广场ai_agent列表成功")


@AiAgentRouter.get("/favorite/list", summary="查询我的收藏ai_agent列表", description="查询我的收藏ai_agent列表")
async def get_favorite_ai_agent_list_controller(
        auth: AuthSchema = Depends(AuthPermission(check_data_scope=False))
) -> JSONResponse:
    result_dict = await AiAgentService.favorite_ai_agent_list_service(auth=auth)
    log.info("查询我的收藏ai_agent列表成功")
    return SuccessResponse(data=result_dict, msg="查询我的收藏ai_agent列表成功")


@AiAgentRouter.get("/knowledge/datasets", summary="查询当前用户可绑定知识库",
                   description="查询当前用户可绑定到智能体的知识库列表")
async def get_available_knowledge_datasets_controller(
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(200, ge=1, le=1000, description="每页数量"),
        auth: AuthSchema = Depends(AuthPermission(check_data_scope=False))
) -> JSONResponse:
    result_dict = await AiAgentService.list_available_knowledge_datasets_service(
        auth=auth,
        page=page,
        page_size=page_size,
    )
    log.info("查询当前用户可绑定知识库成功")
    return SuccessResponse(data=result_dict, msg="查询当前用户可绑定知识库成功")


@AiAgentRouter.post("/create", summary="创建ai_agent", description="创建ai_agent")
async def create_ai_agent_controller(
    data: AiAgentCreateSchema,
        auth: AuthSchema = Depends(AuthPermission(check_data_scope=False))
) -> JSONResponse:
    """创建ai_agent接口"""
    result_dict = await AiAgentService.create_ai_agent_service(auth=auth, data=data)
    log.info("创建ai_agent成功")
    return SuccessResponse(data=result_dict, msg="创建ai_agent成功")


@AiAgentRouter.put("/update/{id}", summary="修改ai_agent", description="修改ai_agent")
async def update_ai_agent_controller(
    data: AiAgentUpdateSchema,
    id: int = Path(..., description="ID"),
        auth: AuthSchema = Depends(AuthPermission(check_data_scope=False))
) -> JSONResponse:
    """修改ai_agent接口"""
    result_dict = await AiAgentService.update_ai_agent_service(auth=auth, id=id, data=data)
    log.info("修改ai_agent成功")
    return SuccessResponse(data=result_dict, msg="修改ai_agent成功")


@AiAgentRouter.post("/{id}/publish", summary="发布ai_agent", description="发布ai_agent")
async def publish_ai_agent_controller(
        data: AiAgentPublishSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission())
) -> JSONResponse:
    result_dict = await AiAgentService.publish_ai_agent_service(auth=auth, id=id, data=data)
    log.info(f"发布ai_agent成功: {id}")
    return SuccessResponse(data=result_dict, msg="发布ai_agent成功")


@AiAgentRouter.put("/{id}/manage", summary="管理广场ai_agent", description="管理广场ai_agent")
async def manage_ai_agent_controller(
        data: AiAgentManageSchema,
        id: int = Path(..., description="ID"),
        auth: AuthSchema = Depends(AuthPermission())
) -> JSONResponse:
    result_dict = await AiAgentService.manage_ai_agent_service(auth=auth, id=id, data=data)
    log.info(f"管理ai_agent成功: {id}")
    return SuccessResponse(data=result_dict, msg="管理ai_agent成功")


@AiAgentRouter.post("/{id}/offline", summary="下线ai_agent", description="下线ai_agent")
async def offline_ai_agent_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission())
) -> JSONResponse:
    result_dict = await AiAgentService.offline_ai_agent_service(auth=auth, id=id)
    log.info(f"下线ai_agent成功: {id}")
    return SuccessResponse(data=result_dict, msg="下线ai_agent成功")


@AiAgentRouter.post("/{id}/clone", summary="克隆 ai_agent", description="克隆 ai_agent")
@AiAgentRouter.post("/{id}/fork", summary="fork ai_agent", description="fork ai_agent")
async def clone_ai_agent_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(check_data_scope=False))
) -> JSONResponse:
    result_dict = await AiAgentService.clone_ai_agent_service(auth=auth, id=id)
    log.info(f"clone ai_agent成功: {id}")
    return SuccessResponse(data=result_dict, msg="clone ai_agent成功")


@AiAgentRouter.delete("/{id}/delete", summary="删除私有ai_agent", description="删除私有ai_agent")
async def delete_private_ai_agent_controller(
    id: int = Path(..., description="ID"),
        auth: AuthSchema = Depends(AuthPermission(check_data_scope=False))
) -> JSONResponse:
    await AiAgentService.delete_private_ai_agent_service(auth=auth, id=id)
    log.info(f"删除私有ai_agent成功: {id}")
    return SuccessResponse(msg="删除私有ai_agent成功")

# For admin
@AiAgentRouter.delete("/delete", summary="彻底删除ai_agent", description="删除ai_agent")
async def delete_ai_agent_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_agent:delete"]))
) -> JSONResponse:
    """删除ai_agent接口"""
    await AiAgentService.delete_ai_agent_service(auth=auth, ids=ids)
    log.info(f"删除ai_agent成功: {ids}")
    return SuccessResponse(msg="删除ai_agent成功")


@AiAgentRouter.patch("/available/setting", summary="批量修改ai_agent状态", description="批量修改ai_agent状态")
async def batch_set_available_ai_agent_controller(
    data: BatchSetAvailable,
        auth: AuthSchema = Depends(AuthPermission(check_data_scope=False))
) -> JSONResponse:
    """批量修改ai_agent状态接口"""
    await AiAgentService.set_available_ai_agent_service(auth=auth, data=data)
    log.info(f"批量修改ai_agent状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改ai_agent状态成功")


@AiAgentRouter.post('/export', summary="导出ai_agent", description="导出ai_agent")
async def export_ai_agent_list_controller(
    search: AiAgentQueryParam = Depends(),
        auth: AuthSchema = Depends(AuthPermission(check_data_scope=False))
) -> StreamingResponse:
    """导出ai_agent接口"""
    result_dict_list = await AiAgentService.list_ai_agent_service(search=search, auth=auth)
    export_result = await AiAgentService.batch_export_ai_agent_service(obj_list=result_dict_list)
    log.info('导出ai_agent成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=ai_agent.xlsx'
        }
    )


@AiAgentRouter.post('/import', summary="导入ai_agent", description="导入ai_agent")
async def import_ai_agent_list_controller(
    file: UploadFile,
        auth: AuthSchema = Depends(AuthPermission(check_data_scope=False))
) -> JSONResponse:
    """导入ai_agent接口"""
    batch_import_result = await AiAgentService.batch_import_ai_agent_service(file=file, auth=auth, update_support=True)
    log.info("导入ai_agent成功")
    return SuccessResponse(data=batch_import_result, msg="导入ai_agent成功")


@AiAgentRouter.post('/download/template', summary="获取ai_agent导入模板", description="获取ai_agent导入模板",
                    dependencies=[Depends(AuthPermission(check_data_scope=False))])
async def export_ai_agent_template_controller() -> StreamingResponse:
    """获取ai_agent导入模板接口"""
    import_template_result = await AiAgentService.import_template_download_ai_agent_service()
    log.info('获取ai_agent导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=ai_agent_template.xlsx'}
    )
