from langchain_core.tools import Tool
from app.core.database import db

async def search_my_incheon_data(query: str):
    print(f" 에이전트가 요청한 검색어: {query}") 
    
    cursor = db.incheon_contents.find({
        "$or": [
            {"PlaceName": {"$regex": query, "$options": "i"}},
            {"Tags": {"$regex": query, "$options": "i"}},
            {"Comment": {"$regex": query, "$options": "i"}}
        ]
    }).limit(3)
    
    results = await cursor.to_list(length=3)
    print(f" 검색 결과 개수: {len(results)}개")

    if not results:
        # 검색 결과가 없을 때 에이전트에게 가이드를 줍니다.
        return f"'{query}'와 관련된 장소를 정훈님의 데이터에서 찾지 못했습니다. 태그명(예: #ISTP, #역사)으로 다시 검색해보세요."
    
    formatted = []
    for r in results:
        # DB의 원본 데이터를 'Raw Data'라고 명시해서 전달
        info = (
            f"[[원본데이터]]\n"
            f"장소명: {r['PlaceName']}\n"
            f"위도(Y): {r.get('Y', '')}\n"
            f"경도(X): {r.get('X', '')}\n"
            f"이미지: {r.get('Image', '')}\n"
            f"설명: {r['Comment']}\n"
            f"태그: {r['Tags']}"
        )
        formatted.append(info)
    
    return "\n\n".join(formatted)

incheon_tool = Tool(
    name="IncheonExpertSearch",
    func=None, # 동기 함수 자리
    coroutine=search_my_incheon_data, # 비동기 함수 자리
    description="인천의 관광지 데이터를 검색할 때 사용하세요."
)