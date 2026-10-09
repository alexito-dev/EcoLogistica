"""Regression for browser preflight requests used by the fleet PUT routes."""

from fastapi.testclient import TestClient

from app.main import app
from app.config import get_settings


def test_cors_allows_preflight_for_fleet_updates():
    origin = get_settings().cors_origin
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.options(
            "/api/v1/vehiculos/00000000-0000-0000-0000-000000000001/disponibilidad",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "PUT",
                "Access-Control-Request-Headers": "content-type",
            },
        )

    assert response.status_code == 200
    assert "PUT" in response.headers["access-control-allow-methods"]
