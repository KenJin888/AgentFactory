# -*- coding: utf-8 -*-

import io

import pandas as pd
from fastapi import UploadFile

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.core.logger import log
from app.utils.excel_util import ExcelUtil
from .crud import AiRoleDatasetCRUD
from .schema import (
    AiRoleDatasetCreateSchema,
    AiRoleDatasetUpdateSchema,
    AiRoleDatasetOutSchema,
    AiRoleDatasetQueryParam,
)


class AiRoleDatasetService:
    """
    AIRoleDataset服务层
    """

    _PERMISSION_PRIORITY = {
        "只读": 1,
        "读写": 2,
    }

    @staticmethod
    def get_current_role_ids(auth: AuthSchema) -> list[int]:
        """获取当前用户所有有效角色ID。"""
        return sorted(
            {role.id for role in (auth.user.roles or []) if role and getattr(role, "id", None) is not None}
        )

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
    async def list_current_role_dataset_relations(
            cls,
            auth: AuthSchema,
            dataset_ids: list[str] | None = None,
            permission: str | None = None,
    ):
        """查询当前用户角色与知识库的关联关系。"""
        role_ids = cls.get_current_role_ids(auth)
        if not role_ids:
            return []

        search = {"role_id": ("in", role_ids)}
        if dataset_ids is not None:
            if not dataset_ids:
                return []
            search["datasets_id"] = ("in", sorted(set(dataset_ids)))
        if permission:
            search["permission"] = ("eq", permission)

        return await AiRoleDatasetCRUD(auth).list_ai_role_dataset_crud(
            search=search,
            order_by=[{"id": "asc"}],
            preload=[],
        )

    @classmethod
    async def list_dataset_relations_by_ids(cls, auth: AuthSchema, dataset_ids: list[str]):
        """查询指定知识库ID对应的全部关系。"""
        if not dataset_ids:
            return []
        return await AiRoleDatasetCRUD(auth).list_ai_role_dataset_crud(
            search={"datasets_id": ("in", sorted(set(dataset_ids)))},
            order_by=[{"id": "asc"}],
            preload=[],
        )

    @classmethod
    async def get_current_role_dataset_ids(cls, auth: AuthSchema) -> list[str] | None:
        """获取当前用户可见的知识库ID列表，管理员返回None表示不限制。"""
        if cls.is_admin_user(auth):
            return None
        relations = await cls.list_current_role_dataset_relations(auth)
        return sorted({relation.datasets_id for relation in relations})

    @classmethod
    async def get_current_user_dataset_permission_map(
            cls,
            auth: AuthSchema,
            dataset_ids: list[str] | None = None,
    ) -> dict[str, str]:
        """获取当前用户对指定知识库的最高权限映射。"""
        if cls.is_admin_user(auth):
            if dataset_ids is None:
                return {}
            return {str(dataset_id): "读写" for dataset_id in sorted(set(dataset_ids)) if dataset_id}

        relations = await cls.list_current_role_dataset_relations(auth=auth, dataset_ids=dataset_ids)
        permission_map: dict[str, str] = {}
        for relation in relations:
            dataset_id = str(relation.datasets_id)
            current_permission = permission_map.get(dataset_id)
            relation_permission = str(relation.permission)
            if cls._PERMISSION_PRIORITY.get(relation_permission, 0) >= cls._PERMISSION_PRIORITY.get(
                    current_permission, 0
            ):
                permission_map[dataset_id] = relation_permission

        return permission_map

    @classmethod
    async def ensure_current_user_dataset_permissions(
            cls,
            auth: AuthSchema,
            dataset_ids: list[str],
            permission: str | None,
            action_text: str,
    ) -> None:
        """校验当前用户对知识库的操作权限。"""
        if cls.is_admin_user(auth):
            return

        relations = await cls.list_current_role_dataset_relations(
            auth=auth, dataset_ids=dataset_ids, permission=permission
        )
        allowed_dataset_ids = {relation.datasets_id for relation in relations}
        for dataset_id in dataset_ids:
            if dataset_id not in allowed_dataset_ids:
                raise CustomException(msg=f"无权限{action_text}该知识库: {dataset_id}", status_code=403)

    @classmethod
    async def create_current_role_dataset_relations(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            permission: str = "读写",
    ) -> None:
        """为当前用户所有角色创建知识库关系。"""
        role_ids = cls.get_current_role_ids(auth)
        if not cls.is_admin_user(auth) and not role_ids:
            raise CustomException(msg="当前用户未绑定角色，无法创建知识库", status_code=403)

        for role_id in role_ids:
            await AiRoleDatasetCRUD(auth).create_ai_role_dataset_crud(
                data=AiRoleDatasetCreateSchema(role_id=role_id, datasets_id=dataset_id, permission=permission)
            )

    @classmethod
    async def delete_dataset_relations_by_dataset_ids(cls, auth: AuthSchema, dataset_ids: list[str]) -> None:
        """删除指定知识库ID对应的全部关系。"""
        relations = await cls.list_dataset_relations_by_ids(auth=auth, dataset_ids=dataset_ids)
        relation_ids = sorted({relation.id for relation in relations})
        if relation_ids:
            await AiRoleDatasetCRUD(auth).delete_ai_role_dataset_crud(ids=relation_ids)

    @classmethod
    async def detail_ai_role_dataset_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await AiRoleDatasetCRUD(auth).get_by_id_ai_role_dataset_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return AiRoleDatasetOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def list_ai_role_dataset_service(
            cls,
            auth: AuthSchema,
            search: AiRoleDatasetQueryParam | None = None,
            order_by: list[dict] | None = None,
    ) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await AiRoleDatasetCRUD(auth).list_ai_role_dataset_crud(search=search_dict, order_by=order_by)
        return [AiRoleDatasetOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_ai_role_dataset_service(
            cls,
            auth: AuthSchema,
            page_no: int,
            page_size: int,
            search: AiRoleDatasetQueryParam | None = None,
            order_by: list[dict] | None = None,
    ) -> dict:
        """分页查询（数据库分页）"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        result = await AiRoleDatasetCRUD(auth).page_ai_role_dataset_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        return result

    @classmethod
    async def create_ai_role_dataset_service(cls, auth: AuthSchema, data: AiRoleDatasetCreateSchema) -> dict:
        """创建"""
        obj = await AiRoleDatasetCRUD(auth).create_ai_role_dataset_crud(data=data)
        return AiRoleDatasetOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_ai_role_dataset_service(cls, auth: AuthSchema, id: int, data: AiRoleDatasetUpdateSchema) -> dict:
        """更新"""
        obj = await AiRoleDatasetCRUD(auth).get_by_id_ai_role_dataset_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')

        obj = await AiRoleDatasetCRUD(auth).update_ai_role_dataset_crud(id=id, data=data)
        return AiRoleDatasetOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_ai_role_dataset_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await AiRoleDatasetCRUD(auth).get_by_id_ai_role_dataset_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
        await AiRoleDatasetCRUD(auth).delete_ai_role_dataset_crud(ids=ids)

    @classmethod
    async def set_available_ai_role_dataset_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await AiRoleDatasetCRUD(auth).set_available_ai_role_dataset_crud(ids=data.ids, status=data.status)

    @classmethod
    async def batch_export_ai_role_dataset_service(cls, obj_list: list[dict]) -> bytes:
        """批量导出"""
        mapping_dict = {
            'role_id': '',
            'datasets_id': '',
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
    async def batch_import_ai_role_dataset_service(
            cls,
            auth: AuthSchema,
            file: UploadFile,
            update_support: bool = False,
    ) -> str:
        """批量导入"""
        header_dict = {
            '': 'role_id',
            '': 'datasets_id',
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
                        "datasets_id": row['datasets_id'],
                        "permission": row['permission'],
                        "id": row['id'],
                        "uuid": row['uuid'],
                        "status": row['status'],
                        "description": row['description'],
                        "created_time": row['created_time'],
                        "updated_time": row['updated_time'],
                    }
                    create_schema = AiRoleDatasetCreateSchema.model_validate(data)
                    await AiRoleDatasetCRUD(auth).create_ai_role_dataset_crud(data=create_schema)
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
    async def import_template_download_ai_role_dataset_service(cls) -> bytes:
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
