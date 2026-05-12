from app.services.search.category_service import detect_category
from app.services.search.search_formatter import (
    format_search_results,
    format_search_results_for_agent,
)
from app.services.search.vector_search_service import run_vector_search
from app.services.search.region_service import detect_region
from app.services.search.query_analyzer import detect_naegift_need


async def search_my_incheon_data(
    query: str,
    is_course: bool = False,
    for_agent: bool = False,
    return_raw: bool = False,
):
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
        if return_raw:
            return {
                "formatted_text": f"'{query}'와 유사한 장소를 찾지 못했습니다.",
                "raw_places": [],
            }
        return [] if is_course else f"'{query}'와 유사한 장소를 찾지 못했습니다."

    if is_course:
        return filtered_results

    if for_agent:
        formatted_text = format_search_results_for_agent(filtered_results)
    else:
        formatted_text = format_search_results(filtered_results)

    if return_raw:
        return {
            "formatted_text": formatted_text,
            "raw_places": filtered_results,
        }

    return formatted_text