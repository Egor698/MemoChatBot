from langchain_core.messages import AIMessage, HumanMessage
from src.core.db.models import BufferMessage
from src.core.schemas.call_message import CallMessageSchema


class MessageConverter:
    """Конвертер между форматами сообщений БД и LangChain."""

    @staticmethod
    async def buffer_to_langchain_messages(buffer_messages: list[BufferMessage]) -> list[AIMessage | HumanMessage]:
        langchain_messages = []

        for msg in buffer_messages:
            if msg.role == 'ai':
                message = AIMessage(content=msg.content)
            else:
                message = HumanMessage(content=msg.content)

            langchain_messages.append(message)

        return langchain_messages


    @staticmethod
    async def langchain_to_buffer_messages(langchain_messages: list[AIMessage | HumanMessage]) -> list[BufferMessage]:
        buffer_messages = []

        for msg in langchain_messages:
            message = BufferMessage(role=msg.type, content=msg.content)

            buffer_messages.append(message)

        return buffer_messages


    @staticmethod
    async def call_message_to_langchain_message(call_message: CallMessageSchema):
        return HumanMessage(content=call_message.content)
