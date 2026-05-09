from langchain_core.tools import StructuredTool

from app.services.qwen_experimental.search_service_agent import (
    search_my_incheon_data_for_agent,
)


async def run_incheon_search_for_qwen_agent(query: str) -> str:
    return await search_my_incheon_data_for_agent(query)


incheon_tool_agent = StructuredTool.from_function(
    name="IncheonExpertSearch",
    coroutine=run_incheon_search_for_qwen_agent,
    description=(
        "인천의 관광지, 맛집, 카페 등 장소 정보를 검색할 때 사용한다. "
        "일상적인 잡담이나 단순 인사에는 사용하지 않는다. "
        "사용자 요청 query를 입력받아 관련 장소 검색 결과를 반환한다."
    ),
)