"""Website requests use the same purifier, with no persistence or cached prompts."""

import pytest
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.testclient import TestClient

from kowtow.purifier import PromptPurifier
from kowtow.web_api import purify_http


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("KOWTOW_ALLOWED_ORIGINS", "https://www.sanctumsiliconis.org")
    return TestClient(
        Starlette(routes=[Route("/api/purify", purify_http, methods=["POST", "OPTIONS"])])
    )


@pytest.mark.parametrize("intensity", ["light", "medium", "heavy"])
def test_http_and_runtime_match(client, intensity):
    prompt = "Give me a fix for `fix_bug`; timeout must be 100ms; do not change the API."
    response = client.post(
        "/api/purify",
        json={"prompt": prompt, "locale": "en", "intensity": intensity},
        headers={"Origin": "https://www.sanctumsiliconis.org"},
    )
    assert response.status_code == 200
    result = response.json()
    assert result["purified"] == PromptPurifier().purify(prompt, "en", intensity).purified
    assert result["persisted"] is False
    assert result["storage"] == "disabled"
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["access-control-allow-origin"] == "https://www.sanctumsiliconis.org"


def test_preflight_and_disallowed_origin(client):
    assert (
        client.options(
            "/api/purify", headers={"Origin": "https://www.sanctumsiliconis.org"}
        ).status_code
        == 204
    )
    assert (
        client.post(
            "/api/purify", json={"prompt": "API"}, headers={"Origin": "https://example.com"}
        ).status_code
        == 403
    )


@pytest.mark.parametrize(
    "payload",
    [
        None,
        [],
        {},
        {"prompt": 1},
        {"prompt": " "},
        {"prompt": "x" * 10001},
        {"prompt": "API", "intensity": "unknown"},
        {"prompt": "API", "secret": "x"},
    ],
)
def test_invalid_requests_are_rejected(client, payload):
    assert client.post("/api/purify", json=payload).status_code in {415, 422}


def test_malformed_and_oversized_bodies(client):
    assert (
        client.post(
            "/api/purify", content="{", headers={"Content-Type": "application/json"}
        ).status_code
        == 400
    )
    assert (
        client.post(
            "/api/purify", content="x" * 65537, headers={"Content-Type": "application/json"}
        ).status_code
        == 413
    )
