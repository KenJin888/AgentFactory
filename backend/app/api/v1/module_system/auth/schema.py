from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.module_system.user.model import UserModel


class AuthSchema(BaseModel):
    """权限认证模型"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    user: UserModel | None = Field(default=None, description="用户信息")
    check_data_scope: bool = Field(default=True, description="是否检查数据权限")
    db: AsyncSession = Field(description="数据库会话")


class JWTPayloadSchema(BaseModel):
    """JWT载荷模型"""

    sub: str = Field(..., description="用户登录信息")
    is_refresh: bool = Field(default=False, description="是否刷新token")
    exp: datetime | int = Field(..., description="过期时间")

    @model_validator(mode="after")
    def validate_fields(self):
        if not self.sub or len(self.sub.strip()) == 0:
            raise ValueError("会话编号不能为空")
        return self


class JWTOutSchema(BaseModel):
    """JWT响应模型"""

    model_config = ConfigDict(from_attributes=True)

    access_token: str = Field(..., min_length=1, description="访问token")
    refresh_token: str = Field(..., min_length=1, description="刷新token")
    token_type: str = Field(default="Bearer", description="token类型")
    expires_in: int = Field(..., gt=0, description="过期时间(秒)")


class SSOJWTOutSchema(JWTOutSchema):
    """SSO JWT响应模型"""
    sso_code: str = Field(..., description='单点登录码')
    sso_code_expired_in: int = Field(..., gt=0, description='单点登录吗过期时间')


class RefreshTokenPayloadSchema(BaseModel):
    """刷新Token载荷模型"""

    refresh_token: str = Field(..., min_length=1, description="刷新token")


class LogoutPayloadSchema(BaseModel):
    """退出登录载荷模型"""

    token: str = Field(..., min_length=1, description="token")


class CaptchaOutSchema(BaseModel):
    """验证码响应模型"""

    model_config = ConfigDict(from_attributes=True)

    enable: bool = Field(default=True, description="是否启用验证码")
    key: str = Field(..., min_length=1, description="验证码唯一标识")
    img_base: str = Field(..., min_length=1, description="Base64编码的验证码图片")


class WechatLoginQRCodeOutSchema(BaseModel):
    """微信公众号扫码登录二维码响应"""

    login_id: str = Field(..., min_length=1, description="扫码登录会话ID")
    poll_token: str = Field(..., min_length=1, description="轮询状态令牌")
    scene_id: int = Field(..., ge=1, description="微信场景值")
    ticket: str = Field(..., min_length=1, description="二维码票据")
    qrcode_url: str = Field(..., min_length=1, description="二维码图片URL")
    expire_seconds: int = Field(..., gt=0, description="二维码有效期(秒)")
    status: Literal["pending"] = Field(default="pending", description="当前扫码状态")


class WechatLoginStatusOutSchema(BaseModel):
    """微信公众号扫码登录状态响应"""

    status: Literal["pending", "scanned", "logged_in", "need_bind", "expired", "failed"] = Field(
        ..., description="扫码登录状态"
    )
    msg: str = Field(default="", description="状态描述")
    access_token: str | None = Field(default=None, description="访问令牌")
    refresh_token: str | None = Field(default=None, description="刷新令牌")
    token_type: str | None = Field(default=None, description="令牌类型")
    expires_in: int | None = Field(default=None, description="令牌过期时间(秒)")
