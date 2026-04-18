import ast
import json
from pathlib import Path

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.menu.crud import MenuCRUD
from app.core.exceptions import CustomException
from app.utils.common_util import recursive_to_tree

from .schema import (
    AllPermissionSummarySchema,
    PluginPermissionSummarySchema,
)


class ExServicesService:
    _EX_MENU_NAME = "_ex_"
    _EX_MENU_TYPE = 1

    @classmethod
    def _extract_auth_permissions(cls, node: ast.Call) -> set[str]:
        if not isinstance(node.func, ast.Name) or node.func.id != "AuthPermission":
            return set()

        permissions_node = None
        if node.args:
            permissions_node = node.args[0]
        else:
            for keyword in node.keywords:
                if keyword.arg == "permissions":
                    permissions_node = keyword.value
                    break

        if not isinstance(permissions_node, (ast.List, ast.Tuple, ast.Set)):
            return set()

        permissions: set[str] = set()
        for item in permissions_node.elts:
            if isinstance(item, ast.Constant) and isinstance(item.value, str):
                permission = item.value.strip()
                if permission:
                    permissions.add(permission)
        return permissions

    @classmethod
    def _collect_module_permissions(cls, scan_root: Path) -> dict[str, set[str]]:
        module_names = sorted(path.name for path in scan_root.glob("module_*") if path.is_dir())
        module_permissions: dict[str, set[str]] = {module_name: set() for module_name in module_names}

        controller_files = sorted(scan_root.glob("module_*/**/controller.py"))
        for controller_file in controller_files:
            module_name = controller_file.relative_to(scan_root).parts[0]
            module_permissions.setdefault(module_name, set())

            try:
                source = controller_file.read_text(encoding="utf-8")
                tree = ast.parse(source)
            except Exception:
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    module_permissions[module_name].update(cls._extract_auth_permissions(node))

        return module_permissions

    @classmethod
    def _build_modules_payload(cls, module_permissions: dict[str, set[str]]) -> list[dict]:
        return [
            {"module": module_name, "permissions": sorted(permissions)}
            for module_name, permissions in sorted(module_permissions.items())
        ]

    @classmethod
    def get_plugin_permissions_service(cls) -> PluginPermissionSummarySchema:
        plugin_root = Path(__file__).resolve().parents[2]
        module_permissions = cls._collect_module_permissions(plugin_root)
        modules = cls._build_modules_payload(module_permissions)
        all_permissions = {perm for permissions in module_permissions.values() for perm in permissions}
        return PluginPermissionSummarySchema(
            modules=modules,
            total_modules=len(modules),
            total_permissions=len(all_permissions),
        )

    @classmethod
    def get_all_permissions_service(cls) -> AllPermissionSummarySchema:
        app_root = Path(__file__).resolve().parents[3]
        api_v1_root = app_root / "api" / "v1"
        plugin_root = app_root / "plugin"

        api_v1_permissions = cls._collect_module_permissions(api_v1_root)
        plugin_permissions = cls._collect_module_permissions(plugin_root)

        api_v1_modules = cls._build_modules_payload(api_v1_permissions)
        plugin_modules = cls._build_modules_payload(plugin_permissions)

        all_permissions = sorted(
            {
                permission
                for permissions in api_v1_permissions.values()
                for permission in permissions
            }
            | {
                permission
                for permissions in plugin_permissions.values()
                for permission in permissions
            }
        )

        return AllPermissionSummarySchema(
            plugin_modules=plugin_modules,
            api_v1_modules=api_v1_modules,
            all_permissions=all_permissions,
            total_plugin_modules=len(plugin_modules),
            total_api_v1_modules=len(api_v1_modules),
            total_permissions=len(all_permissions),
        )
