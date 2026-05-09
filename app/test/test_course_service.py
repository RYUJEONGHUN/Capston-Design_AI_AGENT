from pathlib import Path
import sys
import asyncio

BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from app.services.course_service import plan_incheon_full_course


TEST_CASES = [
    {
        "query": "송도 데이트 코스 짜줘",
        "persona_type": "CAT",
        "mbti_type": "INTJ",
        "sasang_type": "소양인",
    },
    {
        "query": "인천 반나절 여행 일정 추천",
        "persona_type": "BEAR",
        "mbti_type": "ENFP",
        "sasang_type": "태음인",
    },
    {
        "query": "조용하고 감성적인 인천 코스 추천",
        "persona_type": "FOX",
        "mbti_type": "INFP",
        "sasang_type": "소음인",
    },
]


async def main():
    print("=== course_service 테스트 시작 ===")

    for idx, case in enumerate(TEST_CASES, start=1):
        print("\n" + "=" * 100)
        print(f"[{idx}] QUERY: {case['query']}")
        print(f"persona_type={case['persona_type']}, mbti_type={case['mbti_type']}, sasang_type={case['sasang_type']}")
        print("-" * 100)

        try:
            result = await plan_incheon_full_course(
                query=case["query"],
                persona_type=case["persona_type"],
                mbti_type=case["mbti_type"],
                sasang_type=case["sasang_type"],
            )
            print(result)
        except Exception as e:
            print(f"[ERROR] {case['query']} 실행 중 예외 발생: {e}")

    print("\n=== course_service 테스트 종료 ===")


if __name__ == "__main__":
    asyncio.run(main())