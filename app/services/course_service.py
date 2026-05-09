import asyncio

from app.services.search_service import search_my_incheon_data
from app.services.course.candidates import select_course_candidates
from app.services.course.optimizer import annotate_route, find_best_course_route
from app.services.course.route_formatter import format_route_data
from app.services.course.course_prompt_builder import build_course_context


async def plan_incheon_full_course(
    query: str,
    persona_type: str = "BEAR",
    mbti_type: str = "알수없음",
    sasang_type: str = "알수없음",
) -> str:
    try:
        places_task = search_my_incheon_data(
            f"{query} 관광지",
            is_course=True,
        )
        restaurants_task = search_my_incheon_data(
            f"{query} 맛집",
            is_course=True,
        )

        places_list, restaurants_list = await asyncio.gather(
            places_task,
            restaurants_task,
        )

        places_list = places_list or []
        restaurants_list = restaurants_list or []

        candidate_places, candidate_restaurants = select_course_candidates(
            places_list,
            restaurants_list,
            query=query,
            mbti_type=mbti_type,
            sasang_type=sasang_type,
            max_places=3,
            max_restaurants=2,
        )

        best_route, total_distance = find_best_course_route(
            candidate_places,
            candidate_restaurants,
            query=query,
        )

        annotated_route = annotate_route(best_route)
        route_text = format_route_data(annotated_route, total_distance)

    except Exception as e:
        print(f"코스 생성 중 에러 발생: {e}")
        route_text = "추천 가능한 코스 데이터를 생성하지 못했습니다."

    return build_course_context(
        query=query,
        persona_type=persona_type,
        mbti_type=mbti_type,
        sasang_type=sasang_type,
        route_text=route_text,
    )