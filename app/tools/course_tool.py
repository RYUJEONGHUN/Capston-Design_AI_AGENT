
from pydantic import BaseModel, Field
from langchain_core.tools import Tool

from app.agents.request_store import set_course_route
from app.services.course_service import plan_incheon_full_course


class IncheonCourseInput(BaseModel):
    query: str = Field(..., description="사용자 코스 생성 질의")
    persona_type: str = Field(default="BEAR")
    mbti_type: str | None = Field(default=None)
    sasang_type: str | None = Field(default=None)


def build_incheon_course_tool(session_id: str):
    async def run_incheon_course(
        query: str,
        persona_type: str = "BEAR",
        mbti_type: str | None = None,
        sasang_type: str | None = None,
    ) -> str:
        result = await plan_incheon_full_course(
            query=query,
            persona_type=persona_type,
            mbti_type=mbti_type or "알수없음",
            sasang_type=sasang_type or "알수없음",
            return_raw=True,
        )

        raw_route = result.get("raw_route", [])
        route_text = result.get("route_text", "")

        print("[DEBUG] route count in tool =", len(raw_route))
        if raw_route:
            print("[DEBUG] first route place =", raw_route[0].get("PlaceName"))

        set_course_route(session_id, raw_route)

        return route_text

    return Tool(
        name="IncheonCoursePlanner",
        func=None,
        coroutine=run_incheon_course,
        description=(
            "인천 여행 코스, 데이트 코스, 반나절 일정, 하루 일정 추천이 필요할 때 사용하는 도구다. "
            "입력은 반드시 문자열 query 하나여야 한다. "
            "예: 송도 반나절 데이트 코스 추천"
        ),
    )
