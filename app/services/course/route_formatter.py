def _format_tags(value) -> str:
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    if value is None:
        return ""
    return str(value)


def format_route_data(route: list[dict], total_distance: float) -> str:
    if not route:
        return "추천 가능한 코스 데이터가 없습니다."

    lines = []
    lines.append("[최적 코스 데이터]")
    lines.append(f"- 총 예상 이동거리: {total_distance:.2f}km")
    lines.append("")

    for idx, item in enumerate(route, start=1):
        lines.append(f"{idx}. 장소명: {item.get('PlaceName', '')}")
        lines.append(f"   - 카테고리: {item.get('category', '')}")
        lines.append(f"   - 세부카테고리: {item.get('subCategory', '')}")
        lines.append(f"   - 주소: {item.get('Address', '')}")
        lines.append(f"   - 지역: {item.get('Region', '')}")
        lines.append(f"   - 태그: {_format_tags(item.get('Tags', ''))}")
        lines.append(f"   - MBTI 태그: {_format_tags(item.get('mbtiTags', ''))}")
        lines.append(f"   - 사상체질 태그: {_format_tags(item.get('sasangTags', ''))}")
        lines.append(f"   - 평점: {item.get('Rating', '')}")
        lines.append(f"   - 설명: {item.get('Comment', '')}")
        lines.append(f"   - 위도(Y): {item.get('Y', '')}")
        lines.append(f"   - 경도(X): {item.get('X', '')}")
        lines.append(f"   - 이미지: {item.get('ImageURL', '')}")
        lines.append(f"   - 내기프트 연계 ID: {item.get('naegiftId', '')}")
        lines.append(
            f"   - 이전 장소로부터 거리: {item.get('distance_from_prev', 0.0):.2f}km"
        )
        lines.append("")

    return "\n".join(lines).strip()