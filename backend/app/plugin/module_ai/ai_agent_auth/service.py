# -*- coding: utf-8 -*-

from sqlalchemy import and_, or_, select

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.role.model import RoleModel
from app.api.v1.module_system.user.model import UserModel
from .crud import AiAgentAuthCRUD
from .model import AiAgentAuthModel
from .schema import AiAgentAuthCreateSchema, AiAgentAuthRuleOutSchema, AiAgentAuthRuleSchema


class AiAgentAuthService:
    _TARGET_GLOBAL = "global"
    _TARGET_ROLE = "role"
    _TARGET_USER = "user"

    @staticmethod
    def is_admin_user(auth: AuthSchema) -> bool:
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

    @staticmethod
    def get_current_user_id(auth: AuthSchema) -> int:
        return int(getattr(auth.user, "id", 0) or 0)

    @staticmethod
    def get_current_role_ids(auth: AuthSchema) -> list[int]:
        return sorted(
            {
                int(role.id)
                for role in (auth.user.roles or [])
                if role and getattr(role, "id", None) is not None and getattr(role, "status", None) == "0"
            }
        )

    @classmethod
    def build_match_clause(cls, auth: AuthSchema, min_right: int):
        clauses = [
            and_(
                AiAgentAuthModel.target_type == cls._TARGET_GLOBAL,
                AiAgentAuthModel.target_right >= min_right,
            )
        ]

        role_ids = cls.get_current_role_ids(auth)
        if role_ids:
            clauses.append(
                and_(
                    AiAgentAuthModel.target_type == cls._TARGET_ROLE,
                    AiAgentAuthModel.target_value.in_([str(role_id) for role_id in role_ids]),
                    AiAgentAuthModel.target_right >= min_right,
                )
            )

        current_user_id = cls.get_current_user_id(auth)
        if current_user_id:
            clauses.append(
                and_(
                    AiAgentAuthModel.target_type == cls._TARGET_USER,
                    AiAgentAuthModel.target_value == str(current_user_id),
                    AiAgentAuthModel.target_right >= min_right,
                )
            )

        return or_(*clauses)

    @classmethod
    async def resolve_agent_right_map(cls, auth: AuthSchema, agent_ids: list[int]) -> dict[int, int]:
        if not agent_ids:
            return {}

        if cls.is_admin_user(auth):
            return {int(agent_id): 2 for agent_id in sorted(set(agent_ids))}

        sql = (
            select(
                AiAgentAuthModel.agent_id,
                AiAgentAuthModel.target_right,
            )
            .where(AiAgentAuthModel.agent_id.in_(sorted(set(agent_ids))))
            .where(cls.build_match_clause(auth=auth, min_right=1))
        )
        result = await auth.db.execute(sql)
        right_map: dict[int, int] = {}
        for agent_id, target_right in result.all():
            agent_id_int = int(agent_id)
            right_map[agent_id_int] = max(int(target_right or 0), right_map.get(agent_id_int, 0))
        return right_map

    @classmethod
    async def resolve_agent_right(cls, auth: AuthSchema, agent_id: int) -> int:
        right_map = await cls.resolve_agent_right_map(auth=auth, agent_ids=[agent_id])
        return int(right_map.get(int(agent_id), 0))

    @classmethod
    def normalize_rules(cls, rules: list[AiAgentAuthRuleSchema] | None) -> list[AiAgentAuthRuleSchema]:
        dedup_rules: dict[tuple[str, str | None], AiAgentAuthRuleSchema] = {}
        for item in rules or []:
            rule = item if isinstance(item, AiAgentAuthRuleSchema) else AiAgentAuthRuleSchema.model_validate(item)
            key = (rule.target_type, rule.target_value)
            existed = dedup_rules.get(key)
            if existed is None or rule.target_right > existed.target_right:
                dedup_rules[key] = rule
        return list(dedup_rules.values())

    @classmethod
    async def replace_agent_auth_rules(
            cls,
            auth: AuthSchema,
            agent_id: int,
            rules: list[AiAgentAuthRuleSchema] | None,
    ) -> list[AiAgentAuthRuleOutSchema]:
        normalized_rules = cls.normalize_rules(rules=rules)
        crud = AiAgentAuthCRUD(auth)
        await crud.delete_by_agent_id_ai_agent_auth_crud(agent_id=agent_id)

        current_user_id = cls.get_current_user_id(auth)
        for rule in normalized_rules:
            await crud.create_ai_agent_auth_crud(
                AiAgentAuthCreateSchema(
                    agent_id=agent_id,
                    target_type=rule.target_type,
                    target_value=rule.target_value,
                    target_right=rule.target_right,
                    granted_by=current_user_id,
                )
            )

        return await cls.list_agent_auth_rules(auth=auth, agent_id=agent_id)

    @classmethod
    async def list_agent_auth_rules(cls, auth: AuthSchema, agent_id: int) -> list[AiAgentAuthRuleOutSchema]:
        rules = await AiAgentAuthCRUD(auth).list_ai_agent_auth_crud(
            search={"agent_id": agent_id},
            order_by=[{"target_type": "asc"}, {"target_value": "asc"}, {"id": "asc"}],
        )
        if not rules:
            return []

        role_ids = {int(rule.target_value) for rule in rules if
                    rule.target_type == cls._TARGET_ROLE and rule.target_value}
        user_ids = {int(rule.target_value) for rule in rules if
                    rule.target_type == cls._TARGET_USER and rule.target_value}

        role_name_map: dict[int, str] = {}
        user_name_map: dict[int, str] = {}
        if role_ids:
            role_rows = await auth.db.execute(
                select(RoleModel.id, RoleModel.name).where(RoleModel.id.in_(sorted(role_ids))))
            role_name_map = {int(role_id): str(name) for role_id, name in role_rows.all()}
        if user_ids:
            user_rows = await auth.db.execute(
                select(UserModel.id, UserModel.name).where(UserModel.id.in_(sorted(user_ids))))
            user_name_map = {int(user_id): str(name) for user_id, name in user_rows.all()}

        result: list[AiAgentAuthRuleOutSchema] = []
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
                AiAgentAuthRuleOutSchema(
                    id=int(rule.id),
                    target_type=str(rule.target_type),
                    target_value=rule.target_value,
                    target_label=target_label,
                    target_right=int(rule.target_right),
                    granted_by=int(rule.granted_by),
                    granted_at=rule.granted_at.strftime("%Y-%m-%d %H:%M:%S") if rule.granted_at else None,
                )
            )
        return result
