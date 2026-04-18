from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from redis import Redis

from app.common.response import SuccessResponse
from app.core.dependencies import AuthPermission, redis_getter
from app.core.logger import log
from app.core.redis_crud import RedisCURD
from app.core.router_class import OperationLogRoute
from app.plugin.module_ai.ai_tools.service import AIToolsService

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
    cache_key = "ai_tools_list"
    redis_crud = RedisCURD(redis)
    # 检查缓存是否有效（5分钟内）
    if not force_refresh:
        cached_data = await redis_crud.get(cache_key)
        if cached_data:
            import json
            try:
                result_dict = json.loads(cached_data)
                log.info("使用缓存的统计数据")
                return SuccessResponse(data=result_dict, msg="列出工具列表成功")
            except json.JSONDecodeError:
                log.error("解析缓存数据失败")
    # 获取最新统计数据
    result = AIToolsService.list_tools()
    # 更新缓存，设置5分钟过期
    await redis_crud.set(cache_key, result, expire=600)
    log.info("列出工具列表成功")
    return SuccessResponse(data=result, msg="列出工具列表成功")
