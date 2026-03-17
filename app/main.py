from fastapi import FastAPI
from app.api import chat, data

app = FastAPI(title="IncheonMate AI Server")

# 라우터 연결 (prefix를 통해 URL을 구분합니다)
app.include_router(data.router, prefix="/api/v1/data")
app.include_router(chat.router, prefix="/api/v1/ai")

@app.get("/")
async def root():
    return {"message": "IncheonMate FastAPI Server is running"}


