from fastapi import APIRouter, Body

from app.core.qwen_client import generate_with_qwen
from app.agents.qwen_prompts import (
    build_qwen_search_prompt,
    build_qwen_course_prompt,
    truncate_context,
)
from app.services.search_service import search_my_incheon_data
from app.services.course_service import plan_incheon_full_course
from app.services.qwen_router_service import choose_tool_with_qwen

router = APIRouter()


def detect_is_course_query(user_input: str) -> bool:
    course_keywords = ["코스", "일정", "데이트 코스", "반나절", "하루 코스", "여행 코스", "동선"]
    return any(keyword in user_input for keyword in course_keywords)


@router.post("/chat/qwen")
async def chat_qwen(
    user_input: str = Body(..., embed=True),
    persona_type: str = Body("BEAR", embed=True),
    mbti_type: str = Body(None, embed=True),
    sasang_type: str = Body(None, embed=True),
):
    try:
        is_course = detect_is_course_query(user_input)

        if is_course:
            course_result = await plan_incheon_full_course(
                query=user_input,
                persona_type=persona_type,
                mbti_type=mbti_type or "알수없음",
                sasang_type=sasang_type or "알수없음",
            )

            course_result = truncate_context(course_result, max_chars=3200)

            prompt = build_qwen_course_prompt(
                user_input=user_input,
                course_result_text=course_result,
                persona_type=persona_type,
                mbti_type=mbti_type,
                sasang_type=sasang_type,
            )

            answer = await generate_with_qwen(
                prompt=prompt,
                max_new_tokens=500,
                temperature=0.0,
            )

            return {
                "answer": answer,
                "isCourse": True,
                "responseType": "course",
                "provider": "qwen",
            }

        search_result = await search_my_incheon_data(user_input, is_course=False)
        search_result = truncate_context(search_result, max_chars=2200)

        prompt = build_qwen_search_prompt(
            user_input=user_input,
            search_result_text=search_result,
            persona_type=persona_type,
            mbti_type=mbti_type,
            sasang_type=sasang_type,
        )

        answer = await generate_with_qwen(
            prompt=prompt,
            max_new_tokens=500,
            temperature=0.0,
        )

        return {
            "answer": answer,
            "isCourse": False,
            "responseType": "search",
            "provider": "qwen",
        }

    except Exception as e:
        return {
            "error": str(e),
            "isCourse": False,
            "responseType": "error",
            "provider": "qwen",
        }


@router.post("/chat/qwen/tool-choice")
async def qwen_tool_choice(
    user_input: str = Body(..., embed=True),
):
    try:
        tool = await choose_tool_with_qwen(user_input)

        return {
            "user_input": user_input,
            "tool": tool,
            "provider": "qwen",
        }

    except Exception as e:
        return {
            "error": str(e),
            "provider": "qwen",
        }