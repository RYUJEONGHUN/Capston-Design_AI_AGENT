import os
import httpx
from typing import Any, List, Optional

from langchain_core.language_models.llms import LLM


class QwenHTTPLLM(LLM):
    base_url: str = os.getenv("QWEN_BASE_URL", "http://18.209.101.243:8001")
    temperature: float = 0.0
    max_new_tokens: int = 180
    timeout: float = 120.0

    @property
    def _llm_type(self) -> str:
        return "qwen_http_experimental"

    def _cleanup_text(self, text: str, stop: Optional[List[str]] = None) -> str:
        text = text.strip()

        # LangChain이 넘겨주는 stop만 적용
        if stop:
            for token in stop:
                if token in text:
                    text = text.split(token)[0]

        return text.strip()

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> str:
        payload = {
            "prompt": prompt,
            "temperature": kwargs.get("temperature", self.temperature),
            "max_new_tokens": kwargs.get("max_new_tokens", self.max_new_tokens),
        }

        response = httpx.post(
            f"{self.base_url}/generate",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()

        text = response.json().get("text", "")
        print("[QWEN_AGENT RAW OUTPUT _call]", repr(text), flush=True)

        cleaned = self._cleanup_text(text, stop)
        print("[QWEN_AGENT CLEANED OUTPUT _call]", repr(cleaned), flush=True)

        return cleaned

    async def _acall(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> str:
        payload = {
            "prompt": prompt,
            "temperature": kwargs.get("temperature", self.temperature),
            "max_new_tokens": kwargs.get("max_new_tokens", self.max_new_tokens),
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/generate",
                json=payload,
            )
            response.raise_for_status()
            text = response.json().get("text", "")

        print("[QWEN_AGENT RAW OUTPUT _acall]", repr(text), flush=True)

        cleaned = self._cleanup_text(text, stop)
        print("[QWEN_AGENT CLEANED OUTPUT _acall]", repr(cleaned), flush=True)

        return cleaned