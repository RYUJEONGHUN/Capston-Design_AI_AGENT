UNKNOWN_SASANG_VALUES = {"", "알수없음", "정보 없음", "미상"}
UNKNOWN_MBTI_VALUES = {"", "알수없음", "정보 없음", "미상"}


MBTI_PROFILES = {
    "ISTJ": {"keywords": ["전통", "역사", "정돈", "안정", "계획", "조용"], "guide": "계획적이고 안정적인 코스, 검증된 장소를 선호한다."},
    "ISFJ": {"keywords": ["따뜻", "안정", "휴식", "전통", "가족", "조용"], "guide": "편안하고 배려가 느껴지는 장소, 부담 없는 동선을 선호한다."},
    "INFJ": {"keywords": ["조용", "감성", "전시", "산책", "의미", "차분"], "guide": "의미 있고 조용한 감성 장소, 생각을 정리할 수 있는 코스를 선호한다."},
    "INTJ": {"keywords": ["전망", "건축", "전시", "역사", "계획", "집중"], "guide": "짜임새 있고 관찰 포인트가 분명한 장소를 선호한다."},
    "ISTP": {"keywords": ["체험", "산책", "야외", "전망", "실용", "자유"], "guide": "자유롭게 보고 체감할 수 있는 실용적인 코스를 선호한다."},
    "ISFP": {"keywords": ["감성", "카페", "자연", "사진", "아늑", "여유"], "guide": "감각적으로 편안하고 사진 찍기 좋은 장소, 여유롭게 머무는 코스를 선호한다."},
    "INFP": {"keywords": ["감성", "조용", "책", "전시", "산책", "카페"], "guide": "조용히 깊게 머무를 수 있는 감성적인 코스를 선호한다."},
    "INTP": {"keywords": ["전시", "역사", "건축", "책", "탐색", "조용"], "guide": "스스로 탐색할 여지가 있고 호기심을 자극하는 장소를 선호한다."},
    "ESTP": {"keywords": ["활동", "체험", "야외", "시장", "맛집", "전망"], "guide": "즉흥적으로 즐길 수 있는 활동적이고 생동감 있는 장소를 선호한다."},
    "ESFP": {"keywords": ["핫플", "맛집", "사진", "체험", "활기", "카페"], "guide": "분위기가 살아 있고 사진과 대화거리가 많은 코스를 선호한다."},
    "ENFP": {"keywords": ["감성", "체험", "카페", "산책", "이색", "자유"], "guide": "새롭고 변화감 있는 장소, 감성과 체험이 섞인 코스를 선호한다."},
    "ENTP": {"keywords": ["이색", "체험", "전시", "시장", "탐색", "활기"], "guide": "예상 밖의 재미와 이야깃거리가 있는 탐색형 코스를 선호한다."},
    "ESTJ": {"keywords": ["계획", "맛집", "전통", "명소", "효율", "안정"], "guide": "시간 대비 만족도가 높고 효율적인 코스를 선호한다."},
    "ESFJ": {"keywords": ["맛집", "가족", "카페", "전통", "활기", "편안"], "guide": "동행자가 함께 편하게 즐길 수 있는 균형 잡힌 코스를 선호한다."},
    "ENFJ": {"keywords": ["감성", "전망", "맛집", "산책", "대화", "기념일"], "guide": "함께 이야기 나누기 좋고 분위기와 만족도가 균형 잡힌 코스를 선호한다."},
    "ENTJ": {"keywords": ["전망", "고급", "명소", "효율", "계획", "핫플"], "guide": "핵심 명소를 효율적으로 잇고 인상이 강한 장소를 선호한다."},
}


SASANG_PROFILES = {
    "태양인": {"keywords": ["전망", "바다", "산책", "개방감", "활동", "야외"], "guide": "개방감 있는 전망, 가벼운 산책, 답답하지 않은 야외 동선을 우선한다."},
    "태음인": {"keywords": ["휴식", "자연", "공원", "든든한", "여유", "전통"], "guide": "무리하지 않는 여유로운 동선, 자연과 휴식, 든든한 식사 경험을 우선한다."},
    "소양인": {"keywords": ["시원", "바다", "전망", "산책", "활동", "가벼운"], "guide": "시원하고 변화감 있는 장소, 짧고 경쾌한 이동, 가벼운 활동을 우선한다."},
    "소음인": {"keywords": ["조용", "따뜻", "실내", "카페", "휴식", "차분"], "guide": "조용하고 안정적인 분위기, 부담 적은 동선, 따뜻하고 편안한 장소를 우선한다."},
}


