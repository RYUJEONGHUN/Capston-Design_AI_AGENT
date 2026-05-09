import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "us-east-1")

    # Bedrock 모델
    MODEL_ID = "us.anthropic.claude-sonnet-4-6"
    EMBEDDING_ID = "amazon.titan-embed-text-v2:0"

    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://incheon_mate-redis:6379/0")


settings = Settings()