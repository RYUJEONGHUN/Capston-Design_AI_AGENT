import asyncio
from app.core.database import db
from app.services.agent import embeddings 

async def migrate_incheon_data_to_vectors():
    print(" 벡터 마이그레이션 시작...")
    collection = db.incheon_contents
    
    # 1. 모든 데이터 가져오기
    cursor = collection.find({})
    items = await cursor.to_list(length=200)
    
    for item in items:
        # 2. 임베딩할 '통합 문장' 만들기
        # 이름, 태그, 설명을 합쳐야 검색이 풍부해집니다.
        combined_text = f"장소: {item['PlaceName']}. 태그: {item['Tags']}. 설명: {item['Comment']}"
        
        # 3. 임베딩 생성 (Titan 모델 호출)
        vector = await embeddings.aembed_query(combined_text)
        print(f"생성된 벡터 차원: {len(vector)}") 

        # 4. DB 업데이트 (embedding 필드 추가)
        await collection.update_one(
            {"_id": item["_id"]},
            {"$set": {"embedding": vector}}
        )
        print(f" 완료: {item['PlaceName']}")

    print(" 모든 데이터에 벡터가 생성되었습니다!")

if __name__ == "__main__":
    asyncio.run(migrate_incheon_data_to_vectors())