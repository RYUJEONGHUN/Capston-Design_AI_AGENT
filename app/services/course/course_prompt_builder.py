from app.agents.prompts import COURSE_PLANNING_GUIDE
from app.core.persona import PERSONA_CONFIG
from app.core.sasang_profile import build_64_profile_prompt_guide, build_sasang_prompt_guide
from app.services.course.query_analyzer import extract_region_keywords


def build_course_context(
    query: str,
    persona_type: str,
    mbti_type: str,
    sasang_type: str,
    route_text: str,
) -> str:
    persona = PERSONA_CONFIG.get(persona_type, PERSONA_CONFIG["BEAR"])

    current_name = persona["name"]
    persona_prompt = persona["prompt"]
    current_closing = persona["closing"]

    region_keywords = extract_region_keywords(query)
    region_text = ", ".join(region_keywords) if region_keywords else "명시되지 않음"
    sasang_guide = build_sasang_prompt_guide(sasang_type)
    profile_64_guide = build_64_profile_prompt_guide(mbti_type, sasang_type)

    return (
        f"### [시스템 모드: {current_name}] ###\n"
        f"너의 정체성과 말투 지침: {persona_prompt}\n\n"
        f"--- [사용자 맞춤형 프로필] ---\n"
        f"- 사용자 MBTI: {mbti_type}\n"
        f"- 사용자 사상의학 체질: {sasang_type}\n"
        f"- 사상체질 추천 가이드: {sasang_guide}\n"
        f"- MBTI+사상체질 64유형 가이드: {profile_64_guide}\n\n"
        f"사용자의 실제 요청: {query}\n"
        f"- 시작/중심 지역 힌트: {region_text}\n\n"
        f"{route_text}\n\n"
        f"--- [코스 작성 가이드] ---\n"
        f"{COURSE_PLANNING_GUIDE}\n\n"
        f"--- [추가 지시] ---\n"
        f"- 추천 이유는 반드시 {current_name}의 페르소나 말투를 유지할 것.\n"
        f"- 사용자가 특정 시작 지역이나 중심 지역을 언급했다면 그 지역 중심으로 동선을 해석할 것.\n"
        f"- 코스가 불필요하게 다른 권역으로 크게 퍼지지 않도록 설명할 것.\n"
        f"- restaurants 순서에서는 반드시 category가 restaurants인 장소만 식사 장소로 소개할 것.\n"
        f"- places 장소를 식당처럼 해석하거나 식사 장소로 대체하지 말 것.\n"
        f"- cafes 장소를 관광지나 식당처럼 바꿔 해석하지 말 것.\n"
        f"- MBTI와 사상체질은 route_text에 포함된 mbtiTags, sasangTags와 64유형 가이드를 참고하여 자연스럽게 반영할 것.\n"
        f"- 64유형은 한의학적 검증, 의학적 판단, 성격 단정이 아니라 관광 추천용 취향 참고값으로만 표현할 것.\n"
        f"- 확보된 데이터가 부족하면 솔직하게 말하고, 무리하게 지어내지 말 것.\n"
        f"- 마지막 문장은 {current_closing} 느낌으로 마무리할 것.\n"
        f"- 전체 답변은 1500토큰 이내로 작성할 것."
    )
