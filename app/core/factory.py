from botocore.config import Config
from langchain_aws import BedrockEmbeddings, ChatBedrock
from app.core.config import settings
from app.core.qwen_experimental.qwen_http_llm import QwenHTTPLLM


retry_config = Config(
    retries={
        "max_attempts": 10,
        "mode": "standard",
    }
)

llm = ChatBedrock(
    model_id=settings.MODEL_ID,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION_NAME,
    config=retry_config,
    model_kwargs={
        "temperature": 0.7,
        "max_tokens": 4096,
    },
)

embeddings = BedrockEmbeddings(
    model_id=settings.EMBEDDING_ID,
    region_name=settings.AWS_REGION_NAME,
    credentials_profile_name=None,
)



qwen_agent_llm = QwenHTTPLLM(
    temperature=0.0,
    max_new_tokens=300,
)
