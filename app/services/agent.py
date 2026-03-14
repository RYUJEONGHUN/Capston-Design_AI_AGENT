from langchain_aws import ChatBedrock
from langchain_classic.agents import initialize_agent, AgentType
from langchain_classic.memory import ConversationBufferMemory
from app.core.config import settings
from app.tools.incheon_tool import incheon_tool
from langchain_aws import BedrockEmbeddings

# LLM 초기화
llm = ChatBedrock(
    model_id=settings.MODEL_ID,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION_NAME,
    model_kwargs={"temperature": 0.7}
)

# 메모리 및 에이전트 설정
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent_executor = initialize_agent(
    tools=[incheon_tool],
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True
)


# 임베딩 모델 초기화
embeddings = BedrockEmbeddings(
    model_id=settings.EMBEDDING_ID, 
    region_name=settings.AWS_REGION_NAME,
    credentials_profile_name=None # 세팅에 맞게 조절
)