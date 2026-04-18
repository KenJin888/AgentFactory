# -*- coding: utf-8 -*-
import hashlib
import json
from datetime import datetime
from typing import Annotated
from typing import Union, Dict

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.response import ErrorResponse, SuccessResponse
from app.config.setting import settings
from app.core.dependencies import (
    db_getter,
    get_current_user,
    redis_getter
)
from app.core.exceptions import CustomException
from app.core.logger import log
from app.core.logger import logger
from app.core.router_class import OperationLogRoute
from app.core.security import CustomOAuth2PasswordRequestForm
from app.utils.hash_bcrpy_util import AesEncryption
from .schema import (
    CaptchaOutSchema,
    JWTOutSchema,
    LogoutPayloadSchema,
    RefreshTokenPayloadSchema,
    WechatLoginQRCodeOutSchema,
    WechatLoginStatusOutSchema,
)
from .schema import (
    SSOJWTOutSchema,
)
from .service import CaptchaService, LoginService, WechatLoginService

AuthRouter = APIRouter(route_class=OperationLogRoute, prefix="/auth", tags=["认证授权"])


@AuthRouter.post(
    '/code', summary='登录并获取单点登录码', description='登录并获取单点登录码', response_model=SSOJWTOutSchema)
async def login_for_code_controller(
        request: Request,
        redis: Redis = Depends(redis_getter),
        login_form: CustomOAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(db_getter),
) -> Union[JSONResponse, Dict]:
    sha1 = hashlib.sha1()
    sha1.update('password{}timestamp{}username{}{}'.format(
        login_form.password, login_form.timestamp, login_form.username, settings.SIGNATURE_KEY).encode('utf-8'))
    true_signature = sha1.hexdigest()
    if login_form.signature != true_signature:
        raise CustomException(msg="签名校验失败")

    login_token = await LoginService.authenticate_user_service(
        request=request, redis=redis, login_form=login_form, db=db, sso=True)
    logger.info(f'用户{login_form.username}登录成功')

    # 如果是文档请求，则不记录日志:http://localhost:8000/api/v1/docs
    data = login_token.model_dump()
    if settings.DOCS_URL in request.headers.get('referer', ''):
        return data
    return SuccessResponse(data=data, msg='登录成功')


@AuthRouter.post('/code/check', summary='使用登录码登录', description='使用登录码登录', response_model=JWTOutSchema)
async def login_by_code_controller(
        request: Request,
        redis: Redis = Depends(redis_getter),
        login_form: CustomOAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(db_getter),
):
    sha1 = hashlib.sha1()
    sha1.update('sso_code{}timestamp{}{}'.format(
        login_form.sso_code, login_form.timestamp, settings.SIGNATURE_KEY).encode('utf-8'))
    true_signature = sha1.hexdigest()
    if login_form.signature != true_signature:
        raise CustomException(msg="签名校验失败")

    ssoinfo = json.loads(AesEncryption().decrypt(login_form.sso_code))
    if ssoinfo['sso_code_expires_time'] <= datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
        raise CustomException(msg="sso_code已过期")

    login_form.username = ssoinfo['username']
    login_form.password = ssoinfo['password']
    login_token = await LoginService.authenticate_user_service(
        request=request, redis=redis, login_form=login_form, db=db)
    logger.info(f'用户{login_form.username}登录成功')

    # 如果是文档请求，则不记录日志:http://localhost:8000/api/v1/docs
    if settings.DOCS_URL in request.headers.get('referer', ''):
        return login_token.model_dump()
    return SuccessResponse(data=login_token.model_dump(), msg='登录成功')


@AuthRouter.post(
    "/login",
    summary="登录",
    description="登录",
    response_model=JWTOutSchema,
)
async def login_for_access_token_controller(
        request: Request,
        redis: Annotated[Redis, Depends(redis_getter)],
        login_form: Annotated[CustomOAuth2PasswordRequestForm, Depends()],
        db: Annotated[AsyncSession, Depends(db_getter)],
) -> JSONResponse | dict:
    """
    用户登录

    参数:
    - request (Request): FastAPI请求对象
    - login_form (CustomOAuth2PasswordRequestForm): 登录表单数据
    - db (AsyncSession): 数据库会话对象

    返回:
    - JWTOutSchema: 包含访问令牌和刷新令牌的响应模型

    异常:
    - CustomException: 认证失败时抛出异常。
    """
    login_token = await LoginService.authenticate_user_service(
        request=request, redis=redis, login_form=login_form, db=db
    )

    log.info(f"用户{login_form.username}登录成功")

    # 如果是文档请求，则不记录日志:http://localhost:8000/api/v1/docs
    if settings.DOCS_URL in request.headers.get("referer", ""):
        return login_token.model_dump()
    return SuccessResponse(data=login_token.model_dump(), msg="登录成功")


@AuthRouter.get(
    "/wechat/qrcode",
    summary="获取微信公众号扫码登录二维码",
    description="获取微信公众号扫码登录二维码",
    response_model=WechatLoginQRCodeOutSchema,
)
async def get_wechat_qrcode_controller(
        redis: Annotated[Redis, Depends(redis_getter)],
) -> JSONResponse:
    """
    获取微信公众号扫码登录二维码

    参数:
    - redis (Redis): Redis客户端

    返回:
    - JSONResponse: 二维码信息
    """
    qrcode = await WechatLoginService.create_wechat_qrcode_service(redis=redis)
    return SuccessResponse(data=qrcode, msg="获取二维码成功")


