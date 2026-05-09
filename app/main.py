from fastapi import FastAPI
from app.api import chat
from app.api.chat_qwen import router as chat_qwen_router
from app.api.qwen_experimental.chat_qwen_agent import router as chat_qwen_agent_router

app = FastAPI(title="IncheonMate AI Server")

# 라우터 연결 (prefix를 통해 URL을 구분합니다)
app.include_router(chat.router, prefix="/api/v1/ai")
app.include_router(chat_qwen_router, prefix="/api/v1/ai")
app.include_router(chat_qwen_agent_router, prefix="/api/v1/ai")

# 테스트
@app.get("/")
async def root():
    return {"message": "IncheonMate FastAPI Server is running, test plz"}


