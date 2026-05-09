from itertools import permutations

from app.services.course.distance import safe_distance
from app.services.course.query_analyzer import extract_region_keywords


def _normalize_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(str(v).strip() for v in value if str(v).strip())
    return str(value).strip()


def total_route_distance(route: list[dict]) -> float:
    if len(route) < 2:
        return 0.0

    total = 0.0
    for i in range(len(route) - 1):
        total += safe_distance(route[i], route[i + 1])
    return total


def annotate_route(route: list[dict]) -> list[dict]:
    annotated = []

    for idx, place in enumerate(route):
        copied = dict(place)
        copied["distance_from_prev"] = 0.0 if idx == 0 else safe_distance(route[idx - 1], route[idx])
        annotated.append(copied)

    return annotated


def build_item_text(item: dict) -> str:
    parts = [
        _normalize_text(item.get("PlaceName")),
        _normalize_text(item.get("Address")),
        _normalize_text(item.get("Region")),
        _normalize_text(item.get("Comment")),
        _normalize_text(item.get("Tags")),
    ]
    return " ".join(part for part in parts if part)


def item_matches_region(item: dict, region_keywords: list[str]) -> bool:
    if not region_keywords:
        return True

    text = build_item_text(item)
    return any(region in text for region in region_keywords)


def region_penalty(route: list[dict], query: str) -> float:
    region_keywords = extract_region_keywords(query)
    if not region_keywords:
        return 0.0

    penalty = 0.0
    for item in route:
        if not item_matches_region(item, region_keywords):
            penalty += 12.0
    return penalty


def cluster_penalty(route: list[dict]) -> float:
    if len(route) < 3:
        return 0.0

    penalty = 0.0
    for i in range(len(route)):
        for j in range(i + 1, len(route)):
            dist = safe_distance(route[i], route[j])
            if dist > 10:
                penalty += 2.5
            if dist > 20:
                penalty += 4.0
    return penalty


def has_duplicate_places(route: list[dict]) -> bool:
    names = [_normalize_text(item.get("PlaceName")) for item in route]
    return len(names) != len(set(names))


def route_cost(route: list[dict], query: str) -> float:
    duplicate_penalty = 999999.0 if has_duplicate_places(route) else 0.0
    return (
        total_route_distance(route)
        + region_penalty(route, query)
        + cluster_penalty(route)
        + duplicate_penalty
    )


def find_best_course_route(
    places_list: list[dict],
    restaurants_list: list[dict],
    query: str,
) -> tuple[list[dict], float]:
    if not places_list:
        return [], 0.0

    best_route = []
    best_cost = float("inf")

    if len(places_list) >= 3 and len(restaurants_list) >= 2:
        for place_order in permutations(places_list, 3):
            for restaurant_order in permutations(restaurants_list, 2):
                route = [
                    place_order[0],
                    restaurant_order[0],
                    place_order[1],
                    restaurant_order[1],
                    place_order[2],
                ]
                cost = route_cost(route, query)
                if cost < best_cost:
                    best_cost = cost
                    best_route = route

    elif len(places_list) >= 2 and len(restaurants_list) >= 1:
        for place_order in permutations(places_list, 2):
            for restaurant in restaurants_list:
                route = [
                    place_order[0],
                    restaurant,
                    place_order[1],
                ]
                cost = route_cost(route, query)
                if cost < best_cost:
                    best_cost = cost
                    best_route = route

    else:
        for place_order in permutations(places_list, len(places_list)):
            route = list(place_order)
            cost = route_cost(route, query)
            if cost < best_cost:
                best_cost = cost
                best_route = route

    pure_distance = total_route_distance(best_route) if best_route else 0.0
    return best_route, pure_distance