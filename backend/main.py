import argparse
import os

import uvicorn
from alembic import command
from alembic.config import Config
from fastapi import FastAPI

from app.common.enums import EnvironmentEnum

alembic_cfg = Config("alembic.ini")


def create_app() -> FastAPI:
    """创建 FastAPI 应用实例"""
    from app.config.setting import settings
    from app.plugin.init_app import (
        lifespan,
        register_exceptions,
        register_files,
        register_middlewares,
        register_routers,
        reset_api_docs,
        register_mcp,
    )

    # 创建FastAPI应用
    app = FastAPI(**settings.FASTAPI_CONFIG, lifespan=lifespan)

    # 注册各种组件
    register_exceptions(app)
    # 注册中间件
    register_middlewares(app)
    # 注册路由
    register_routers(app)
    # 注册静态文件
    register_files(app)
    # 重设API文档
    reset_api_docs(app)
    # 注册MCP
    register_mcp(app)

    return app


def run(
        env: EnvironmentEnum = EnvironmentEnum.DEV,
        sync_missing_columns: bool = False,
) -> None:
    """启动FastAPI服务"""

    try:
        # 设置环境变量
        os.environ["ENVIRONMENT"] = env.value
        os.environ["SYNC_MISSING_COLUMNS"] = "1" if sync_missing_columns else "0"
        print("项目启动中...")

        # 清除配置缓存，确保重新加载配置
        from app.config.setting import get_settings

        get_settings.cache_clear()
        settings = get_settings()

        from app.core.logger import setup_logging

        setup_logging()

        # 显示启动横幅
        from app.utils.banner import worship

        worship(env.value)

        # 启动uvicorn服务
        uvicorn.run(
            app="main:create_app",
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
            reload=env.value == EnvironmentEnum.DEV.value,
            factory=True,
            log_config=None,
        )
    except Exception:
        raise
    finally:
        from app.core.logger import cleanup_logging

        cleanup_logging()


def revision(env: EnvironmentEnum = EnvironmentEnum.DEV) -> None:
    """生成新的 Alembic 迁移脚本"""
    os.environ["ENVIRONMENT"] = env.value
    command.revision(alembic_cfg, autogenerate=True, message="迁移脚本")
    print("迁移脚本已生成")


def upgrade(env: EnvironmentEnum = EnvironmentEnum.DEV) -> None:
    """应用最新的 Alembic 迁移"""
    os.environ["ENVIRONMENT"] = env.value
    command.upgrade(alembic_cfg, "head")
    print("所有迁移已应用")


def build_parser() -> argparse.ArgumentParser:
    """构建命令行解析器"""
    parser = argparse.ArgumentParser(description="FastapiAdmin 命令行工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command_name, help_text in {
        "run": "启动 FastapiAdmin 服务",
        "revision": "生成新的 Alembic 迁移脚本",
        "upgrade": "应用最新的 Alembic 迁移",
    }.items():
        sub_parser = subparsers.add_parser(command_name, help=help_text)
        sub_parser.add_argument(
            "--env",
            default=EnvironmentEnum.DEV.value,
            choices=[item.value for item in EnvironmentEnum],
            help="运行环境 (dev, prod)，默认 dev",
        )
        if command_name == "run":
            sub_parser.add_argument(
                "--sync-missing-columns",
                action="store_true",
                help="启动时比对并自动补齐已有表缺失字段及其简单索引",
            )

    return parser


def main() -> None:
    """CLI 入口"""
    args = build_parser().parse_args()
    env = EnvironmentEnum(args.env)
    if args.command == "run":
        run(env, sync_missing_columns=args.sync_missing_columns)
        return

    commands = {"revision": revision, "upgrade": upgrade}
    commands[args.command](env)


if __name__ == "__main__":
    main()
