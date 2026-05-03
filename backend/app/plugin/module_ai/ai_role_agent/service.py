# -*- coding: utf-8 -*-

import io

import pandas as pd
from fastapi import UploadFile

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.core.logger import log
from app.utils.excel_util import ExcelUtil
from .crud import AiRoleAgentCRUD
from .schema import AiRoleAgentCreateSchema, AiRoleAgentUpdateSchema, AiRoleAgentOutSchema, AiRoleAgentQueryParam


class AiRoleAgentService:
    """
    AIRoleAgent服务层
    """

    _PERMISSION_PRIORITY = {
        "只读": 1,
        "读写": 2,
    }

    @staticmethod
    def get_current_role_ids(auth: AuthSchema) -> list[int]:
        """获取当前用户所有有效角色ID。"""
        return sorted({role.id for role in (auth.user.roles or []) if role and getattr(role, "id", None) is not None})

    @staticmethod
    def is_admin_user(auth: AuthSchema) -> bool:
        """判断当前用户是否为管理员。"""
        if not auth.user:
            return False
        if auth.user.is_superuser:
            return True

        role_codes = {
            str(role.code).upper()
            for role in (auth.user.roles or [])
            if role and getattr(role, "code", None)
        }
        role_names = {
            str(role.name)
            for role in (auth.user.roles or [])
            if role and getattr(role, "name", None)
        }
        return "ADMIN" in role_codes or any("管理员" in role_name for role_name in role_names)

    @classmethod
    async def list_current_role_agent_relations(
            cls,
            auth: AuthSchema,
            agent_ids: list[int] | None = None,
            permission: str | None = None,
    ):
        """查询当前用户角色与智能体的关联关系。"""
        role_ids = cls.get_current_role_ids(auth)
        if not role_ids:
            return []

        search = {"role_id": ("in", role_ids)}
        if agent_ids is not None:
            if not agent_ids:
                return []
            search["agent_id"] = ("in", sorted(set(agent_ids)))
        if permission:
            search["permission"] = ("eq", permission)

        return await AiRoleAgentCRUD(auth).list_ai_role_agent_crud(
            search=search,
            order_by=[{"id": "asc"}],
            preload=[]
        )

    @classmethod
    async def get_current_role_agent_ids(cls, auth: AuthSchema) -> list[int] | None:
        """获取当前用户可见的智能体ID列表，管理员返回None表示不限制。"""
        if cls.is_admin_user(auth):
            return None
        relations = await cls.list_current_role_agent_relations(auth)
        return sorted({relation.agent_id for relation in relations})

    @classmethod
    async def get_current_user_agent_permission_map(
            cls,
            auth: AuthSchema,
            agent_ids: list[int] | None = None,
    ) -> dict[int, str]:
        """获取当前用户对指定智能体的最高权限映射。"""
        if cls.is_admin_user(auth):
            if agent_ids is None:
                return {}
            return {int(agent_id): "读写" for agent_id in sorted(set(agent_ids))}

        relations = await cls.list_current_role_agent_relations(auth=auth, agent_ids=agent_ids)
        permission_map: dict[int, str] = {}
        for relation in relations:
            agent_id = int(relation.agent_id)
            current_permission = permission_map.get(agent_id)
            relation_permission = str(relation.permission)
            if cls._PERMISSION_PRIORITY.get(relation_permission, 0) >= cls._PERMISSION_PRIORITY.get(
                    current_permission, 0
            ):
                permission_map[agent_id] = relation_permission

        return permission_map

    @classmethod
    async def ensure_current_user_agent_permissions(
            cls,
            auth: AuthSchema,
            agent_ids: list[int],
            permission: str | None,
            action_text: str,
    ) -> None:
        """校验当前用户对智能体的操作权限。"""
        if cls.is_admin_user(auth):
            return

        relations = await cls.list_current_role_agent_relations(auth, agent_ids=agent_ids, permission=permission)
        allowed_agent_ids = {relation.agent_id for relation in relations}
        for agent_id in agent_ids:
            if agent_id not in allowed_agent_ids:
                raise CustomException(msg=f"无权限{action_text}智能体: {agent_id}", status_code=403)

    @classmethod
    async def create_current_role_agent_relations(
            cls,
            auth: AuthSchema,
            agent_id: int,
            permission: str = "读写",
    ) -> None:
        """为当前用户所有角色创建智能体关系。"""
        role_ids = cls.get_current_role_ids(auth)
        if not cls.is_admin_user(auth) and not role_ids:
            raise CustomException(msg="当前用户未绑定角色，无法创建智能体", status_code=403)

        for role_id in role_ids:
            await AiRoleAgentCRUD(auth).create_ai_role_agent_crud(
                data=AiRoleAgentCreateSchema(role_id=role_id, agent_id=agent_id, permission=permission)
            )

    @classmethod
    async def delete_current_role_agent_relations(
            cls,
            auth: AuthSchema,
            agent_ids: list[int],
            permission: str | None = None,
    ) -> None:
        """删除当前用户角色下指定智能体关系。"""
        if cls.is_admin_user(auth):
            return

        relations = await cls.list_current_role_agent_relations(auth, agent_ids=agent_ids, permission=permission)
        relation_ids = sorted({relation.id for relation in relations})
        if relation_ids:
            await AiRoleAgentCRUD(auth).delete_ai_role_agent_crud(ids=relation_ids)

    @classmethod
    async def detail_ai_role_agent_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await AiRoleAgentCRUD(auth).get_by_id_ai_role_agent_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return AiRoleAgentOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def list_ai_role_agent_service(cls, auth: AuthSchema, search: AiRoleAgentQueryParam | None = None,
                                         order_by: list[dict] | None = None) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await AiRoleAgentCRUD(auth).list_ai_role_agent_crud(search=search_dict, order_by=order_by)
        return [AiRoleAgentOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_ai_role_agent_service(cls, auth: AuthSchema, page_no: int, page_size: int,
                                         search: AiRoleAgentQueryParam | None = None,
                                         order_by: list[dict] | None = None) -> dict:
        """分页查询（数据库分页）"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        result = await AiRoleAgentCRUD(auth).page_ai_role_agent_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        return result

    @classmethod
    async def create_ai_role_agent_service(cls, auth: AuthSchema, data: AiRoleAgentCreateSchema) -> dict:
        """创建"""
        obj = await AiRoleAgentCRUD(auth).create_ai_role_agent_crud(data=data)
        return AiRoleAgentOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_ai_role_agent_service(cls, auth: AuthSchema, id: int, data: AiRoleAgentUpdateSchema) -> dict:
        """更新"""
        obj = await AiRoleAgentCRUD(auth).get_by_id_ai_role_agent_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')

        obj = await AiRoleAgentCRUD(auth).update_ai_role_agent_crud(id=id, data=data)
        return AiRoleAgentOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_ai_role_agent_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await AiRoleAgentCRUD(auth).get_by_id_ai_role_agent_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
        await AiRoleAgentCRUD(auth).delete_ai_role_agent_crud(ids=ids)

    @classmethod
    async def set_available_ai_role_agent_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await AiRoleAgentCRUD(auth).set_available_ai_role_agent_crud(ids=data.ids, status=data.status)

    @classmethod
    async def batch_export_ai_role_agent_service(cls, obj_list: list[dict]) -> bytes:
        """批量导出"""
        mapping_dict = {
            'role_id': '',
            'agent_id': '',
            'permission': '',
            'id': '',
            'uuid': '',
            'status': '',
            'description': '',
            'created_time': '',
            'updated_time': '',
            'updated_id': '更新者ID',
        }

        data = obj_list.copy()
        for item in data:
            if 'status' in item:
                item['status'] = '启用' if item.get('status') == '0' else '停用'
            creator_info = item.get('creator')
            if isinstance(creator_info, dict):
                item['creator'] = creator_info.get('name', '未知')
            elif creator_info is None:
                item['creator'] = '未知'

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)

    @classmethod
    async def batch_import_ai_role_agent_service(cls, auth: AuthSchema, file: UploadFile,
                                                 update_support: bool = False) -> str:
        """批量导入"""
        header_dict = {
            '': 'role_id',
            '': 'agent_id',
            '': 'permission',
            '': 'id',
            '': 'uuid',
            '': 'status',
            '': 'description',
            '': 'created_time',
            '': 'updated_time',
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

            error_msgs = []
            success_count = 0
            count = 0

            for index, row in df.iterrows():
                count += 1
                try:
                    data = {
                        "role_id": row['role_id'],
                        "agent_id": row['agent_id'],
                        "permission": row['permission'],
                        "id": row['id'],
                        "uuid": row['uuid'],
                        "status": row['status'],
                        "description": row['description'],
                        "created_time": row['created_time'],
                        "updated_time": row['updated_time'],
                    }
                    create_schema = AiRoleAgentCreateSchema.model_validate(data)
                    await AiRoleAgentCRUD(auth).create_ai_role_agent_crud(data=create_schema)
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
    async def import_template_download_ai_role_agent_service(cls) -> bytes:
        """下载导入模板"""
        header_list = [
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
        ]
        selector_header_list = []
        option_list = []

        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list
        )
