from pydantic import BaseModel, Field
from langchain_core.tools import Tool

from app.agents.request_store import set_search_places
from app.services.search_service import search_my_incheon_data


class IncheonSearchInput(BaseModel):
    query: str = Field(..., description="사용자 검색 질의")




def build_incheon_tool(
    session_id: str,
    mbti_type: str | None = None,
    sasang_type: str | None = None,
):
    default_mbti_type = mbti_type
    default_sasang_type = sasang_type

    async def run_incheon_search(query: str) -> str:
        result = await search_my_incheon_data(
            query=query,
            is_course=False,
            return_raw=True,
            mbti_type=default_mbti_type or "알수없음",
            sasang_type=default_sasang_type or "알수없음",
        )

        raw_places = result.get("raw_places", [])
        formatted_text = result.get("formatted_text", "")

        print("[DEBUG] tool bound session_id =", session_id)
        print("[DEBUG] raw_places count in tool =", len(raw_places))

        set_search_places(session_id, raw_places)
        return formatted_text

    
    return Tool(
        name="IncheonExpertSearch",
        func=None,
        coroutine=run_incheon_search,
        description=(
            "인천의 관광지, 맛집, 카페 등 장소 정보를 검색할 때 사용한다. "
            "일상적인 잡담이나 단순 인사에는 사용하지 않는다. "
            "사용자는 query만 전달하면 된다."
            "예: 송도 맛집 추천, 인천 데이트 카페 추천"
        ),
    )
