# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, UploadFile, Body, Path
from fastapi.responses import StreamingResponse, JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import SuccessResponse, StreamResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import BatchSetAvailable
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.utils.common_util import bytes2file_response
from .schema import AiMcpCreateSchema, AiMcpUpdateSchema, AiMcpQueryParam
from .service import AiMcpService

AiMcpRouter = APIRouter(prefix='/ai_mcp', tags=["ai_mcp模块"])


@AiMcpRouter.get("/detail/{id}", summary="获取ai_mcp详情", description="获取ai_mcp详情")
async def get_ai_mcp_detail_controller(
        id: int = Path(..., description="ID"),
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_mcp:query"], check_data_scope=False))
) -> JSONResponse:
    """获取ai_mcp详情接口"""
    result_dict = await AiMcpService.detail_ai_mcp_service(auth=auth, id=id)
    log.info(f"获取ai_mcp详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取ai_mcp详情成功")


@AiMcpRouter.get("/list", summary="查询ai_mcp列表", description="查询ai_mcp列表")
async def get_ai_mcp_list_controller(
        page: PaginationQueryParam = Depends(),
        search: AiMcpQueryParam = Depends(),
        auth: AuthSchema = Depends(AuthPermission(check_data_scope=False))
) -> JSONResponse:
    """查询ai_mcp列表接口（数据库分页）"""
    result_dict = await AiMcpService.page_ai_mcp_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询ai_mcp列表成功")
    return SuccessResponse(data=result_dict, msg="查询ai_mcp列表成功")


@AiMcpRouter.post("/create", summary="创建ai_mcp", description="创建ai_mcp")
async def create_ai_mcp_controller(
        data: AiMcpCreateSchema,
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_mcp:create"], check_data_scope=False))
) -> JSONResponse:
    """创建ai_mcp接口"""
    result_dict = await AiMcpService.create_ai_mcp_service(auth=auth, data=data)
    log.info("创建ai_mcp成功")
    return SuccessResponse(data=result_dict, msg="创建ai_mcp成功")


@AiMcpRouter.put("/update/{id}", summary="修改ai_mcp", description="修改ai_mcp")
async def update_ai_mcp_controller(
        data: AiMcpUpdateSchema,
        id: int = Path(..., description="ID"),
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_mcp:update"], check_data_scope=False))
) -> JSONResponse:
    """修改ai_mcp接口"""
    result_dict = await AiMcpService.update_ai_mcp_service(auth=auth, id=id, data=data)
    log.info("修改ai_mcp成功")
    return SuccessResponse(data=result_dict, msg="修改ai_mcp成功")


@AiMcpRouter.delete("/delete", summary="删除ai_mcp", description="删除ai_mcp")
async def delete_ai_mcp_controller(
        ids: list[int] = Body(..., description="ID列表"),
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_mcp:delete"], check_data_scope=False))
) -> JSONResponse:
    """删除ai_mcp接口"""
    await AiMcpService.delete_ai_mcp_service(auth=auth, ids=ids)
    log.info(f"删除ai_mcp成功: {ids}")
    return SuccessResponse(msg="删除ai_mcp成功")


@AiMcpRouter.patch("/available/setting", summary="批量修改ai_mcp状态", description="批量修改ai_mcp状态")
async def batch_set_available_ai_mcp_controller(
        data: BatchSetAvailable,
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_mcp:query"], check_data_scope=False))
) -> JSONResponse:
    """批量修改ai_mcp状态接口"""
    await AiMcpService.set_available_ai_mcp_service(auth=auth, data=data)
    log.info(f"批量修改ai_mcp状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改ai_mcp状态成功")


@AiMcpRouter.post('/export', summary="导出ai_mcp", description="导出ai_mcp")
async def export_ai_mcp_list_controller(
        search: AiMcpQueryParam = Depends(),
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_mcp:query"], check_data_scope=False))
) -> StreamingResponse:
    """导出ai_mcp接口"""
    result_dict_list = await AiMcpService.list_ai_mcp_service(search=search, auth=auth)
    export_result = await AiMcpService.batch_export_ai_mcp_service(obj_list=result_dict_list)
    log.info('导出ai_mcp成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=ai_mcp.xlsx'
        }
    )


@AiMcpRouter.post('/import', summary="导入ai_mcp", description="导入ai_mcp")
async def import_ai_mcp_list_controller(
        file: UploadFile,
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_mcp:query"], check_data_scope=False))
) -> JSONResponse:
    """导入ai_mcp接口"""
    batch_import_result = await AiMcpService.batch_import_ai_mcp_service(file=file, auth=auth, update_support=True)
    log.info("导入ai_mcp成功")
    return SuccessResponse(data=batch_import_result, msg="导入ai_mcp成功")


@AiMcpRouter.post('/download/template', summary="获取ai_mcp导入模板", description="获取ai_mcp导入模板",
                  dependencies=[Depends(AuthPermission(["module_ai:ai_mcp:query"], check_data_scope=False))])
async def export_ai_mcp_template_controller() -> StreamingResponse:
    """获取ai_mcp导入模板接口"""
    import_template_result = await AiMcpService.import_template_download_ai_mcp_service()
    log.info('获取ai_mcp导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=ai_mcp_template.xlsx'}
    )
