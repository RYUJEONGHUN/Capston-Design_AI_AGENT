from app.core.qwen_client import generate_with_qwen
from app.core.persona import PERSONA_CONFIG


async def rewrite_with_persona(
    draft_answer: str,
    persona_type: str = "BEAR",
) -> str:
    if not draft_answer.strip():
        return draft_answer

    persona = PERSONA_CONFIG.get(persona_type, PERSONA_CONFIG["BEAR"])
    persona_info = persona["prompt"]

    prompt = f"""
너는 답변 스타일만 다듬는 역할이다.

페르소나:
{persona_info}

원본 답변:
{draft_answer}

규칙:
- 원본 내용의 사실을 바꾸지 마라.
- 장소 이름을 바꾸지 마라.
- 없는 정보를 추가하지 마라.
- 말투와 분위기만 페르소나에 맞게 자연스럽게 바꿔라.
- 너무 과장하지 말고 자연스럽게 유지해라.
- 문장 길이와 정보량은 원본과 비슷하게 유지해라.
- 한국어로만 답해라.
""".strip()

    styled = await generate_with_qwen(
        prompt=prompt,
        max_new_tokens=320,
        temperature=0.0,
    )

    return styled.strip() if styled.strip() else draft_answer