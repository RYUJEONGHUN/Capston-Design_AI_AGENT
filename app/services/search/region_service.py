from langchain_core.prompts import PromptTemplate

from app.core.factory import llm

REGION_KEYWORDS = [
    # --- 행정구 (필수) ---
    "중구", "연수구", "남동구", "미추홀구", "서구", "부평구", "계양구", "동구", "강화군", "옹진군",

    # --- 주요 거점 및 동네 (데이터 출처 기준) ---
    "송도", "청라", "영종도", "부평", "구월동", "논현동", "주안", "학익동", "도화동",
    "계산동", "작전동", "검단", "가좌동", "옥련동", "동춘동", "만수동", "숭의동",
    
    # --- 관광 및 특수 지역 (데이터 및 주소 기준) ---
    "강화도", "영흥도", "차이나타운", "월미도", "을왕리", "마시란", "신포동", "인현동"
]


REGION_EXTRACT_PROMPT = PromptTemplate.from_template(
    """
사용자의 질문에서 지역 또는 장소 권역을 가장 잘 대표하는 단어 하나만 골라줘.

선택 가능 후보:
[{region_candidates}]

규칙:
- 반드시 후보 중 하나만 출력해.
- 해당되는 지역이 없으면 None만 출력해.
- 다른 설명은 절대 하지 마.

질문: {query}
지역:
"""
)


def detect_region_by_rule(query: str) -> str | None:
    for keyword in REGION_KEYWORDS:
        if keyword in query:
            return keyword
    return None


async def detect_region(query: str) -> str | None:
    try:
        prompt = REGION_EXTRACT_PROMPT.format(
            query=query,
            region_candidates=", ".join(REGION_KEYWORDS),
        )
        response = await llm.ainvoke(prompt)
        detected = response.content.strip()

        if detected in REGION_KEYWORDS:
            return detected
    except Exception:
        pass

    return detect_region_by_rule(query)