from pathlib import Path
import sys
import asyncio

# 프로젝트 루트를 sys.path에 추가
BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from app.data.mongo import db
from app.core.factory import embeddings


COLLECTION_NAME = "incheon_contents"
BATCH_SIZE = 50


def normalize_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(str(v).strip() for v in value if v is not None and str(v).strip())
    return str(value).strip()


def build_embedding_text(doc: dict) -> str:
    place_name = normalize_text(doc.get("PlaceName"))
    category = normalize_text(doc.get("category"))
    sub_category = normalize_text(doc.get("subCategory"))
    region = normalize_text(doc.get("Region"))
    tags = normalize_text(doc.get("Tags"))
    comment = normalize_text(doc.get("Comment"))

    parts = [
        f"장소명: {place_name}",
        f"카테고리: {category}",
        f"세부카테고리: {sub_category}",
        f"지역: {region}",
        f"태그: {tags}",
        f"설명: {comment}",
    ]

    return "\n".join(part for part in parts if part.split(": ", 1)[1]).strip()


async def embed_texts(texts: list[str]) -> list[list[float]]:
    # 구현체가 aembed_documents를 지원하면 그걸 우선 사용
    if hasattr(embeddings, "aembed_documents"):
        return await embeddings.aembed_documents(texts)

    # fallback: 하나씩 query 임베딩
    vectors = await asyncio.gather(*(embeddings.aembed_query(text) for text in texts))
    return vectors


async def update_batch_embeddings(batch: list[dict]):
    texts = [build_embedding_text(doc) for doc in batch]
    vectors = await embed_texts(texts)

    update_tasks = []
    for doc, text, vector in zip(batch, texts, vectors):
        update_tasks.append(
            db[COLLECTION_NAME].update_one(
                {"_id": doc["_id"]},
                {
                    "$set": {
                        "embeddingText": text,
                        "embedding": vector,
                    }
                },
            )
        )

    await asyncio.gather(*update_tasks)


async def main():
    print("임베딩 채우기 시작")

    collection = db[COLLECTION_NAME]
    total = await collection.count_documents({})
    done = 0

    print(f"전체 문서 수: {total}")

    cursor = collection.find(
        {},
        {
            "_id": 1,
            "PlaceName": 1,
            "category": 1,
            "subCategory": 1,
            "Region": 1,
            "Tags": 1,
            "Comment": 1,
         
        },
    )

    batch = []

    async for doc in cursor:
        batch.append(doc)

        if len(batch) >= BATCH_SIZE:
            await update_batch_embeddings(batch)
            done += len(batch)
            print(f"{done}/{total} 문서 처리 완료")
            batch = []

    if batch:
        await update_batch_embeddings(batch)
        done += len(batch)
        print(f"{done}/{total} 문서 처리 완료")

    print("임베딩 채우기 완료")


if __name__ == "__main__":
    asyncio.run(main())