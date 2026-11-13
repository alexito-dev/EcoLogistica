"""Mide el peso del listado de pedidos antes/después de la paginación de 12 y la compresión.

ANTES  = un solo listado de 100 registros sin comprimir (comportamiento previo: limite=100, sin Accept-Encoding).
DESPUÉS = primera página de 12 registros con Brotli, y revalidación con ETag (304).
Uso: python scripts/medir_api_verde.py [cantidad_de_pedidos]   (datos sintéticos, memoria)
"""

import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("USUARIOS_ARCHIVO", str(Path(tempfile.mkdtemp()) / "usuarios.json"))
os.environ.setdefault("JWT_SECRET", "clave-solo-para-medicion-0123456789-abcdef")
os.environ["DATABASE_URL"] = ""
os.environ["DEMO_PEDIDOS"] = "false"
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient  # noqa: E402

from app.auth.dependencias import usuario_actual  # noqa: E402
from app.auth.domain import Rol, Usuario  # noqa: E402
from app.main import app  # noqa: E402
from app.pedidos.memory_repository import PedidosMemoryRepository  # noqa: E402
from app.pedidos.router import get_repositorio  # noqa: E402

BASE = "/api/v1/pedidos"
ORIGEN = {"Origin": "http://localhost:3000"}
PEDIDO = {
    "direccion": "Jr. Real 123, Huancayo", "distrito": "Huancayo", "latitud": -12.0651, "longitud": -75.2049,
    "ventanaInicio": "2026-10-05T08:00:00-05:00", "ventanaFin": "2026-10-05T12:00:00-05:00",
    "demandaKg": 25, "demandaM3": 0.3, "destinatarioAlias": "Bodega de prueba",
}


def main() -> None:
    cantidad = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    repo = PedidosMemoryRepository()
    app.dependency_overrides[get_repositorio] = lambda: repo
    app.dependency_overrides[usuario_actual] = lambda: Usuario(
        id="u", correo="p@prueba.test", nombre="P", rol=Rol.PLANIFICADOR, clave_hash="x"
    )
    with TestClient(app) as c:
        for i in range(cantidad):
            assert c.post(BASE, json={**PEDIDO, "codigo": f"PED-M-{i:04d}"}, headers=ORIGEN).status_code == 201
        antes = c.get(BASE, params={"limite": 100}, headers={"Accept-Encoding": "identity"})
        primera = c.get(BASE, params={"pagina": 1, "limite": 12}, headers={"Accept-Encoding": "br"})
        etag = primera.headers["etag"]
        revalidada = c.get(BASE, params={"pagina": 1, "limite": 12}, headers={"Accept-Encoding": "br", "If-None-Match": etag})
        # Tamaño real en red: httpx descomprime, por lo que se mide también el cuerpo sin decodificar.
        bytes_antes = len(antes.content)
        bytes_despues = int(primera.headers.get("content-length", len(primera.content)))
        print(f"pedidos sintéticos: {cantidad}")
        print(f"ANTES   (100 registros, sin compresión): {bytes_antes} B")
        print(f"DESPUÉS (12 registros, {primera.headers.get('content-encoding', 'sin compresión')}): {bytes_despues} B")
        print(f"REVALIDACIÓN (304 con ETag): {len(revalidada.content)} B, estado {revalidada.status_code}")
        print(f"Reducción: {100 * (1 - bytes_despues / bytes_antes):.1f} %")
    app.dependency_overrides.clear()


if __name__ == "__main__":
    main()
