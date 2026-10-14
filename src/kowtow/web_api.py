"""Thin, stateless website bridge to the same Python purification engine."""

import json
import os
from dataclasses import asdict

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from kowtow.purifier import PromptPurifier

MAX_BODY_BYTES = 64 * 1024
MAX_PROMPT_CHARS = 10_000


def _cors_headers(request: Request) -> dict[str, str] | None:
    origin = request.headers.get("origin")
    allowed = {
        value.strip().rstrip("/")
        for value in os.getenv("KOWTOW_ALLOWED_ORIGINS", "").split(",")
        if value.strip()
    }
    if not origin:
        return {}
    if origin not in allowed and origin != f"{request.url.scheme}://{request.url.netloc}":
        return None
    return {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Vary": "Origin",
    }


async def purify_http(request: Request) -> Response:
    headers = _cors_headers(request)
    if headers is None:
        return JSONResponse({"error": "origin_not_allowed"}, status_code=403)
    headers["Cache-Control"] = "no-store"
    if request.method == "OPTIONS":
        return Response(status_code=204, headers=headers)
    if request.headers.get("content-type", "").split(";")[0].strip().lower() != "application/json":
        return JSONResponse({"error": "json_required"}, status_code=415, headers=headers)
    body = bytearray()
    async for chunk in request.stream():
        body.extend(chunk)
        if len(body) > MAX_BODY_BYTES:
            return JSONResponse({"error": "request_too_large"}, status_code=413, headers=headers)
    try:
        payload = json.loads(body)
    except (ValueError, UnicodeDecodeError):
        return JSONResponse({"error": "invalid_json"}, status_code=400, headers=headers)
    if not isinstance(payload, dict) or payload.keys() - {"prompt", "locale", "intensity"}:
        return JSONResponse({"error": "invalid_request"}, status_code=422, headers=headers)
    prompt = payload.get("prompt")
    locale = payload.get("locale", "zh-cn")
    intensity = payload.get("intensity", "medium")
    if (
        not isinstance(prompt, str)
        or not 1 <= len(prompt) <= MAX_PROMPT_CHARS
        or not isinstance(locale, str)
        or len(locale) > 32
        or not isinstance(intensity, str)
    ):
        return JSONResponse({"error": "invalid_request"}, status_code=422, headers=headers)
    try:
        result = PromptPurifier().purify(prompt, locale, intensity)
    except ValueError:
        return JSONResponse({"error": "invalid_request"}, status_code=422, headers=headers)
    return JSONResponse(
        {**asdict(result), "storage": "disabled", "persisted": False}, headers=headers
    )
