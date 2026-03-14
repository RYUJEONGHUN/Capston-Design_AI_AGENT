from fastapi import APIRouter, Body
from app.services.agent import agent_executor
from app.core.database import db

router = APIRouter(tags=["AI Chat"])

@router.post("/chat")
async def chat(user_input: str = Body(..., embed=True)):
    try:
        instruction = (
        f"사용자 질문: {user_input}\n\n"
        "지침:\n"
        "1. 반드시 'IncheonExpertSearch' 도구의 결과에 있는 데이터만 사용해.\n"
        "2. 위도(Y)와 경도(X) 값은 절대로 수정하지 말고 그대로 출력해.\n"
        "3. 지도 링크는 카카오맵 형식을 사용해: https://map.kakao.com/link/map/장소명,위도,경도\n"
        "   (예: 장소명이 '덕진진'이고 위도가 37.1, 경도가 126.1이면 https://map.kakao.com/link/map/덕진진,37.1,126.1)\n"
        "4. 답변 마지막에 이미지 URL이 있다면 반드시 포함해줘."
    )
        
        response = await agent_executor.arun(input=instruction)
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}

@router.get("/recommend/me")
async def recommend_for_me():
    # ryugh0210@naver.com 정훈님 데이터 조회
    user_persona = await db.members.find_one({"email": "ryugh0210@naver.com"})
    if not user_persona:
        return {"error": "페르소나를 찾을 수 없습니다."}

    system_prompt = f"""
    너는 '인천메이트'의 AI 가이드야. 주인님은 '{user_persona['name']}'님이야.
    백엔드 개발자답게 효율적인 여행을 추천해드려.
    이 정보를 바탕으로, 정훈님께 첫 인사를 건네고 인천의 장소 하나를 추천해드려봐.
    """
    # 에이전트 서비스에서 정의한 llm을 직접 사용하거나 agent를 통해 실행
    from app.services.agent import llm
    response = llm.invoke(system_prompt)
    
    return {
        "persona": user_persona['name'],
        "ai_response": response.content
    }