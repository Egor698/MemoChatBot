from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.core.agent.components.models import base_llm, summarization_llm
from src.core.agent.states import DialogState

from src.core.agent.prompts import GENERATED_SUMMARY_PROMPT, GENERATED_RESPONSE_PROMPT

async def generate_ai_response(state: DialogState) -> DialogState:
    """Генерация ответа ассистента на основе контекста буффера сообщений и суммаризации."""

    prompt_template = ChatPromptTemplate.from_messages([
        ('system', GENERATED_RESPONSE_PROMPT),
        MessagesPlaceholder("messages_history")
    ])

    chain = prompt_template | base_llm

    response_ai = await chain.ainvoke({
        "messages_history": [*state['buffered_messages'], state['call_message']],
        "summary": state["existing_summary"]
    })

    return {'response_ai': response_ai, 'clean_response_ai': response_ai.content}


async def generate_conversation_summary(state: DialogState) -> DialogState:
    """Генерация/обновление суммаризации на основе буфера сообщений и прошлого саммари."""

    prompt_template = ChatPromptTemplate.from_messages([
        ('system', GENERATED_SUMMARY_PROMPT),
        MessagesPlaceholder("buffered_messages")
    ])

    chain = prompt_template | summarization_llm | StrOutputParser()

    generated_summary_content = await chain.ainvoke({"buffered_messages": state["buffered_messages"],
                                                    "existing_summary": state["existing_summary"]})

    return {'new_summary': generated_summary_content}