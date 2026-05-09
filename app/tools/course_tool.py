from langchain_core.tools import StructuredTool

from app.services.course_service import plan_incheon_full_course

incheon_course_tool = StructuredTool.from_function(
    name="IncheonCoursePlanner",
    coroutine=plan_incheon_full_course,
    description=(
        "인천 여행 코스, 데이트 코스, 반나절 일정, 하루 일정 추천이 필요할 때 사용하는 도구다. "
        "사용자 요청(query)과 persona_type, mbti_type, sasang_type을 입력받아 "
        "관광지와 맛집을 조합한 코스용 데이터를 생성한다"
    ),
)