SASANG_MBTI_NAMES = {
    "태양인": {
        "ENTJ": ("대담한 통솔자", "스티브 잡스형. 비전을 제시하고 앞에서 이끄는 혁신적 CEO 성향."),
        "INTJ": ("용의주도한 전략가", "일론 머스크형. 큰 목표를 세우고 전략적으로 현실화하는 성향."),
        "ENTP": ("뜨거운 논쟁을 즐기는 변론가", "혁신적인 스타트업 창업가형. 새 아이디어와 도전을 즐기는 성향."),
        "INTP": ("논리적인 사색가", "아인슈타인형. 이치를 탐구하고 새 패러다임을 제시하는 성향."),
        "ENFJ": ("정의로운 사회운동가", "마틴 루터 킹 목사형. 카리스마와 연설력으로 사람을 움직이는 성향."),
        "INFJ": ("선의의 옹호자", "잔 다르크형. 신념과 직관을 바탕으로 목표를 향하는 성향."),
        "ENFP": ("재기발랄한 활동가", "세상을 바꾸는 크리에이터형. 열정과 창의력으로 에너지를 전하는 성향."),
        "INFP": ("열정적인 중재자", "존 레논형. 평화와 이상을 예술적 메시지로 전하는 성향."),
        "ESTJ": ("엄격한 관리자", "철혈 재상형. 원칙과 카리스마로 조직을 이끄는 성향."),
        "ISTJ": ("청렴결백한 논리주의자", "대법원장형. 신념과 원칙으로 정의를 구현하려는 성향."),
        "ESFJ": ("사교적인 외교관", "카리스마 있는 친화형. 넓은 인맥과 친화력으로 모임을 이끄는 성향."),
        "ISFJ": ("용감한 수호자", "나를 구하는 영웅형. 중요한 사람과 목적을 위해 묵묵히 버티는 성향."),
        "ESTP": ("모험을 즐기는 사업가", "리처드 브랜슨형. 도전을 즐기고 타고난 승부사 기질을 보이는 성향."),
        "ISTP": ("만능 재주꾼", "최첨단 기술 발명가형. 직관과 기술력으로 가능성을 여는 성향."),
        "ESFP": ("자유로운 영혼의 연예인", "글로벌 팝스타형. 압도적인 에너지로 분위기를 이끄는 성향."),
        "ISFP": ("호기심 많은 예술가", "아방가르드 아티스트형. 독창적인 감각으로 새로움을 만드는 성향."),
    },
    "태음인": {
        "ESTJ": ("엄격한 관리자", "워런 버핏형. 원칙과 성실함으로 안정적으로 목표를 달성하는 성향."),
        "ISTJ": ("청렴결백한 논리주의자", "정주영 명예회장형. 근면함과 인내심으로 역경을 이겨내는 성향."),
        "ESFJ": ("사교적인 외교관", "든든한 맏형 리더형. 포용력으로 사람들을 따뜻하게 품는 성향."),
        "ISFJ": ("용감한 수호자", "마더 테레사형. 타인을 위해 헌신하며 안정감을 주는 성향."),
        "ENTJ": ("대담한 통솔자", "장기스칸형. 리더십에 끈기와 인내를 더해 큰 목표를 추진하는 성향."),
        "INTJ": ("용의주도한 전략가", "제갈량형. 깊은 통찰과 장기적 안목으로 문제를 풀어가는 성향."),
        "ENTP": ("뜨거운 논쟁을 즐기는 변론가", "실용적인 발명가형. 아이디어를 현실적인 결과로 연결하는 성향."),
        "INTP": ("논리적인 사색가", "우직한 학자형. 한 분야를 깊이 파고드는 탐구 성향."),
        "ENFJ": ("정의로운 사회운동가", "만델라형. 오래 버티는 포용력으로 사람들을 이끄는 성향."),
        "INFJ": ("선의의 옹호자", "묵묵한 조언자형. 공감과 통찰로 사람의 마음을 치유하려는 성향."),
        "ENFP": ("재기발랄한 활동가", "친근한 동네 이장님형. 긍정적인 에너지로 사람을 챙기는 성향."),
        "INFP": ("열정적인 중재자", "자연 친화적 시인형. 자연과 평화를 지향하고 내면을 표현하는 성향."),
        "ESTP": ("모험을 즐기는 사업가", "자수성가형 사업가. 현실 감각과 뚝심으로 추진하는 성향."),
        "ISTP": ("만능 재주꾼", "명장형. 묵묵히 기술을 갈고닦는 성향."),
        "ESFP": ("자유로운 영혼의 연예인", "강호동형. 친화력과 듬직함, 에너지로 분위기를 살리는 성향."),
        "ISFP": ("호기심 많은 예술가", "우직한 예술가형. 자기 색깔을 꾸준히 담아내는 성향."),
    },
    "소양인": {
        "ESFP": ("자유로운 영혼의 연예인", "유재석형. 에너지와 친화력으로 분위기를 주도하는 성향."),
        "ESTP": ("모험을 즐기는 사업가", "손흥민형. 빠른 반응과 열정으로 무대를 장악하는 성향."),
        "ENFP": ("재기발랄한 활동가", "인간 비타민형. 톡톡 튀는 아이디어와 긍정 에너지의 성향."),
        "ENTP": ("뜨거운 논쟁을 즐기는 변론가", "유쾌한 트렌드세터형. 언변과 재치로 이목을 끄는 성향."),
        "ESFJ": ("사교적인 외교관", "열정적인 파티 호스트형. 사람 만나는 것을 좋아하는 성향."),
        "ESTJ": ("엄격한 관리자", "행동파 리더형. 빠른 판단력과 추진력으로 팀을 이끄는 성향."),
        "ENTJ": ("대담한 통솔자", "카리스마 넘치는 CEO형. 빠른 판단과 추진력으로 목표를 향하는 성향."),
        "ENFJ": ("정의로운 사회운동가", "열혈 행동가형. 사람들을 이끌어 적극적으로 행동하는 성향."),
        "ISFP": ("호기심 많은 예술가", "트렌디한 아티스트형. 유행에 민감하고 감각적인 재능을 담는 성향."),
        "ISTP": ("만능 재주꾼", "익스트림 스포츠 마니아형. 스릴과 모험을 즐기는 성향."),
        "ISFJ": ("용감한 수호자", "의리파 친구형. 속정이 깊고 필요한 친구를 챙기는 성향."),
        "ISTJ": ("청렴결백한 논리주의자", "신속 정확한 해결사형. 빠른 판단으로 효율적으로 해결하는 성향."),
        "INFP": ("열정적인 중재자", "감수성 풍부한 로맨티스트형. 풍부한 감수성을 표현하는 성향."),
        "INFJ": ("선의의 옹호자", "정열적인 이상주의자형. 이상을 실현하려는 열정이 있는 성향."),
        "INTP": ("논리적인 사색가", "번뜩이는 아이디어 뱅크형. 호기심과 아이디어가 많은 성향."),
        "INTJ": ("용의주도한 전략가", "민첩한 전략가형. 빠른 분석과 통찰로 전략을 세우는 성향."),
    },
    "소음인": {
        "ISTJ": ("청렴결백한 논리주의자", "유형열형/철저한 분석가형. 계획적으로 처리하는 성향."),
        "ISFJ": ("용감한 수호자", "따뜻한 치유자형. 세심한 배려로 조용히 돌보는 성향."),
        "INFJ": ("선의의 옹호자", "깊이 있는 학자/구도자형. 깊게 분석하고 훈련하는 성향."),
        "INTJ": ("용의주도한 전략가", "치밀한 설계자형. 분석과 통찰로 계획을 세우는 성향."),
        "ISTP": ("만능 재주꾼", "정밀한 세공사형. 예리한 관찰력으로 정밀하게 다루는 성향."),
        "ISFP": ("호기심 많은 예술가", "아이유형/섬세한 아티스트형. 섬세한 감수성과 감각의 성향."),
        "INTP": ("논리적인 사색가", "깊이 있는 학자형. 혼자 깊이 연구하고 분석하는 성향."),
        "INFP": ("열정적인 중재자", "감성적인 작가형. 내면과 감정을 글과 예술로 표현하는 성향."),
        "ESTJ": ("엄격한 관리자", "깐깐한 완벽주의 리더형. 원칙과 관리로 운영하는 성향."),
        "ESFJ": ("사교적인 외교관", "세심한 행정가형. 작은 변화를 놓치지 않고 챙기는 성향."),
        "ENFJ": ("정의로운 사회운동가", "설득력 있는 멘토형. 공감과 논리로 마음을 움직이는 성향."),
        "ENTJ": ("대담한 통솔자", "분석적인 전략 리더형. 데이터를 바탕으로 전략을 수립하는 성향."),
        "ESTP": ("모험을 즐기는 사업가", "신중한 승부사형. 현실 감각과 계산으로 추진하는 성향."),
        "ESFP": ("자유로운 영혼의 연예인", "엔터테이너형. 활발하지만 보이지 않는 곳에서 노력하는 성향."),
        "ENTP": ("뜨거운 논쟁을 즐기는 변론가", "예리한 비평가형. 분석과 논리로 새 시각을 제시하는 성향."),
        "ENFP": ("재기발랄한 활동가", "섬세한 아이디어 뱅크형. 창의성과 현실성을 함께 따지는 성향."),
    },
}


