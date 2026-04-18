# -*- coding: utf-8 -*-
"""
Token消耗统计Service层
"""
import datetime
from collections import defaultdict
from sqlalchemy import func, select, and_
from app.api.v1.module_system.auth.schema import AuthSchema
from app.plugin.module_ai.ai_chat.model import AiChatModel
from .schema import (
    DeptTokenRankOut, AgentTokenRankOut, UserTokenRankOut,
    TokenTrendOut, UserTokenDetailOut, TokenOverviewOut, ChatTrendOut, ModelConsumptionOut,
    DeptTokenRankItem, AgentTokenRankItem, UserTokenRankItem,
    TokenTrendItem, UserTokenDetailItem, ChatTrendItem, ModelConsumptionItem
)


class AiChatTokenStatsService:
    """
    Token消耗统计服务层
    """

    @classmethod
    def _get_time_range(
        cls,
        time_range: str,
        start_date: str | None = None,
        end_date: str | None = None
    ) -> tuple[datetime.datetime, datetime.datetime]:
        """获取时间范围"""
        # 如果提供了自定义日期范围，优先使用
        if start_date and end_date:
            try:
                start_time = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                # 结束日期设置为当天的23:59:59
                end_time = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                end_time = end_time.replace(hour=23, minute=59, second=59)
                return start_time, end_time
            except ValueError:
                pass
        
        # 否则使用预设的时间范围
        now = datetime.datetime.now()
        if time_range == "day":
            start_time = now - datetime.timedelta(days=1)
        elif time_range == "week":
            start_time = now - datetime.timedelta(weeks=1)
        elif time_range == "month":
            start_time = now - datetime.timedelta(days=30)
        else:
            start_time = now - datetime.timedelta(weeks=1)
        return start_time, now

    @classmethod
    async def get_dept_token_rank_service(
        cls,
        auth: AuthSchema,
        time_range: str,
        start_date: str | None,
        end_date: str | None,
        page_no: int,
        page_size: int
    ) -> DeptTokenRankOut:
        """获取部门Token消耗排名"""
        from app.api.v1.module_system.dept.crud import DeptCRUD
        from app.api.v1.module_system.user.crud import UserCRUD
        
        start_time, end_time = cls._get_time_range(time_range, start_date, end_date)
        
        # 获取所有部门
        dept_list = await DeptCRUD(auth).get_list_crud()
        dept_map = {dept.id: dept for dept in dept_list}
        
        # 获取所有用户
        user_list = await UserCRUD(auth).get_list_crud()
        user_dept_map = {user.id: user.dept_id for user in user_list if hasattr(user, 'dept_id')}
        
        # 查询Token消耗
        async with auth.db as session:
            result = await session.execute(
                select(
                    AiChatModel.user_id,
                    AiChatModel.model_id,
                    AiChatModel.provider_id,
                    func.sum(AiChatModel.tokens).label('total_tokens')
                ).where(
                    and_(
                        AiChatModel.created_time >= start_time,
                        AiChatModel.created_time <= end_time
                    )
                ).group_by(
                    AiChatModel.user_id,
                    AiChatModel.model_id,
                    AiChatModel.provider_id
                )
            )
            rows = result.all()
        
        # 按部门汇总
        dept_stats = defaultdict(lambda: {'total_tokens': 0, 'models': defaultdict(int)})
        for row in rows:
            user_id = row.user_id
            dept_id = user_dept_map.get(user_id, 0)
            # dept_id为0表示未分配部门
            dept_stats[dept_id]['total_tokens'] += row.total_tokens or 0
            model_key = f"{row.provider_id}/{row.model_id}" if row.provider_id and row.model_id else "未知模型"
            dept_stats[dept_id]['models'][model_key] += row.total_tokens or 0
        
        # 构建响应数据
        items = []
        for dept_id, stats in sorted(dept_stats.items(), key=lambda x: x[1]['total_tokens'], reverse=True):
            if dept_id == 0:
                dept_name = "未分配部门"
            else:
                dept = dept_map.get(dept_id)
                dept_name = dept.name if dept and hasattr(dept, 'name') else f"部门{dept_id}"
            
            model_distribution = [
                {'model': model, 'tokens': tokens}
                for model, tokens in stats['models'].items()
            ]
            items.append(DeptTokenRankItem(
                dept_id=dept_id,
                dept_name=dept_name,
                total_tokens=stats['total_tokens'],
                model_distribution=model_distribution
            ))
        
        total = len(items)
        # 分页
        start = (page_no - 1) * page_size
        end = start + page_size
        items = items[start:end]
        
        return DeptTokenRankOut(items=items, total=total)

    @classmethod
    async def get_agent_token_rank_service(
        cls,
        auth: AuthSchema,
        time_range: str,
        start_date: str | None,
        end_date: str | None,
        dept_id: int | None,
        position_id: int | None,
        page_no: int,
        page_size: int
    ) -> AgentTokenRankOut:
        """获取智能体Token消耗排名"""
        from app.plugin.module_ai.ai_agent.crud import AiAgentCRUD
        from app.api.v1.module_system.user.crud import UserCRUD
        from app.api.v1.module_system.position.crud import PositionCRUD
        
        start_time, end_time = cls._get_time_range(time_range, start_date, end_date)
        
        # 获取所有智能体
        agent_list = await AiAgentCRUD(auth).list_ai_agent_crud()
        agent_map = {agent.id: agent for agent in agent_list}
        
        # 获取所有岗位
        position_list = await PositionCRUD(auth).get_list_crud()
        position_map = {pos.id: pos for pos in position_list}
        
        # 获取用户信息用于过滤
        user_list = await UserCRUD(auth).get_list_crud()
        
        # 构建用户-岗位映射（从positions关系中获取）
        user_position_map = {}
        for user in user_list:
            user_position_map[user.id] = set()
            if hasattr(user, 'positions') and user.positions:
                for pos in user.positions:
                    user_position_map[user.id].add(pos.id)
        
        user_filter_map = {}
        for user in user_list:
            dept_match = dept_id is None or (hasattr(user, 'dept_id') and user.dept_id == dept_id)
            position_match = position_id is None or (position_id in user_position_map.get(user.id, set()))
            if dept_match and position_match:
                user_filter_map[user.id] = user
        
        # 查询Token消耗（包含agent_id为0的记录）
        async with auth.db as session:
            query = select(
                AiChatModel.agent_id,
                AiChatModel.user_id,
                func.sum(AiChatModel.tokens).label('total_tokens')
            ).where(
                and_(
                    AiChatModel.created_time >= start_time,
                    AiChatModel.created_time <= end_time
                )
            ).group_by(
                AiChatModel.agent_id,
                AiChatModel.user_id
            )
            
            result = await session.execute(query)
            rows = result.all()
        
        # 按智能体汇总（包含岗位分布）
        agent_stats = defaultdict(lambda: {'total_tokens': 0, 'users': set(), 'positions': defaultdict(int)})
        for row in rows:
            if row.user_id in user_filter_map:
                # agent_id为0表示未指定智能体（通用对话）
                agent_id = row.agent_id if row.agent_id > 0 else 0
                agent_stats[agent_id]['total_tokens'] += row.total_tokens or 0
                agent_stats[agent_id]['users'].add(row.user_id)
                # 统计岗位分布
                user_pos_ids = user_position_map.get(row.user_id, set())
                for pos_id in user_pos_ids:
                    agent_stats[agent_id]['positions'][pos_id] += row.total_tokens or 0
        
        # 构建响应数据
        items = []
        for agent_id, stats in sorted(agent_stats.items(), key=lambda x: x[1]['total_tokens'], reverse=True):
            if agent_id == 0:
                # 未指定智能体的记录
                agent_name = "通用对话（未指定智能体）"
            else:
                agent = agent_map.get(agent_id)
                agent_name = agent.name if agent and hasattr(agent, 'name') else f"智能体{agent_id}"
            
            # 构建岗位分布
            position_distribution = []
            for pos_id, tokens in stats['positions'].items():
                pos = position_map.get(pos_id)
                if pos:
                    position_distribution.append({
                        'position': pos.name if hasattr(pos, 'name') else str(pos_id),
                        'tokens': tokens
                    })
            position_distribution.sort(key=lambda x: x['tokens'], reverse=True)
            
            items.append(AgentTokenRankItem(
                agent_id=agent_id,
                agent_name=agent_name,
                total_tokens=stats['total_tokens'],
                user_count=len(stats['users']),
                position_distribution=position_distribution
            ))
        
        total = len(items)
        start = (page_no - 1) * page_size
        end = start + page_size
        items = items[start:end]
        
        return AgentTokenRankOut(items=items, total=total)

    @classmethod
    async def get_user_token_rank_service(
        cls,
        auth: AuthSchema,
        time_range: str,
        start_date: str | None,
        end_date: str | None,
        dept_id: int | None,
        position_id: int | None,
        page_no: int,
        page_size: int
    ) -> UserTokenRankOut:
        """获取人员Token消耗排名"""
        from app.api.v1.module_system.user.crud import UserCRUD
        from app.api.v1.module_system.dept.crud import DeptCRUD
        from app.api.v1.module_system.position.crud import PositionCRUD
        
        start_time, end_time = cls._get_time_range(time_range, start_date, end_date)
        
        # 获取所有用户、部门和岗位
        user_list = await UserCRUD(auth).get_list_crud()
        dept_list = await DeptCRUD(auth).get_list_crud()
        position_list = await PositionCRUD(auth).get_list_crud()
        
        dept_map = {dept.id: dept for dept in dept_list}
        position_map = {pos.id: pos for pos in position_list}
        
        # 构建用户-岗位映射（从positions关系中获取）
        user_position_map = {}
        for user in user_list:
            user_position_map[user.id] = set()
            if hasattr(user, 'positions') and user.positions:
                for pos in user.positions:
                    user_position_map[user.id].add(pos.id)
        
        # 过滤用户
        user_filter_map = {}
        for user in user_list:
            dept_match = dept_id is None or (hasattr(user, 'dept_id') and user.dept_id == dept_id)
            position_match = position_id is None or (position_id in user_position_map.get(user.id, set()))
            if dept_match and position_match:
                user_filter_map[user.id] = user
        
        # 查询Token消耗
        async with auth.db as session:
            result = await session.execute(
                select(
                    AiChatModel.user_id,
                    AiChatModel.agent_id,
                    func.sum(AiChatModel.tokens).label('total_tokens')
                ).where(
                    and_(
                        AiChatModel.created_time >= start_time,
                        AiChatModel.created_time <= end_time,
                        AiChatModel.user_id.in_(list(user_filter_map.keys())) if user_filter_map else True
                    )
                ).group_by(
                    AiChatModel.user_id,
                    AiChatModel.agent_id
                )
            )
            rows = result.all()
        
        # 按用户汇总（包含岗位分布）
        user_stats = defaultdict(lambda: {'total_tokens': 0, 'agents': set(), 'positions': defaultdict(int)})
        for row in rows:
            user_stats[row.user_id]['total_tokens'] += row.total_tokens or 0
            user_stats[row.user_id]['agents'].add(row.agent_id)
            # 统计岗位分布
            user_pos_ids = user_position_map.get(row.user_id, set())
            for pos_id in user_pos_ids:
                user_stats[row.user_id]['positions'][pos_id] += row.total_tokens or 0
        
        # 构建响应数据
        items = []
        for user_id, stats in sorted(user_stats.items(), key=lambda x: x[1]['total_tokens'], reverse=True):
            user = user_filter_map.get(user_id)
            if user:
                dept = dept_map.get(user.dept_id if hasattr(user, 'dept_id') else 0)
                # 获取用户的第一个岗位名称（用户可能有多个岗位）
                user_positions = user_position_map.get(user_id, set())
                position_name = ''
                if user_positions:
                    first_position_id = list(user_positions)[0]
                    position = position_map.get(first_position_id)
                    position_name = position.name if position and hasattr(position, 'name') else ''
                
                # 构建岗位分布
                position_distribution = []
                for pos_id, tokens in stats['positions'].items():
                    pos = position_map.get(pos_id)
                    if pos:
                        position_distribution.append({
                            'position': pos.name if hasattr(pos, 'name') else str(pos_id),
                            'tokens': tokens
                        })
                position_distribution.sort(key=lambda x: x['tokens'], reverse=True)
                
                items.append(UserTokenRankItem(
                    user_id=user_id,
                    user_name=user.name if hasattr(user, 'name') else str(user_id),
                    dept_name=dept.name if dept and hasattr(dept, 'name') else '',
                    position_name=position_name,
                    total_tokens=stats['total_tokens'],
                    agent_count=len(stats['agents']),
                    position_distribution=position_distribution
                ))
        
        total = len(items)
        start = (page_no - 1) * page_size
        end = start + page_size
        items = items[start:end]
        
        return UserTokenRankOut(items=items, total=total)

    @classmethod
    async def get_token_trend_service(
        cls,
        auth: AuthSchema,
        time_range: str,
        start_date: str | None,
        end_date: str | None,
        dept_id: int | None,
        user_id: int | None
    ) -> TokenTrendOut:
        """获取Token消耗趋势"""
        from app.api.v1.module_system.user.crud import UserCRUD
        
        start_time, end_time = cls._get_time_range(time_range, start_date, end_date)
        
        # 确定时间粒度
        if time_range == "day":
            date_format = "%Y-%m-%d %H:00"
            group_format = "%Y-%m-%d %H"
        elif time_range == "week":
            date_format = "%Y-%m-%d"
            group_format = "%Y-%m-%d"
        else:  # month
            date_format = "%Y-%m-%d"
            group_format = "%Y-%m-%d"
        
        # 构建查询条件
        conditions = [
            AiChatModel.created_time >= start_time,
            AiChatModel.created_time <= end_time
        ]
        
        if user_id:
            conditions.append(AiChatModel.user_id == user_id)
        elif dept_id:
            # 获取部门下所有用户
            user_list = await UserCRUD(auth).get_list_crud()
            dept_user_ids = [u.id for u in user_list if hasattr(u, 'dept_id') and u.dept_id == dept_id]
            if dept_user_ids:
                conditions.append(AiChatModel.user_id.in_(dept_user_ids))
        
        # 查询Token消耗
        async with auth.db as session:
            result = await session.execute(
                select(
                    AiChatModel.created_time,
                    AiChatModel.user_id,
                    func.sum(AiChatModel.tokens).label('total_tokens')
                ).where(
                    and_(*conditions)
                ).group_by(
                    AiChatModel.created_time,
                    AiChatModel.user_id
                ).order_by(AiChatModel.created_time)
            )
            rows = result.all()
        
        # 按日期汇总
        date_stats = defaultdict(lambda: {'total_tokens': 0, 'users': set()})
        for row in rows:
            date_key = row.created_time.strftime(date_format) if isinstance(row.created_time, datetime.datetime) else str(row.created_time)
            date_stats[date_key]['total_tokens'] += row.total_tokens or 0
            date_stats[date_key]['users'].add(row.user_id)
        
        # 生成日期列表（补全缺失日期）
        dates = []
        current = start_time
        while current <= end_time:
            if time_range == "day":
                dates.append(current.strftime("%Y-%m-%d %H:00"))
                current += datetime.timedelta(hours=1)
            else:
                dates.append(current.strftime("%Y-%m-%d"))
                current += datetime.timedelta(days=1)
        
        # 构建响应数据
        items = []
        for date in dates:
            stats = date_stats.get(date, {'total_tokens': 0, 'users': set()})
            user_count = len(stats['users'])
            avg_tokens = stats['total_tokens'] // user_count if user_count > 0 else 0
            items.append(TokenTrendItem(
                date=date,
                total_tokens=stats['total_tokens'],
                avg_tokens=avg_tokens,
                user_count=user_count
            ))
        
        return TokenTrendOut(items=items, dates=dates)

    @classmethod
    async def get_user_token_detail_service(
        cls,
        auth: AuthSchema,
        time_range: str,
        start_date: str | None,
        end_date: str | None,
        dept_id: int | None,
        position_id: int | None,
        page_no: int,
        page_size: int
    ) -> UserTokenDetailOut:
        """获取人员Token消耗明细（符合筛选条件的最近10条）"""
        from app.api.v1.module_system.user.crud import UserCRUD
        from app.api.v1.module_system.dept.crud import DeptCRUD
        from app.api.v1.module_system.position.crud import PositionCRUD
        from app.plugin.module_ai.ai_agent.crud import AiAgentCRUD
        
        # 获取时间范围
        start_time, end_time = cls._get_time_range(time_range, start_date, end_date)
        
        # 获取用户信息
        user_list = await UserCRUD(auth).get_list_crud()
        dept_list = await DeptCRUD(auth).get_list_crud()
        position_list = await PositionCRUD(auth).get_list_crud()
        agent_list = await AiAgentCRUD(auth).list_ai_agent_crud()
        
        dept_map = {dept.id: dept for dept in dept_list}
        position_map = {pos.id: pos for pos in position_list}
        agent_map = {agent.id: agent for agent in agent_list}
        
        # 构建用户-岗位映射（从positions关系中获取）
        user_position_map = {}
        for user in user_list:
            user_position_map[user.id] = set()
            if hasattr(user, 'positions') and user.positions:
                for pos in user.positions:
                    user_position_map[user.id].add(pos.id)
        
        # 过滤用户（根据部门和岗位）
        user_filter_map = {}
        for user in user_list:
            dept_match = dept_id is None or (hasattr(user, 'dept_id') and user.dept_id == dept_id)
            position_match = position_id is None or (position_id in user_position_map.get(user.id, set()))
            if dept_match and position_match:
                user_filter_map[user.id] = user
        
        # 如果没有符合条件的用户，直接返回空结果
        if not user_filter_map:
            return UserTokenDetailOut(items=[], total=0)
        
        async with auth.db as session:
            # 查询符合筛选条件的最近10条记录
            result = await session.execute(
                select(
                    AiChatModel.id,
                    AiChatModel.user_id,
                    AiChatModel.agent_id,
                    AiChatModel.title,
                    AiChatModel.model_id,
                    AiChatModel.provider_id,
                    AiChatModel.tokens,
                    AiChatModel.created_time
                ).where(
                    and_(
                        AiChatModel.created_time >= start_time,
                        AiChatModel.created_time <= end_time,
                        AiChatModel.user_id.in_(list(user_filter_map.keys()))
                    )
                ).order_by(AiChatModel.created_time.desc())
                .limit(10)
            )
            rows = result.all()

        # 构建响应数据
        items = []
        for row in rows:
            user = user_filter_map.get(row.user_id)
            if user:
                dept = dept_map.get(user.dept_id if hasattr(user, 'dept_id') else 0)
                # 获取用户的第一个岗位名称
                user_positions = user_position_map.get(user.id, set())
                position_name = ''
                if user_positions:
                    first_position_id = list(user_positions)[0]
                    position = position_map.get(first_position_id)
                    position_name = position.name if position and hasattr(position, 'name') else ''
                agent = agent_map.get(row.agent_id)

                items.append(UserTokenDetailItem(
                    user_id=row.user_id,
                    user_name=user.name if hasattr(user, 'name') else str(row.user_id),
                    dept_name=dept.name if dept and hasattr(dept, 'name') else '',
                    position_name=position_name,
                    date=row.created_time.strftime("%Y-%m-%d %H:%M") if isinstance(row.created_time, datetime.datetime) else str(row.created_time),
                    tokens=row.tokens or 0,
                    title=row.title or '',
                    model_name=f"{row.provider_id}/{row.model_id}" if row.provider_id and row.model_id else '',
                    agent_name=agent.name if agent and hasattr(agent, 'name') else '',
                    conversation_id=row.id
                ))

        return UserTokenDetailOut(items=items, total=len(items))

    @classmethod
    async def get_token_overview_service(
        cls,
        auth: AuthSchema,
        time_range: str,
        start_date: str | None,
        end_date: str | None,
        dept_id: int | None,
        position_id: int | None
    ) -> TokenOverviewOut:
        """获取Token统计概览"""
        from app.api.v1.module_system.user.crud import UserCRUD
        from app.api.v1.module_system.position.crud import PositionCRUD
        
        start_time, end_time = cls._get_time_range(time_range, start_date, end_date)
        
        # 获取用户信息用于过滤
        user_list = await UserCRUD(auth).get_list_crud()
        
        # 构建用户-岗位映射
        user_position_map = {}
        for user in user_list:
            user_position_map[user.id] = set()
            if hasattr(user, 'positions') and user.positions:
                for pos in user.positions:
                    user_position_map[user.id].add(pos.id)
        
        # 过滤用户
        user_filter_map = {}
        for user in user_list:
            dept_match = dept_id is None or (hasattr(user, 'dept_id') and user.dept_id == dept_id)
            position_match = position_id is None or (position_id in user_position_map.get(user.id, set()))
            if dept_match and position_match:
                user_filter_map[user.id] = user
        
        # 查询统计数据
        async with auth.db as session:
            result = await session.execute(
                select(
                    AiChatModel.user_id,
                    AiChatModel.agent_id,
                    func.count(AiChatModel.id).label('chat_count'),
                    func.sum(AiChatModel.tokens).label('total_tokens')
                ).where(
                    and_(
                        AiChatModel.created_time >= start_time,
                        AiChatModel.created_time <= end_time
                    )
                ).group_by(
                    AiChatModel.user_id,
                    AiChatModel.agent_id
                )
            )
            rows = result.all()
        
        # 统计
        total_tokens = 0
        total_chats = 0
        active_agents = set()
        active_users = set()
        
        for row in rows:
            if row.user_id in user_filter_map:
                total_tokens += row.total_tokens or 0
                total_chats += row.chat_count or 0
                active_users.add(row.user_id)
                if row.agent_id and row.agent_id > 0:
                    active_agents.add(row.agent_id)
        
        return TokenOverviewOut(
            total_tokens=total_tokens,
            total_chats=total_chats,
            active_agents=len(active_agents),
            active_users=len(active_users)
        )

    @classmethod
    async def get_personal_token_overview_service(
        cls,
        auth: AuthSchema,
        start_date: str | None,
        end_date: str | None
    ) -> TokenOverviewOut:
        """获取个人Token统计概览"""
        # 获取当前用户ID
        current_user_id = auth.user.id if auth.user else None
        if not current_user_id:
            return TokenOverviewOut(
                total_tokens=0,
                total_chats=0,
                active_agents=0,
                active_users=0
            )
        
        # 处理时间范围
        if start_date and end_date:
            try:
                start_time = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                end_time = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                end_time = end_time.replace(hour=23, minute=59, second=59)
            except ValueError:
                # 日期格式错误，查询全部
                start_time = None
                end_time = None
        else:
            start_time = None
            end_time = None
        
        # 查询当前用户的统计数据
        async with auth.db as session:
            query = select(
                AiChatModel.agent_id,
                func.count(AiChatModel.id).label('chat_count'),
                func.sum(AiChatModel.tokens).label('total_tokens')
            ).where(
                AiChatModel.user_id == current_user_id
            )
            
            # 添加时间范围条件
            if start_time and end_time:
                query = query.where(
                    and_(
                        AiChatModel.created_time >= start_time,
                        AiChatModel.created_time <= end_time
                    )
                )
            
            query = query.group_by(AiChatModel.agent_id)
            result = await session.execute(query)
            rows = result.all()
        
        # 统计
        total_tokens = 0
        total_chats = 0
        active_agents = set()
        
        for row in rows:
            total_tokens += row.total_tokens or 0
            total_chats += row.chat_count or 0
            if row.agent_id and row.agent_id > 0:
                active_agents.add(row.agent_id)
        
        return TokenOverviewOut(
            total_tokens=total_tokens,
            total_chats=total_chats,
            active_agents=len(active_agents),
            active_users=1  # 个人统计，活跃用户数为1
        )

    @classmethod
    async def get_personal_token_detail_service(
        cls,
        auth: AuthSchema,
        start_date: str | None,
        end_date: str | None,
        page_no: int,
        page_size: int
    ) -> UserTokenDetailOut:
        """获取个人Token消耗明细"""
        from app.plugin.module_ai.ai_agent.crud import AiAgentCRUD
        
        # 获取当前用户ID
        current_user_id = auth.user.id if auth.user else None
        if not current_user_id:
            return UserTokenDetailOut(items=[], total=0)
        
        # 获取用户信息
        user = auth.user
        dept_name = ''
        position_name = ''
        if user:
            if hasattr(user, 'dept') and user.dept:
                dept_name = user.dept.name if hasattr(user.dept, 'name') else ''
            if hasattr(user, 'positions') and user.positions:
                first_pos = user.positions[0]
                position_name = first_pos.name if hasattr(first_pos, 'name') else ''
        
        # 处理时间范围
        if start_date and end_date:
            try:
                start_time = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                end_time = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                end_time = end_time.replace(hour=23, minute=59, second=59)
            except ValueError:
                start_time = None
                end_time = None
        else:
            start_time = None
            end_time = None
        
        # 获取智能体信息
        agent_list = await AiAgentCRUD(auth).list_ai_agent_crud()
        agent_map = {agent.id: agent for agent in agent_list}
        
        async with auth.db as session:
            # 构建查询
            query = select(
                AiChatModel.id,
                AiChatModel.agent_id,
                AiChatModel.title,
                AiChatModel.model_id,
                AiChatModel.provider_id,
                AiChatModel.tokens,
                AiChatModel.created_time
            ).where(
                and_(
                    AiChatModel.user_id == current_user_id,
                    AiChatModel.status == "0"
                )
            )

            # 添加时间范围条件
            if start_time and end_time:
                query = query.where(
                    and_(
                        AiChatModel.created_time >= start_time,
                        AiChatModel.created_time <= end_time
                    )
                )

            # 先查询总数
            count_query = select(func.count(AiChatModel.id)).where(
                and_(
                    AiChatModel.user_id == current_user_id,
                    AiChatModel.status == "0"
                )
            )
            if start_time and end_time:
                count_query = count_query.where(
                    and_(
                        AiChatModel.created_time >= start_time,
                        AiChatModel.created_time <= end_time
                    )
                )
            count_result = await session.execute(count_query)
            total = count_result.scalar() or 0

            # 查询明细数据（按时间倒序）
            query = query.order_by(AiChatModel.created_time.desc())
            query = query.offset((page_no - 1) * page_size).limit(page_size)
            result = await session.execute(query)
            rows = result.all()

        # 构建响应数据
        items = []
        for row in rows:
            agent = agent_map.get(row.agent_id)
            items.append(UserTokenDetailItem(
                user_id=current_user_id,
                user_name=user.name if user and hasattr(user, 'name') else str(current_user_id),
                dept_name=dept_name,
                position_name=position_name,
                date=row.created_time.strftime("%Y-%m-%d %H:%M") if isinstance(row.created_time, datetime.datetime) else str(row.created_time),
                tokens=row.tokens or 0,
                title=row.title or '',
                model_name=f"{row.provider_id}/{row.model_id}" if row.provider_id and row.model_id else '',
                agent_name=agent.name if agent and hasattr(agent, 'name') else '',
                conversation_id=row.id
            ))

        return UserTokenDetailOut(items=items, total=total)

    @classmethod
    async def get_chat_trend_service(
        cls,
        auth: AuthSchema,
        time_range: str,
        start_date: str | None,
        end_date: str | None,
        dept_id: int | None,
        position_id: int | None
    ) -> ChatTrendOut:
        """获取对话趋势"""
        from app.api.v1.module_system.user.crud import UserCRUD
        
        start_time, end_time = cls._get_time_range(time_range, start_date, end_date)
        
        # 确定时间粒度
        if time_range == "day":
            date_format = "%Y-%m-%d %H:00"
        else:
            date_format = "%Y-%m-%d"
        
        # 获取用户信息用于过滤
        user_list = await UserCRUD(auth).get_list_crud()
        
        # 构建用户-岗位映射
        user_position_map = {}
        for user in user_list:
            user_position_map[user.id] = set()
            if hasattr(user, 'positions') and user.positions:
                for pos in user.positions:
                    user_position_map[user.id].add(pos.id)
        
        # 过滤用户
        user_filter_map = {}
        for user in user_list:
            dept_match = dept_id is None or (hasattr(user, 'dept_id') and user.dept_id == dept_id)
            position_match = position_id is None or (position_id in user_position_map.get(user.id, set()))
            if dept_match and position_match:
                user_filter_map[user.id] = user
        
        # 查询对话统计
        async with auth.db as session:
            result = await session.execute(
                select(
                    AiChatModel.created_time,
                    func.count(AiChatModel.id).label('chat_count')
                ).where(
                    and_(
                        AiChatModel.created_time >= start_time,
                        AiChatModel.created_time <= end_time
                    )
                ).group_by(
                    AiChatModel.created_time
                ).order_by(AiChatModel.created_time)
            )
            rows = result.all()
        
        # 按日期汇总
        date_stats = defaultdict(int)
        for row in rows:
            date_key = row.created_time.strftime(date_format) if isinstance(row.created_time, datetime.datetime) else str(row.created_time)
            date_stats[date_key] += row.chat_count or 0
        
        # 生成日期列表（补全缺失日期）
        dates = []
        current = start_time
        while current <= end_time:
            if time_range == "day":
                dates.append(current.strftime("%Y-%m-%d %H:00"))
                current += datetime.timedelta(hours=1)
            else:
                dates.append(current.strftime("%Y-%m-%d"))
                current += datetime.timedelta(days=1)
        
        # 构建响应数据
        items = []
        for date in dates:
            chat_count = date_stats.get(date, 0)
            items.append(ChatTrendItem(
                date=date,
                chat_count=chat_count
            ))
        
        return ChatTrendOut(items=items, dates=dates)

    @classmethod
    async def get_model_consumption_service(
        cls,
        auth: AuthSchema,
        time_range: str,
        start_date: str | None,
        end_date: str | None,
        dept_id: int | None,
        position_id: int | None
    ) -> ModelConsumptionOut:
        """获取模型消耗占比"""
        from app.api.v1.module_system.user.crud import UserCRUD
        
        start_time, end_time = cls._get_time_range(time_range, start_date, end_date)
        
        # 获取用户信息用于过滤
        user_list = await UserCRUD(auth).get_list_crud()
        
        # 构建用户-岗位映射
        user_position_map = {}
        for user in user_list:
            user_position_map[user.id] = set()
            if hasattr(user, 'positions') and user.positions:
                for pos in user.positions:
                    user_position_map[user.id].add(pos.id)
        
        # 过滤用户
        user_filter_map = {}
        for user in user_list:
            dept_match = dept_id is None or (hasattr(user, 'dept_id') and user.dept_id == dept_id)
            position_match = position_id is None or (position_id in user_position_map.get(user.id, set()))
            if dept_match and position_match:
                user_filter_map[user.id] = user
        
        # 查询模型消耗
        async with auth.db as session:
            result = await session.execute(
                select(
                    AiChatModel.model_id,
                    AiChatModel.provider_id,
                    func.sum(AiChatModel.tokens).label('total_tokens')
                ).where(
                    and_(
                        AiChatModel.created_time >= start_time,
                        AiChatModel.created_time <= end_time
                    )
                ).group_by(
                    AiChatModel.model_id,
                    AiChatModel.provider_id
                )
            )
            rows = result.all()
        
        # 按模型汇总
        model_stats = defaultdict(int)
        for row in rows:
            model_key = f"{row.provider_id}/{row.model_id}" if row.provider_id and row.model_id else "未知模型"
            model_stats[model_key] += row.total_tokens or 0
        
        # 计算总量和占比
        total_tokens = sum(model_stats.values())
        
        items = []
        for model_name, tokens in sorted(model_stats.items(), key=lambda x: x[1], reverse=True):
            percentage = (tokens / total_tokens * 100) if total_tokens > 0 else 0
            items.append(ModelConsumptionItem(
                model_name=model_name,
                tokens=tokens,
                percentage=round(percentage, 2)
            ))
        
        return ModelConsumptionOut(items=items, total=len(items))
