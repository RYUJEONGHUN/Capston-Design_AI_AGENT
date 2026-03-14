import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "us-east-1")
    # 사용할 모델 ID (Claude 3.5 Sonnet 추천)
    MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    EMBEDDING_ID = "amazon.titan-embed-text-v2:0"

settings = Settings()