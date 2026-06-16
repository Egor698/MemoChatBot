from aiogram import Router
from aiogram.types import Message

from src.core.service.agentservice import AgentService
from src.core.schemas.call_message import CallMessageSchema

router = Router()


@router.message()
async def accept_message(msg: Message, agent_service: AgentService):
    answer = await agent_service.call_agent(CallMessageSchema(content=msg.text))

    await msg.answer(answer.content)




