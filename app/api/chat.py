from fastapi import APIRouter, Body

from app.agents.executor import get_agent_executor
from app.agents.prompts import build_chat_instruction


router = APIRouter()


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
        
        agent_executor = get_agent_executor(session_id)

        instruction = build_chat_instruction(
            user_input=user_input,
            persona_type=persona_type,
            mbti_type=mbti_type,
            sasang_type=sasang_type,
        )

        agent_result = await agent_executor.ainvoke({"input": instruction})

        answer = agent_result.get("output", "")
        intermediate_steps = agent_result.get("intermediate_steps", [])

        response_type = parse_response_type(intermediate_steps)
        is_course = response_type == "course"

        return {
            "answer": answer,
            "isCourse": is_course,
            "responseType": response_type,
            "provider": "claude",
        }

    except Exception as e:
        return {
            "error": str(e),
            "isCourse": False,
            "responseType": "error",
            "provider": "claude",
        }