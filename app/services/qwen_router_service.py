from app.core.qwen_client import generate_with_qwen


def normalize_tool_choice(text: str) -> str:
    text = text.strip()

    if "IncheonCoursePlanner" in text:
        return "IncheonCoursePlanner"
    if "IncheonExpertSearch" in text:
        return "IncheonExpertSearch"
    if "CHAT" in text:
        return "CHAT"

    lowered = text.lower()
    if "course" in lowered or "코스" in text or "일정" in text:
        return "IncheonCoursePlanner"
    if "맛집" in text or "카페" in text or "관광지" in text or "추천" in text:
        return "IncheonExpertSearch"

    return "CHAT"


async def choose_tool_with_qwen(user_input: str) -> str:
    prompt = f"""
너의 역할은 사용자의 질문을 보고 사용할 도구 이름 하나만 고르는 것이다.

선택 가능한 값은 아래 셋뿐이다.
- IncheonExpertSearch
- IncheonCoursePlanner
- CHAT

규칙:
- 반드시 셋 중 하나만 정확히 출력해라.
- 다른 설명은 절대 쓰지 마라.
- 장소/맛집/카페/관광지 추천이면 IncheonExpertSearch
- 여행 코스/데이트 코스/반나절 일정/하루 일정이면 IncheonCoursePlanner
- 일반 잡담/인사/도구가 필요 없는 대화면 CHAT

질문: {user_input}
답:
""".strip()

    result = await generate_with_qwen(
        prompt=prompt,
        max_new_tokens=20,
        temperature=0.0,
    )

    return normalize_tool_choice(result)