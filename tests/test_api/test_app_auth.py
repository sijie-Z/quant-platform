"""Tests for optional API token authentication."""

from fastapi.testclient import TestClient

from quant_platform.app import create_app


def test_api_open_when_token_not_configured(monkeypatch):
    monkeypatch.delenv("QUANT_API_TOKEN", raising=False)
    app = create_app(serve_frontend=False)
    client = TestClient(app)
    resp = client.get("/api/health")
    assert resp.status_code == 200


def test_api_requires_token_when_configured(monkeypatch):
    monkeypatch.setenv("QUANT_API_TOKEN", "secret")
    app = create_app(serve_frontend=False)
    client = TestClient(app)

    assert client.get("/api/health").status_code == 200
    assert client.get("/api/config").status_code == 401
    assert client.get("/api/config", headers={"X-API-Key": "secret"}).status_code == 200
    assert client.get(
        "/api/config", headers={"Authorization": "Bearer secret"}
    ).status_code == 200
