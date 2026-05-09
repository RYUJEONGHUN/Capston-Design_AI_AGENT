from pathlib import Path
import sys
import asyncio

BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from app.data.mongo import db

async def main():
    doc = await db["incheon_contents"].find_one(
        {"embedding": {"$exists": True}},
        {"embedding": 1}
    )
    print("임베딩 차원 수:", len(doc["embedding"]))

if __name__ == "__main__":
    asyncio.run(main())