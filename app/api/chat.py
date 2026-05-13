from fastapi import APIRouter, Body

from app.agents.executor import get_agent_executor
from app.agents.memory import clear_memory, get_clean_chat_history_text, save_clean_chat_turn
from app.agents.request_store import (
    clear_search_places,
    get_search_places,
    clear_course_route,
    get_course_route,
)
from app.services.search.search_formatter import build_places_metadata
from app.services.course.route_formatter import build_route_metadata

router = APIRouter()


@router.post("/chat/reset")
async def reset_chat_memory(
    session_id: str = Body("guest_user", embed=True),
):
    clear_memory(session_id)
    clear_search_places(session_id)
    clear_course_route(session_id)
    return {
        "ok": True,
        "session_id": session_id,
    }


def parse_response_type(intermediate_steps: list) -> str:
    for step in intermediate_steps:
        try:
            action = step[0]
            tool_name = getattr(action, "tool", None)

            if tool_name == "IncheonCoursePlanner":
                return "course"
            if tool_name == "IncheonExpertSearch":
                return "search"
        except Exception:
            continue

    return "chat"


@router.post("/chat")
async def chat(
    user_input: str = Body(..., embed=True),
    session_id: str = Body("guest_user", embed=True),
    persona_type: str = Body("BEAR", embed=True),
    mbti_type: str = Body(None, embed=True),
    sasang_type: str = Body(None, embed=True),
):
    try:
        clear_search_places(session_id)
        clear_course_route(session_id)

        print("[DEBUG] incoming session_id =", session_id)

        agent_executor = get_agent_executor(
            session_id=session_id,
            persona_type=persona_type,
            mbti_type=mbti_type,
            sasang_type=sasang_type,
        )

        agent_result = await agent_executor.ainvoke(
            {
                "input": user_input,
                "chat_history": get_clean_chat_history_text(session_id),
            }
        )

        answer = agent_result.get("output", "")
        intermediate_steps = agent_result.get("intermediate_steps", [])

        response_type = parse_response_type(intermediate_steps)
        is_course = response_type == "course"

        raw_places = get_search_places(session_id)
        places = build_places_metadata(raw_places) if response_type == "search" else []

        raw_route = get_course_route(session_id)
        route = build_route_metadata(raw_route) if response_type == "course" else []

        save_clean_chat_turn(session_id, user_input, answer)

        clear_search_places(session_id)
        clear_course_route(session_id)

        return {
            "answer": answer,
            "isCourse": is_course,
            "responseType": response_type,
            "provider": "claude",
            "places": places,
            "route": route,
        }

    except Exception as e:
        clear_search_places(session_id)
        clear_course_route(session_id)
        return {
            "error": str(e),
            "isCourse": False,
            "responseType": "error",
            "provider": "claude",
            "places": [],
            "route": [],
        }
