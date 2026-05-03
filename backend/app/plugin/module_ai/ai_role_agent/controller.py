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
from .schema import AiRoleAgentCreateSchema, AiRoleAgentUpdateSchema, AiRoleAgentQueryParam
from .service import AiRoleAgentService

AiRoleAgentRouter = APIRouter(prefix='/ai_role_agent', tags=["AIRoleAgent模块"])


@AiRoleAgentRouter.get("/detail/{id}", summary="获取AIRoleAgent详情", description="获取AIRoleAgent详情")
async def get_ai_role_agent_detail_controller(
        id: int = Path(..., description="ID"),
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_agent:query"]))
) -> JSONResponse:
    """获取AIRoleAgent详情接口"""
    result_dict = await AiRoleAgentService.detail_ai_role_agent_service(auth=auth, id=id)
    log.info(f"获取AIRoleAgent详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取AIRoleAgent详情成功")


@AiRoleAgentRouter.get("/list", summary="查询AIRoleAgent列表", description="查询AIRoleAgent列表")
async def get_ai_role_agent_list_controller(
        page: PaginationQueryParam = Depends(),
        search: AiRoleAgentQueryParam = Depends(),
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_agent:query"]))
) -> JSONResponse:
    """查询AIRoleAgent列表接口（数据库分页）"""
    result_dict = await AiRoleAgentService.page_ai_role_agent_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询AIRoleAgent列表成功")
    return SuccessResponse(data=result_dict, msg="查询AIRoleAgent列表成功")


@AiRoleAgentRouter.post("/create", summary="创建AIRoleAgent", description="创建AIRoleAgent")
async def create_ai_role_agent_controller(
        data: AiRoleAgentCreateSchema,
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_agent:create"]))
) -> JSONResponse:
    """创建AIRoleAgent接口"""
    result_dict = await AiRoleAgentService.create_ai_role_agent_service(auth=auth, data=data)
    log.info("创建AIRoleAgent成功")
    return SuccessResponse(data=result_dict, msg="创建AIRoleAgent成功")


@AiRoleAgentRouter.put("/update/{id}", summary="修改AIRoleAgent", description="修改AIRoleAgent")
async def update_ai_role_agent_controller(
        data: AiRoleAgentUpdateSchema,
        id: int = Path(..., description="ID"),
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_agent:update"]))
) -> JSONResponse:
    """修改AIRoleAgent接口"""
    result_dict = await AiRoleAgentService.update_ai_role_agent_service(auth=auth, id=id, data=data)
    log.info("修改AIRoleAgent成功")
    return SuccessResponse(data=result_dict, msg="修改AIRoleAgent成功")


@AiRoleAgentRouter.delete("/delete", summary="删除AIRoleAgent", description="删除AIRoleAgent")
async def delete_ai_role_agent_controller(
        ids: list[int] = Body(..., description="ID列表"),
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_agent:delete"]))
) -> JSONResponse:
    """删除AIRoleAgent接口"""
    await AiRoleAgentService.delete_ai_role_agent_service(auth=auth, ids=ids)
    log.info(f"删除AIRoleAgent成功: {ids}")
    return SuccessResponse(msg="删除AIRoleAgent成功")


@AiRoleAgentRouter.patch("/available/setting", summary="批量修改AIRoleAgent状态", description="批量修改AIRoleAgent状态")
async def batch_set_available_ai_role_agent_controller(
        data: BatchSetAvailable,
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_agent:patch"]))
) -> JSONResponse:
    """批量修改AIRoleAgent状态接口"""
    await AiRoleAgentService.set_available_ai_role_agent_service(auth=auth, data=data)
    log.info(f"批量修改AIRoleAgent状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改AIRoleAgent状态成功")


@AiRoleAgentRouter.post('/export', summary="导出AIRoleAgent", description="导出AIRoleAgent")
async def export_ai_role_agent_list_controller(
        search: AiRoleAgentQueryParam = Depends(),
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_agent:export"]))
) -> StreamingResponse:
    """导出AIRoleAgent接口"""
    result_dict_list = await AiRoleAgentService.list_ai_role_agent_service(search=search, auth=auth)
    export_result = await AiRoleAgentService.batch_export_ai_role_agent_service(obj_list=result_dict_list)
    log.info('导出AIRoleAgent成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=ai_role_agent.xlsx'
        }
    )


@AiRoleAgentRouter.post('/import', summary="导入AIRoleAgent", description="导入AIRoleAgent")
async def import_ai_role_agent_list_controller(
        file: UploadFile,
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_agent:import"]))
) -> JSONResponse:
    """导入AIRoleAgent接口"""
    batch_import_result = await AiRoleAgentService.batch_import_ai_role_agent_service(file=file, auth=auth,
                                                                                      update_support=True)
    log.info("导入AIRoleAgent成功")
    return SuccessResponse(data=batch_import_result, msg="导入AIRoleAgent成功")


@AiRoleAgentRouter.post('/download/template', summary="获取AIRoleAgent导入模板", description="获取AIRoleAgent导入模板",
                        dependencies=[Depends(AuthPermission(["module_ai:ai_role_agent:download"]))])
async def export_ai_role_agent_template_controller() -> StreamingResponse:
    """获取AIRoleAgent导入模板接口"""
    import_template_result = await AiRoleAgentService.import_template_download_ai_role_agent_service()
    log.info('获取AIRoleAgent导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=ai_role_agent_template.xlsx'}
    )
