"""OpenRouter API istemcisi."""

import json
import os
from typing import Any

import httpx
from fastapi import HTTPException

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-oss-120b:free"
DEFAULT_TIMEOUT = 90.0


def _ascii_header(value: str, fallback: str = "Gebetakip") -> str:
    """HTTP başlıkları yalnızca ASCII olmalı (Windows httpx/httpcore uyumu)."""
    try:
        return value.encode("ascii").decode("ascii")
    except UnicodeEncodeError:
        return value.encode("ascii", "replace").decode("ascii") or fallback


def _api_key() -> str:
    key = (os.getenv("OPENROUTER_API_KEY") or "").strip()
    if not key:
        raise HTTPException(status_code=503, detail="OpenRouter API anahtarı yapılandırılmamış.")
    return key


def _model() -> str:
    return (os.getenv("OPENROUTER_MODEL") or DEFAULT_MODEL).strip()


def _extract_assistant_text(message: dict[str, Any]) -> str:
    """Yanıt metnini message.content veya reasoning alanlarından okur."""
    content = (message.get("content") or "").strip()
    if content:
        return content
    for key in ("reasoning", "reasoning_content"):
        alt = (message.get(key) or "").strip()
        if alt:
            return alt
    return ""


def chat_completion(
    messages: list[dict[str, Any]],
    *,
    reasoning_enabled: bool = True,
) -> str:
    """OpenRouter chat/completions çağrısı; asistan metnini döndürür."""
    payload: dict[str, Any] = {
        "model": _model(),
        "messages": messages,
    }
    if reasoning_enabled:
        # exclude: iç düşünme tokenları ayrı alanda döner; sohbet için content dolu kalsın
        payload["reasoning"] = {"enabled": True, "exclude": True}

    headers = {
        "Authorization": f"Bearer {_api_key()}",
        "Content-Type": "application/json; charset=utf-8",
        "HTTP-Referer": _ascii_header(
            os.getenv("OPENROUTER_HTTP_REFERER", "http://localhost:5173")
        ),
        "X-Title": _ascii_header(
            os.getenv("OPENROUTER_APP_TITLE", "Gebelik Asistani")
        ),
    }

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            response = client.post(OPENROUTER_URL, headers=headers, content=body)
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="AI yanıtı zaman aşımına uğradı. Lütfen tekrar deneyin.")
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"OpenRouter bağlantı hatası: {exc}")

    if response.status_code != 200:
        detail = response.text[:300] if response.text else "Bilinmeyen hata"
        raise HTTPException(status_code=502, detail=f"OpenRouter hatası ({response.status_code}): {detail}")

    data = response.json()
    choices = data.get("choices") or []
    if not choices:
        raise HTTPException(status_code=502, detail="OpenRouter boş yanıt döndürdü.")

    message = choices[0].get("message") or {}
    content = _extract_assistant_text(message)
    if not content:
        raise HTTPException(
            status_code=502,
            detail=(
                "AI yanıtı boş geldi. OPENROUTER_API_KEY ve OPENROUTER_MODEL değerlerini "
                "kontrol edin; ücretsiz model kotası dolmuş olabilir."
            ),
        )
    return content
