from langchain_aws import ChatBedrock
from langchain_aws import BedrockEmbeddings
from app.core.config import settings

# LLM 초기화
llm = ChatBedrock(
    model_id=settings.MODEL_ID,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION_NAME,
    model_kwargs={"temperature": 0.7}
)

# 임베딩 모델 초기화
embeddings = BedrockEmbeddings(
    model_id=settings.EMBEDDING_ID, 
    region_name=settings.AWS_REGION_NAME,
    credentials_profile_name=None # 세팅에 맞게 조절
)