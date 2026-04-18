import hashlib
import json
import random
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from types import SimpleNamespace
from typing import NewType
from urllib.parse import quote_plus

import httpx
from dateutil.relativedelta import relativedelta
from fastapi import Request
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from user_agents import parse

from app.api.v1.module_monitor.online.schema import OnlineOutSchema
from app.api.v1.module_system.user.crud import UserCRUD
from app.api.v1.module_system.user.model import UserModel
from app.common.enums import RedisInitKeyConfig
from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import log
from app.core.redis_crud import RedisCURD
from app.core.security import (
    CustomOAuth2PasswordRequestForm,
    create_access_token,
    decode_access_token,
)
from app.utils.captcha_util import CaptchaUtil
from app.utils.common_util import get_random_character
from app.utils.hash_bcrpy_util import PwdUtil, AesEncryption
from app.utils.ip_local_util import IpLocalUtil
from .schema import (
    AuthSchema,
    CaptchaOutSchema,
    JWTOutSchema,
    JWTPayloadSchema,
    LogoutPayloadSchema,
    RefreshTokenPayloadSchema,
    SSOJWTOutSchema,
    WechatLoginQRCodeOutSchema,
    WechatLoginStatusOutSchema,
)

CaptchaKey = NewType("CaptchaKey", str)
CaptchaBase64 = NewType("CaptchaBase64", str)


