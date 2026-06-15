from aiogram import Router
from aiogram.types import Message

from src.core.service.agentservice import AgentService
from src.core.schemas.call_message import CallMessageSchema
from src.core.db.database import sessionfactory

router = Router()


@router.message()
async def accept_message(msg: Message):
    async with sessionfactory() as session:
        service = AgentService(msg.from_user.id, session)
        answer = await service.call_agent(CallMessageSchema(content=msg.text))

    await msg.answer(answer.content)




