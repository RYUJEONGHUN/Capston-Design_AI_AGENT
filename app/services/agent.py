from langchain_classic.agents import initialize_agent, AgentType
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_classic.memory import ConversationBufferWindowMemory
from app.tools.incheon_tool import incheon_tool
from app.core.factory import llm

# Redis 주소 설정 (컨테이너 이름을 사용하세요)
REDIS_URL = "redis://incheon_mate-redis:6379/0"

def get_memory(session_id: str):
    """세션 ID별로 Redis 대화 기록을 관리하는 메모리 객체 생성"""
    chat_history = RedisChatMessageHistory(
        url=REDIS_URL,
        session_id=session_id,
        ttl=86400  # 24시간 동안 대화 보관
    )
    return ConversationBufferWindowMemory(
        memory_key="chat_history",
        chat_memory=chat_history,
        return_messages=True,
        k=5 # 최근 5개의 대화 묶음을 기억합니다. 
    )

def get_agent_executor(session_id: str):
    """요청마다 개별 메모리를 가진 에이전트를 반환"""
    memory = get_memory(session_id)
    
    return initialize_agent(
        tools=[incheon_tool],
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        handle_parsing_errors=True
    )