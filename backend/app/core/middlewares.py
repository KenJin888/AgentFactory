import json
import time

from starlette.datastructures import MutableHeaders
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp
from starlette.types import Receive, Scope, Send

from app.api.v1.module_system.params.service import ParamsService
from app.common.response import ErrorResponse
from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import log
from app.core.security import decode_access_token


class CustomCORSMiddleware(CORSMiddleware):
    """CORS跨域中间件"""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(
            app,
            allow_origins=settings.ALLOW_ORIGINS,
            allow_methods=settings.ALLOW_METHODS,
            allow_headers=settings.ALLOW_HEADERS,
            allow_credentials=settings.ALLOW_CREDENTIALS,
            expose_headers=settings.CORS_EXPOSE_HEADERS,
        )


class RequestLogMiddleware:
    """
    记录请求日志中间件: 提供一个基础的中间件类，允许你自定义请求和响应处理逻辑。
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    @staticmethod
    def _extract_session_id_from_request(request: Request) -> str | None:
        """
        从请求中提取session_id（支持从Token或已设置的scope中获取）

        参数:
        - request (Request): 请求对象

        返回:
        - str | None: 会话ID，如果无法提取则返回None
        """
        # 1. 先检查 scope 中是否已经有 session_id（登录接口会设置）
        session_id = request.scope.get("session_id")
        if session_id:
            return session_id

        # 2. 尝试从 Authorization Header 中提取
        try:
            authorization = request.headers.get("Authorization")
            if not authorization:
                return None

            # 处理Bearer token
            token = authorization.replace("Bearer ", "").strip()

            # 解码token
            payload = decode_access_token(token)
            if not payload or not hasattr(payload, "sub"):
                return None

            # 从payload中提取session_id
            user_info = json.loads(payload.sub)
            session_id = user_info.get("session_id")

            # 同时设置到request.scope中，避免后续重复解析
            if session_id:
                request.scope["session_id"] = session_id

            return session_id
        except Exception:
            # 解析失败静默处理，返回None（可能是未认证请求）
            return None

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        start_time = time.time()

        # 尝试提取session_id
        session_id = self._extract_session_id_from_request(request)

        # 组装请求日志字段
        log_fields = (
            f"请求来源: {request.client.host if request.client else '未知'},"
            f"请求方法: {request.method},"
            f"请求路径: {request.url.path}"
        )
        log.info(log_fields)

        # 获取请求路径
        path = request.scope.get("path")

        # 尝试获取客户端真实IP
        request_ip = None
        request_ip = (
            x_forwarded_for.split(",")[0].strip()
            if (x_forwarded_for := request.headers.get("X-Forwarded-For"))
            else request.client.host
            if request.client
            else None
        )
        # 检查是否启用演示模式
        demo_enable = False
        ip_white_list = []
        white_api_list_path = []
        ip_black_list = []

        try:
            # 从应用实例获取Redis连接
            redis = request.app.state.redis
            if not redis:
                raise CustomException(msg="无法获取Redis连接")

            # 使用ParamsService获取系统配置
            system_config = await ParamsService.get_system_config_for_middleware(redis)
            # 提取配置值
            demo_enable = system_config["demo_enable"]
            ip_white_list = system_config["ip_white_list"]
            white_api_list_path = system_config["white_api_list_path"]
            ip_black_list = system_config["ip_black_list"]

        except Exception as e:
            log.error(f"获取系统配置失败: {e}")

        # 检查是否需要拦截请求
        should_block = False
        block_reason = ""

        # 1. 首先检查IP是否在黑名单中
        if request_ip and request_ip in ip_black_list:
            should_block = True
            block_reason = f"IP地址 {request_ip} 在黑名单中"

        # 2. 如果不在黑名单中，检查是否在演示模式下需要拦截
        elif demo_enable in ["true", "True"] and request.method != "GET":
            # 在演示模式下，非GET请求需要检查白名单
            is_ip_whitelisted = request_ip in ip_white_list
            is_path_whitelisted = path in white_api_list_path

            if not is_ip_whitelisted and not is_path_whitelisted:
                should_block = True
                block_reason = f"演示模式下拦截非GET请求，IP: {request_ip}, 路径: {path}"

        if should_block:
            # 增强安全审计：记录详细的拦截日志
            log.warning([
                f"会话ID: {session_id or '未认证'}",
                f"请求被拦截: {block_reason}",
                f"请求来源: {request_ip}",
                f"请求方法: {request.method}",
                f"请求路径: {path}",
                f"用户代理: {request.headers.get('user-agent', '未知')}",
                f"演示模式: {demo_enable}",
            ])
            response = ErrorResponse(msg="演示环境，禁止操作")
            await response(scope, receive, send)
            return

        response_logged = False

        async def send_wrapper(message):
            nonlocal response_logged

            if message["type"] == "http.response.start":
                process_time = round(time.time() - start_time, 5)
                headers = MutableHeaders(scope=message)
                headers["X-Process-Time"] = str(process_time)
                content_length = headers.get("content-length", "0")
                response_info = (
                    f"响应状态: {message['status']}, 响应内容长度: {content_length}, "
                    f"处理时间: {round(process_time * 1000, 3)}ms"
                )
                log.info(response_info)
                response_logged = True

            await send(message)

        await self.app(scope, receive, send_wrapper)

        if not response_logged:
            process_time = round(time.time() - start_time, 5)
            log.info(f"响应完成: 请求路径={path}, 处理时间: {round(process_time * 1000, 3)}ms")


class CustomGZipMiddleware(GZipMiddleware):
    """GZip压缩中间件"""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(
            app,
            minimum_size=settings.GZIP_MIN_SIZE,
            compresslevel=settings.GZIP_COMPRESS_LEVEL,
        )
        # 定义需要排除的MCP路由前缀
        self.exclude_paths = settings.GZIP_EXCLUDE_PATHS

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # 如果是HTTP请求且路径需要排除，直接调用app而不使用Gzip
        if scope["type"] == "http":
            path = scope.get("path", "")
            # 检查是否应该排除当前路径
            if any(path.__contains__(exclude_path) for exclude_path in self.exclude_paths):
                await self.app(scope, receive, send)
                return

        # 对于其他路由，使用父类的Gzip逻辑
        await super().__call__(scope, receive, send)