class LoginService:
    """登录认证服务"""

    @classmethod
    async def authenticate_user_service(
            cls,
            request: Request,
            redis: Redis,
            login_form: CustomOAuth2PasswordRequestForm,
            db: AsyncSession,
            sso: bool = False,
    ) -> JWTOutSchema:
        """
        用户认证

        参数:
        - request (Request): FastAPI请求对象
        - login_form (CustomOAuth2PasswordRequestForm): 登录表单数据
        - db (AsyncSession): 数据库会话对象

        返回:
        - JWTOutSchema: 包含访问令牌和刷新令牌的响应模型

        异常:
        - CustomException: 认证失败时抛出异常。
        """
        # 判断是否来自API文档
        referer = request.headers.get("referer", "")
        request_from_docs = referer.endswith(("docs", "redoc"))

        # 验证码校验
        if settings.CAPTCHA_ENABLE and not request_from_docs and not sso:
            if not login_form.captcha_key or not login_form.captcha:
                raise CustomException(msg="验证码不能为空")
            await CaptchaService.check_captcha_service(
                redis=redis,
                key=login_form.captcha_key,
                captcha=login_form.captcha,
            )

        # 用户认证
        auth = AuthSchema(db=db)
        user = await UserCRUD(auth).get_by_username_crud(username=login_form.username)

        if not user:
            raise CustomException(msg="用户不存在")

        if not PwdUtil.verify_password(
                plain_password=login_form.password, password_hash=user.password
        ):
            raise CustomException(msg="账号或密码错误")

        if user.status == "1":
            raise CustomException(msg="用户已被停用")

        # 更新最后登录时间
        user = await UserCRUD(auth).update_last_login_crud(id=user.id)
        if not user:
            raise CustomException(msg="用户不存在")
        if not login_form.login_type:
            raise CustomException(msg="登录类型不能为空")

        # 创建token
        token = await cls.create_token_service(
            request=request,
            redis=redis,
            user=user,
            login_form=login_form,
            sso=sso,
        )

        return token

    @classmethod
    async def create_token_service(
            cls, request: Request, redis: Redis, user: UserModel,
            login_form: CustomOAuth2PasswordRequestForm, sso: bool = False
    ) -> JWTOutSchema | SSOJWTOutSchema:
        """
        创建访问令牌和刷新令牌

        参数:
        - request (Request): FastAPI请求对象
        - redis (Redis): Redis客户端对象
        - user (UserModel): 用户模型对象
        - login_type (str): 登录类型

        返回:
        - JWTOutSchema: 包含访问令牌和刷新令牌的响应模型

        异常:
        - CustomException: 创建令牌失败时抛出异常。
        """
        # 生成会话编号
        session_id = str(uuid.uuid4())
        request.scope["session_id"] = session_id

        user_agent = parse(request.headers.get("user-agent"))
        request_ip = None
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            # 取第一个 IP 地址，通常为客户端真实 IP
            request_ip = x_forwarded_for.split(",")[0].strip()
        else:
            # 若没有 X-Forwarded-For 头，则使用 request.client.host
            request_ip = request.client.host if request.client else "127.0.0.1"

        login_location = await IpLocalUtil.get_ip_location(request_ip)
        request.scope["login_location"] = login_location

        # 确保在请求上下文中设置用户名和会话ID
        request.scope["user_username"] = user.username

        access_expires = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        refresh_expires = timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS)

        now = datetime.now()

        # 记录租户信息到日志
        log.info(f"用户ID: {user.id}, 用户名: {user.username} 正在生成JWT令牌")

        # 生成会话信息
        session_info = OnlineOutSchema(
            session_id=session_id,
            user_id=user.id,
            name=user.name,
            user_name=user.username,
            ipaddr=request_ip,
            login_location=login_location,
            os=user_agent.os.family,
            browser=user_agent.browser.family,
            login_time=user.last_login,
            login_type=login_form.login_type,
        ).model_dump_json()

        access_token = create_access_token(
            payload=JWTPayloadSchema(
                sub=session_info,
                is_refresh=False,
                exp=now + access_expires,
            )
        )
        refresh_token = create_access_token(
            payload=JWTPayloadSchema(
                sub=session_info,
                is_refresh=True,
                exp=now + refresh_expires,
            )
        )

        # 设置新的token
        await RedisCURD(redis).set(
            key=f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}",
            value=access_token,
            expire=int(access_expires.total_seconds()),
        )

        await RedisCURD(redis).set(
            key=f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{session_id}",
            value=refresh_token,
            expire=int(refresh_expires.total_seconds()),
        )

        if sso:
            sso_code = AesEncryption().encrypt(json.dumps({
                'username': login_form.username,
                'password': login_form.password,
                'sso_code_expires_time': (datetime.now() + relativedelta(months=3)).strftime('%Y-%m-%d %H:%M:%S')
            }, ensure_ascii=False))

            return SSOJWTOutSchema(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=int(access_expires.total_seconds()),
                token_type=settings.TOKEN_TYPE,
                sso_code=sso_code,
                sso_code_expired_in=settings.SSO_CODE_EXPIRE_MINUTES,
            )
        else:
            return JWTOutSchema(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=int(access_expires.total_seconds()),
                token_type=settings.TOKEN_TYPE,
            )

    @classmethod
    async def refresh_token_service(
            cls,
            db: AsyncSession,
            redis: Redis,
            request: Request,
            refresh_token: RefreshTokenPayloadSchema,
    ) -> JWTOutSchema:
        """
        刷新访问令牌

        参数:
        - db (AsyncSession): 数据库会话对象
        - redis (Redis): Redis客户端对象
        - request (Request): FastAPI请求对象
        - refresh_token (RefreshTokenPayloadSchema): 刷新令牌数据

        返回:
        - JWTOutSchema: 新的令牌对象

        异常:
        - CustomException: 刷新令牌无效时抛出异常
        """
        token_payload: JWTPayloadSchema = decode_access_token(token=refresh_token.refresh_token)
        if not token_payload.is_refresh:
            raise CustomException(msg="非法凭证，请传入刷新令牌")

        # 去 Redis 查完整信息
        session_info = json.loads(token_payload.sub)
        session_id = session_info.get("session_id")
        user_id = session_info.get("user_id")

        if not session_id or not user_id:
            raise CustomException(msg="非法凭证,无法获取会话编号或用户ID")

        # 用户认证
        auth = AuthSchema(db=db)
        user = await UserCRUD(auth).get_by_id_crud(id=user_id)
        if not user:
            raise CustomException(msg="刷新token失败，用户不存在")

        # 记录刷新令牌时的租户信息
        log.info(f"用户ID: {user.id}, 用户名: {user.username} 正在刷新JWT令牌")

        # 设置新的 token
        access_expires = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        refresh_expires = timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS)
        now = datetime.now()

        session_info_json = json.dumps(session_info)

        access_token = create_access_token(
            payload=JWTPayloadSchema(
                sub=session_info_json,
                is_refresh=False,
                exp=now + access_expires,
            )
        )

        refresh_token_new = create_access_token(
            payload=JWTPayloadSchema(
                sub=session_info_json,
                is_refresh=True,
                exp=now + refresh_expires,
            )
        )

        # 覆盖写入 Redis
        await RedisCURD(redis).set(
            key=f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}",
            value=access_token,
            expire=int(access_expires.total_seconds()),
        )

        await RedisCURD(redis).set(
            key=f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{session_id}",
            value=refresh_token_new,
            expire=int(refresh_expires.total_seconds()),
        )

        return JWTOutSchema(
            access_token=access_token,
            refresh_token=refresh_token_new,
            token_type=settings.TOKEN_TYPE,
            expires_in=int(access_expires.total_seconds()),
        )

    @classmethod
    async def logout_service(cls, redis: Redis, token: LogoutPayloadSchema) -> bool:
        """
        退出登录

        参数:
        - redis (Redis): Redis客户端对象
        - token (LogoutPayloadSchema): 退出登录令牌数据

        返回:
        - bool: 退出成功返回True

        异常:
        - CustomException: 令牌无效时抛出异常
        """
        payload: JWTPayloadSchema = decode_access_token(token=token.token)
        session_info = json.loads(payload.sub)
        session_id = session_info.get("session_id")

        if not session_id:
            raise CustomException(msg="非法凭证,无法获取会话编号")

        # 删除Redis中的在线用户、访问令牌、刷新令牌
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}")
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{session_id}")

        log.info(f"用户退出登录成功,会话编号:{session_id}")

        return True


