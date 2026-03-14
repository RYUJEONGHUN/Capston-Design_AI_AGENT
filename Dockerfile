FROM python:3.11-slim

# 기본 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

# 시스템 패키지(필요 최소)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 복사
COPY app ./app

# (권장) non-root 유저
RUN useradd -m appuser
USER appuser

EXPOSE 8000

# uvicorn 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]