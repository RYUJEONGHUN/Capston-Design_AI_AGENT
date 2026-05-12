from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory

from app.core.config import settings


def get_memory(session_id: str) -> ConversationBufferWindowMemory:
    chat_history = RedisChatMessageHistory(
        url=settings.REDIS_URL,
        session_id=session_id,
        ttl=86400,
    )

    memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        chat_memory=chat_history,
        return_messages=False,
        input_key="input",
        output_key="output",
        k=10,
    )

    print("[DEBUG] memory session_id =", session_id)
    print("[DEBUG] loaded memory vars =", memory.load_memory_variables({}))

    return memory