def normalize_mbti_type(mbti_type: str | None) -> str:
    if not mbti_type:
        return ""
    return str(mbti_type).strip().upper()


def normalize_sasang_type(sasang_type: str | None) -> str:
    if not sasang_type:
        return ""
    return str(sasang_type).strip()


def has_known_mbti_type(mbti_type: str | None) -> bool:
    normalized = normalize_mbti_type(mbti_type)
    return normalized not in UNKNOWN_MBTI_VALUES and normalized in MBTI_PROFILES


def has_known_sasang_type(sasang_type: str | None) -> bool:
    normalized = normalize_sasang_type(sasang_type)
    return normalized not in UNKNOWN_SASANG_VALUES and normalized in SASANG_PROFILES


def get_mbti_keywords(mbti_type: str | None) -> list[str]:
    normalized = normalize_mbti_type(mbti_type)
    return MBTI_PROFILES.get(normalized, {}).get("keywords", [])


def get_sasang_keywords(sasang_type: str | None) -> list[str]:
    normalized = normalize_sasang_type(sasang_type)
    return SASANG_PROFILES.get(normalized, {}).get("keywords", [])


def get_64_profile(mbti_type: str | None, sasang_type: str | None) -> dict:
    mbti = normalize_mbti_type(mbti_type)
    sasang = normalize_sasang_type(sasang_type)
    name, summary = SASANG_MBTI_NAMES.get(sasang, {}).get(mbti, ("", ""))
    if not name:
        return {}
    return {
        "name": name,
        "summary": summary,
        "keywords": get_64_profile_keywords(mbti, sasang),
    }


