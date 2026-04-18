from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException

from .crud import ExUserPreferenceCRUD
from .schema import (
    ExUserPreferenceCreateSchema,
    ExUserPreferenceOutSchema,
    ExUserPreferenceQueryParam,
    ExUserPreferenceUpdateSchema,
)


class ExUserPreferenceService:
    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        obj = await ExUserPreferenceCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return ExUserPreferenceOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: ExUserPreferenceQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        return await ExUserPreferenceCRUD(auth).page_crud(
            offset=(page_no - 1) * page_size,
            limit=page_size,
            order_by=order_by,
            search=search.__dict__ if search else {},
        )

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: ExUserPreferenceCreateSchema) -> dict:
        exist_obj = await ExUserPreferenceCRUD(auth).get_by_user_key_crud(
            user_id=data.user_id, pref_key=data.pref_key
        )
        if exist_obj:
            raise CustomException(msg="创建失败，该偏好键已存在")
        obj = await ExUserPreferenceCRUD(auth).create_crud(data=data)
        return ExUserPreferenceOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(
        cls, auth: AuthSchema, id: int, data: ExUserPreferenceUpdateSchema
    ) -> dict:
        obj = await ExUserPreferenceCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="更新失败，该数据不存在")

        target_user_id = data.user_id if data.user_id is not None else obj.user_id
        target_pref_key = data.pref_key if data.pref_key is not None else obj.pref_key
        exist_obj = await ExUserPreferenceCRUD(auth).get_by_user_key_crud(
            user_id=target_user_id, pref_key=target_pref_key
        )
        if exist_obj and exist_obj.id != id:
            raise CustomException(msg="更新失败，该偏好键已存在")

        new_obj = await ExUserPreferenceCRUD(auth).update_crud(id=id, data=data)
        return ExUserPreferenceOutSchema.model_validate(new_obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        if not ids:
            raise CustomException(msg="删除失败，删除对象不能为空")
        for id in ids:
            obj = await ExUserPreferenceCRUD(auth).get_by_id_crud(id=id)
            if not obj:
                raise CustomException(msg=f"删除失败，ID为{id}的数据不存在")
        await ExUserPreferenceCRUD(auth).delete_crud(ids=ids)

    @classmethod
    async def get_my_preference_service(cls, auth: AuthSchema, pref_key: str) -> dict:
        if not auth.user:
            raise CustomException(msg="用户未登录")
        obj = await ExUserPreferenceCRUD(auth).get_by_user_key_crud(
            user_id=auth.user.id, pref_key=pref_key
        )
        if not obj:
            return {"pref_key": pref_key, "pref_value": None}
        return {"pref_key": obj.pref_key, "pref_value": obj.pref_value}

    @classmethod
    async def set_my_preference_service(cls, auth: AuthSchema, pref_key: str, pref_value: str | None) -> dict:
        if not auth.user:
            raise CustomException(msg="用户未登录")
        obj = await ExUserPreferenceCRUD(auth).get_by_user_key_crud(
            user_id=auth.user.id, pref_key=pref_key
        )
        if obj:
            new_obj = await ExUserPreferenceCRUD(auth).update_crud(
                id=obj.id, data=ExUserPreferenceUpdateSchema(pref_value=pref_value)
            )
            return {"pref_key": new_obj.pref_key, "pref_value": new_obj.pref_value}
        created_obj = await ExUserPreferenceCRUD(auth).create_crud(
            data=ExUserPreferenceCreateSchema(
                user_id=auth.user.id,
                pref_key=pref_key,
                pref_value=pref_value,
                status="0",
            )
        )
        return {"pref_key": created_obj.pref_key, "pref_value": created_obj.pref_value}