@AuthRouter.get(
    "/wechat/status",
    summary="查询微信公众号扫码登录状态",
    description="查询微信公众号扫码登录状态",
    response_model=WechatLoginStatusOutSchema,
)
async def get_wechat_login_status_controller(
        login_id: str = Query(..., min_length=1, description="扫码登录会话ID"),
        poll_token: str = Query(..., min_length=1, description="轮询令牌"),
        redis: Redis = Depends(redis_getter),
) -> JSONResponse:
    """
    查询微信公众号扫码登录状态

    参数:
    - login_id (str): 扫码登录会话ID
    - poll_token (str): 轮询令牌
    - redis (Redis): Redis客户端

    返回:
    - JSONResponse: 登录状态
    """
    status = await WechatLoginService.get_wechat_login_status_service(
        redis=redis,
        login_id=login_id,
        poll_token=poll_token,
    )
    return SuccessResponse(data=status, msg="获取扫码状态成功")


@AuthRouter.get(
    "/wechat/callback",
    summary="微信公众号回调校验",
    description="微信公众号回调校验",
)
async def wechat_callback_verify_controller(
        signature: str = Query(..., min_length=1, description="微信签名"),
        timestamp: str = Query(..., min_length=1, description="时间戳"),
        nonce: str = Query(..., min_length=1, description="随机串"),
        echostr: str = Query(..., min_length=1, description="随机字符串"),
) -> PlainTextResponse:
    """
    微信公众号回调URL校验

    参数:
    - signature (str): 微信签名
    - timestamp (str): 时间戳
    - nonce (str): 随机串
    - echostr (str): 回显字符串

    返回:
    - PlainTextResponse: 回显字符串
    """
    verified = WechatLoginService.check_callback_signature_service(
        signature=signature,
        timestamp=timestamp,
        nonce=nonce,
    )
    if not verified:
        raise CustomException(msg="微信回调签名校验失败")
    return PlainTextResponse(content=echostr)


@AuthRouter.post(
    "/wechat/callback",
    summary="微信公众号扫码回调",
    description="微信公众号扫码回调",
)
async def wechat_callback_event_controller(
        request: Request,
        redis: Annotated[Redis, Depends(redis_getter)],
        db: Annotated[AsyncSession, Depends(db_getter)],
        signature: str = Query(..., min_length=1, description="微信签名"),
        timestamp: str = Query(..., min_length=1, description="时间戳"),
        nonce: str = Query(..., min_length=1, description="随机串"),
        encrypt_type: str | None = Query(default=None, description="加密类型"),
) -> PlainTextResponse:
    """
    微信公众号扫码事件回调

    参数:
    - request (Request): 请求对象
    - redis (Redis): Redis客户端
    - db (AsyncSession): 数据库会话
    - signature (str): 微信签名
    - timestamp (str): 时间戳
    - nonce (str): 随机串
    - encrypt_type (str | None): 加密模式

    返回:
    - PlainTextResponse: 微信平台响应
    """
    await WechatLoginService.process_wechat_callback_service(
        request=request,
        redis=redis,
        db=db,
        signature=signature,
        timestamp=timestamp,
        nonce=nonce,
        encrypt_type=encrypt_type,
    )
    return PlainTextResponse(content="success")


@AuthRouter.post(
    "/token/refresh",
    summary="刷新token",
    description="刷新token",
    response_model=JWTOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def get_new_token_controller(
        request: Request,
        payload: RefreshTokenPayloadSchema,
        db: Annotated[AsyncSession, Depends(db_getter)],
        redis: Annotated[Redis, Depends(redis_getter)],
) -> JSONResponse:
    """
    刷新token

    参数:
    - request (Request): FastAPI请求对象
    - payload (RefreshTokenPayloadSchema): 刷新令牌负载模型

    返回:
    - JWTOutSchema: 包含新的访问令牌和刷新令牌的响应模型

    异常:
    - CustomException: 刷新令牌失败时抛出异常。
    """
    # 解析当前的访问Token以获取用户名
    new_token = await LoginService.refresh_token_service(
        db=db, request=request, redis=redis, refresh_token=payload
    )
    token_dict = new_token.model_dump()
    log.info(f"刷新token成功: {token_dict}")
    return SuccessResponse(data=token_dict, msg="刷新成功")


@AuthRouter.get(
    "/captcha/get",
    summary="获取验证码",
    description="获取登录验证码",
    response_model=CaptchaOutSchema,
)
async def get_captcha_for_login_controller(
        redis: Annotated[Redis, Depends(redis_getter)],
) -> JSONResponse:
    """
    获取登录验证码

    参数:
    - redis (Redis): Redis客户端对象

    返回:
    - CaptchaOutSchema: 包含验证码图片和key的响应模型

    异常:
    - CustomException: 获取验证码失败时抛出异常。
    """
    # 获取验证码
    captcha = await CaptchaService.get_captcha_service(redis=redis)
    log.info("获取验证码成功")
    return SuccessResponse(data=captcha, msg="获取验证码成功")


@AuthRouter.post(
    "/logout",
    summary="退出登录",
    description="退出登录",
    dependencies=[Depends(get_current_user)],
)
async def logout_controller(
        payload: LogoutPayloadSchema,
        redis: Annotated[Redis, Depends(redis_getter)],
) -> JSONResponse:
    """
    退出登录

    参数:
    - payload (LogoutPayloadSchema): 退出登录负载模型
    - redis (Redis): Redis客户端对象

    返回:
    - JSONResponse: 包含退出登录结果的响应模型

    异常:
    - CustomException: 退出登录失败时抛出异常。
    """
    if await LoginService.logout_service(redis=redis, token=payload):
        log.info("退出成功")
        return SuccessResponse(msg="退出成功")
    return ErrorResponse(msg="退出失败")
