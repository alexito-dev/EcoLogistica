"""Sonda de disponibilidad /health usada por el despliegue y por las pruebas E2E de resiliencia (Sprint 5)."""

from fastapi.testclient import TestClient

from app.main import app


def test_salud_responde_200_sin_sesion_y_sin_base_configurada():
    with TestClient(app, raise_server_exceptions=False) as client:
        respuesta = client.get("/health")

    assert respuesta.status_code == 200
    assert respuesta.json()["status"] == "ok"
    assert respuesta.headers["x-content-type-options"] == "nosniff"


def test_salud_no_figura_en_el_contrato_openapi():
    with TestClient(app) as client:
        rutas = client.get("/openapi.json").json()["paths"]

    assert "/health" not in rutas
