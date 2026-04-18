# -*- coding: utf-8 -*-

import io
from fastapi import UploadFile
import pandas as pd

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.core.logger import log
from app.api.v1.module_system.auth.schema import AuthSchema
from .schema import AiMcpCreateSchema, AiMcpUpdateSchema, AiMcpOutSchema, AiMcpQueryParam
from .crud import AiMcpCRUD


class AiMcpService:
    """
    ai_mcp服务层
    """
    
    @classmethod
    async def detail_ai_mcp_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await AiMcpCRUD(auth).get_by_id_ai_mcp_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return AiMcpOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def list_ai_mcp_service(cls, auth: AuthSchema, search: AiMcpQueryParam | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await AiMcpCRUD(auth).list_ai_mcp_crud(search=search_dict, order_by=order_by)
        return [AiMcpOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_ai_mcp_service(cls, auth: AuthSchema, page_no: int, page_size: int, search: AiMcpQueryParam | None = None, order_by: list[dict] | None = None) -> dict:
        """分页查询（数据库分页）"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        result = await AiMcpCRUD(auth).page_ai_mcp_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        return result
    
    @classmethod
    async def create_ai_mcp_service(cls, auth: AuthSchema, data: AiMcpCreateSchema) -> dict:
        """创建"""
        # 检查唯一性约束
        if await AiMcpCRUD(auth).get(name=data.name):
            raise CustomException(msg=f"名称 {data.name} 已存在")
        obj = await AiMcpCRUD(auth).create_ai_mcp_crud(data=data)
        return AiMcpOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_ai_mcp_service(cls, auth: AuthSchema, id: int, data: AiMcpUpdateSchema) -> dict:
        """更新"""
        # 检查数据是否存在
        obj = await AiMcpCRUD(auth).get_by_id_ai_mcp_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        
        # 检查唯一性约束
        if data.name:
            exist = await AiMcpCRUD(auth).get(name=data.name)
            if exist and exist.id != id:
                raise CustomException(msg=f"名称 {data.name} 已存在")
            
        obj = await AiMcpCRUD(auth).update_ai_mcp_crud(id=id, data=data)
        return AiMcpOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_ai_mcp_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await AiMcpCRUD(auth).get_by_id_ai_mcp_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
        await AiMcpCRUD(auth).delete_ai_mcp_crud(ids=ids)
    
    @classmethod
    async def set_available_ai_mcp_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await AiMcpCRUD(auth).set_available_ai_mcp_crud(ids=data.ids, status=data.status)
    
    @classmethod
    async def batch_export_ai_mcp_service(cls, obj_list: list[dict]) -> bytes:
        """批量导出"""
        mapping_dict = {
            'id': '主键ID',
            'uuid': 'UUID全局唯一标识',
            'status': '是否启用(0:启用 1:禁用)',
            'description': '备注/描述',
            'created_time': '创建时间',
            'updated_time': '更新时间',
            'created_id': '创建人ID',
            'updated_id': '更新人ID',
            'name': 'mcp名称',
            'type': '类型',
            'abstract': '摘要',
            'category': '分类',
            'config': 'mcp配置',
            'tools': '工具配置',
            'cover': '封面图片URL',
        }

        data = obj_list.copy()
        for item in data:
            # 状态转换
            if 'status' in item:
                item['status'] = '启用' if item.get('status') == '0' else '停用'
            # 创建者转换
            creator_info = item.get('creator')
            if isinstance(creator_info, dict):
                item['creator'] = creator_info.get('name', '未知')
            elif creator_info is None:
                item['creator'] = '未知'

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)

    @classmethod
    async def batch_import_ai_mcp_service(cls, auth: AuthSchema, file: UploadFile, update_support: bool = False) -> str:
        """批量导入"""
        header_dict = {
            '主键ID': 'id',
            'UUID全局唯一标识': 'uuid',
            '是否启用(0:启用 1:禁用)': 'status',
            '备注/描述': 'description',
            '创建时间': 'created_time',
            '更新时间': 'updated_time',
            '创建人ID': 'created_id',
            '更新人ID': 'updated_id',
            'mcp名称': 'name',
            '类型': 'type',
            '摘要': 'abstract',
            '分类': 'category',
            'mcp配置': 'config',
            '工具配置': 'tools',
            '封面图片URL': 'cover',
        }

        try:
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            await file.close()
            
            if df.empty:
                raise CustomException(msg="导入文件为空")
            
            missing_headers = [header for header in header_dict.keys() if header not in df.columns]
            if missing_headers:
                raise CustomException(msg=f"导入文件缺少必要的列: {', '.join(missing_headers)}")
            
            df.rename(columns=header_dict, inplace=True)
            
            # 验证必填字段
            
            error_msgs = []
            success_count = 0
            count = 0
            
            for index, row in df.iterrows():
                count += 1
                try:
                    data = {
                        "id": row['id'],
                        "uuid": row['uuid'],
                        "status": row['status'],
                        "description": row['description'],
                        "created_time": row['created_time'],
                        "updated_time": row['updated_time'],
                        "created_id": row['created_id'],
                        "updated_id": row['updated_id'],
                        "name": row['name'],
                        "type": row['type'],
                        "abstract": row['abstract'],
                        "category": row['category'],
                        "config": row['config'],
                        "tools": row['tools'],
                        "cover": row['cover'],
                    }
                    # 使用CreateSchema做校验后入库
                    create_schema = AiMcpCreateSchema.model_validate(data)
                    
                    # 检查唯一性约束
                    
                    await AiMcpCRUD(auth).create_ai_mcp_crud(data=create_schema)
                    success_count += 1
                except Exception as e:
                    error_msgs.append(f"第{count}行: {str(e)}")
                    continue

            result = f"成功导入 {success_count} 条数据"
            if error_msgs:
                result += "\n错误信息:\n" + "\n".join(error_msgs)
            return result
            
        except Exception as e:
            log.error(f"批量导入失败: {str(e)}")
            raise CustomException(msg=f"导入失败: {str(e)}")
    
    @classmethod
    async def import_template_download_ai_mcp_service(cls) -> bytes:
        """下载导入模板"""
        header_list = [
            '主键ID',
            'UUID全局唯一标识',
            '是否启用(0:启用 1:禁用)',
            '备注/描述',
            '创建时间',
            '更新时间',
            '创建人ID',
            '更新人ID',
            'mcp名称',
            '类型',
            '摘要',
            '分类',
            'mcp配置',
            '工具配置',
            '封面图片URL',
        ]
        selector_header_list = []
        option_list = []
        
        # 添加下拉选项
        
        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list
        )