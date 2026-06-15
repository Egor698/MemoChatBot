import uuid
from datetime import datetime
from typing import Literal

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import BigInteger, func, CheckConstraint


class Base(DeclarativeBase):
    pass


class Summary(Base):
    __tablename__ = 'user_summaries'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    content: Mapped[str]


class BufferMessage(Base):
    __tablename__ = 'chat_message_buffer'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column(BigInteger)

    role: Mapped[Literal["ai", "human"]]
    content: Mapped[str]
    buffered_at: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())

    __table_args__ = (CheckConstraint("""role IN ('ai', 'human')""", name="check_role_valid"), )
