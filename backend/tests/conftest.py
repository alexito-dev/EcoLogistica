import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.pedidos.memory_repository import PedidosMemoryRepository
from app.pedidos.router import get_repositorio


@pytest.fixture
def client():
    """Cliente con un repositorio en memoria nuevo por prueba."""
    repo = PedidosMemoryRepository()
    app.dependency_overrides[get_repositorio] = lambda: repo
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def pedido_valido() -> dict:
    return {
        "direccion": "Jr. Real 123, Huancayo",
        "distrito": "Huancayo",
        "latitud": -12.0651,
        "longitud": -75.2049,
        "demandaKg": 25.5,
        "demandaM3": 0.3,
        "ventanaInicio": "2026-10-05T08:00:00-05:00",
        "ventanaFin": "2026-10-05T12:00:00-05:00",
    }