class CaptchaService:
    """验证码服务"""

    @classmethod
    async def get_captcha_service(cls, redis: Redis) -> dict[str, CaptchaKey | CaptchaBase64]:
        """
        获取验证码

        参数:
        - redis (Redis): Redis客户端对象

        返回:
        - dict[str, CaptchaKey | CaptchaBase64]: 包含验证码key和base64图片的字典

        异常:
        - CustomException: 验证码服务未启用时抛出异常
        """
        if not settings.CAPTCHA_ENABLE:
            raise CustomException(msg="未开启验证码服务")

        # 生成验证码图片和值
        captcha_base64, captcha_value = CaptchaUtil.captcha_arithmetic()
        captcha_key = get_random_character()

        # 保存到Redis并设置过期时间
        redis_key = f"{RedisInitKeyConfig.CAPTCHA_CODES.key}:{captcha_key}"
        await RedisCURD(redis).set(
            key=redis_key,
            value=captcha_value,
            expire=settings.CAPTCHA_EXPIRE_SECONDS,
        )

        log.info(f"生成验证码成功,验证码:{captcha_value}")

        # 返回验证码信息
        return CaptchaOutSchema(
            enable=settings.CAPTCHA_ENABLE,
            key=CaptchaKey(captcha_key),
            img_base=CaptchaBase64(f"data:image/png;base64,{captcha_base64}"),
        ).model_dump()

    @classmethod
    async def check_captcha_service(cls, redis: Redis, key: str, captcha: str) -> bool:
        """
        校验验证码

        参数:
        - redis (Redis): Redis客户端对象
        - key (str): 验证码key
        - captcha (str): 用户输入的验证码

        返回:
        - bool: 验证通过返回True

        异常:
        - CustomException: 验证码无效或错误时抛出异常
        """
        if not captcha:
            raise CustomException(msg="验证码不能为空")

        # 获取Redis中存储的验证码
        redis_key = f"{RedisInitKeyConfig.CAPTCHA_CODES.key}:{key}"

        captcha_value = await RedisCURD(redis).get(redis_key)
        if not captcha_value:
            log.error("验证码已过期或不存在")
            raise CustomException(msg="验证码已过期")

        # 验证码不区分大小写比对
        if captcha.lower() != captcha_value.lower():
            log.error(f"验证码错误,用户输入:{captcha},正确值:{captcha_value}")
            raise CustomException(msg="验证码错误")

        # 验证成功后删除验证码,避免重复使用
        await RedisCURD(redis).delete(redis_key)
        log.info(f"验证码校验成功,key:{key}")
        return True


