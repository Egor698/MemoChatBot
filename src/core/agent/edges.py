from src.core.agent.states import DialogState


async def is_need_summarization(state: DialogState):
    """Определяет, вызовет ли дополнительно граф суммаризацию сообщений из буффера."""

    if state['is_need_summarization']:
        return ["generate_conversation_summary", "generate_ai_response_2"]
    else:
        return "generate_ai_response"

