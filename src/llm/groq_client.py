from langchain_groq import ChatGroq
from src.config.settings import settings

def get_groq_llm():
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.model_name,
        temperature=settings.temperature
    )