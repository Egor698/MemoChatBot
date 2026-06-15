from langchain_openai import ChatOpenAI

from src.config import settings

base_llm = ChatOpenAI(base_url=settings.OPENAI_BASE_URL,
                 api_key=settings.OPENAI_API_KEY,
                 model=settings.BASE_MODEL)


summarization_llm = ChatOpenAI(base_url=settings.OPENAI_BASE_URL,
                 api_key=settings.OPENAI_API_KEY,
                 model=settings.SUMMARIZATION_MODEL,
                 temperature=0.2)