# -*- coding: utf-8 -*-

from collections.abc import Sequence

from sqlalchemy import delete

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase
from .model import AiAgentAuthModel
from .schema import AiAgentAuthCreateSchema


class AiAgentAuthCRUD(CRUDBase[AiAgentAuthModel, AiAgentAuthCreateSchema, AiAgentAuthCreateSchema]):
    """ai_agent_auth数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(model=AiAgentAuthModel, auth=auth)

    async def list_ai_agent_auth_crud(
            self,
            search: dict | None = None,
            order_by: list[dict] | None = None,
    ) -> Sequence[AiAgentAuthModel]:
        return await self.list(search=search, order_by=order_by, preload=[])

    async def create_ai_agent_auth_crud(self, data: AiAgentAuthCreateSchema) -> AiAgentAuthModel | None:
        return await self.create(data=data)

    async def delete_by_agent_id_ai_agent_auth_crud(self, agent_id: int) -> None:
        await self.auth.db.execute(delete(AiAgentAuthModel).where(AiAgentAuthModel.agent_id == agent_id))
        await self.auth.db.flush()
