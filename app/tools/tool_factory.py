from app.tools.incheon_tool import build_incheon_tool
from app.tools.course_tool import build_incheon_course_tool


def build_session_tools(session_id: str):
    return [
        build_incheon_tool(session_id),
        build_incheon_course_tool(session_id),
    ]