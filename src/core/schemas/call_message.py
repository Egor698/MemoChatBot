from pydantic import BaseModel

class CallMessageSchema(BaseModel):
    """Схема входящего сообщения"""
    content: str
