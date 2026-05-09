from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory

from app.core.config import settings


def get_memory(session_id: str) -> ConversationBufferWindowMemory:
    chat_history = RedisChatMessageHistory(
        url=settings.REDIS_URL,
        session_id=session_id,
        ttl=86400,
    )

    return ConversationBufferWindowMemory(
        memory_key="chat_history",
        chat_memory=chat_history,
        return_messages=True,
        k=5,
    )