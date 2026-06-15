from langgraph.graph import StateGraph, START, END

from src.core.agent.nodes.call_models import generate_conversation_summary, generate_ai_response
from src.core.agent.nodes.chat_memory import (append_dialog_to_buffer,
                                          load_user_context,
                                          persist_updated_state)

from src.core.agent.edges import is_need_summarization

from src.core.agent.states import DialogState, InputState, OutputState


builder = StateGraph(DialogState,
                     input_schema=InputState,
                     output_schema=OutputState)


builder.add_node("load_user_context", load_user_context)
builder.add_node("generate_ai_response", generate_ai_response)
builder.add_node("generate_ai_response_2", generate_ai_response)
builder.add_node("generate_conversation_summary", generate_conversation_summary)
builder.add_node("persist_updated_state", persist_updated_state)
builder.add_node("append_dialog_to_buffer", append_dialog_to_buffer)

# Стартовая точка входа
builder.add_edge(START, "load_user_context")


# Анализируем состояние буфера
# Функция is_need_summarization возвращает:
#   - ["generate_conversation_summary", "generate_ai_response_2"]  -> буфер полон, нужно вызвать параллельно суммаризацию и дать ответ
#   - "generate_ai_response" -> буфер не полон, можно генерировать просто ответ
builder.add_conditional_edges(
    "load_user_context",
            is_need_summarization)


# Если нужно вызвать параллельно суммаризацию и дать ответ.
# Очищаем буффер, записываем новое summary и добавляем диалог в буффер
builder.add_edge("generate_conversation_summary", "persist_updated_state")
builder.add_edge(["generate_ai_response_2", "persist_updated_state"], "append_dialog_to_buffer")


# Генерация ответ
# Генерируем ответ и добавляем диалог в буффер
builder.add_edge("generate_ai_response", "append_dialog_to_buffer")

# Конечная точка
builder.add_edge("append_dialog_to_buffer", END)


graph = builder.compile()
