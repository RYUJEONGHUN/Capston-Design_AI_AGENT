def extract_region_keywords(query: str) -> list[str]:
    region_keywords = [
        "송도",
        "영종도",
        "월미도",
        "강화도",
        "청라",
        "부평",
        "구월동",
        "연수구",
        "미추홀구",
        "계양구",
        "중구",
        "동구",
        "서구",
        "남동구",
        "옹진군",
        "동인천",
        "개항장",
        "신포",
        "차이나타운",
        "센트럴파크",
        "트리플스트리트",
    ]
    return [region for region in region_keywords if region in query]


def extract_food_keywords(query: str) -> list[str]:
    food_keywords = [
        "고기", "삼겹살", "소고기", "돼지고기", "갈비", "양꼬치", "스테이크",
        "회", "초밥", "스시", "칼국수", "국밥", "브런치", "디저트",
        "카페", "커피", "파스타", "피자", "치킨", "중식", "짜장", "짬뽕",
        "라멘", "막국수", "수육", "베이커리", "곰탕", "해물", "오마카세",
    ]
    return [food for food in food_keywords if food in query]


def extract_mood_keywords(query: str) -> list[str]:
    mood_keywords = [
        "데이트", "조용한", "감성", "야경", "오션뷰", "로맨틱",
        "분위기", "차분한", "아늑한", "힐링", "산책", "뷰", "노을",
        "고급", "프라이빗", "모던", "혼밥", "가족", "기념일",
    ]
    return [mood for mood in mood_keywords if mood in query]