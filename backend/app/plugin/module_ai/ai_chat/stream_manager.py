import asyncio
from typing import Any

from app.core.logger import log


class AiChatStreamManager:
    _lock = asyncio.Lock()
    _tasks: dict[tuple[int, int], asyncio.Task[Any]] = {}

    @classmethod
    def _build_key(cls, user_id: int | None, conversation_id: int | None) -> tuple[int, int] | None:
        if not conversation_id:
            return None
        return int(user_id or 0), int(conversation_id)

    @classmethod
    async def register(
            cls,
            user_id: int | None,
            conversation_id: int | None,
            task: asyncio.Task[Any],
    ) -> None:
        key = cls._build_key(user_id=user_id, conversation_id=conversation_id)
        if key is None:
            return

        previous_task: asyncio.Task[Any] | None = None
        async with cls._lock:
            previous_task = cls._tasks.get(key)
            cls._tasks[key] = task

        if previous_task and previous_task is not task and not previous_task.done():
            previous_task.cancel()
            log.info("检测到重复AI对话流，已取消旧流: user_id=%s conversation_id=%s", key[0], key[1])

    @classmethod
    async def unregister(
            cls,
            user_id: int | None,
            conversation_id: int | None,
            task: asyncio.Task[Any] | None,
    ) -> None:
        key = cls._build_key(user_id=user_id, conversation_id=conversation_id)
        if key is None:
            return

        async with cls._lock:
            current_task = cls._tasks.get(key)
            if current_task is task:
                cls._tasks.pop(key, None)

    @classmethod
    async def cancel(cls, user_id: int | None, conversation_id: int | None) -> bool:
        key = cls._build_key(user_id=user_id, conversation_id=conversation_id)
        if key is None:
            return False

        async with cls._lock:
            task = cls._tasks.get(key)

        if not task or task.done():
            return False

        task.cancel()
        log.info("收到停止AI对话请求: user_id=%s conversation_id=%s", key[0], key[1])
        return True
