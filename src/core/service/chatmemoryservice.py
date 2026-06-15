from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.models import BufferMessage, Summary

from src.core.repositories.buffer_message_repository import BufferMessageRepository
from src.core.repositories.summary_repository import SummaryRepository

MAX_BUFFER_SIZE = 6

class ChatMemoryService:
    def __init__(self, active_user: 'UserContext', session: AsyncSession):
        self.active_user = active_user
        self.session = session
        self.message_buffer_repo = BufferMessageRepository(session)
        self.summary_repo = SummaryRepository(session)


    async def get_current_state(self) -> tuple[list[BufferMessage], Summary | None]:
        """Получить текущее состояние: буфер сообщений и существующую суммаризацию"""
        buffered_messages = await self.message_buffer_repo.get_messages(self.active_user.id)
        existing_summary = await self.summary_repo.get_summary_by_user(self.active_user.id)

        return buffered_messages, existing_summary


    async def is_buffer_full(self):
        """Проверить, достиг ли буфер максимального размера"""
        buffer_state = await self.message_buffer_repo.get_buffer_size(self.active_user.id)
        return buffer_state >= MAX_BUFFER_SIZE


    async def append_dialog_messages_to_buffer(self, human_message: BufferMessage, ai_message: BufferMessage):
        """Добавить сообщения в буфер"""
        human_message.user_id = self.active_user.id
        ai_message.user_id = self.active_user.id

        await self.message_buffer_repo.add_dialog_messages(human_message, ai_message)
        await self.session.commit()


    async def save_summary_and_clear_buffer(self, new_summary_content: str):
        """Сохранить суммаризацию и очистить буфер"""
        existing_summary = await self.summary_repo.get_summary_by_user(self.active_user.id)

        if existing_summary is None:
            await self.summary_repo.create_summary(self.active_user.id, new_summary_content)
        else:
            await self.summary_repo.update_summary_content(self.active_user.id, new_summary_content)

        await self.message_buffer_repo.delete_all_messages(self.active_user.id)

        await self.session.commit()








