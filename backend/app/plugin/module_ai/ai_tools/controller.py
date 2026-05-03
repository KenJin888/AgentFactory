from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from redis import Redis

from app.common.response import SuccessResponse
from app.core.dependencies import AuthPermission, redis_getter
from app.core.logger import log
from app.core.redis_crud import RedisCURD
from app.core.router_class import OperationLogRoute
from app.plugin.module_ai.ai_tools.service import AIToolsService, get_tools

AIToolsRouter = APIRouter(
    route_class=OperationLogRoute,
    prefix="/ai_tools",
    tags=["内置工具管理"]
)


@AIToolsRouter.get(
    "/list",
    summary="内置工具列表",
    description="列出所有内置工具",
    dependencies=[Depends(AuthPermission())],
)
async def list_tools_controller(
        force_refresh: bool = False,
        redis: Redis = Depends(redis_getter),
) -> JSONResponse:
    result = await get_tools(True, redis)
    return SuccessResponse(data=result, msg="列出工具列表成功")