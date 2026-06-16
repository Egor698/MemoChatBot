from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from src.core.db.database import sessionfactory
from src.core.service.agentservice import AgentService


class Middleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        async with sessionfactory() as session:
            service = AgentService(event.from_user.id, session)
            data["agent_service"] = service

            result = await handler(event, data)

        return result