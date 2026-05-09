import os
import httpx

QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "http://18.209.101.243:8001")


async def generate_with_qwen(
    prompt: str,
    max_new_tokens: int = 500,
    temperature: float = 0.0,
) -> str:
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{QWEN_BASE_URL}/generate",
            json={
                "prompt": prompt,
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data.get("text", "").strip()