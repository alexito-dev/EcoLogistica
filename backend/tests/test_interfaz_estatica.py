"""Entrega de la interfaz compilada desde la API (despliegue de un solo servicio, Sprint 4)."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.config import Settings
from app.estaticos import servir_interfaz


@pytest.fixture
def cliente(tmp_path):
    (tmp_path / "assets").mkdir()
    (tmp_path / "index.html").write_text("<!doctype html><title>EcoLogística</title>", encoding="utf8")
    (tmp_path / "assets" / "app-abc123.js").write_text("console.log('ok')", encoding="utf8")
    (tmp_path.parent / "secreto.txt").write_text("no debe salir", encoding="utf8")
    app = FastAPI()

    @app.get("/api/v1/ping")
    def ping():
        return {"pong": True}

    servir_interfaz(app, tmp_path)
    return TestClient(app)


def test_la_raiz_y_las_rutas_de_la_spa_devuelven_index(cliente):
    for ruta in ("/", "/pedidos", "/rutas/mapa"):
        r = cliente.get(ruta)
        assert r.status_code == 200 and "EcoLogística" in r.text
        assert r.headers["cache-control"] == "no-cache"


def test_los_assets_con_hash_se_cachean_como_inmutables(cliente):
    r = cliente.get("/assets/app-abc123.js")
    assert r.status_code == 200
    assert "immutable" in r.headers["cache-control"]


def test_una_ruta_de_la_api_no_se_pisa_con_la_interfaz(cliente):
    assert cliente.get("/api/v1/ping").json() == {"pong": True}
    r = cliente.get("/api/v1/no-existe")
    assert r.status_code == 404 and r.json()["status"] == 404


def test_un_archivo_con_extension_inexistente_es_404_y_no_index(cliente):
    assert cliente.get("/assets/falta.js").status_code == 404


def test_no_permite_salir_de_la_carpeta_compilada(cliente):
    for ruta in ("/../secreto.txt", "/%2e%2e/secreto.txt", "/assets/../../secreto.txt"):
        r = cliente.get(ruta)
        assert "no debe salir" not in r.text


def test_exige_un_build_valido(tmp_path):
    with pytest.raises(RuntimeError):
        servir_interfaz(FastAPI(), tmp_path)


@pytest.mark.parametrize("origen", ["postgres://u:p@h/db", "postgresql://u:p@h/db"])
def test_normaliza_la_url_de_base_de_datos_de_los_hostings(origen):
    ajustes = Settings(database_url=origen, _env_file=None)
    assert ajustes.database_url == "postgresql+psycopg://u:p@h/db"


def test_respeta_una_url_con_controlador_explicito():
    url = "postgresql+psycopg://u:p@h/db"
    assert Settings(database_url=url, _env_file=None).database_url == url
