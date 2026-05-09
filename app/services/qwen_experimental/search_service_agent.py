from app.services.search.category_service import detect_category
from app.services.search.vector_search_service import run_vector_search


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
            f"세부카테고리: {r.get('subCategory', '')}\n"
            f"분위기 태그: {_safe_join_tags(r.get('Tags'), 4)}\n"
            f"MBTI 태그: {_safe_join_tags(r.get('mbtiTags'), 2)}\n"
            f"사상체질 태그: {_safe_join_tags(r.get('sasangTags'), 2)}\n"
            f"평점: {r.get('Rating', '')}\n"
            f"설명: {str(r.get('Comment', ''))[:180]}"
        )
        formatted.append(info)

    return "\n\n".join(formatted)


async def search_my_incheon_data_for_agent(query: str) -> str:
    target_category = await detect_category(query)

    filtered_results = await run_vector_search(
        query=query,
        target_category=target_category,
        limit=5,
        score_threshold=0.6,
    )

    if not filtered_results:
        return f"'{query}'와 유사한 장소를 찾지 못했습니다."

    return format_search_results_for_agent(filtered_results)