# -*- coding: utf-8 -*-

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from .crud import AiChatMsgCRUD
from .schema import AiChatMsgCreateSchema, AiChatMsgUpdateSchema, AiChatMsgOutSchema, AiChatMsgQueryParam


class AiChatMsgService:
    """
    ai_chat_msg服务层
    """

    @classmethod
    async def detail_ai_chat_msg_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await AiChatMsgCRUD(auth).get_by_id_ai_chat_msg_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return AiChatMsgOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def page_ai_chat_msg_service(cls, auth: AuthSchema, page_no: int, page_size: int,
                                       search: AiChatMsgQueryParam | None = None,
                                       order_by: list[dict] | None = None) -> dict:
        """分页查询（数据库分页）"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        result = await AiChatMsgCRUD(auth).page_ai_chat_msg_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        return result

    @classmethod
    async def create_ai_chat_msg_service(cls, auth: AuthSchema, data: AiChatMsgCreateSchema) -> dict:
        """创建"""
        # 检查唯一性约束
        obj = await AiChatMsgCRUD(auth).create_ai_chat_msg_crud(data=data)
        return AiChatMsgOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_ai_chat_msg_service(cls, auth: AuthSchema, id: int, data: AiChatMsgUpdateSchema) -> dict:
        """更新"""
        # 检查数据是否存在
        obj = await AiChatMsgCRUD(auth).get_by_id_ai_chat_msg_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')

        # 检查唯一性约束

        obj = await AiChatMsgCRUD(auth).update_ai_chat_msg_crud(id=id, data=data)
        return AiChatMsgOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_ai_chat_msg_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await AiChatMsgCRUD(auth).get_by_id_ai_chat_msg_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
        await AiChatMsgCRUD(auth).delete_ai_chat_msg_crud(ids=ids)

    @classmethod
    async def set_available_ai_chat_msg_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await AiChatMsgCRUD(auth).set_available_ai_chat_msg_crud(ids=data.ids, status=data.status)

    @classmethod
    async def batch_export_ai_chat_msg_service(cls, obj_list: list[dict]) -> bytes:
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
            'chat_id': '会话id',
            'role': 'role',
            'content': '内容',
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
