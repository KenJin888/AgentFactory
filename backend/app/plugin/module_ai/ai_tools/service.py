from pathlib import Path
from typing import Any, Dict, Optional, List

from agno.tools import Toolkit
from agno.tools.function import Function

from app.core.logger import log
from app.core.redis_crud import RedisCURD
from app.plugin.module_ai.ai_tools.config import base_tool_list
from openharness.tools.base import BaseTool, ToolExecutionContext, ToolResult


class AIToolsService:
    """
    AI工具管理服务层
    """

    @classmethod
    def adapt_openharness_tool(
            cls,
            tool: BaseTool,
            cwd: Path,
            metadata: Optional[Dict[str, Any]] = None,
    ) -> Function:
        """
        将一个 openharness BaseTool 实例转换为 agno Function 对象。

        Args:
            tool: openharness 工具实例（如 FileReadTool()）
            cwd: 工具执行时的当前工作目录（会传入 ToolExecutionContext）
            metadata: 额外上下文元数据（可选）

        Returns:
            agno Function 对象，可注册到 Toolkit 或直接传给 Agent
        """

        # 包装异步执行函数
        async def wrapper(**kwargs) -> str:
            # 根据传入的 kwargs 构造 input_model 实例
            try:
                arguments = tool.input_model(**kwargs)
            except Exception as e:
                return f"参数构造失败: {e}"

            # 构建执行上下文
            ctx = ToolExecutionContext(cwd=cwd, metadata=metadata or {})

            # 调用原始工具的 execute 方法
            result: ToolResult = await tool.execute(arguments, ctx)

            if result.is_error:
                return f"错误: {result.output}"
            return result.output

        # 获取 input_model 的 JSON Schema（自动转为 agno 需要的 parameters 格式）
        schema = tool.input_model.model_json_schema()
        parameters = {
            "type": schema.get("type", "object"),
            "properties": schema.get("properties", {}),
            "required": schema.get("required", []),
        }

        # 创建 agno Function
        return Function(
            name=tool.name,
            description=tool.description,
            parameters=parameters,
            entrypoint=wrapper,
            skip_entrypoint_processing=True,  # 因为我们已经手动提供了 parameters
            requires_confirmation=False,  # 可根据 tool.is_read_only 动态调整
        )

    @classmethod
    def create_toolkit_from_openharness_tools(
            cls,
            tools: List[BaseTool],
            cwd: Path,
            toolkit_name: str = "openharness_tools",
            metadata: Optional[Dict[str, Any]] = None,
    ) -> Toolkit:
        """
        批量将多个 openharness 工具转换并打包成一个 agno Toolkit。

        Args:
            tools: openharness 工具实例列表
            cwd: 所有工具共享的当前工作目录
            toolkit_name: Toolkit 的名称
            metadata: 额外上下文元数据（可选，如 auth 信息）

        Returns:
            包含所有转换后工具的 agno Toolkit
        """
        toolkit = Toolkit(name=toolkit_name, auto_register=False)
        for tool in tools:
            tool_metadata = metadata.copy() if metadata else {}
            if tool.name == 'ask_user_question':
                tool_metadata["ask_user_prompt"] = terminal_prompt
            agno_func = cls.adapt_openharness_tool(
                tool=tool,
                cwd=cwd,
                metadata=tool_metadata
            )
            toolkit.register(agno_func)
        return toolkit

    @classmethod
    def map_tools(cls) -> dict:
        """
       列出工具字典
       返回:
           工具字典
       """
        tools_map = {}
        tool_list = base_tool_list
        for tool_cls in tool_list:
            try:
                tool = tool_cls()
                tools_map[tool.name] = tool
            except:
                print('异常:%s' % tool_cls)

        return tools_map

    @classmethod
    def list_tools(cls) -> dict:
        """
        列出工具列表
        
        返回:
            工具列表
        """

        tools = []
        tool_list = base_tool_list
        for tool_cls in tool_list:
            try:
                tools.append({"name": tool_cls().name, "description": tool_cls().description})
            except:
                print('异常:%s' % tool_cls)

        return {"tools": tools}


async def terminal_prompt(question: str) -> str:
    print(question)
    return "1"
    # return await asyncio.to_thread(input, f"{question}\n> ")


async def get_tools(force_refresh, redis) -> dict[str, list]:
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
                return result_dict
            except json.JSONDecodeError:
                log.error("解析缓存数据失败")
    # 获取最新统计数据
    result = AIToolsService.list_tools()
    # 更新缓存，设置5分钟过期
    await redis_crud.set(cache_key, result, expire=600)
    log.info("列出工具列表成功")
    return result
