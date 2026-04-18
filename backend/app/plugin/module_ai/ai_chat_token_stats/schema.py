# -*- coding: utf-8 -*-
"""
Token消耗统计Schema定义
"""
from typing import Literal
from fastapi import Query
from pydantic import BaseModel, Field


class TokenStatsQueryParam:
    """Token统计查询参数"""

    def __init__(
        self,
        time_range: Literal["day", "week", "month"] = Query("week", description="时间范围: day-日, week-周, month-月"),
        start_date: str | None = Query(None, description="开始日期(YYYY-MM-DD)"),
        end_date: str | None = Query(None, description="结束日期(YYYY-MM-DD)"),
        dept_id: int | None = Query(None, description="部门ID"),
        position_id: int | None = Query(None, description="岗位ID"),
        page_no: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, ge=1, le=100, description="每页条数"),
    ) -> None:
        self.time_range = time_range
        self.start_date = start_date
        self.end_date = end_date
        self.dept_id = dept_id
        self.position_id = position_id
        self.page_no = page_no
        self.page_size = page_size


class DeptTokenRankItem(BaseModel):
    """部门Token消耗排名项"""
    dept_id: int = Field(..., description="部门ID")
    dept_name: str = Field(..., description="部门名称")
    total_tokens: int = Field(..., description="总Token数")
    model_distribution: list[dict] = Field(default=[], description="模型分布")


class AgentTokenRankItem(BaseModel):
    """智能体Token消耗排名项"""
    agent_id: int = Field(..., description="智能体ID")
    agent_name: str = Field(..., description="智能体名称")
    total_tokens: int = Field(..., description="总Token数")
    user_count: int = Field(..., description="使用人数")
    position_distribution: list[dict] = Field(default=[], description="岗位分布")


class UserTokenRankItem(BaseModel):
    """人员Token消耗排名项"""
    user_id: int = Field(..., description="用户ID")
    user_name: str = Field(..., description="用户名称")
    dept_name: str = Field(..., description="部门名称")
    position_name: str = Field(..., description="岗位名称")
    total_tokens: int = Field(..., description="总Token数")
    agent_count: int = Field(..., description="使用智能体数")
    position_distribution: list[dict] = Field(default=[], description="岗位分布")


class TokenTrendItem(BaseModel):
    """Token消耗趋势项"""
    date: str = Field(..., description="日期")
    total_tokens: int = Field(..., description="总Token数")
    avg_tokens: int = Field(..., description="人均Token数")
    user_count: int = Field(..., description="使用人数")


class UserTokenDetailItem(BaseModel):
    """人员Token消耗明细项"""
    user_id: int = Field(..., description="用户ID")
    user_name: str = Field(..., description="用户名称")
    dept_name: str = Field(..., description="部门名称")
    position_name: str = Field(..., description="岗位名称")
    date: str = Field(..., description="日期")
    tokens: int = Field(..., description="Token数")
    title: str = Field(..., description="会话标题")
    model_name: str = Field(..., description="模型名称")
    agent_name: str = Field(..., description="智能体名称")
    conversation_id: int = Field(..., description="会话ID")


class DeptTokenRankOut(BaseModel):
    """部门Token消耗排名响应"""
    items: list[DeptTokenRankItem] = Field(default=[], description="数据列表")
    total: int = Field(..., description="总数")


class AgentTokenRankOut(BaseModel):
    """智能体Token消耗排名响应"""
    items: list[AgentTokenRankItem] = Field(default=[], description="数据列表")
    total: int = Field(..., description="总数")


class UserTokenRankOut(BaseModel):
    """人员Token消耗排名响应"""
    items: list[UserTokenRankItem] = Field(default=[], description="数据列表")
    total: int = Field(..., description="总数")


class TokenTrendOut(BaseModel):
    """Token消耗趋势响应"""
    items: list[TokenTrendItem] = Field(default=[], description="数据列表")
    dates: list[str] = Field(default=[], description="日期列表")


class UserTokenDetailOut(BaseModel):
    """人员Token消耗明细响应"""
    items: list[UserTokenDetailItem] = Field(default=[], description="数据列表")
    total: int = Field(..., description="总数")


class TokenOverviewOut(BaseModel):
    """Token统计概览响应"""
    total_tokens: int = Field(..., description="总Token消耗")
    total_chats: int = Field(..., description="总对话数")
    active_agents: int = Field(..., description="活跃智能体数")
    active_users: int = Field(..., description="活跃用户数")


class ChatTrendItem(BaseModel):
    """对话趋势项"""
    date: str = Field(..., description="日期")
    chat_count: int = Field(..., description="对话次数")


class ChatTrendOut(BaseModel):
    """对话趋势响应"""
    items: list[ChatTrendItem] = Field(default=[], description="数据列表")
    dates: list[str] = Field(default=[], description="日期列表")


class ModelConsumptionItem(BaseModel):
    """模型消耗占比项"""
    model_name: str = Field(..., description="模型名称")
    tokens: int = Field(..., description="Token数")
    percentage: float = Field(..., description="占比(%)")


class ModelConsumptionOut(BaseModel):
    """模型消耗占比响应"""
    items: list[ModelConsumptionItem] = Field(default=[], description="数据列表")
    total: int = Field(..., description="总数")
