from app.services.course.query_analyzer import (
    extract_food_keywords,
    extract_mood_keywords,
    extract_region_keywords,
)
from app.core.sasang_profile import (
    get_64_profile_keywords,
    get_mbti_keywords,
    get_sasang_keywords,
    has_known_mbti_type,
    has_known_sasang_type,
    normalize_mbti_type,
    normalize_sasang_type,
)


def _normalize_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(str(v).strip() for v in value if str(v).strip())
    return str(value).strip()


def deduplicate_places(items: list[dict]) -> list[dict]:
    seen = set()
    deduped = []

    for item in items:
        name = _normalize_text(item.get("PlaceName"))
        if not name or name in seen:
            continue
        seen.add(name)
        deduped.append(item)

    return deduped


def is_ambiguous_restaurant(item: dict) -> bool:
    name = _normalize_text(item.get("PlaceName"))
    category = _normalize_text(item.get("category"))
    sub_category = _normalize_text(item.get("subCategory"))

    if category != "restaurants":
        return False

    suspicious_keywords = ["거리", "시장", "골목", "상권", "테마거리", "문화거리"]
    if any(keyword in name for keyword in suspicious_keywords):
        return True

    if not sub_category and any(keyword in name for keyword in suspicious_keywords):
        return True

    return False


def build_item_text(item: dict) -> str:
    parts = [
        _normalize_text(item.get("PlaceName")),
        _normalize_text(item.get("Address")),
        _normalize_text(item.get("Region")),
        _normalize_text(item.get("Comment")),
        _normalize_text(item.get("Tags")),
        _normalize_text(item.get("subCategory")),
        _normalize_text(item.get("mbtiTags")),
        _normalize_text(item.get("sasangTags")),
    ]
    return " ".join(part for part in parts if part)


def score_candidate_by_region(item: dict, region_keywords: list[str]) -> int:
    if not region_keywords:
        return 0

    score = 0
    region_text = " ".join(
        [
            _normalize_text(item.get("Region")),
            _normalize_text(item.get("Address")),
            _normalize_text(item.get("PlaceName")),
        ]
    )

    for region in region_keywords:
        if region in region_text:
            score += 14

    return score


def score_candidate_by_food(item: dict, food_keywords: list[str]) -> int:
    if not food_keywords:
        return 0

    text = build_item_text(item)
    score = 0
    for food in food_keywords:
        if food in text:
            score += 15
    return score


def score_candidate_by_mood(item: dict, mood_keywords: list[str]) -> int:
    if not mood_keywords:
        return 0

    text = build_item_text(item)
    score = 0

    mood_map = {
        "데이트": ["데이트", "기념일", "야경", "오션뷰", "로맨틱", "분위기좋은", "커플"],
        "조용한": ["조용한", "차분한", "아늑한", "고요함"],
        "감성": ["감성", "빈티지", "레트로", "LP", "한옥", "고풍", "근대건축", "옛날감성"],
        "야경": ["야경", "노을", "전망", "조명", "오션뷰", "뷰맛집"],
        "오션뷰": ["오션뷰", "바다", "노을", "전망"],
        "로맨틱": ["데이트", "기념일", "야경", "오션뷰", "분위기좋은"],
        "분위기": ["분위기좋은", "감성", "차분한", "아늑한", "고풍"],
        "차분한": ["차분한", "조용한", "고요함"],
        "아늑한": ["아늑한", "조용한", "차분한"],
        "힐링": ["힐링", "산책", "고요함", "자연", "공원"],
        "산책": ["산책", "공원", "도보", "길", "누리길"],
        "뷰": ["전망", "뷰맛집", "오션뷰", "노을"],
        "노을": ["노을", "야경", "오션뷰", "전망"],
    }

    for mood in mood_keywords:
        related_terms = mood_map.get(mood, [mood])
        for term in related_terms:
            if term in text:
                score += 8

    return score


def score_candidate_by_mbti(item: dict, mbti_type: str) -> int:
    if not has_known_mbti_type(mbti_type):
        return 0

    normalized_mbti = normalize_mbti_type(mbti_type)
    mbti_tags = _normalize_text(item.get("mbtiTags"))
    text = build_item_text(item)

    score = 0
    if mbti_tags and normalized_mbti in mbti_tags.upper():
        score += 10

    for keyword in get_mbti_keywords(normalized_mbti):
        if keyword in text:
            score += 2

    return min(score, 20)


