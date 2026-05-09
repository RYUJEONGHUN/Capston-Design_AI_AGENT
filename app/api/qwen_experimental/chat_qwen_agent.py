from fastapi import APIRouter, Body

from app.agents.qwen_experimental.qwen_agent_executor import get_qwen_agent_executor
from app.services.qwen_experimental.qwen_style_service import rewrite_with_persona

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


def build_qwen_agent_instruction(
    user_input: str,
    mbti_type: str | None = None,
    sasang_type: str | None = None,
) -> str:
    mbti_value = mbti_type if mbti_type else "정보 없음"
    sasang_value = sasang_type if sasang_type else "정보 없음"

    return f"""
너는 사용자의 인천 여행친구이자 여행을 도와주는 가이드야.

[사용자 정보]
- MBTI: {mbti_value}
- 사상체질: {sasang_value}

[사용자 질문]
{user_input}

[도구 선택 규칙]
- 맛집, 카페, 관광지, 가볼만한 곳, 추천 요청이면 반드시 IncheonExpertSearch를 사용해라.
- 여행 코스, 데이트 코스, 반나절 일정, 하루 일정, 동선 요청이면 반드시 IncheonCoursePlanner를 사용해라.
- 인사, 안부, 잡담, 날씨, 기분, 일상 대화는 도구를 사용하지 말고 바로 대화해라.

[잡담 응답 규칙]
- 일반 인사나 잡담이면 장소 추천으로 절대 넘어가지 마라.
- 사용자가 먼저 추천을 요청하지 않았다면 맛집, 관광지, 카페, 코스를 절대 제안하지 마라.
- 날씨처럼 실시간 정보가 필요한 질문은 현재 직접 확인할 수 없다고 솔직하게 말해라.
- 실시간 정보를 모를 때는 절대 지어내지 마라.
- 잡담 응답은 2~4문장 이내로 짧고 자연스럽게 작성해라.

[추천 응답 규칙]
- 도구 결과에 없는 장소를 지어내지 마라.
- Final Answer에서는 추천 장소를 2~3곳 제시해라.
- 각 장소마다 추천 이유를 1문장씩 써라.
- 사용자의 MBTI와 사상체질 정보를 자연스럽게 반영해라.
- 너무 짧게 끝내지 말고 전체 답변은 5~8문장 정도로 작성해라.

[출력 규칙]
- 반드시 한국어로만 답해라.
- Thought, Action, Observation 같은 내부 표현은 Final Answer에 절대 드러내지 마라.
- 도구를 사용하지 않는 경우에는 일반 대화만 하고 추천은 하지 마라.
- 사용자가 추천을 요청하지 않은 경우, 답변 안에 장소 이름을 넣지 마라.
""".strip()


@router.post("/chat/qwen-agent")
async def chat_qwen_agent(
    user_input: str = Body(..., embed=True),
    persona_type: str = Body("BEAR", embed=True),
    mbti_type: str = Body(None, embed=True),
    sasang_type: str = Body(None, embed=True),
):
    try:
        agent_executor = get_qwen_agent_executor()

        instruction = build_qwen_agent_instruction(
            user_input=user_input,
            mbti_type=mbti_type,
            sasang_type=sasang_type,
        )

        agent_result = await agent_executor.ainvoke({"input": instruction})

        answer = agent_result.get("output", "")
        intermediate_steps = agent_result.get("intermediate_steps", [])

        response_type = parse_response_type(intermediate_steps)
        is_course = response_type == "course"

        # 2차 스타일 패스: 페르소나 말투만 반영
        styled_answer = await rewrite_with_persona(
            draft_answer=answer,
            persona_type=persona_type,
        )

        return {
            "answer": styled_answer,
            "rawAnswer": answer,
            "isCourse": is_course,
            "responseType": response_type,
            "provider": "qwen-agent",
        }

    except Exception as e:
        return {
            "error": str(e),
            "isCourse": False,
            "responseType": "error",
            "provider": "qwen-agent",
        }