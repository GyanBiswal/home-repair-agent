from langchain_groq import ChatGroq

from repair_agent.config import GROQ_API_KEY, GROQ_MODEL, check_config


def get_llm(temperature: float = 0.0) -> ChatGroq:
    check_config()
    return ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=temperature)