from src.core.agent.states import DialogState

from src.core.agent.nodes.utils import MessageConverter


async def load_user_context(state: DialogState) -> DialogState:
    """Загрузка контекста пользователя: буфер сообщений и суммаризация."""
    service = state['chat_memory_service']

    buffered_messages, existing_summary = await service.get_current_state()
    is_need_summarization = await service.is_buffer_full()

    converted_buffered_messages = await MessageConverter.buffer_to_langchain_messages(buffered_messages)
    converted_call_message = await MessageConverter.call_message_to_langchain_message(state['call_message'])

    return {
            'buffered_messages': converted_buffered_messages,
            'call_message': converted_call_message,
            'existing_summary': existing_summary.content if existing_summary else None,
            'is_need_summarization': is_need_summarization
            }


async def persist_updated_state(state: DialogState) -> DialogState:
    """Сохранение обновленного состояния: обновление суммаризации и очистка буфера."""
    service = state['chat_memory_service']
    await service.save_summary_and_clear_buffer(state['new_summary'])


async def append_dialog_to_buffer(state: DialogState) -> DialogState:
    """Добавление текущего диалога (вопрос пользователя + ответ LLM) в буфер."""
    service = state['chat_memory_service']
    new_buffer_messages = await MessageConverter.langchain_to_buffer_messages([state['call_message'], state['response_ai']])

    await service.append_dialog_messages_to_buffer(new_buffer_messages[0], new_buffer_messages[1])

