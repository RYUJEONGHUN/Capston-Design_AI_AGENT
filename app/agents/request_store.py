search_places_store: dict[str, list] = {}
course_route_store: dict[str, list] = {}


def set_search_places(session_id: str, places: list) -> None:
    search_places_store[session_id] = places


def get_search_places(session_id: str) -> list:
    return search_places_store.get(session_id, [])


def clear_search_places(session_id: str) -> None:
    search_places_store.pop(session_id, None)


def set_course_route(session_id: str, route: list) -> None:
    course_route_store[session_id] = route


def get_course_route(session_id: str) -> list:
    return course_route_store.get(session_id, [])


def clear_course_route(session_id: str) -> None:
    course_route_store.pop(session_id, None)