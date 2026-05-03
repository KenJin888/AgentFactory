from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules

from openharness.tools.base import BaseTool

TOOLS_PACKAGE = "app.tools"


def _import_tool_modules() -> None:
    # 自动导入 app/tools 下所有 *_tool.py，确保 BaseTool 子类已加载到运行时
    tools_dir = Path(__file__).resolve().parents[3] / "tools"
    for module_info in iter_modules([str(tools_dir)]):
        module_name = module_info.name
        if module_name.endswith("_tool"):
            import_module(f"{TOOLS_PACKAGE}.{module_name}")

def _all_subclasses(cls: type) -> set[type]:
    subclasses = set(cls.__subclasses__())
    for subclass in list(subclasses):
        subclasses.update(_all_subclasses(subclass))
    return subclasses


def get_base_tool_list() -> list[type[BaseTool]]:
    _import_tool_modules()
    # 仅保留当前包下定义的工具类，避免混入其他模块工具
    return sorted(
        (
            tool_cls
            for tool_cls in _all_subclasses(BaseTool)
            if tool_cls.__module__.startswith(f"{TOOLS_PACKAGE}.")
        ),
        key=lambda cls: cls.__name__,
    )


# 兼容旧调用方；推荐使用 get_base_tool_list() 获取实时列表
base_tool_list = get_base_tool_list()

# 导入所有工具
# base_tool_list = BaseTool.__subclasses__()
