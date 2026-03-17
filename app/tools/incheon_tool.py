from langchain_core.tools import Tool
from app.core.database import db
from app.core.factory import embeddings, llm # agent.py에 정의된 객체 사용
from langchain_core.prompts import PromptTemplate

# AI가 판단할 기준 
CATEGORY_MAP = {
    "관광지": "places",
    "식당": "restaurants",
    "카페": "cafes"
}

CATEGORY_EXTRACT_PROMPT = PromptTemplate.from_template("""
사용자의 질문을 분석해서 가장 적합한 카테고리 하나만 골라줘: [관광지, 식당, 카페].
만약 질문이 특정 카테고리를 가리키지 않는다면 'None'이라고 답해줘.
오직 단어 하나만 출력해.

질문: {query}
카테고리:""")

async def search_my_incheon_data(query: str):
    print(f" 에이전트 판단 질문: {query}") 
    
    # AI가 질문에서 카테고리 추출
    category_response = await llm.ainvoke(CATEGORY_EXTRACT_PROMPT.format(query=query))
    detected_korean = category_response.content.strip()
    
    # 한글 카테고리를 DB용 영어 값으로 변환
    target_category = CATEGORY_MAP.get(detected_korean) # 매핑결과 없으면 None
    print(f" AI 판단: {detected_korean} -> DB 필터: {target_category}")

    # Vector Search 쿼리 구성
    query_vector = await embeddings.aembed_query(query)
    search_config = {
        "index": "vector_index",
        "path": "embedding",
        "queryVector": query_vector,
        "numCandidates": 100,
        "limit": 5
    }

    # 변환된 영어 값이 있을 때만 필터 적용
    if target_category:
        search_config["filter"] = { "category": target_category }

    pipeline = [
        { "$vectorSearch": search_config },
        { "$project": { 
            "PlaceName": 1, "category": 1, "Comment": 1, 
            "X": 1, "Y": 1, "ImageURL": 1, "Tags": 1,
            "score": { "$meta": "vectorSearchScore" } 
        }}
    ]
    
    cursor = db.incheon_contents.aggregate(pipeline)
    results = await cursor.to_list(length=5)
        
    filtered_results = [r for r in results if r['score'] >= 0.6]

    if not filtered_results:
        return f"'{query}'와 충분히 유사한 장소를 찾지 못했습니다. 조금 더 구체적으로 물어봐 주시겠어요?"
    
    
    # 결과를 에이전트가 읽기 좋게 포맷팅
    formatted = []
    for r in filtered_results:
        info = (
            f"[[검색데이터]]\n"
            f"장소명: {r['PlaceName']}\n"
            f"이 장소의 분위기 태그: {r.get('Tags', '')}\n"
            f"카테고리: {r.get('category', '')}\n"
            f"위도(Y): {r.get('Y', '')}\n"
            f"경도(X): {r.get('X', '')}\n"
            f"이미지: {r.get('ImageURL', '')}\n"
            f"설명: {r['Comment']}\n"
            f"태그: {r.get('Tags', '')}\n"
            f"유사도 점수: {r['score']:.4f}"
        )
        formatted.append(info)
    
    return "\n\n".join(formatted)


incheon_tool = Tool(
    name="IncheonExpertSearch",
    func=None, # 동기 함수 자리
    coroutine=search_my_incheon_data, # 비동기 함수 자리
    description=(
        "인천의 관광지, 맛집, 장소 정보를 검색할 때만 사용하세요. "
        "사용자가 단순히 인사를 하거나, 본인의 정보를 말하거나, 이전 대화를 기억하는지 묻는 등 "
        "일상적인 대화를 할 때는 절대로 이 도구를 호출하지 마세요."
    )
)