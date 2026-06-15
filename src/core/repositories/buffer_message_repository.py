from sqlalchemy import select, func, delete
from sqlalchemy.sql.functions import coalesce

from src.core.db.models import BufferMessage

from src.core.repositories.base_repository import BaseRepository


class BufferMessageRepository(BaseRepository):
    async def get_messages(self, user_id: int) -> list[BufferMessage]:
        """Получить сообщения в порядке диалога и новые в конце списка"""
        query = (select(BufferMessage)
                .where(BufferMessage.user_id == user_id)
                .order_by(BufferMessage.buffered_at.asc(), BufferMessage.role.desc()))

        result = await self.session.scalars(query)

        return list(result)


    async def get_buffer_size(self, user_id: int) -> int:
        """Получить количество сообщений в буфере пользователя"""
        query = (select(func.coalesce(func.count(BufferMessage.id), 0))
                 .where(BufferMessage.user_id == user_id))

        count = await self.session.scalar(query)

        return count


    async def add_dialog_messages(self, human_message: BufferMessage, ai_message: BufferMessage):
        """Добавить сообщения в буфер"""

        self.session.add(human_message)
        await self.session.flush()

        self.session.add(ai_message)
        await self.session.flush()


    async def delete_all_messages(self, user_id: int):
        """Удалить все сообщения пользователя из буфера"""
        query = (delete(BufferMessage)
                .where(BufferMessage.user_id == user_id))

        await self.session.execute(query)

