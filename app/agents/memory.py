from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage

from app.core.config import settings


def get_chat_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(
        url=settings.REDIS_URL,
        session_id=session_id,
        ttl=86400,
    )


def summarize_answer_for_memory(answer: str, max_chars: int = 500) -> str:
    cleaned = " ".join(str(answer or "").split())
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[:max_chars].rstrip() + "..."


def get_clean_chat_history_text(session_id: str, k: int = 6) -> str:
    chat_history = get_chat_history(session_id)
    messages = chat_history.messages[-k * 2 :]

    lines = []
    for message in messages:
        content = " ".join(str(message.content or "").split())
        if not content:
            continue

        if isinstance(message, HumanMessage):
            lines.append(f"사용자: {content}")
        elif isinstance(message, AIMessage):
            lines.append(f"assistant 최종 답변 요약: {content}")

    print("[DEBUG] memory session_id =", session_id)
    return "\n".join(lines)


def save_clean_chat_turn(session_id: str, user_input: str, answer: str) -> None:
    chat_history = get_chat_history(session_id)
    chat_history.add_user_message(str(user_input or "").strip())
    chat_history.add_ai_message(summarize_answer_for_memory(answer))


def clear_memory(session_id: str) -> None:
    get_chat_history(session_id).clear()
