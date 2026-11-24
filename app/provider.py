import httpx
from fastapi import HTTPException
from app.config import settings

async def generate(message: str, model: str) -> str:
    # OpenAI-compatible example adapter. Keep provider credentials server-side.
    if not settings.model_provider_url or not settings.model_api_key:
        raise HTTPException(status_code=503, detail="Model provider is not configured")
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(45.0)) as client:
            response = await client.post(
                settings.model_provider_url.rstrip("/") + "/chat/completions",
                headers={"Authorization": f"Bearer {settings.model_api_key}"},
                json={"model": model, "messages": [{"role": "user", "content": message}]},
            )
            response.raise_for_status()
            data = response.json()
            return str(data["choices"][0]["message"]["content"])
    except (httpx.HTTPError, KeyError, IndexError, ValueError):
        raise HTTPException(status_code=502, detail="Upstream model request failed") from None
