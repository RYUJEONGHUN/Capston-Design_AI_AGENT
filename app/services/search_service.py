from app.services.search.category_service import detect_category
from app.services.search.region_service import detect_region
from app.services.search.query_analyzer import detect_naegift_need
from app.services.search.search_formatter import format_search_results
from app.services.search.vector_search_service import run_vector_search


async def search_my_incheon_data(query: str, is_course: bool = False):
    target_category = await detect_category(query)
    region = await detect_region(query)
    require_naegift = detect_naegift_need(query)

    filtered_results = await run_vector_search(
        query=query,
        target_category=target_category,
        region=region,
        require_naegift=require_naegift,
        limit=5,
        score_threshold=0.45,
    )

    if not filtered_results:
        return [] if is_course else f"'{query}'와 유사한 장소를 찾지 못했습니다."

    if is_course:
        return filtered_results

    return format_search_results(filtered_results)