# -*- coding: utf-8 -*-

from sqlalchemy import and_, or_, select

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.role.model import RoleModel
from app.api.v1.module_system.user.model import UserModel
from app.core.exceptions import CustomException
from app.plugin.module_ai.ai_agent_auth.service import AiAgentAuthService
from .crud import AiDatasetAuthCRUD
from .model import AiDatasetAuthModel
from .schema import (
    AiDatasetAuthCreateSchema,
    AiDatasetAuthRuleOutSchema,
    AiDatasetAuthRuleSchema,
)


class AiDatasetAuthService:
    _TARGET_GLOBAL = "global"
    _TARGET_ROLE = "role"
    _TARGET_USER = "user"
    _DEFAULT_RIGHT = 0

    @staticmethod
    def is_admin_user(auth: AuthSchema) -> bool:
        return AiAgentAuthService.is_admin_user(auth)

    @staticmethod
    def get_current_user_id(auth: AuthSchema) -> int:
        return AiAgentAuthService.get_current_user_id(auth)

    @staticmethod
    def get_current_role_ids(auth: AuthSchema) -> list[int]:
        return AiAgentAuthService.get_current_role_ids(auth)

    @staticmethod
    def _normalize_dataset_id(dataset_id: str | None) -> str:
        return str(dataset_id or "").strip()

    @classmethod
    def build_match_clause(cls, auth: AuthSchema, min_right: int):
        clauses = [
            and_(
                AiDatasetAuthModel.target_type == cls._TARGET_GLOBAL,
                AiDatasetAuthModel.target_right >= min_right,
            )
        ]

        role_ids = cls.get_current_role_ids(auth)
        if role_ids:
            clauses.append(
                and_(
                    AiDatasetAuthModel.target_type == cls._TARGET_ROLE,
                    AiDatasetAuthModel.target_value.in_([str(role_id) for role_id in role_ids]),
                    AiDatasetAuthModel.target_right >= min_right,
                )
            )

        current_user_id = cls.get_current_user_id(auth)
        if current_user_id:
            clauses.append(
                and_(
                    AiDatasetAuthModel.target_type == cls._TARGET_USER,
                    AiDatasetAuthModel.target_value == str(current_user_id),
                    AiDatasetAuthModel.target_right >= min_right,
                )
            )

        return or_(*clauses)

    @classmethod
    async def resolve_dataset_right_map(cls, auth: AuthSchema, dataset_ids: list[str]) -> dict[str, int]:
        normalized_ids = [
            dataset_id
            for dataset_id in {cls._normalize_dataset_id(item) for item in dataset_ids}
            if dataset_id
        ]
        if not normalized_ids:
            return {}

        if cls.is_admin_user(auth):
            return {dataset_id: 2 for dataset_id in normalized_ids}

        configured_rows = await auth.db.execute(
            select(AiDatasetAuthModel.dataset_id).where(AiDatasetAuthModel.dataset_id.in_(normalized_ids))
        )
        configured_ids = {cls._normalize_dataset_id(dataset_id) for dataset_id in configured_rows.scalars().all() if
                          dataset_id}

        right_map: dict[str, int] = {
            dataset_id: cls._DEFAULT_RIGHT
            for dataset_id in normalized_ids
            if dataset_id not in configured_ids
        }

        if configured_ids:
            sql = (
                select(
                    AiDatasetAuthModel.dataset_id,
                    AiDatasetAuthModel.target_right,
                )
                .where(AiDatasetAuthModel.dataset_id.in_(sorted(configured_ids)))
                .where(cls.build_match_clause(auth=auth, min_right=1))
            )
            result = await auth.db.execute(sql)
            for dataset_id, target_right in result.all():
                normalized_dataset_id = cls._normalize_dataset_id(dataset_id)
                right_map[normalized_dataset_id] = max(
                    int(target_right or 0),
                    right_map.get(normalized_dataset_id, 0),
                )

        return right_map

    @classmethod
    async def resolve_dataset_right(cls, auth: AuthSchema, dataset_id: str) -> int:
        normalized_dataset_id = cls._normalize_dataset_id(dataset_id)
        if not normalized_dataset_id:
            return 0
        right_map = await cls.resolve_dataset_right_map(auth=auth, dataset_ids=[normalized_dataset_id])
        return int(right_map.get(normalized_dataset_id, 0))

    @classmethod
    async def has_dataset_auth_rules(cls, auth: AuthSchema, dataset_id: str) -> bool:
        normalized_dataset_id = cls._normalize_dataset_id(dataset_id)
        if not normalized_dataset_id:
            return False

        result = await auth.db.execute(
            select(AiDatasetAuthModel.id).where(AiDatasetAuthModel.dataset_id == normalized_dataset_id).limit(1)
        )
        return result.scalar() is not None

    @classmethod
    def normalize_rules(cls, rules: list[AiDatasetAuthRuleSchema] | None) -> list[AiDatasetAuthRuleSchema]:
        dedup_rules: dict[tuple[str, str | None], AiDatasetAuthRuleSchema] = {}
        for item in rules or []:
            rule = item if isinstance(item, AiDatasetAuthRuleSchema) else AiDatasetAuthRuleSchema.model_validate(item)
            key = (rule.target_type, rule.target_value)
            existed = dedup_rules.get(key)
            if existed is None or rule.target_right > existed.target_right:
                dedup_rules[key] = rule
        return list(dedup_rules.values())

    @classmethod
    async def create_creator_rule(cls, auth: AuthSchema, dataset_id: str) -> list[AiDatasetAuthRuleOutSchema]:
        current_user_id = cls.get_current_user_id(auth)
        if current_user_id <= 0:
            return []

        return await cls.replace_dataset_auth_rules(
            auth=auth,
            dataset_id=dataset_id,
            rules=[
                AiDatasetAuthRuleSchema(
                    target_type=cls._TARGET_USER,
                    target_value=str(current_user_id),
                    target_right=2,
                )
            ],
        )

    @classmethod
    async def ensure_dataset_read_permission(cls, auth: AuthSchema, dataset_id: str) -> int:
        right = await cls.resolve_dataset_right(auth=auth, dataset_id=dataset_id)
        if right < 1:
            raise CustomException(msg="无权限访问该知识库", status_code=403)
        return right

    @classmethod
    async def ensure_dataset_write_permission(cls, auth: AuthSchema, dataset_id: str) -> int:
        right = await cls.resolve_dataset_right(auth=auth, dataset_id=dataset_id)
        if right < 2:
            raise CustomException(msg="无权限修改该知识库", status_code=403)
        return right

    @classmethod
    async def replace_dataset_auth_rules(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            rules: list[AiDatasetAuthRuleSchema] | None,
    ) -> list[AiDatasetAuthRuleOutSchema]:
        normalized_dataset_id = cls._normalize_dataset_id(dataset_id)
        if not normalized_dataset_id:
            raise CustomException(msg="知识库ID不能为空", status_code=400)

        normalized_rules = cls.normalize_rules(rules=rules)
        if not normalized_rules:
            raise CustomException(msg="至少保留一条授权规则", status_code=400)

        crud = AiDatasetAuthCRUD(auth)
        await crud.delete_by_dataset_id_ai_dataset_auth_crud(dataset_id=normalized_dataset_id)

        current_user_id = cls.get_current_user_id(auth)
        for rule in normalized_rules:
            await crud.create_ai_dataset_auth_crud(
                AiDatasetAuthCreateSchema(
                    dataset_id=normalized_dataset_id,
                    target_type=rule.target_type,
                    target_value=rule.target_value,
                    target_right=rule.target_right,
                    granted_by=current_user_id,
                )
            )

        return await cls.list_dataset_auth_rules(
            auth=auth,
            dataset_id=normalized_dataset_id,
            include_default=False,
        )

    @classmethod
    async def list_dataset_auth_rules(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            include_default: bool = True,
    ) -> list[AiDatasetAuthRuleOutSchema]:
        normalized_dataset_id = cls._normalize_dataset_id(dataset_id)
        if not normalized_dataset_id:
            return []

        rules = await AiDatasetAuthCRUD(auth).list_ai_dataset_auth_crud(
            search={"dataset_id": normalized_dataset_id},
            order_by=[{"target_type": "asc"}, {"target_value": "asc"}, {"id": "asc"}],
        )
        if not rules:
            return []

        role_ids = {
            int(rule.target_value)
            for rule in rules
            if rule.target_type == cls._TARGET_ROLE and rule.target_value
        }
        user_ids = {
            int(rule.target_value)
            for rule in rules
            if rule.target_type == cls._TARGET_USER and rule.target_value
        }

        role_name_map: dict[int, str] = {}
        user_name_map: dict[int, str] = {}
        if role_ids:
            role_rows = await auth.db.execute(
                select(RoleModel.id, RoleModel.name).where(RoleModel.id.in_(sorted(role_ids)))
            )
            role_name_map = {int(role_id): str(name) for role_id, name in role_rows.all()}
        if user_ids:
            user_rows = await auth.db.execute(
                select(UserModel.id, UserModel.name).where(UserModel.id.in_(sorted(user_ids)))
            )
            user_name_map = {int(user_id): str(name) for user_id, name in user_rows.all()}

        result: list[AiDatasetAuthRuleOutSchema] = []
        for rule in rules:
            target_label: str | None
            if rule.target_type == cls._TARGET_GLOBAL:
                target_label = "所有人"
            elif rule.target_type == cls._TARGET_ROLE and rule.target_value:
                target_label = role_name_map.get(int(rule.target_value), rule.target_value)
            elif rule.target_type == cls._TARGET_USER and rule.target_value:
                target_label = user_name_map.get(int(rule.target_value), rule.target_value)
            else:
                target_label = rule.target_value

            result.append(
                AiDatasetAuthRuleOutSchema(
                    id=int(rule.id),
                    target_type=str(rule.target_type),
                    target_value=rule.target_value,
                    target_label=target_label,
                    target_right=int(rule.target_right),
                    granted_by=int(rule.granted_by),
                    granted_at=rule.granted_at.strftime("%Y-%m-%d %H:%M:%S") if rule.granted_at else None,
                    is_default=False,
                )
            )
        return result

    @classmethod
    async def delete_dataset_auth_rules_by_dataset_ids(cls, auth: AuthSchema, dataset_ids: list[str]) -> None:
        normalized_ids = [
            dataset_id
            for dataset_id in {cls._normalize_dataset_id(item) for item in dataset_ids}
            if dataset_id
        ]
        if not normalized_ids:
            return

        await AiDatasetAuthCRUD(auth).delete_by_dataset_ids_ai_dataset_auth_crud(dataset_ids=normalized_ids)
