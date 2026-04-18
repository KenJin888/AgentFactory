# -*- coding: utf-8 -*-

from collections.abc import Sequence

from sqlalchemy import delete

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase
from .model import AiDatasetAuthModel
from .schema import AiDatasetAuthCreateSchema


class AiDatasetAuthCRUD(CRUDBase[AiDatasetAuthModel, AiDatasetAuthCreateSchema, AiDatasetAuthCreateSchema]):
    """ai_dataset_auth数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(model=AiDatasetAuthModel, auth=auth)

    async def list_ai_dataset_auth_crud(
            self,
            search: dict | None = None,
            order_by: list[dict] | None = None,
    ) -> Sequence[AiDatasetAuthModel]:
        return await self.list(search=search, order_by=order_by, preload=[])

    async def create_ai_dataset_auth_crud(self, data: AiDatasetAuthCreateSchema) -> AiDatasetAuthModel | None:
        return await self.create(data=data)

    async def delete_by_dataset_id_ai_dataset_auth_crud(self, dataset_id: str) -> None:
        await self.auth.db.execute(delete(AiDatasetAuthModel).where(AiDatasetAuthModel.dataset_id == dataset_id))
        await self.auth.db.flush()

    async def delete_by_dataset_ids_ai_dataset_auth_crud(self, dataset_ids: list[str]) -> None:
        if not dataset_ids:
            return
        await self.auth.db.execute(delete(AiDatasetAuthModel).where(AiDatasetAuthModel.dataset_id.in_(dataset_ids)))
        await self.auth.db.flush()
