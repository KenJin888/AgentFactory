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
from .schema import AiRoleDatasetCreateSchema, AiRoleDatasetUpdateSchema, AiRoleDatasetQueryParam
from .service import AiRoleDatasetService

AiRoleDatasetRouter = APIRouter(prefix='/ai_role_dataset', tags=["AIRoleDataset模块"])


@AiRoleDatasetRouter.get("/detail/{id}", summary="获取AIRoleDataset详情", description="获取AIRoleDataset详情")
async def get_ai_role_dataset_detail_controller(
        id: int = Path(..., description="ID"),
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_dataset:query"]))
) -> JSONResponse:
    """获取AIRoleDataset详情接口"""
    result_dict = await AiRoleDatasetService.detail_ai_role_dataset_service(auth=auth, id=id)
    log.info(f"获取AIRoleDataset详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取AIRoleDataset详情成功")


@AiRoleDatasetRouter.get("/list", summary="查询AIRoleDataset列表", description="查询AIRoleDataset列表")
async def get_ai_role_dataset_list_controller(
        page: PaginationQueryParam = Depends(),
        search: AiRoleDatasetQueryParam = Depends(),
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_dataset:query"]))
) -> JSONResponse:
    """查询AIRoleDataset列表接口（数据库分页）"""
    result_dict = await AiRoleDatasetService.page_ai_role_dataset_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询AIRoleDataset列表成功")
    return SuccessResponse(data=result_dict, msg="查询AIRoleDataset列表成功")


@AiRoleDatasetRouter.post("/create", summary="创建AIRoleDataset", description="创建AIRoleDataset")
async def create_ai_role_dataset_controller(
        data: AiRoleDatasetCreateSchema,
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_dataset:create"]))
) -> JSONResponse:
    """创建AIRoleDataset接口"""
    result_dict = await AiRoleDatasetService.create_ai_role_dataset_service(auth=auth, data=data)
    log.info("创建AIRoleDataset成功")
    return SuccessResponse(data=result_dict, msg="创建AIRoleDataset成功")


@AiRoleDatasetRouter.put("/update/{id}", summary="修改AIRoleDataset", description="修改AIRoleDataset")
async def update_ai_role_dataset_controller(
        data: AiRoleDatasetUpdateSchema,
        id: int = Path(..., description="ID"),
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_dataset:update"]))
) -> JSONResponse:
    """修改AIRoleDataset接口"""
    result_dict = await AiRoleDatasetService.update_ai_role_dataset_service(auth=auth, id=id, data=data)
    log.info("修改AIRoleDataset成功")
    return SuccessResponse(data=result_dict, msg="修改AIRoleDataset成功")


@AiRoleDatasetRouter.delete("/delete", summary="删除AIRoleDataset", description="删除AIRoleDataset")
async def delete_ai_role_dataset_controller(
        ids: list[int] = Body(..., description="ID列表"),
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_dataset:delete"]))
) -> JSONResponse:
    """删除AIRoleDataset接口"""
    await AiRoleDatasetService.delete_ai_role_dataset_service(auth=auth, ids=ids)
    log.info(f"删除AIRoleDataset成功: {ids}")
    return SuccessResponse(msg="删除AIRoleDataset成功")


@AiRoleDatasetRouter.patch("/available/setting", summary="批量修改AIRoleDataset状态",
                           description="批量修改AIRoleDataset状态")
async def batch_set_available_ai_role_dataset_controller(
        data: BatchSetAvailable,
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_dataset:patch"]))
) -> JSONResponse:
    """批量修改AIRoleDataset状态接口"""
    await AiRoleDatasetService.set_available_ai_role_dataset_service(auth=auth, data=data)
    log.info(f"批量修改AIRoleDataset状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改AIRoleDataset状态成功")


@AiRoleDatasetRouter.post('/export', summary="导出AIRoleDataset", description="导出AIRoleDataset")
async def export_ai_role_dataset_list_controller(
        search: AiRoleDatasetQueryParam = Depends(),
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_dataset:export"]))
) -> StreamingResponse:
    """导出AIRoleDataset接口"""
    result_dict_list = await AiRoleDatasetService.list_ai_role_dataset_service(search=search, auth=auth)
    export_result = await AiRoleDatasetService.batch_export_ai_role_dataset_service(obj_list=result_dict_list)
    log.info('导出AIRoleDataset成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=ai_role_dataset.xlsx'
        }
    )


@AiRoleDatasetRouter.post('/import', summary="导入AIRoleDataset", description="导入AIRoleDataset")
async def import_ai_role_dataset_list_controller(
        file: UploadFile,
        auth: AuthSchema = Depends(AuthPermission(["module_ai:ai_role_dataset:import"]))
) -> JSONResponse:
    """导入AIRoleDataset接口"""
    batch_import_result = await AiRoleDatasetService.batch_import_ai_role_dataset_service(file=file, auth=auth,
                                                                                          update_support=True)
    log.info("导入AIRoleDataset成功")
    return SuccessResponse(data=batch_import_result, msg="导入AIRoleDataset成功")


@AiRoleDatasetRouter.post('/download/template', summary="获取AIRoleDataset导入模板",
                          description="获取AIRoleDataset导入模板",
                          dependencies=[Depends(AuthPermission(["module_ai:ai_role_dataset:download"]))])
async def export_ai_role_dataset_template_controller() -> StreamingResponse:
    """获取AIRoleDataset导入模板接口"""
    import_template_result = await AiRoleDatasetService.import_template_download_ai_role_dataset_service()
    log.info('获取AIRoleDataset导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=ai_role_dataset_template.xlsx'}
    )
