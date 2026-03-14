import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def migrate_all_data():
    # 1. 연결 설정
    LOCAL_URI = "mongodb://localhost:27017" # 정훈님의 도커 몽고 주소
    ATLAS_URI = "mongodb+srv://junghunryu4_db_user:0pjCQBp1qDT9nDJR@incheonmate-cluster.qmi6bvl.mongodb.net/?appName=IncheonMate-Cluster"
    
    local_client = AsyncIOMotorClient(LOCAL_URI)
    atlas_client = AsyncIOMotorClient(ATLAS_URI)
    
    # 2. 데이터베이스 선택 (기존에 쓰시던 DB 이름 입력)
    source_db = local_client["incheon_mate_db"] 
    target_db = atlas_client["incheon_mate_db"]
    
    # 3. 존재하는 모든 컬렉션 목록 가져오기
    collections = await source_db.list_collection_names()
    print(f" 이사할 목록: {collections}")
    
    for coll_name in collections:
        print(f" {coll_name} 이동 중...")
        
        # 데이터 읽기
        cursor = source_db[coll_name].find({})
        data = await cursor.to_list(length=None) # 전체 데이터
        
        if data:
            # Atlas에 데이터 밀어넣기
            await target_db[coll_name].insert_many(data)
            print(f" {coll_name} 완료! ({len(data)}건)")
        else:
            print(f" {coll_name}는 비어있어서 건너뜁니다.")

    print("\n 모든 데이터가 Atlas로 안전하게 복사되었습니다!")

if __name__ == "__main__":
    asyncio.run(migrate_all_data())