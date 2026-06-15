from pydantic import BaseModel

class AnswerMessageSchema(BaseModel):
    """Схема полученного ответа от LLM"""
    content: str