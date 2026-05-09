import os
from dotenv import load_dotenv 
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

# MongoDB 설정
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client[os.getenv("MONGO_DB_NAME", "incheon_mate")]