class WechatLoginService:
    """微信公众号扫码登录服务"""

    @classmethod
    async def create_wechat_qrcode_service(cls, redis: Redis) -> dict:
        """
        创建微信公众号扫码登录二维码

        参数:
        - redis (Redis): Redis客户端

        返回:
        - dict: 二维码信息
        """
        cls._check_wechat_mp_config()
        redis_client = RedisCURD(redis)
        scene_id = await cls._generate_scene_id(redis_client=redis_client)
        login_id = str(uuid.uuid4())
        poll_token = get_random_character()

        access_token = await cls._get_wechat_access_token(redis=redis)
        qrcode_data = await cls._create_wechat_qrcode(
            access_token=access_token,
            scene_id=scene_id,
        )

        ttl = max(settings.WECHAT_MP_LOGIN_POLL_EXPIRE_SECONDS, 60)
        await redis_client.set(
            key=cls._scene_cache_key(scene_id),
            value={"login_id": login_id},
            expire=ttl,
        )
        await redis_client.set(
            key=cls._state_cache_key(login_id),
            value={
                "status": "pending",
                "msg": "等待扫码",
                "scene_id": scene_id,
                "poll_token": poll_token,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
            expire=ttl,
        )

        return WechatLoginQRCodeOutSchema(
            login_id=login_id,
            poll_token=poll_token,
            scene_id=scene_id,
            ticket=qrcode_data["ticket"],
            qrcode_url=qrcode_data["qrcode_url"],
            expire_seconds=qrcode_data["expire_seconds"],
            status="pending",
        ).model_dump()

    @classmethod
    async def get_wechat_login_status_service(
        cls, redis: Redis, login_id: str, poll_token: str
    ) -> dict:
        """
        获取微信公众号扫码登录状态

        参数:
        - redis (Redis): Redis客户端
        - login_id (str): 登录会话ID
        - poll_token (str): 轮询令牌

        返回:
        - dict: 登录状态
        """
        redis_client = RedisCURD(redis)
        state_raw = await redis_client.get(cls._state_cache_key(login_id))
        if not state_raw:
            return WechatLoginStatusOutSchema(status="expired", msg="二维码已过期").model_dump()

        state = cls._loads_json(state_raw)
        if poll_token != state.get("poll_token"):
            raise CustomException(msg="无效的轮询令牌")

        status = state.get("status", "pending")
        if status == "logged_in":
            return WechatLoginStatusOutSchema(
                status="logged_in",
                msg=state.get("msg", "登录成功"),
                access_token=state.get("access_token"),
                refresh_token=state.get("refresh_token"),
                token_type=state.get("token_type"),
                expires_in=state.get("expires_in"),
            ).model_dump()

        if status == "need_bind":
            return WechatLoginStatusOutSchema(status="need_bind", msg=state.get("msg", "未绑定账号")).model_dump()

        if status == "failed":
            return WechatLoginStatusOutSchema(status="failed", msg=state.get("msg", "登录失败")).model_dump()

        if status == "scanned":
            return WechatLoginStatusOutSchema(status="scanned", msg=state.get("msg", "已扫码，等待确认")).model_dump()

        return WechatLoginStatusOutSchema(status="pending", msg=state.get("msg", "等待扫码")).model_dump()

    @classmethod
    def check_callback_signature_service(
        cls,
        signature: str,
        timestamp: str,
        nonce: str,
    ) -> bool:
        """
        校验微信公众号回调签名

        参数:
        - signature (str): 微信签名
        - timestamp (str): 时间戳
        - nonce (str): 随机数

        返回:
        - bool: 校验是否通过
        """
        cls._check_wechat_mp_config()
        raw = "".join(sorted([settings.WECHAT_MP_TOKEN, timestamp, nonce]))
        local_signature = hashlib.sha1(raw.encode("utf-8")).hexdigest()
        return local_signature == signature

    @classmethod
    async def process_wechat_callback_service(
        cls,
        request: Request,
        redis: Redis,
        db: AsyncSession,
        signature: str,
        timestamp: str,
        nonce: str,
        encrypt_type: str | None = None,
    ) -> None:
        """
        处理微信公众号扫码回调事件

        参数:
        - request (Request): 请求对象
        - redis (Redis): Redis客户端
        - db (AsyncSession): 数据库会话
        - signature (str): 微信签名
        - timestamp (str): 时间戳
        - nonce (str): 随机数
        - encrypt_type (str | None): 加密模式

        返回:
        - None
        """
        if not cls.check_callback_signature_service(signature, timestamp, nonce):
            raise CustomException(msg="微信签名校验失败")

        if encrypt_type == "aes":
            raise CustomException(msg="暂不支持微信安全模式回调，请改为明文模式")

        body = await request.body()
        if not body:
            raise CustomException(msg="微信回调内容为空")

        try:
            root = ET.fromstring(body.decode("utf-8"))
        except ET.ParseError as exc:
            raise CustomException(msg="微信回调XML解析失败") from exc

        msg_type = (root.findtext("MsgType") or "").strip().lower()
        if msg_type != "event":
            return

        event = (root.findtext("Event") or "").strip()
        event_key = (root.findtext("EventKey") or "").strip()
        openid = (root.findtext("FromUserName") or "").strip()
        if not openid:
            return

        scene_id = cls._parse_scene_id(event=event, event_key=event_key)
        if scene_id is None:
            return

        redis_client = RedisCURD(redis)
        scene_raw = await redis_client.get(cls._scene_cache_key(scene_id))
        if not scene_raw:
            log.warning(f"微信扫码场景不存在: scene_id={scene_id}")
            return

        scene_data = cls._loads_json(scene_raw)
        login_id = scene_data.get("login_id")
        if not login_id:
            log.warning(f"微信扫码场景缺少login_id: scene_id={scene_id}")
            return

        state_key = cls._state_cache_key(login_id)
        state_raw = await redis_client.get(state_key)
        if not state_raw:
            log.warning(f"微信扫码状态不存在: login_id={login_id}")
            return

        state = cls._loads_json(state_raw)
        if state.get("status") in {"logged_in", "need_bind", "failed"}:
            return
        state.update(
            {
                "status": "scanned",
                "msg": "已扫码，正在登录",
                "openid": openid,
                "event": event,
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

        auth = AuthSchema(db=db, check_data_scope=False)
        user = await UserCRUD(auth).get_by_wx_login_crud(wx_login=openid)
        if not user:
            state.update(
                {
                    "status": "need_bind",
                    "msg": "该微信号未绑定系统账号，请先绑定",
                }
            )
            await redis_client.set(
                key=state_key,
                value=state,
                expire=max(settings.WECHAT_MP_LOGIN_POLL_EXPIRE_SECONDS, 60),
            )
            return

        if user.status == "1":
            state.update(
                {
                    "status": "failed",
                    "msg": "用户已被停用",
                }
            )
            await redis_client.set(
                key=state_key,
                value=state,
                expire=max(settings.WECHAT_MP_LOGIN_POLL_EXPIRE_SECONDS, 60),
            )
            return

        updated_user = await UserCRUD(auth).update_last_login_crud(id=user.id)
        login_user = updated_user or user

        login_form = SimpleNamespace(
            username=login_user.username,
            password="",
            login_type=settings.WECHAT_MP_LOGIN_TYPE,
        )
        token = await LoginService.create_token_service(
            request=request,
            redis=redis,
            user=login_user,
            login_form=login_form,
            sso=False,
        )
        state.update(
            {
                "status": "logged_in",
                "msg": "登录成功",
                "access_token": token.access_token,
                "refresh_token": token.refresh_token,
                "token_type": token.token_type,
                "expires_in": token.expires_in,
                "user_id": login_user.id,
                "username": login_user.username,
            }
        )
        await redis_client.set(
            key=state_key,
            value=state,
            expire=max(settings.WECHAT_MP_LOGIN_POLL_EXPIRE_SECONDS, 60),
        )

    @classmethod
    def _check_wechat_mp_config(cls) -> None:
        if not settings.WECHAT_MP_ENABLE:
            raise CustomException(msg="未开启微信公众号扫码登录")
        if not settings.WECHAT_MP_APP_ID:
            raise CustomException(msg="缺少微信公众号配置: WECHAT_MP_APP_ID")
        if not settings.WECHAT_MP_APP_SECRET:
            raise CustomException(msg="缺少微信公众号配置: WECHAT_MP_APP_SECRET")
        if not settings.WECHAT_MP_TOKEN:
            raise CustomException(msg="缺少微信公众号配置: WECHAT_MP_TOKEN")

    @classmethod
    async def _generate_scene_id(cls, redis_client: RedisCURD) -> int:
        for _ in range(8):
            scene_id = random.randint(100000, 999999999)
            if not await redis_client.exists(cls._scene_cache_key(scene_id)):
                return scene_id
        raise CustomException(msg="生成微信扫码场景值失败，请稍后重试")

    @classmethod
    async def _get_wechat_access_token(cls, redis: Redis) -> str:
        redis_client = RedisCURD(redis)
        token_key = f"{RedisInitKeyConfig.WECHAT_MP_ACCESS_TOKEN.key}:default"
        cached = await redis_client.get(token_key)
        if cached:
            try:
                cached_obj = cls._loads_json(cached)
                cached_token = cached_obj.get("access_token")
                if cached_token:
                    return str(cached_token)
            except Exception:
                pass

        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": settings.WECHAT_MP_APP_ID,
            "secret": settings.WECHAT_MP_APP_SECRET,
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
        except Exception as exc:
            raise CustomException(msg=f"获取微信access_token失败: {exc!s}") from exc

        if data.get("errcode"):
            raise CustomException(msg=f"获取微信access_token失败: {data.get('errmsg', '未知错误')}")

        access_token = data.get("access_token")
        expires_in = int(data.get("expires_in", 7200))
        if not access_token:
            raise CustomException(msg="微信access_token返回为空")

        await redis_client.set(
            key=token_key,
            value={"access_token": access_token},
            expire=max(expires_in - 120, 60),
        )
        return str(access_token)

    @classmethod
    async def _create_wechat_qrcode(
        cls,
        access_token: str,
        scene_id: int,
    ) -> dict:
        url = f"https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={access_token}"
        payload = {
            "expire_seconds": max(30, min(settings.WECHAT_MP_QRCODE_EXPIRE_SECONDS, 2592000)),
            "action_name": "QR_SCENE",
            "action_info": {
                "scene": {
                    "scene_id": scene_id,
                }
            },
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
        except Exception as exc:
            raise CustomException(msg=f"创建微信二维码失败: {exc!s}") from exc

        if data.get("errcode"):
            raise CustomException(msg=f"创建微信二维码失败: {data.get('errmsg', '未知错误')}")

        ticket = data.get("ticket")
        if not ticket:
            raise CustomException(msg="微信二维码ticket为空")

        return {
            "ticket": ticket,
            "qrcode_url": f"https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={quote_plus(ticket)}",
            "expire_seconds": int(data.get("expire_seconds", settings.WECHAT_MP_QRCODE_EXPIRE_SECONDS)),
        }

    @staticmethod
    def _loads_json(value: str | bytes) -> dict:
        if isinstance(value, bytes):
            value = value.decode("utf-8")
        return json.loads(value)

    @staticmethod
    def _parse_scene_id(event: str, event_key: str) -> int | None:
        event_upper = event.upper()
        if event_upper not in {"SUBSCRIBE", "SCAN"}:
            return None

        if event_upper == "SUBSCRIBE":
            if not event_key.startswith("qrscene_"):
                return None
            raw = event_key.replace("qrscene_", "", 1)
        else:
            raw = event_key

        if not raw.isdigit():
            return None
        return int(raw)

    @staticmethod
    def _scene_cache_key(scene_id: int) -> str:
        return f"{RedisInitKeyConfig.WECHAT_MP_LOGIN_SCENE.key}:{scene_id}"

    @staticmethod
    def _state_cache_key(login_id: str) -> str:
        return f"{RedisInitKeyConfig.WECHAT_MP_LOGIN_STATE.key}:{login_id}"