def get_64_profile_keywords(mbti_type: str | None, sasang_type: str | None) -> list[str]:
    if not has_known_mbti_type(mbti_type) or not has_known_sasang_type(sasang_type):
        return []

    keywords = []
    for keyword in get_mbti_keywords(mbti_type) + get_sasang_keywords(sasang_type):
        if keyword not in keywords:
            keywords.append(keyword)
    return keywords


def build_sasang_prompt_guide(sasang_type: str | None) -> str:
    normalized = normalize_sasang_type(sasang_type)
    profile = SASANG_PROFILES.get(normalized)
    if not profile:
        return "사상체질 정보가 없으면 장소 데이터와 사용자 요청을 우선한다."

    return (
        f"{normalized} 여행 추천 가이드: {profile['guide']} "
        "단, 의학적 진단처럼 단정하지 말고 추천 이유에 자연스럽게만 반영한다."
    )


def build_64_profile_prompt_guide(mbti_type: str | None, sasang_type: str | None) -> str:
    mbti = normalize_mbti_type(mbti_type)
    sasang = normalize_sasang_type(sasang_type)

    if not has_known_mbti_type(mbti) and not has_known_sasang_type(sasang):
        return "MBTI와 사상체질 정보가 없으면 사용자 요청과 장소 데이터를 우선한다."
    if not has_known_mbti_type(mbti):
        return build_sasang_prompt_guide(sasang)
    if not has_known_sasang_type(sasang):
        return f"{mbti} 여행 성향 가이드: {MBTI_PROFILES[mbti]['guide']} 단, 성격을 단정하지 말고 자연스럽게만 반영한다."

    profile = get_64_profile(mbti, sasang)
    keywords = ", ".join(get_64_profile_keywords(mbti, sasang))
    return (
        f"{sasang}+{mbti} 64유형: {profile['name']}. {profile['summary']} "
        f"MBTI 기준으로는 {MBTI_PROFILES[mbti]['guide']} "
        f"사상체질 기준으로는 {SASANG_PROFILES[sasang]['guide']} "
        f"추천 키워드는 {keywords}이다. "
        "이 조합은 과학적 진단이 아니라 관광 추천용 취향 참고값으로만 사용한다."
    )
