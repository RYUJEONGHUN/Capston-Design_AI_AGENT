from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

from app.agents.request_store import set_search_places
from app.services.search_service import search_my_incheon_data


class IncheonSearchInput(BaseModel):
    query: str = Field(..., description="사용자 검색 질의")


def build_incheon_tool(session_id: str):
    async def run_incheon_search(query: str) -> str:
        result = await search_my_incheon_data(
            query=query,
            is_course=False,
            return_raw=True,
        )

        raw_places = result.get("raw_places", [])
        formatted_text = result.get("formatted_text", "")

        print("[DEBUG] tool bound session_id =", session_id)
        print("[DEBUG] raw_places count in tool =", len(raw_places))

        set_search_places(session_id, raw_places)
        return formatted_text

    return StructuredTool.from_function(
        name="IncheonExpertSearch",
        coroutine=run_incheon_search,
        args_schema=IncheonSearchInput,
        description=(
            "인천의 관광지, 맛집, 카페 등 장소 정보를 검색할 때 사용한다. "
            "일상적인 잡담이나 단순 인사에는 사용하지 않는다. "
            "사용자는 query만 전달하면 된다."
            "사용자 요청 query를 입력받아 관련 장소 검색 결과를 반환한다."

        ),
    )
