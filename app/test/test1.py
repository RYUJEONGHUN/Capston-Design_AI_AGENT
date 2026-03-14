import asyncio
from app.core.database import db
from app.services.agent import embeddings # 정훈님의 임베딩 모델

async def test_vector_search():
    # 1. 사용자의 질문 (테스트용)
    query = "바다가 보이는 조용한 카페 추천해줘"
    
    # 2. 질문을 벡터로 변환 (1024차원)
    query_vector = await embeddings.aembed_query(query)
    
    # 3. MongoDB Vector Search 실행
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index", # 아까 지은 인덱스 이름
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": 100, # 후보군 수
                "limit": 5 # 최종 결과 개수
            }
        },
        {
            "$project": {
                "PlaceName": 1,
                "Comment": 1,
                "score": {"$meta": "vectorSearchScore"} # 유사도 점수
            }
        }
    ]
    
    cursor = db.incheon_contents.aggregate(pipeline)
    results = await cursor.to_list(length=5)
    
    print(f"\n🔍 '{query}' 검색 결과:")
    for res in results:
        print(f"📍 {res['PlaceName']} (점수: {res['score']:.4f})")
        print(f"📝 {res.get('Comment', '설명 없음')[:50]}...")
        print("-" * 30)

if __name__ == "__main__":
    asyncio.run(test_vector_search())