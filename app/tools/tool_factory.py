from app.tools.incheon_tool import build_incheon_tool
from app.tools.course_tool import build_incheon_course_tool


def build_session_tools(
    session_id: str,
    persona_type: str = "BEAR",
    mbti_type: str | None = None,
    sasang_type: str | None = None,
):
    return [
        build_incheon_tool(
            session_id,
            mbti_type=mbti_type,
            sasang_type=sasang_type,
        ),
        build_incheon_course_tool(
            session_id,
            persona_type=persona_type,
            mbti_type=mbti_type,
            sasang_type=sasang_type,
        ),
    ]
