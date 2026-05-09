from app.core.persona import PERSONA_CONFIG


def truncate_context(text: str, max_chars: int = 2200) -> str:
    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    return text[:max_chars]


def build_qwen_search_prompt(
    user_input: str,
    search_result_text: str,
    persona_type: str = "BEAR",
    mbti_type: str | None = None,
    sasang_type: str | None = None,
) -> str:
    persona = PERSONA_CONFIG.get(persona_type, PERSONA_CONFIG["BEAR"])
    persona_info = persona["prompt"]

    mbti_value = mbti_type if mbti_type else "정보 없음"
    sasang_value = sasang_type if sasang_type else "정보 없음"

    return f"""
너는 인천 여행 추천 비서다.

[페르소나]
{persona_info}

[사용자 정보]
- MBTI: {mbti_value}
- 사상의학 체질: {sasang_value}

[질문]
{user_input}

[검색 결과]
{search_result_text}

규칙:
- 검색 결과에 있는 장소만 사용해라.
- 장소 이름은 검색 결과에 나온 이름 그대로 써라.
- 없는 장소는 절대 지어내지 마라.
- 한국어로만 답해라.
- 최대 3곳까지만 추천해라.
- 각 장소 설명은 2문장 이내로 써라.
- 마지막 답변은 너무 길지 않게 마무리해라.
""".strip()


def build_qwen_course_prompt(
    user_input: str,
    course_result_text: str,
    persona_type: str = "BEAR",
    mbti_type: str | None = None,
    sasang_type: str | None = None,
) -> str:
    persona = PERSONA_CONFIG.get(persona_type, PERSONA_CONFIG["BEAR"])
    persona_info = persona["prompt"]

    mbti_value = mbti_type if mbti_type else "정보 없음"
    sasang_value = sasang_type if sasang_type else "정보 없음"

    return f"""
너는 인천 여행 코스 추천 비서다.

[페르소나]
{persona_info}

[사용자 정보]
- MBTI: {mbti_value}
- 사상의학 체질: {sasang_value}

[질문]
{user_input}

[코스 데이터]
{course_result_text}

규칙:
- 반드시 제공된 코스 데이터만 사용해라.
- 없는 장소를 지어내지 마라.
- 한국어로만 답해라.
- 코스 순서를 유지해서 설명해라.
- 각 장소 설명은 2문장 이내로 써라.
- 마지막 답변은 너무 길지 않게 마무리해라.
""".strip()