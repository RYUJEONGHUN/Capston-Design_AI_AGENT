def format_search_results(results: list[dict]) -> str:
    formatted = []

    for r in results:
        companion_tags = []
        if r.get("isFamily"):
            companion_tags.append("가족")
        if r.get("isSole"):
            companion_tags.append("혼자")
        if r.get("isCouple"):
            companion_tags.append("커플")
        if r.get("isFriend"):
            companion_tags.append("친구")

        info = (
            f"[[검색데이터]]\n"
            f"장소명: {r.get('PlaceName', '')}\n"
            f"주소: {r.get('Address', '')}\n"
            f"지역: {r.get('Region', '')}\n"
            f"카테고리: {r.get('category', '')}\n"
            f"세부카테고리: {r.get('subCategory', '')}\n"
            f"분위기 태그: {r.get('Tags', [])}\n"
            f"MBTI 태그: {r.get('mbtiTags', [])}\n"
            f"사상체질 태그: {r.get('sasangTags', [])}\n"
            f"추천 동행: {companion_tags}\n"
            f"평점: {r.get('Rating', '')}\n"
            f"위도(Y): {r.get('Y', '')}\n"
            f"경도(X): {r.get('X', '')}\n"
            f"이미지: {r.get('ImageURL', '')}\n"
            f"설명: {r.get('Comment', '')}\n"
            f"내기프트 연계 ID: {r.get('naegiftId', '')}\n"
            f"유사도 점수: {r.get('score', 0):.4f}"
        )
        formatted.append(info)

    return "\n\n".join(formatted)



def build_places_metadata(results: list[dict]) -> list[dict]:
    places = []

    for idx, item in enumerate(results, start=1):
        places.append({
            "rank": idx,
            "placeName": item.get("PlaceName"),
            "category": item.get("category"),
            "subCategory": item.get("subCategory"),
            "address": item.get("Address"),
            "region": item.get("Region"),
            "rating": item.get("Rating"),
            "kakaoId": item.get("KakaoId"),
            "imageUrl": item.get("ImageURL"),
            "x": item.get("X"),
            "y": item.get("Y"),
            "naegiftId": item.get("naegiftId"),
        })

    return places



def _safe_join_tags(value, limit: int = 4) -> str:
    if isinstance(value, list):
        return ", ".join(str(v) for v in value[:limit])
    if value is None:
        return ""
    return str(value)


def format_search_results_for_agent(results: list[dict]) -> str:
    formatted = []

    for r in results[:3]:
        info = (
            f"장소명: {r.get('PlaceName', '')}\n"
            f"주소: {r.get('Address', '')}\n"
            f"지역: {r.get('Region', '')}\n"
            f"세부카테고리: {r.get('subCategory', '')}\n"
            f"분위기 태그: {_safe_join_tags(r.get('Tags'), 4)}\n"
            f"MBTI 태그: {_safe_join_tags(r.get('mbtiTags'), 2)}\n"
            f"사상체질 태그: {_safe_join_tags(r.get('sasangTags'), 2)}\n"
            f"평점: {r.get('Rating', '')}\n"
            f"설명: {str(r.get('Comment', ''))[:160]}"
        )
        formatted.append(info)

    return "\n\n".join(formatted)