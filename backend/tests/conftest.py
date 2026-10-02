import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# Antes de importar la app: almacén de usuarios temporal y clave de firma fija para las pruebas.
_TMP = Path(tempfile.mkdtemp(prefix="eco-tests-"))
os.environ["USUARIOS_ARCHIVO"] = str(_TMP / "usuarios.json")
os.environ["JWT_SECRET"] = "clave-de-pruebas-suficientemente-larga-0123456789"
os.environ["DEMO_CLAVE"] = "clave-de-pruebas-demo"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.auth.archivo_repository import UsuariosArchivoRepository  # noqa: E402
from app.auth.dependencias import get_repositorio_usuarios, usuario_actual  # noqa: E402
from app.auth.domain import Rol, Usuario  # noqa: E402
from app.auth.siembra import sembrar_usuarios_demo  # noqa: E402
from app.main import app  # noqa: E402
from app.pedidos.memory_repository import PedidosMemoryRepository  # noqa: E402
from app.pedidos.router import get_repositorio  # noqa: E402

CLAVE_DEMO = "clave-de-pruebas-demo"
ORIGEN = "http://localhost:3000"


def usuario_de_prueba(rol: Rol = Rol.PLANIFICADOR) -> Usuario:
    return Usuario(id=f"u-{rol.value}", correo=f"{rol.value.lower()}@prueba.test", nombre="Prueba", rol=rol, clave_hash="x")


@pytest.fixture
def client():
    """Cliente con sesión simulada de PLANIFICADOR y repositorio de pedidos nuevo por prueba."""
    repo = PedidosMemoryRepository()
    app.dependency_overrides[get_repositorio] = lambda: repo
    app.dependency_overrides[usuario_actual] = lambda: usuario_de_prueba(Rol.PLANIFICADOR)
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def cliente_con_rol():
    """Fábrica de clientes con sesión simulada del rol indicado."""
    repo = PedidosMemoryRepository()
    app.dependency_overrides[get_repositorio] = lambda: repo

    def _crear(rol: Rol) -> TestClient:
        app.dependency_overrides[usuario_actual] = lambda: usuario_de_prueba(rol)
        return TestClient(app, raise_server_exceptions=False)

    yield _crear
    app.dependency_overrides.clear()


@pytest.fixture
def repo_usuarios(tmp_path) -> UsuariosArchivoRepository:
    repo = UsuariosArchivoRepository(tmp_path / "usuarios.json")
    sembrar_usuarios_demo(repo, CLAVE_DEMO)
    return repo


@pytest.fixture
def cliente_real(repo_usuarios):
    """Cliente sin sesión simulada: usa la autenticación real con un almacén temporal."""
    repo_pedidos = PedidosMemoryRepository()
    app.dependency_overrides[get_repositorio] = lambda: repo_pedidos
    app.dependency_overrides[get_repositorio_usuarios] = lambda: repo_usuarios
    with TestClient(app, raise_server_exceptions=False, headers={"Origin": ORIGEN}) as c:
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


class Reloj:
    """Reloj controlable para probar expiraciones sin esperar."""

    def __init__(self, inicio: datetime | None = None) -> None:
        self.ahora = inicio or datetime(2026, 10, 5, 13, 0, tzinfo=timezone.utc)

    def __call__(self) -> datetime:
        return self.ahora

    def avanzar(self, **delta) -> None:
        from datetime import timedelta

        self.ahora += timedelta(**delta)
