from fastapi import APIRouter, Body
from app.services.agent import get_agent_executor
from app.core.database import db

router = APIRouter(tags=["AI Chat"])

@router.post("/chat")
async def chat(user_input: str = Body(..., embed=True), session_id: str = Body("guest_user", embed=True)):
    try:
        agent_executor = get_agent_executor(session_id)
        instruction = (
        f"사용자 질문: {user_input}\n\n"
        "지침:\n"
        "1. [공감] 모든 답변의 시작은 사용자의 상태에 대한 따뜻한 공감으로 시작해."
        "2. [의도 파악] 사용자의 질문이 '정보 검색'인지 '단순 대화'인지 먼저 판단해.\n"
        "3. [대화 모드] 인사를 하거나 사소한 이야기를 할 때는 도구를 쓰지 말고 친절하게 대답만 해줘.\n"
        "4. [정보 검색 모드] 장소 추천이나 맛집 질문일 때만 'IncheonExpertSearch' 도구를 사용해.\n"
        "5. [기억 활용] 사용자가 본인의 정보를 말하면(이름, 직업 등) 도구를 쓰지 말고 Redis 메모리에 잘 기록해뒀다가 나중에 활용해."
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