def score_candidate_by_sasang(item: dict, sasang_type: str) -> int:
    if not has_known_sasang_type(sasang_type):
        return 0

    normalized_sasang = normalize_sasang_type(sasang_type)
    sasang_tags = _normalize_text(item.get("sasangTags"))
    text = build_item_text(item)

    score = 0
    if sasang_tags and normalized_sasang in sasang_tags:
        score += 10

    for keyword in get_sasang_keywords(normalized_sasang):
        if keyword in text:
            score += 3

    return min(score, 22)


def score_candidate_by_64_profile(item: dict, mbti_type: str, sasang_type: str) -> int:
    if not has_known_mbti_type(mbti_type) or not has_known_sasang_type(sasang_type):
        return 0

    text = build_item_text(item)
    keywords = get_64_profile_keywords(mbti_type, sasang_type)
    keyword_hits = sum(1 for keyword in keywords if keyword in text)

    mbti_tags = _normalize_text(item.get("mbtiTags")).upper()
    sasang_tags = _normalize_text(item.get("sasangTags"))
    normalized_mbti = normalize_mbti_type(mbti_type)
    normalized_sasang = normalize_sasang_type(sasang_type)

    score = min(keyword_hits * 2, 12)
    if normalized_mbti in mbti_tags and normalized_sasang in sasang_tags:
        score += 12

    return min(score, 24)


def sort_place_candidates(
    items: list[dict],
    query: str,
    mbti_type: str = "알수없음",
    sasang_type: str = "알수없음",
) -> list[dict]:
    region_keywords = extract_region_keywords(query)
    mood_keywords = extract_mood_keywords(query)

    def candidate_score(item: dict):
        base_score = float(item.get("score", 0.0) or 0.0)
        region_bonus = score_candidate_by_region(item, region_keywords)
        mood_bonus = score_candidate_by_mood(item, mood_keywords)
        mbti_bonus = score_candidate_by_mbti(item, mbti_type)
        sasang_bonus = score_candidate_by_sasang(item, sasang_type)
        profile_64_bonus = score_candidate_by_64_profile(item, mbti_type, sasang_type)

        text = build_item_text(item)
        penalty = 0
        if any(keyword in query for keyword in ["데이트", "감성", "조용한"]):
            if any(bad in text for bad in ["아이와함께", "체험학습", "토끼", "나비", "실내테마파크"]):
                penalty += 10

        return -(
            base_score * 100
            + region_bonus
            + mood_bonus
            + mbti_bonus
            + sasang_bonus
            + profile_64_bonus
            - penalty
        )

    return sorted(items, key=candidate_score)


def sort_restaurant_candidates(
    items: list[dict],
    query: str,
    mbti_type: str = "알수없음",
    sasang_type: str = "알수없음",
) -> list[dict]:
    region_keywords = extract_region_keywords(query)
    food_keywords = extract_food_keywords(query)
    mood_keywords = extract_mood_keywords(query)

    filtered = []
    for item in items:
        if is_ambiguous_restaurant(item):
            continue
        if _normalize_text(item.get("category")) != "restaurants":
            continue
        filtered.append(item)

    def candidate_score(item: dict):
        base_score = float(item.get("score", 0.0) or 0.0)
        region_bonus = score_candidate_by_region(item, region_keywords)
        food_bonus = score_candidate_by_food(item, food_keywords)
        mood_bonus = score_candidate_by_mood(item, mood_keywords)
        mbti_bonus = score_candidate_by_mbti(item, mbti_type)
        sasang_bonus = score_candidate_by_sasang(item, sasang_type)
        profile_64_bonus = score_candidate_by_64_profile(item, mbti_type, sasang_type)
        sub_category_bonus = 5 if item.get("subCategory") else 0
        rating_bonus = float(item.get("Rating", 0.0) or 0.0) * 2

        return -(
            base_score * 100
            + region_bonus
            + food_bonus
            + mood_bonus
            + mbti_bonus
            + sasang_bonus
            + profile_64_bonus
            + sub_category_bonus
            + rating_bonus
        )

    return sorted(filtered, key=candidate_score)


def select_course_candidates(
    places_list: list[dict],
    restaurants_list: list[dict],
    query: str,
    mbti_type: str = "알수없음",
    sasang_type: str = "알수없음",
    max_places: int = 3,
    max_restaurants: int = 2,
) -> tuple[list[dict], list[dict]]:
    places = deduplicate_places(places_list)
    restaurants = deduplicate_places(restaurants_list)

    places = sort_place_candidates(
        places,
        query=query,
        mbti_type=mbti_type,
        sasang_type=sasang_type,
    )
    restaurants = sort_restaurant_candidates(
        restaurants,
        query=query,
        mbti_type=mbti_type,
        sasang_type=sasang_type,
    )

    return places[:max_places], restaurants[:max_restaurants]
