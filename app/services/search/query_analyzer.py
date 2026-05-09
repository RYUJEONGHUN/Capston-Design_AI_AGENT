def detect_naegift_need(query: str) -> bool:
    keywords = ["기프트", "선물", "쿠폰", "내기프트", "연계"]
    return any(keyword in query for keyword in keywords)