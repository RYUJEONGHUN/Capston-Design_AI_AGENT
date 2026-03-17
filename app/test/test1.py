import asyncio
from app.core.database import db
from app.services.agent import embeddings # 정훈님의 임베딩 모델

async def vector_search(query, category=None):
    query_vector = await embeddings.aembed_query(query)
    
    # 기본 검색 조건
    search_config = {
        "index": "vector_index",
        "path": "embedding",
        "queryVector": query_vector,
        "numCandidates": 100,
        "limit": 5
    }

    # 카테고리가 입력되었을 때만 필터 추가
    if category:
        search_config["filter"] = { "Category": category }

    pipeline = [{ "$vectorSearch": search_config }]
    
    
    cursor = db.incheon_contents.aggregate(pipeline)
    results = await cursor.to_list(length=5)
    
    print(f"\n '{query}' 검색 결과:")
    for res in results:
        print(f" {res['PlaceName']} (점수: {res['score']:.4f})")
        print(f" {res.get('Comment', '설명 없음')[:50]}...")
        print("-" * 30)

if __name__ == "__main__":
    asyncio.run(vector_search())