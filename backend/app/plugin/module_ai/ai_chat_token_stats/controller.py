# -*- coding: utf-8 -*-
"""
Token消耗统计Controller层
"""
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import SuccessResponse
from app.core.dependencies import AuthPermission
from app.core.logger import log

from .schema import TokenStatsQueryParam
from .service import AiChatTokenStatsService

AiChatTokenStatsRouter = APIRouter(prefix="/ai_chat_token_stats", tags=["Token消耗统计模块"])


@AiChatTokenStatsRouter.get("/dept_rank", summary="部门Token消耗排名", description="部门Token消耗排名")
async def get_dept_token_rank_controller(
    search: TokenStatsQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """部门Token消耗排名接口"""
    result = await AiChatTokenStatsService.get_dept_token_rank_service(
        auth=auth,
        time_range=search.time_range,
        start_date=search.start_date,
        end_date=search.end_date,
        page_no=search.page_no,
        page_size=search.page_size
    )
    log.info("获取部门Token消耗排名成功")
    return SuccessResponse(data=result.model_dump(), msg="获取成功")


@AiChatTokenStatsRouter.get("/agent_rank", summary="智能体Token消耗排名", description="智能体Token消耗排名")
async def get_agent_token_rank_controller(
    search: TokenStatsQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """智能体Token消耗排名接口"""
    result = await AiChatTokenStatsService.get_agent_token_rank_service(
        auth=auth,
        time_range=search.time_range,
        start_date=search.start_date,
        end_date=search.end_date,
        dept_id=search.dept_id,
        position_id=search.position_id,
        page_no=search.page_no,
        page_size=search.page_size
    )
    log.info("获取智能体Token消耗排名成功")
    return SuccessResponse(data=result.model_dump(), msg="获取成功")


@AiChatTokenStatsRouter.get("/user_rank", summary="人员Token消耗排名", description="人员Token消耗排名")
async def get_user_token_rank_controller(
    search: TokenStatsQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """人员Token消耗排名接口"""
    result = await AiChatTokenStatsService.get_user_token_rank_service(
        auth=auth,
        time_range=search.time_range,
        start_date=search.start_date,
        end_date=search.end_date,
        dept_id=search.dept_id,
        position_id=search.position_id,
        page_no=search.page_no,
        page_size=search.page_size
    )
    log.info("获取人员Token消耗排名成功")
    return SuccessResponse(data=result.model_dump(), msg="获取成功")


@AiChatTokenStatsRouter.get("/trend", summary="Token消耗趋势", description="Token消耗趋势")
async def get_token_trend_controller(
    search: TokenStatsQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """Token消耗趋势接口"""
    result = await AiChatTokenStatsService.get_token_trend_service(
        auth=auth,
        time_range=search.time_range,
        start_date=search.start_date,
        end_date=search.end_date,
        dept_id=search.dept_id,
        user_id=None
    )
    log.info("获取Token消耗趋势成功")
    return SuccessResponse(data=result.model_dump(), msg="获取成功")


@AiChatTokenStatsRouter.get("/user_detail", summary="人员Token消耗明细", description="人员Token消耗明细")
async def get_user_token_detail_controller(
    search: TokenStatsQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """人员Token消耗明细接口"""
    result = await AiChatTokenStatsService.get_user_token_detail_service(
        auth=auth,
        time_range=search.time_range,
        start_date=search.start_date,
        end_date=search.end_date,
        dept_id=search.dept_id,
        position_id=search.position_id,
        page_no=search.page_no,
        page_size=search.page_size
    )
    log.info("获取人员Token消耗明细成功")
    return SuccessResponse(data=result.model_dump(), msg="获取成功")


@AiChatTokenStatsRouter.get("/overview", summary="Token统计概览", description="Token统计概览")
async def get_token_overview_controller(
    search: TokenStatsQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """Token统计概览接口"""
    result = await AiChatTokenStatsService.get_token_overview_service(
        auth=auth,
        time_range=search.time_range,
        start_date=search.start_date,
        end_date=search.end_date,
        dept_id=search.dept_id,
        position_id=search.position_id
    )
    log.info("获取Token统计概览成功")
    return SuccessResponse(data=result.model_dump(), msg="获取成功")


@AiChatTokenStatsRouter.get("/personal_overview", summary="个人Token统计概览", description="获取当前登录用户的Token统计概览")
async def get_personal_token_overview_controller(
    start_date: str | None = None,
    end_date: str | None = None,
    auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """个人Token统计概览接口"""
    result = await AiChatTokenStatsService.get_personal_token_overview_service(
        auth=auth,
        start_date=start_date,
        end_date=end_date
    )
    log.info("获取个人Token统计概览成功")
    return SuccessResponse(data=result.model_dump(), msg="获取成功")


@AiChatTokenStatsRouter.get("/personal_detail", summary="个人Token消耗明细", description="获取当前登录用户的Token消耗明细")
async def get_personal_token_detail_controller(
    start_date: str | None = None,
    end_date: str | None = None,
    page_no: int = 1,
    page_size: int = 10,
    auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """个人Token消耗明细接口"""
    result = await AiChatTokenStatsService.get_personal_token_detail_service(
        auth=auth,
        start_date=start_date,
        end_date=end_date,
        page_no=page_no,
        page_size=page_size
    )
    log.info("获取个人Token消耗明细成功")
    return SuccessResponse(data=result.model_dump(), msg="获取成功")


@AiChatTokenStatsRouter.get("/chat_trend", summary="对话趋势", description="对话趋势")
async def get_chat_trend_controller(
    search: TokenStatsQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """对话趋势接口"""
    result = await AiChatTokenStatsService.get_chat_trend_service(
        auth=auth,
        time_range=search.time_range,
        start_date=search.start_date,
        end_date=search.end_date,
        dept_id=search.dept_id,
        position_id=search.position_id
    )
    log.info("获取对话趋势成功")
    return SuccessResponse(data=result.model_dump(), msg="获取成功")


@AiChatTokenStatsRouter.get("/model_consumption", summary="模型消耗占比", description="模型消耗占比")
async def get_model_consumption_controller(
    search: TokenStatsQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission()),
) -> JSONResponse:
    """模型消耗占比接口"""
    result = await AiChatTokenStatsService.get_model_consumption_service(
        auth=auth,
        time_range=search.time_range,
        start_date=search.start_date,
        end_date=search.end_date,
        dept_id=search.dept_id,
        position_id=search.position_id
    )
    log.info("获取模型消耗占比成功")
    return SuccessResponse(data=result.model_dump(), msg="获取成功")
