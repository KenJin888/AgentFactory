import os

from fastapi import FastAPI
from redis import exceptions
from redis.asyncio import Redis
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.config.setting import settings
from app.core.base_model import MappedBase
from app.core.exceptions import CustomException
from app.core.logger import log
from app.core.schema_sync import sync_missing_columns, sync_missing_indexes
from app.utils.import_util import ImportUtil


def create_engine_and_session(
        db_url: str = settings.DB_URI,
) -> tuple[Engine, sessionmaker]:
    """
    创建同步数据库引擎和会话工厂。

    参数:
    - db_url (str): 数据库连接URL,默认从配置中获取。

    返回:
    - tuple[Engine, sessionmaker]: 同步数据库引擎和会话工厂。
    """
    try:
        if not settings.SQL_DB_ENABLE:
            raise CustomException(
                msg="请先开启数据库连接",
                data="请启用 app/config/setting.py: SQL_DB_ENABLE",
            )
        # 同步数据库引擎
        engine: Engine = create_engine(
            url=db_url,
            echo=settings.DATABASE_ECHO,
            pool_pre_ping=settings.POOL_PRE_PING,
            pool_recycle=settings.POOL_RECYCLE,
        )
    except Exception as e:
        log.error(f"❌ 数据库连接失败 {e}")
        raise
    else:
        # 同步数据库会话工厂
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return engine, SessionLocal


def create_async_engine_and_session(
        db_url: str = settings.ASYNC_DB_URI,
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """
    获取异步数据库会话连接。

    返回:
    - tuple[AsyncEngine, async_sessionmaker[AsyncSession]]: 异步数据库引擎和会话工厂。
    """
    try:
        if not settings.SQL_DB_ENABLE:
            raise CustomException(
                msg="请先开启数据库连接",
                data="请启用 app/config/setting.py: SQL_DB_ENABLE",
            )
        # 异步数据库引擎
        if settings.DATABASE_TYPE == "sqlite":
            async_engine = create_async_engine(
                url=db_url,
                echo=settings.DATABASE_ECHO,
                echo_pool=settings.ECHO_POOL,
                pool_pre_ping=settings.POOL_PRE_PING,
                future=settings.FUTURE,
                pool_recycle=settings.POOL_RECYCLE,
            )
        else:
            async_engine = create_async_engine(
                url=db_url,
                echo=settings.DATABASE_ECHO,
                echo_pool=settings.ECHO_POOL,
                pool_pre_ping=settings.POOL_PRE_PING,
                future=settings.FUTURE,
                pool_recycle=settings.POOL_RECYCLE,
                pool_size=settings.POOL_SIZE,
                max_overflow=settings.MAX_OVERFLOW,
                pool_timeout=settings.POOL_TIMEOUT,
                pool_use_lifo=settings.POOL_USE_LIFO,
            )
    except Exception as e:
        log.error(f"❌ 数据库连接失败 {e}")
        raise
    else:
        # 异步数据库会话工厂
        AsyncSessionLocal = async_sessionmaker(
            bind=async_engine,
            autocommit=settings.AUTOCOMMIT,
            autoflush=settings.AUTOFETCH,
            expire_on_commit=settings.EXPIRE_ON_COMMIT,
            class_=AsyncSession,
        )
        return async_engine, AsyncSessionLocal


engine, db_session = create_engine_and_session(settings.DB_URI)
async_engine, async_db_session = create_async_engine_and_session(settings.ASYNC_DB_URI)


def _is_missing_column_sync_enabled() -> bool:
    return os.getenv("SYNC_MISSING_COLUMNS", "0").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


async def create_tables() -> None:
    """创建数据库表"""
    found_models = ImportUtil.find_models(MappedBase)
    log.info(f"✅ 已加载 {len(found_models)} 个模型定义")

    column_actions: list[dict[str, str | None]] = []
    index_actions: list[dict[str, str | None]] = []

    async with async_engine.begin() as coon:
        await coon.run_sync(MappedBase.metadata.create_all)
        if _is_missing_column_sync_enabled():
            column_actions = await coon.run_sync(
                lambda conn: sync_missing_columns(conn, MappedBase.metadata)
            )
            added_columns = {
                (action["table"], action["column"])
                for action in column_actions
                if action["action"] == "add"
            }
            index_actions = await coon.run_sync(
                lambda conn: sync_missing_indexes(conn, MappedBase.metadata, added_columns)
            )

    for action in column_actions:
        table_name = action["table"]
        column_name = action["column"]
        reason = action["reason"]
        if action["action"] == "add":
            log.info(f"✅ 已自动补齐字段: {table_name}.{column_name}")
            continue
        log.warning(f"⚠️ 跳过自动补齐字段: {table_name}.{column_name}，原因: {reason}")

    for action in index_actions:
        table_name = action["table"]
        index_name = action["index"]
        reason = action["reason"]
        if action["action"] == "add":
            log.info(f"✅ 已自动补齐索引: {table_name}.{index_name}")
            continue
        log.warning(f"⚠️ 跳过自动补齐索引: {table_name}.{index_name}，原因: {reason}")


async def drop_tables() -> None:
    """删除数据库表"""
    async with async_engine.begin() as conn:
        await conn.run_sync(MappedBase.metadata.drop_all)


async def redis_connect(app: FastAPI, status: str) -> Redis | None:
    """
    创建或关闭Redis连接。

    参数:
    - app (FastAPI): FastAPI应用实例。
    - status (bool): 连接状态,True为创建连接,False为关闭连接。

    返回:
    - Redis | None: Redis连接实例,如果连接失败则返回None。
    """
    if not settings.REDIS_ENABLE:
        raise CustomException(
            msg="请先开启Redis连接",
            data="请启用 app/core/config.py: REDIS_ENABLE",
        )

    if status:
        try:
            rd = await Redis.from_url(
                url=settings.REDIS_URI,
                encoding="utf-8",
                decode_responses=True,
                health_check_interval=20,
                max_connections=settings.POOL_SIZE,
                socket_timeout=settings.POOL_TIMEOUT,
            )
            app.state.redis = rd
            if await rd.ping():  # pyright: ignore[reportGeneralTypeIssues]
                return rd
        except exceptions.AuthenticationError as e:
            log.error(f"❌ 数据库 Redis 认证失败: {e}")
            raise
        except exceptions.TimeoutError as e:
            log.error(f"❌ 数据库 Redis 连接超时: {e}")
            raise
        except exceptions.RedisError as e:
            log.error(f"❌ 数据库 Redis 连接错误: {e}")
            raise
    else:
        await app.state.redis.aclose()
        log.info("✅️ Redis连接已关闭")
