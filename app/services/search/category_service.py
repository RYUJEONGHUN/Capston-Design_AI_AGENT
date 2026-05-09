from langchain_core.prompts import PromptTemplate

from app.core.factory import llm

CATEGORY_MAP = {
    "관광지": "places",
    "식당": "restaurants",
    "카페": "cafes",
    "숙박": "stays",
}

CATEGORY_EXTRACT_PROMPT = PromptTemplate.from_template(
    """
사용자의 질문을 분석해서 가장 적합한 카테고리 하나만 골라줘: [관광지, 식당, 카페, 숙박].
만약 질문이 특정 카테고리를 가리키지 않는다면 'None'이라고 답해줘.
오직 단어 하나만 출력해.

질문: {query}
카테고리:
"""
)


async def detect_category(query: str) -> str | None:
    category_response = await llm.ainvoke(
        CATEGORY_EXTRACT_PROMPT.format(query=query)
    )
    detected_korean = category_response.content.strip()
    return CATEGORY_MAP.get(detected_korean)