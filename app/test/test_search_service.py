from pathlib import Path
import sys
import asyncio

BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from app.services.search_service import search_my_incheon_data


TEST_QUERIES = [
    "송도 카페 추천",
    "인천 칼국수 맛집",
    "야경 좋은 관광지",
    "조용한 분위기의 카페",
    "바다 보이는 관광지 추천",
]


async def main():
    print("=== search_service 테스트 시작 ===")

    for idx, query in enumerate(TEST_QUERIES, start=1):
        print("\n" + "=" * 80)
        print(f"[{idx}] QUERY: {query}")
        print("-" * 80)

        try:
            result = await search_my_incheon_data(query)
            print(result)
        except Exception as e:
            print(f"[ERROR] {query} 실행 중 예외 발생: {e}")

    print("\n=== search_service 테스트 종료 ===")


if __name__ == "__main__":
    asyncio.run(main())