# -*- coding: utf-8 -*-

import io
import json
from typing import Any, Sequence

import pandas as pd
from fastapi import UploadFile
from sqlalchemy import asc, desc, exists, func, or_, select

from app.api.v1.module_system.auth.schema import AuthSchema
from app.config.setting import settings
from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.core.logger import log
from app.plugin.module_ai.ai_agent_auth.model import AiAgentAuthModel
from app.plugin.module_ai.ai_agent_auth.service import AiAgentAuthService
from app.plugin.module_ex.ex_user_preference.service import ExUserPreferenceService
from app.utils.excel_util import ExcelUtil
from .crud import AiAgentCRUD
from .model import AiAgentModel
from .schema import (
    AiAgentCreateSchema,
    AiAgentKnowledgeDatasetSchema,
    AiAgentManageSchema,
    AiAgentOutSchema,
    AiAgentPersistSchema,
    AiAgentPublishSchema,
    AiAgentQueryParam,
    AiAgentUpdateSchema,
)


class AiAgentService:
    """
    ai_agent服务层
    """

    _VISIBILITY_PRIVATE = "private"
    _VISIBILITY_PUBLIC = "public"
    _PUBLISH_DRAFT = "draft"
    _PUBLISH_PUBLISHED = "published"
    _PUBLISH_CLONE = "clone"
    _PUBLISH_OFFLINE = "offline"
    _PUBLISH_DELETED = "delete"
    _FORBIDDEN_CODE = 10403
    _FAVORITE_PREF_KEY = "agent_square_favorite_ids"

    @staticmethod
    def _current_user_id(auth: AuthSchema) -> int:
        if not auth.user or not auth.user.id:
            raise CustomException(msg="用户不存在")
        return int(auth.user.id)

    @classmethod
    def _is_owner(cls, auth: AuthSchema, obj) -> bool:
        return int(getattr(obj, "created_id", 0) or 0) == cls._current_user_id(auth)

    @staticmethod
    def _normalize_dataset_id(value: Any) -> str:
        return str(value or "").strip()

    @classmethod
    def _serialize_knowledge_dataset(cls, item: Any) -> dict:
        if isinstance(item, dict):
            dataset_id = cls._normalize_dataset_id(item.get("dataset_id") or item.get("id"))
            return AiAgentKnowledgeDatasetSchema(
                dataset_id=dataset_id,
                name=str(item.get("name") or ""),
                description=item.get("description"),
                document_count=item.get("document_count"),
            ).model_dump()

        dataset_id = cls._normalize_dataset_id(
            getattr(item, "dataset_id", None) or getattr(item, "id", None)
        )
        return AiAgentKnowledgeDatasetSchema(
            dataset_id=dataset_id,
            name=str(getattr(item, "name", "") or ""),
            description=getattr(item, "description", None),
            document_count=getattr(item, "document_count", None),
        ).model_dump()

    @classmethod
    def _to_out_schema(cls, obj) -> dict:
        return AiAgentOutSchema.model_validate(obj).model_dump()

    @classmethod
    def _ensure_private_owner(cls, auth: AuthSchema, obj, action_text: str) -> None:
        if obj.visibility_scope != cls._VISIBILITY_PRIVATE:
            raise CustomException(
                msg=f"仅私有智能体允许{action_text}",
                code=cls._FORBIDDEN_CODE,
                status_code=403,
            )
        if not cls._is_owner(auth=auth, obj=obj):
            raise CustomException(
                msg=f"仅智能体所有者允许{action_text}",
                code=cls._FORBIDDEN_CODE,
                status_code=403,
            )

    @classmethod
    def _build_empty_page(page_no: int, page_size: int) -> dict:
        return {
            "page_no": page_no,
            "page_size": page_size,
            "total": 0,
            "has_next": False,
            "items": [],
        }

    @classmethod
    def _build_order_by(cls, order_by: list[dict] | None) -> list:
        order_expressions = []
        for order_item in order_by or [{"updated_time": "desc"}]:
            for field, direction in order_item.items():
                attr = getattr(AiAgentModel, field, None)
                if attr is None:
                    continue
                order_expressions.append(asc(attr) if str(direction).lower() == "asc" else desc(attr))
        return order_expressions or [desc(AiAgentModel.updated_time)]

    @classmethod
    def _build_search_conditions(cls, search_dict: dict | None) -> list:
        conditions = []
        for key, value in (search_dict or {}).items():
            if value is None or value == "":
                continue

            attr = getattr(AiAgentModel, key, None)
            if attr is None:
                continue

            if isinstance(value, tuple) and len(value) == 2:
                operator, payload = value
                if operator == "like" and payload:
                    conditions.append(attr.like(f"%{payload}%"))
                elif operator in {"eq", "=="}:
                    conditions.append(attr == payload)
                elif operator in {"ne", "!="}:
                    conditions.append(attr != payload)
                elif operator == "in" and payload:
                    conditions.append(attr.in_(payload))
                elif operator == "between" and isinstance(payload, (list, tuple)) and len(payload) == 2:
                    conditions.append(attr.between(payload[0], payload[1]))
                elif operator in {"gt", ">"}:
                    conditions.append(attr > payload)
                elif operator in {"ge", ">="}:
                    conditions.append(attr >= payload)
                elif operator in {"lt", "<"}:
                    conditions.append(attr < payload)
                elif operator in {"le", "<="}:
                    conditions.append(attr <= payload)
                continue

            conditions.append(attr == value)
        return conditions

    @classmethod
    def _build_public_visibility_condition(cls, auth: AuthSchema, min_right: int):
        if AiAgentAuthService.is_admin_user(auth):
            return None

        current_user_id = cls._current_user_id(auth)
        match_clause = AiAgentAuthService.build_match_clause(auth=auth, min_right=min_right)
        return or_(
            AiAgentModel.created_id == current_user_id,
            exists(
                select(1).where(
                    AiAgentAuthModel.agent_id == AiAgentModel.id,
                    match_clause,
                )
            ),
        )

    @classmethod
    async def _append_agent_access(cls, auth: AuthSchema, agents: list[dict]) -> list[dict]:
        if not agents:
            return agents

        is_admin = AiAgentAuthService.is_admin_user(auth)
        current_user_id = cls._current_user_id(auth)
        public_agent_ids = [
            int(agent["id"])
            for agent in agents
            if agent.get("id") is not None
               and agent.get("visibility_scope") == cls._VISIBILITY_PUBLIC
               and agent.get("publish_status") == cls._PUBLISH_PUBLISHED
               and int(agent.get("created_id") or 0) != current_user_id
        ]
        right_map = await AiAgentAuthService.resolve_agent_right_map(auth=auth, agent_ids=public_agent_ids)
        for agent in agents:
            agent_id = int(agent.get("id") or 0)
            is_owner = int(agent.get("created_id") or 0) == current_user_id
            is_public_published = (
                    agent.get("visibility_scope") == cls._VISIBILITY_PUBLIC
                    and agent.get("publish_status") == cls._PUBLISH_PUBLISHED
            )
            current_right = 2 if (is_admin or is_owner) else int(right_map.get(agent_id, 0))

            agent["current_right"] = current_right
            agent["is_owner"] = is_owner
            agent["is_admin"] = is_admin
            agent["can_manage"] = bool(is_admin or is_owner)
            agent["can_view"] = bool(is_admin or is_owner or (is_public_published and current_right >= 1))
            agent["can_clone"] = bool(is_admin or is_owner or (is_public_published and current_right >= 2))
        return agents

    @classmethod
    async def _append_single_agent_access(cls, auth: AuthSchema, agent: dict) -> dict:
        agents = await cls._append_agent_access(auth=auth, agents=[agent])
        return agents[0] if agents else agent

    @staticmethod
    def _parse_favorite_agent_ids(pref_value: str | None) -> list[int]:
        if not pref_value:
            return []

        raw_values = []
        try:
            parsed = json.loads(pref_value)
            if isinstance(parsed, list):
                raw_values = parsed
            elif isinstance(parsed, str):
                raw_values = parsed.split(",")
        except (TypeError, ValueError):
            raw_values = str(pref_value).split(",")

        dedup_ids: list[int] = []
        seen: set[int] = set()
        for raw in raw_values:
            try:
                agent_id = int(str(raw).strip())
            except (TypeError, ValueError):
                continue
            if agent_id <= 0 or agent_id in seen:
                continue
            seen.add(agent_id)
            dedup_ids.append(agent_id)
        return dedup_ids

    @classmethod
    async def _query_public_agents(
            cls,
            auth: AuthSchema,
            *,
            search_dict: dict | None = None,
            order_by: list[dict] | None = None,
            offset: int | None = None,
            limit: int | None = None,
    ) -> tuple[Sequence[Any], int]:
        conditions = [
            AiAgentModel.visibility_scope == cls._VISIBILITY_PUBLIC,
            AiAgentModel.publish_status == cls._PUBLISH_PUBLISHED,
            *cls._build_search_conditions(search_dict),
        ]
        visibility_condition = cls._build_public_visibility_condition(auth=auth, min_right=1)
        if visibility_condition is not None:
            conditions.append(visibility_condition)

        sql = select(AiAgentModel).where(*conditions).order_by(*cls._build_order_by(order_by))
        count_sql = select(func.count(AiAgentModel.id)).where(*conditions)

        total = int((await auth.db.execute(count_sql)).scalar() or 0)
        if offset is not None:
            sql = sql.offset(offset)
        if limit is not None:
            sql = sql.limit(limit)

        result = await auth.db.execute(sql)
        return result.scalars().all(), total

    @classmethod
    async def _load_detail_auth_rules(cls, auth: AuthSchema, obj) -> list[dict]:
        if not (AiAgentAuthService.is_admin_user(auth) or cls._is_owner(auth, obj)):
            return []

        target_agent_id = 0
        if obj.visibility_scope == cls._VISIBILITY_PUBLIC:
            target_agent_id = int(obj.id)
        elif (
                obj.visibility_scope == cls._VISIBILITY_PRIVATE
                and obj.publish_status == cls._PUBLISH_PUBLISHED
                and int(obj.public_agent_id or 0) > 0
        ):
            target_agent_id = int(obj.public_agent_id)

        if target_agent_id <= 0:
            return []

        rules = await AiAgentAuthService.list_agent_auth_rules(auth=auth, agent_id=target_agent_id)
        return [rule.model_dump() for rule in rules]

    @classmethod
    async def detail_ai_agent_service(cls, auth: AuthSchema, id: int) -> dict:
        obj = await AiAgentCRUD(auth).get_by_id_ai_agent_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")

        is_admin = AiAgentAuthService.is_admin_user(auth)
        is_owner = cls._is_owner(auth=auth, obj=obj)
        if obj.visibility_scope == cls._VISIBILITY_PRIVATE and not (is_admin or is_owner):
            raise CustomException(msg="私有智能体仅所有者可访问", code=cls._FORBIDDEN_CODE, status_code=403)

        if obj.visibility_scope == cls._VISIBILITY_PUBLIC:
            if obj.publish_status == cls._PUBLISH_OFFLINE and not (is_admin or is_owner):
                raise CustomException(msg="该智能体已下线", code=cls._FORBIDDEN_CODE, status_code=403)
            if obj.publish_status not in {cls._PUBLISH_PUBLISHED, cls._PUBLISH_OFFLINE} and not (is_admin or is_owner):
                raise CustomException(msg="该智能体不可访问", code=cls._FORBIDDEN_CODE, status_code=403)
            if obj.publish_status == cls._PUBLISH_PUBLISHED and not (is_admin or is_owner):
                current_right = await AiAgentAuthService.resolve_agent_right(auth=auth, agent_id=int(obj.id))
                if current_right < 1:
                    raise CustomException(msg="无权限访问该智能体", code=cls._FORBIDDEN_CODE, status_code=403)

        result = cls._to_out_schema(obj)
        result = await cls._append_single_agent_access(auth=auth, agent=result)
        result["auth_rules"] = await cls._load_detail_auth_rules(auth=auth, obj=obj)
        return result

    @classmethod
    async def list_available_knowledge_datasets_service(
            cls,
            auth: AuthSchema,
            page: int = 1,
            page_size: int = 200,
    ) -> list[dict]:
        if not str(settings.RAGFLOW_API_BASE or "").strip():
            return []

        from app.plugin.module_ai.ai_ragflow.service import AiRagflowService

        datasets_result = await AiRagflowService.list_datasets_service(auth=auth, page=page, page_size=page_size)
        datasets = datasets_result.data or []
        return [cls._serialize_knowledge_dataset(item) for item in datasets]

    @classmethod
    async def list_ai_agent_service(cls, auth: AuthSchema, search: AiAgentQueryParam | None = None,
                                    order_by: list[dict] | None = None) -> list[dict]:
        search_dict = search.__dict__.copy() if search else {}
        if AiAgentAuthService.is_admin_user(auth):
            obj_list = await AiAgentCRUD(auth).list_ai_agent_crud(search=search_dict, order_by=order_by)
            result = [cls._to_out_schema(obj) for obj in obj_list]
            return await cls._append_agent_access(auth=auth, agents=result)

        private_agents = await AiAgentCRUD(auth).list_ai_agent_crud(
            search={
                **search_dict,
                "created_id": cls._current_user_id(auth),
                "visibility_scope": cls._VISIBILITY_PRIVATE,
                "publish_status": ("!=", cls._PUBLISH_DELETED),
            },
            order_by=order_by,
        )
        public_agents, _ = await cls._query_public_agents(auth=auth, search_dict=search_dict, order_by=order_by)

        merged: dict[int, dict] = {}
        for obj in [*private_agents, *public_agents]:
            merged[int(obj.id)] = cls._to_out_schema(obj)
        return await cls._append_agent_access(auth=auth, agents=list(merged.values()))

    @classmethod
    async def page_ai_agent_service(cls, auth: AuthSchema, page_no: int, page_size: int,
                                    search: AiAgentQueryParam | None = None,
                                    order_by: list[dict] | None = None) -> dict:
        if not AiAgentAuthService.is_admin_user(auth):
            return await cls.square_page_ai_agent_service(
                auth=auth,
                page_no=page_no,
                page_size=page_size,
                search=search,
                order_by=order_by,
            )

        search_dict = search.__dict__.copy() if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        result = await AiAgentCRUD(auth).page_ai_agent_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        result["items"] = await cls._append_agent_access(auth=auth, agents=result.get("items") or [])
        return result

    @classmethod
    async def create_ai_agent_service(cls, auth: AuthSchema, data: AiAgentCreateSchema) -> dict:
        create_data = AiAgentPersistSchema(
            status=data.status,
            name=data.name,
            description=data.description,
            type=data.type,
            visibility_scope=cls._VISIBILITY_PRIVATE,
            publish_status=cls._PUBLISH_DRAFT,
            version_no=1,
            public_agent_id=0,
            config=data.config,
            prompt_template=data.prompt_template,
            model=data.model,
            cover=data.cover,
            order_no=data.order_no,
        )
        obj = await AiAgentCRUD(auth).create_ai_agent_crud(data=create_data)
        result = cls._to_out_schema(obj)
        return await cls._append_single_agent_access(auth=auth, agent=result)

    @classmethod
    async def update_ai_agent_service(cls, auth: AuthSchema, id: int, data: AiAgentUpdateSchema) -> dict:
        obj = await AiAgentCRUD(auth).get_by_id_ai_agent_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        cls._ensure_private_owner(auth=auth, obj=obj, action_text="编辑")

        update_data = AiAgentPersistSchema(
            status=data.status,
            name=data.name,
            description=data.description,
            type=data.type,
            visibility_scope=obj.visibility_scope,
            publish_status=obj.publish_status,
            version_no=obj.version_no,
            public_agent_id=obj.public_agent_id,
            config=data.config,
            prompt_template=data.prompt_template,
            model=data.model,
            cover=data.cover,
            order_no=data.order_no,
        )
        obj = await AiAgentCRUD(auth).update_ai_agent_crud(id=id, data=update_data)
        result = cls._to_out_schema(obj)
        return await cls._append_single_agent_access(auth=auth, agent=result)

    @classmethod
    async def my_page_ai_agent_service(cls, auth: AuthSchema, page_no: int, page_size: int,
                                       search: AiAgentQueryParam | None = None,
                                       order_by: list[dict] | None = None) -> dict:
        search_dict = search.__dict__.copy() if search else {}
        search_dict["created_id"] = cls._current_user_id(auth)
        search_dict["visibility_scope"] = cls._VISIBILITY_PRIVATE
        search_dict["publish_status"] = ("!=", cls._PUBLISH_DELETED)
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        result = await AiAgentCRUD(auth).page_ai_agent_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        result["items"] = await cls._append_agent_access(auth=auth, agents=result.get("items") or [])
        return result

    @classmethod
    async def square_page_ai_agent_service(cls, auth: AuthSchema, page_no: int, page_size: int,
                                           search: AiAgentQueryParam | None = None,
                                           order_by: list[dict] | None = None) -> dict:
        search_dict = search.__dict__.copy() if search else {}
        search_dict.pop("visibility_scope", None)
        search_dict.pop("publish_status", None)
        offset = (page_no - 1) * page_size
        items, total = await cls._query_public_agents(
            auth=auth,
            search_dict=search_dict,
            order_by=order_by,
            offset=offset,
            limit=page_size,
        )
        result = {
            "page_no": page_no,
            "page_size": page_size,
            "total": total,
            "has_next": offset + page_size < total,
            "items": [cls._to_out_schema(obj) for obj in items],
        }
        result["items"] = await cls._append_agent_access(auth=auth, agents=result["items"])
        return result

    @classmethod
    async def favorite_ai_agent_list_service(cls, auth: AuthSchema) -> list[dict]:
        preference_result = await ExUserPreferenceService.get_my_preference_service(
            auth=auth,
            pref_key=cls._FAVORITE_PREF_KEY,
        )
        favorite_ids = cls._parse_favorite_agent_ids(preference_result.get("pref_value"))
        if not favorite_ids:
            return []

        obj_list, _ = await cls._query_public_agents(
            auth=auth,
            search_dict={"id": ("in", favorite_ids)},
            order_by=[{"id": "asc"}],
        )
        agents = [cls._to_out_schema(obj) for obj in obj_list]
        agents = await cls._append_agent_access(auth=auth, agents=agents)

        order_map = {agent_id: index for index, agent_id in enumerate(favorite_ids)}
        agents.sort(key=lambda item: order_map.get(int(item.get("id", 0)), len(order_map)))
        return agents

    @classmethod
    async def publish_ai_agent_service(cls, auth: AuthSchema, id: int, data: AiAgentPublishSchema) -> dict:
        source_obj = await AiAgentCRUD(auth).get_by_id_ai_agent_crud(id=id)
        if not source_obj:
            raise CustomException(msg="发布失败，该数据不存在")
        cls._ensure_private_owner(auth=auth, obj=source_obj, action_text="发布")

        publish_payload = AiAgentPublishSchema.model_validate(data)
        publish_name = str(publish_payload.name or "").strip()
        publish_type = str(publish_payload.type or source_obj.type or "").strip()
        if not publish_name:
            raise CustomException(msg="发布名称不能为空")
        if not publish_type:
            raise CustomException(msg="智能体类型不能为空")

        async def ensure_public_name_available(name: str, exclude_id: int | None = None) -> None:
            search = {
                "name": ("eq", name),
                "visibility_scope": cls._VISIBILITY_PUBLIC,
                "publish_status": ("!=", cls._PUBLISH_OFFLINE),
            }
            if exclude_id is not None:
                search["id"] = ("!=", exclude_id)
            duplicated = await AiAgentCRUD(auth).list_ai_agent_crud(
                search=search,
                order_by=[{"id": "asc"}],
                preload=[],
            )
            if duplicated:
                raise CustomException(msg=f"已存在同名广场智能体: {name}")

        if source_obj.public_agent_id and source_obj.publish_status != cls._PUBLISH_CLONE:
            public_obj = await AiAgentCRUD(auth).get_by_id_ai_agent_crud(id=int(source_obj.public_agent_id))
            if not public_obj:
                raise CustomException(msg="发布失败，关联的公用智能体不存在")

            await ensure_public_name_available(name=publish_name, exclude_id=int(public_obj.id))
            public_obj = await AiAgentCRUD(auth).update_ai_agent_crud(
                id=int(public_obj.id),
                data=AiAgentPersistSchema(
                    status=source_obj.status,
                    name=publish_name,
                    description=publish_payload.description,
                    type=publish_type,
                    visibility_scope=cls._VISIBILITY_PUBLIC,
                    publish_status=cls._PUBLISH_PUBLISHED,
                    version_no=int(public_obj.version_no) + 1,
                    public_agent_id=0,
                    config=source_obj.config,
                    prompt_template=source_obj.prompt_template,
                    model=source_obj.model,
                    cover=source_obj.cover,
                ),
            )
            await AiAgentAuthService.replace_agent_auth_rules(
                auth=auth,
                agent_id=int(public_obj.id),
                rules=publish_payload.auth_rules,
            )
            await AiAgentCRUD(auth).update_ai_agent_crud(
                id=int(source_obj.id),
                data=AiAgentPersistSchema(
                    status=source_obj.status,
                    name=publish_name,
                    description=publish_payload.description,
                    type=publish_type,
                    visibility_scope=cls._VISIBILITY_PRIVATE,
                    publish_status=cls._PUBLISH_PUBLISHED,
                    version_no=source_obj.version_no,
                    public_agent_id=int(public_obj.id),
                    config=source_obj.config,
                    prompt_template=source_obj.prompt_template,
                    model=source_obj.model,
                    cover=source_obj.cover,
                ),
            )
            result = cls._to_out_schema(public_obj)
            result = await cls._append_single_agent_access(auth=auth, agent=result)
            result["auth_rules"] = await cls._load_detail_auth_rules(auth=auth, obj=public_obj)
            return result

        await ensure_public_name_available(name=publish_name)
        public_obj = await AiAgentCRUD(auth).create_ai_agent_crud(
            data=AiAgentPersistSchema(
                status=source_obj.status,
                name=publish_name,
                description=publish_payload.description,
                type=publish_type,
                visibility_scope=cls._VISIBILITY_PUBLIC,
                publish_status=cls._PUBLISH_PUBLISHED,
                version_no=1,
                public_agent_id=0,
                config=source_obj.config,
                prompt_template=source_obj.prompt_template,
                model=source_obj.model,
                cover=source_obj.cover,
            )
        )
        await AiAgentAuthService.replace_agent_auth_rules(
            auth=auth,
            agent_id=int(public_obj.id),
            rules=publish_payload.auth_rules,
        )
        await AiAgentCRUD(auth).update_ai_agent_crud(
            id=int(source_obj.id),
            data=AiAgentPersistSchema(
                status=source_obj.status,
                name=publish_name,
                description=publish_payload.description,
                type=publish_type,
                visibility_scope=cls._VISIBILITY_PRIVATE,
                publish_status=cls._PUBLISH_PUBLISHED,
                version_no=source_obj.version_no,
                public_agent_id=int(public_obj.id),
                config=source_obj.config,
                prompt_template=source_obj.prompt_template,
                model=source_obj.model,
                cover=source_obj.cover,
            )
        )
        result = cls._to_out_schema(public_obj)
        result = await cls._append_single_agent_access(auth=auth, agent=result)
        result["auth_rules"] = await cls._load_detail_auth_rules(auth=auth, obj=public_obj)
        return result

    @classmethod
    async def manage_ai_agent_service(cls, auth: AuthSchema, id: int, data: AiAgentManageSchema) -> dict:
        obj = await AiAgentCRUD(auth).get_by_id_ai_agent_crud(id=id)
        if not obj:
            raise CustomException(msg="管理失败，该数据不存在")
        if obj.visibility_scope != cls._VISIBILITY_PUBLIC:
            raise CustomException(msg="仅广场智能体允许管理")
        if not (AiAgentAuthService.is_admin_user(auth) or cls._is_owner(auth=auth, obj=obj)):
            raise CustomException(msg="仅发布者或管理员允许管理", code=cls._FORBIDDEN_CODE, status_code=403)

        manage_payload = AiAgentManageSchema.model_validate(data)
        manage_name = str(manage_payload.name or "").strip()
        manage_type = str(manage_payload.type or obj.type or "").strip()
        if not manage_name:
            raise CustomException(msg="智能体名称不能为空")
        if not manage_type:
            raise CustomException(msg="智能体类型不能为空")

        duplicated = await AiAgentCRUD(auth).list_ai_agent_crud(
            search={
                "name": ("eq", manage_name),
                "visibility_scope": cls._VISIBILITY_PUBLIC,
                "publish_status": ("!=", cls._PUBLISH_DELETED),
                "id": ("!=", int(obj.id)),
            },
            order_by=[{"id": "asc"}],
            preload=[],
        )
        if duplicated:
            raise CustomException(msg=f"已存在同名广场智能体: {manage_name}")

        updated_obj = await AiAgentCRUD(auth).update_ai_agent_crud(
            id=id,
            data=AiAgentPersistSchema(
                status=obj.status,
                name=manage_name,
                description=manage_payload.description,
                type=manage_type,
                visibility_scope=obj.visibility_scope,
                publish_status=obj.publish_status,
                version_no=obj.version_no,
                public_agent_id=obj.public_agent_id,
                config=obj.config,
                prompt_template=obj.prompt_template,
                model=obj.model,
                cover=obj.cover,
                order_no=manage_payload.order_no if manage_payload.order_no is not None else obj.order_no,
                score=manage_payload.score if manage_payload.score is not None else obj.score,
                total_usage=manage_payload.total_usage if manage_payload.total_usage is not None else obj.total_usage,
            ),
        )
        await AiAgentAuthService.replace_agent_auth_rules(
            auth=auth,
            agent_id=int(updated_obj.id),
            rules=manage_payload.auth_rules,
        )
        result = cls._to_out_schema(updated_obj)
        result = await cls._append_single_agent_access(auth=auth, agent=result)
        result["auth_rules"] = await cls._load_detail_auth_rules(auth=auth, obj=updated_obj)
        return result

    @classmethod
    async def offline_ai_agent_service(cls, auth: AuthSchema, id: int) -> dict:
        obj = await AiAgentCRUD(auth).get_by_id_ai_agent_crud(id=id)
        if not obj:
            raise CustomException(msg="下线失败，该数据不存在")
        if obj.visibility_scope != cls._VISIBILITY_PUBLIC:
            raise CustomException(msg="仅广场智能体允许下线")
        if not (AiAgentAuthService.is_admin_user(auth) or cls._is_owner(auth=auth, obj=obj)):
            raise CustomException(msg="仅发布者或管理员允许下线", code=cls._FORBIDDEN_CODE, status_code=403)
        if obj.publish_status != cls._PUBLISH_PUBLISHED:
            raise CustomException(msg="仅已发布状态允许下线")

        updated_obj = await AiAgentCRUD(auth).update_ai_agent_crud(
            id=id,
            data=AiAgentPersistSchema(
                status=obj.status,
                name=obj.name,
                description=obj.description,
                type=obj.type,
                visibility_scope=obj.visibility_scope,
                publish_status=cls._PUBLISH_OFFLINE,
                version_no=obj.version_no,
                public_agent_id=obj.public_agent_id,
                config=obj.config,
                prompt_template=obj.prompt_template,
                model=obj.model,
                cover=obj.cover,
            )
        )
        return cls._to_out_schema(updated_obj)

    @classmethod
    async def clone_ai_agent_service(cls, auth: AuthSchema, id: int) -> dict:
        source_obj = await AiAgentCRUD(auth).get_by_id_ai_agent_crud(id=id)
        if not source_obj:
            raise CustomException(msg="克隆失败，该数据不存在")
        if source_obj.visibility_scope != cls._VISIBILITY_PUBLIC or source_obj.publish_status != cls._PUBLISH_PUBLISHED:
            raise CustomException(msg="仅已发布广场智能体允许克隆")

        if not (AiAgentAuthService.is_admin_user(auth) or cls._is_owner(auth=auth, obj=source_obj)):
            current_right = await AiAgentAuthService.resolve_agent_right(auth=auth, agent_id=int(source_obj.id))
            if current_right < 2:
                raise CustomException(msg="无权限克隆该智能体", code=cls._FORBIDDEN_CODE, status_code=403)

        fork_obj = await AiAgentCRUD(auth).create_ai_agent_crud(
            data=AiAgentPersistSchema(
                status=source_obj.status,
                name=source_obj.name + "_副本",
                description=source_obj.description,
                type=source_obj.type,
                visibility_scope=cls._VISIBILITY_PRIVATE,
                publish_status=cls._PUBLISH_PUBLISHED,
                version_no=source_obj.version_no,
                public_agent_id=source_obj.id,
                config=source_obj.config,
                prompt_template=source_obj.prompt_template,
                model=source_obj.model,
                cover=source_obj.cover,
            )
        )
        fork_result = cls._to_out_schema(fork_obj)
        return await cls._append_single_agent_access(auth=auth, agent=fork_result)

    @classmethod
    async def delete_private_ai_agent_service(cls, auth: AuthSchema, id: int) -> None:
        obj = await AiAgentCRUD(auth).get_by_id_ai_agent_crud(id=id)
        if not obj:
            raise CustomException(msg="删除失败，该数据不存在")
        cls._ensure_private_owner(auth=auth, obj=obj, action_text="删除")

        await AiAgentCRUD(auth).update_ai_agent_crud(
            id=id,
            data=AiAgentPersistSchema(
                status="1",
                name=obj.name,
                description=obj.description,
                type=obj.type,
                visibility_scope=obj.visibility_scope,
                publish_status=cls._PUBLISH_DELETED,
                version_no=obj.version_no,
                public_agent_id=obj.public_agent_id,
                config=obj.config,
                prompt_template=obj.prompt_template,
                model=obj.model,
                cover=obj.cover,
            )
        )

    @classmethod
    async def delete_ai_agent_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await AiAgentCRUD(auth).get_by_id_ai_agent_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
        await AiAgentCRUD(auth).delete_ai_agent_crud(ids=ids)

    @classmethod
    async def set_available_ai_agent_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        await AiAgentCRUD(auth).set_available_ai_agent_crud(ids=data.ids, status=data.status)

    @classmethod
    async def batch_export_ai_agent_service(cls, obj_list: list[dict]) -> bytes:
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
            'name': '智能体名称',
            'type': '智能体类型',
            'config': '智能体配置',
            'prompt_template': '提示词模板',
            'model': '模型配置',
            'cover': '封面图片URL',
            'total_usage': '使用次数',
            'score': '智能体评分',
            'order_no': '排序号',
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
    async def batch_import_ai_agent_service(cls, auth: AuthSchema, file: UploadFile,
                                            update_support: bool = False) -> str:
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
            '智能体名称': 'name',
            '智能体类型': 'type',
            '智能体配置': 'config',
            '提示词模板': 'prompt_template',
            '模型配置': 'model',
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

            error_msgs = []
            success_count = 0
            count = 0

            for index, row in df.iterrows():
                count += 1
                try:
                    # 处理nan值，转换为None或空字符串
                    def handle_nan(value):
                        import math
                        if isinstance(value, float) and math.isnan(value):
                            return ""
                        return value
                    
                    # 处理状态字段，将文字转换为数字
                    def handle_status(status):
                        if status == "启用":
                            return "0"
                        elif status == "停用":
                            return "1"
                        return status
                    
                    data = {
                        "id": row['id'],
                        "uuid": row['uuid'],
                        "status": handle_status(row['status']),
                        "description": handle_nan(row['description']),
                        "created_time": row['created_time'],
                        "updated_time": row['updated_time'],
                        "created_id": row['created_id'],
                        "updated_id": row['updated_id'],
                        "name": row['name'],
                        "type": row['type'],
                        "config": handle_nan(row['config']),
                        "prompt_template": handle_nan(row['prompt_template']),
                        "model": handle_nan(row['model']),
                        "cover": handle_nan(row['cover']),
                    }
                    create_schema = AiAgentCreateSchema.model_validate(data)
                    await AiAgentCRUD(auth).create_ai_agent_crud(
                        data=AiAgentPersistSchema(
                            status=create_schema.status,
                            name=create_schema.name,
                            description=create_schema.description,
                            type=create_schema.type,
                            visibility_scope=cls._VISIBILITY_PRIVATE,
                            publish_status=cls._PUBLISH_DRAFT,
                            version_no=1,
                            public_agent_id=0,
                            config=create_schema.config,
                            prompt_template=create_schema.prompt_template,
                            model=create_schema.model,
                            cover=create_schema.cover,
                        )
                    )
                    success_count += 1
                except Exception as e:
                    error_msg = f"第{count}行: {str(e)}"
                    error_msgs.append(error_msg)
                    log.error(error_msg)
                    continue

            result = f"成功导入 {success_count} 条数据"
            if error_msgs:
                result += "\n错误信息:\n" + "\n".join(error_msgs)
            return result

        except Exception as e:
            log.error(f"批量导入失败: {str(e)}")
            raise CustomException(msg=f"导入失败: {str(e)}")

    @classmethod
    async def import_template_download_ai_agent_service(cls) -> bytes:
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
            '智能体名称',
            '智能体类型',
            '智能体配置',
            '提示词模板',
            '模型配置',
            '封面图片URL',
        ]
        selector_header_list = []
        option_list = []

        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list
        )
