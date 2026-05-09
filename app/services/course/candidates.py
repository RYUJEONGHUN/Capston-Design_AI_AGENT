from app.services.course.query_analyzer import (
    extract_food_keywords,
    extract_mood_keywords,
    extract_region_keywords,
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
    if not mbti_type or mbti_type == "알수없음":
        return 0

    mbti_tags = _normalize_text(item.get("mbtiTags"))
    if not mbti_tags:
        return 0

    return 10 if mbti_type in mbti_tags else 0


def score_candidate_by_sasang(item: dict, sasang_type: str) -> int:
    if not sasang_type or sasang_type == "알수없음":
        return 0

    sasang_tags = _normalize_text(item.get("sasangTags"))
    if not sasang_tags:
        return 0

    return 10 if sasang_type in sasang_tags else 0


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

        text = build_item_text(item)
        penalty = 0
        if any(keyword in query for keyword in ["데이트", "감성", "조용한"]):
            if any(bad in text for bad in ["아이와함께", "체험학습", "토끼", "나비", "실내테마파크"]):
                penalty += 10

        return -(base_score * 100 + region_bonus + mood_bonus + mbti_bonus + sasang_bonus - penalty)

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
        sub_category_bonus = 5 if item.get("subCategory") else 0
        rating_bonus = float(item.get("Rating", 0.0) or 0.0) * 2

        return -(
            base_score * 100
            + region_bonus
            + food_bonus
            + mood_bonus
            + mbti_bonus
            + sasang_bonus
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