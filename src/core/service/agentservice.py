from sqlalchemy.ext.asyncio import AsyncSession

from src.core.service.chatmemoryservice import ChatMemoryService

from src.core.schemas.call_message import CallMessageSchema
from src.core.schemas.answer_message import AnswerMessageSchema

from src.core.agent.graph import graph

class UserContext:
    def __init__(self, telegram_user_id: int):
        self.id = telegram_user_id


class AgentService:
    def __init__(self, telegram_user_id: int, session: AsyncSession):
        self.active_user = UserContext(telegram_user_id)
        self.chat_memory_service = ChatMemoryService(self.active_user, session)


    async def call_agent(self, call_message: CallMessageSchema) -> AnswerMessageSchema:
        response = await graph.ainvoke({
            "chat_memory_service": self.chat_memory_service,
            "call_message": call_message
        })

        return AnswerMessageSchema(content=response["clean_response_ai"])
