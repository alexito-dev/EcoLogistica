"""Cabeceras de endurecimiento HTTP (OWASP A02:2025 — Security Misconfiguration)."""

from fastapi.testclient import TestClient

from app.main import app


def test_api_envia_cabeceras_de_seguridad_aun_sin_sesion():
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/api/v1/auth/sesion")

    assert response.status_code == 401
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert response.headers["content-security-policy"] == "default-src 'none'; frame-ancestors 'none'"


def test_docs_no_recibe_la_csp_estricta_de_la_api():
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/docs")

    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert "content-security-policy" not in response.headers
