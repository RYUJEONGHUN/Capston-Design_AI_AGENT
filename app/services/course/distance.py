from math import asin, cos, radians, sin, sqrt


def get_distance(lat1, lon1, lat2, lon2):
    r = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    return 2 * r * asin(sqrt(a))


def safe_distance(a: dict, b: dict) -> float:
    lat1, lon1 = a.get("Y"), a.get("X")
    lat2, lon2 = b.get("Y"), b.get("X")

    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return 999999.0

    return get_distance(lat1, lon1, lat2, lon2)