import pandas as pd
from pymongo import MongoClient

def load_data_to_mongo():
    # 1. MongoDB 연결 (컨테이너 이름 사용)
    client = MongoClient("mongodb://incheon_mate-mongo:27017")
    db = client["incheon_mate_db"]
    
    # 2. 각 파일 로드 및 삽입
    files = {
        "places": "관광지.csv", # 파일명을 정훈님 로컬 환경에 맞춰 수정하세요
        "restaurants": "식당.csv",
        "cafes": "카페.csv"
    }
    
    for category, file_path in files.items():
        df = pd.read_csv(file_path)
        # 데이터 정제 (NaN 제거 등)
        data = df.to_dict(orient='records')
        
        # 'incheon_data'라는 하나의 컬렉션에 넣고 'category'로 구분
        for item in data:
            item['type'] = category
            
        db.incheon_data.insert_many(data)
        print(f"{category} 데이터 삽입 완료!")

if __name__ == "__main__":
    load_data_to_mongo()