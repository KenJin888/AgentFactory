from typing import Literal

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, model_validator


class PluginModulePermissionSchema(BaseModel):
    module: str = Field(..., description="模块名称")
    permissions: list[str] = Field(default_factory=list, description="权限字列表")


class PluginPermissionSummarySchema(BaseModel):
    modules: list[PluginModulePermissionSchema] = Field(default_factory=list, description="模块权限汇总")
    total_modules: int = Field(0, description="模块总数")
    total_permissions: int = Field(0, description="权限字总数")


class AllPermissionSummarySchema(BaseModel):
    plugin_modules: list[PluginModulePermissionSchema] = Field(
        default_factory=list, description="插件模块权限汇总"
    )
    api_v1_modules: list[PluginModulePermissionSchema] = Field(
        default_factory=list, description="内置 API(v1) 模块权限汇总"
    )
    all_permissions: list[str] = Field(default_factory=list, description="全部权限字列表")
    total_plugin_modules: int = Field(0, description="插件模块总数")
    total_api_v1_modules: int = Field(0, description="API(v1) 模块总数")
    total_permissions: int = Field(0, description="权限字总数")
