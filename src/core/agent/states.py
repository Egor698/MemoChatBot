from typing import TypedDict

from langchain_core.messages import AIMessage, HumanMessage

from src.core.schemas.call_message import CallMessageSchema

from src.core.service.chatmemoryservice import ChatMemoryService


class DialogState(TypedDict):
    chat_memory_service: ChatMemoryService
    call_message: HumanMessage
    buffered_messages: list[AIMessage | HumanMessage]
    existing_summary: str | None
    response_ai: AIMessage
    clean_response_ai: str
    is_need_summarization: bool
    new_summary: str


class InputState(TypedDict):
    chat_memory_service: ChatMemoryService
    call_message: CallMessageSchema


class OutputState(TypedDict):
    clean_response_ai: str


