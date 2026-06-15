from sqlalchemy import select, insert, update

from src.core.repositories.base_repository import BaseRepository
from src.core.db.models import Summary

class SummaryRepository(BaseRepository):
    async def get_summary_by_user(self, user_id: int) -> Summary | None:
        """Получить суммаризацию для пользователя"""
        query = (select(Summary)
                 .where(Summary.user_id == user_id))

        result = await self.session.scalar(query)
        return result


    async def update_summary_content(self, user_id: int, new_content: str):
        """Обновить содержимое суммаризации"""
        query = (update(Summary)
                 .values(content=new_content)
                 .where(Summary.user_id == user_id))

        await self.session.execute(query)


    async def create_summary(self, user_id: int, content: str) -> Summary:
        """Создать новую суммаризацию"""
        query = (insert(Summary)
                 .values(content=content,
                         user_id=user_id))

        await self.session.execute(query)


