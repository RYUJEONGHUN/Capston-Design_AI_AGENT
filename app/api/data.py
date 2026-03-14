from fastapi import APIRouter
import pandas as pd
from app.core.database import db

router = APIRouter(tags=["Data Management"])

@router.get("/init-data")
async def init_data():
    files = {
        "places": "app/data/관광지.csv",
        "restaurants": "app/data/식당.csv",
        "cafes": "app/data/카페.csv"
    }
    total_count = 0 
    try:
        await db.incheon_contents.delete_many({}) 
        for category, file_path in files.items():
            df = pd.read_csv(file_path, encoding='cp949')
            df = df.fillna("")
            items = df.to_dict(orient='records')
            for item in items:
                item['category'] = category 
            
            if items:
                await db.incheon_contents.insert_many(items)
                total_count += len(items)
        return {"status": "success", "message": f"총 {total_count}개 저장 완료!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/check-data")
async def check_data():
    sample = await db.incheon_contents.find_one({})
    if sample:
        sample["_id"] = str(sample["_id"])
        return {"status": "found", "sample": sample}
    return {"status": "empty", "message": "데이터가 없습니다."}