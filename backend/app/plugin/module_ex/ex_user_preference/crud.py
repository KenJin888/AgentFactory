from collections.abc import Sequence

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase

from .model import ExUserPreferenceModel
from .schema import ExUserPreferenceCreateSchema, ExUserPreferenceOutSchema, ExUserPreferenceUpdateSchema


class ExUserPreferenceCRUD(
    CRUDBase[ExUserPreferenceModel, ExUserPreferenceCreateSchema, ExUserPreferenceUpdateSchema]
):
    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(model=ExUserPreferenceModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> ExUserPreferenceModel | None:
        return await self.get(id=id)

    async def get_by_user_key_crud(
        self, user_id: int, pref_key: str
    ) -> ExUserPreferenceModel | None:
        return await self.get(user_id=user_id, pref_key=pref_key)

    async def list_crud(
        self,
        search: dict | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> Sequence[ExUserPreferenceModel]:
        return await self.list(search=search, order_by=order_by)

    async def create_crud(self, data: ExUserPreferenceCreateSchema) -> ExUserPreferenceModel:
        return await self.create(data=data)

    async def update_crud(
        self, id: int, data: ExUserPreferenceUpdateSchema
    ) -> ExUserPreferenceModel:
        return await self.update(id=id, data=data)

    async def delete_crud(self, ids: list[int]) -> None:
        await self.delete(ids=ids)

    async def page_crud(
        self,
        offset: int,
        limit: int,
        order_by: list[dict[str, str]] | None = None,
        search: dict | None = None,
    ) -> dict:
        return await self.page(
            offset=offset,
            limit=limit,
            order_by=order_by or [{"id": "desc"}],
            search=search or {},
            out_schema=ExUserPreferenceOutSchema,
        )
