from langchain_openai import ChatOpenAI
from app.core.config import settings


def get_llm():
    return ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.2,
        openai_api_key=settings.openai_api_key
    )
