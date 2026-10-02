"""Pruebas de los escenarios de openspec/changes/registro-pedidos/specs/pedidos/spec.md."""

from uuid import uuid4

import pytest

BASE = "/api/v1/pedidos"


# --- Registrar pedido con ventana horaria ---------------------------------

def test_registrar_pedido_valido(client, pedido_valido):
    r = client.post(BASE, json=pedido_valido)
    assert r.status_code == 201
    cuerpo = r.json()
    assert cuerpo["estado"] == "PENDIENTE"
    assert cuerpo["id"] and cuerpo["codigo"] == "PED-000001"
    assert cuerpo["ventanaInicio"].startswith("2026-10-05T13:00:00")  # UTC
    assert client.get(f"{BASE}/{cuerpo['id']}").status_code == 200


def test_valores_por_defecto(client, pedido_valido):
    cuerpo = client.post(BASE, json=pedido_valido).json()
    assert cuerpo["tiempoServicioMin"] == 10
    assert cuerpo["prioridad"] == 2


def test_codigo_generado_y_codigo_enviado(client, pedido_valido):
    assert client.post(BASE, json=pedido_valido).json()["codigo"] == "PED-000001"
    r = client.post(BASE, json={**pedido_valido, "codigo": " mi-codigo "})
    assert r.json()["codigo"] == "MI-CODIGO"


# --- Coherencia de la ventana horaria -------------------------------------

@pytest.mark.parametrize("fin", ["2026-10-05T08:00:00-05:00", "2026-10-05T07:00:00-05:00"])
def test_rechazar_ventana_invalida(client, pedido_valido, fin):
    r = client.post(BASE, json={**pedido_valido, "ventanaFin": fin})
    assert r.status_code == 422
    assert "ventanaFin" in r.json()["errors"]
    assert client.get(BASE).json()["total"] == 0


def test_fecha_sin_zona_horaria(client, pedido_valido):
    r = client.post(BASE, json={**pedido_valido, "ventanaInicio": "2026-10-05T08:00:00"})
    assert r.status_code == 400
    assert "ventanaInicio" in r.json()["errors"]


def test_fecha_con_formato_invalido(client, pedido_valido):
    r = client.post(BASE, json={**pedido_valido, "ventanaFin": "mañana"})
    assert r.status_code == 400
    assert "ventanaFin" in r.json()["errors"]


# --- Validación de magnitudes ---------------------------------------------

def test_peso_negativo(client, pedido_valido):
    r = client.post(BASE, json={**pedido_valido, "demandaKg": -1})
    assert r.status_code == 400
    assert "demandaKg" in r.json()["errors"]
    assert client.get(BASE).json()["total"] == 0


def test_sin_carga(client, pedido_valido):
    r = client.post(BASE, json={**pedido_valido, "demandaKg": 0, "demandaM3": 0})
    assert r.status_code == 422
    assert "demandaKg" in r.json()["errors"]


def test_prioridad_fuera_de_rango(client, pedido_valido):
    r = client.post(BASE, json={**pedido_valido, "prioridad": 5})
    assert r.status_code == 400
    assert "prioridad" in r.json()["errors"]


def test_campos_obligatorios_ausentes(client):
    r = client.post(BASE, json={})
    assert r.status_code == 400
    assert {"direccion", "distrito", "latitud", "longitud", "ventanaInicio", "ventanaFin"} <= r.json()[
        "errors"
    ].keys()


def test_campo_desconocido_rechazado(client, pedido_valido):
    r = client.post(BASE, json={**pedido_valido, "estado": "ENTREGADO"})
    assert r.status_code == 400
    assert "estado" in r.json()["errors"]


# --- Pertenencia al ámbito ------------------------------------------------

def test_coordenadas_fuera_del_ambito(client, pedido_valido):
    r = client.post(BASE, json={**pedido_valido, "latitud": -12.04, "longitud": -77.03})
    assert r.status_code == 422
    assert {"latitud", "longitud"} <= r.json()["errors"].keys()


def test_coordenadas_inexistentes(client, pedido_valido):
    r = client.post(BASE, json={**pedido_valido, "latitud": 120})
    assert r.status_code == 400
    assert "latitud" in r.json()["errors"]


def test_distrito_no_configurado(client, pedido_valido):
    r = client.post(BASE, json={**pedido_valido, "distrito": "Miraflores"})
    assert r.status_code == 422
    assert "distrito" in r.json()["errors"]


# --- Unicidad del código --------------------------------------------------

def test_codigo_duplicado(client, pedido_valido):
    primero = client.post(BASE, json={**pedido_valido, "codigo": "ABC-1"}).json()
    r = client.post(BASE, json={**pedido_valido, "codigo": " abc-1 ", "prioridad": 4})
    assert r.status_code == 409
    assert client.get(BASE).json()["total"] == 1
    assert client.get(f"{BASE}/{primero['id']}").json()["prioridad"] == 2


# --- Consulta por identificador -------------------------------------------

def test_consulta_inexistente(client):
    r = client.get(f"{BASE}/{uuid4()}")
    assert r.status_code == 404
    assert r.json()["message"]


def test_consulta_id_mal_formado(client):
    r = client.get(f"{BASE}/no-es-uuid")
    assert r.status_code == 400
    assert "pedido_id" in r.json()["errors"]


# --- Listado --------------------------------------------------------------

def test_listado_por_defecto(client, pedido_valido):
    for _ in range(3):
        client.post(BASE, json=pedido_valido)
    cuerpo = client.get(BASE).json()
    assert (cuerpo["total"], cuerpo["pagina"], cuerpo["limite"]) == (3, 1, 20)
    assert [p["codigo"] for p in cuerpo["items"]] == ["PED-000003", "PED-000002", "PED-000001"]


def test_listado_paginado(client, pedido_valido):
    for _ in range(3):
        client.post(BASE, json=pedido_valido)
    cuerpo = client.get(BASE, params={"pagina": 2, "limite": 2}).json()
    assert cuerpo["total"] == 3 and len(cuerpo["items"]) == 1


def test_listado_filtro_por_estado(client, pedido_valido):
    client.post(BASE, json=pedido_valido)
    assert client.get(BASE, params={"estado": "PENDIENTE"}).json()["total"] == 1
    assert client.get(BASE, params={"estado": "ENTREGADO"}).json()["total"] == 0


def test_listado_estado_invalido(client):
    assert client.get(BASE, params={"estado": "XYZ"}).status_code == 400


def test_listado_limite_excesivo(client):
    r = client.get(BASE, params={"limite": 101})
    assert r.status_code == 400
    assert "limite" in r.json()["errors"]


# --- Errores uniformes y seguros ------------------------------------------

def test_error_con_detalle_por_campo_y_formato_comun(client, pedido_valido):
    r = client.post(BASE, json={**pedido_valido, "demandaKg": -1, "prioridad": 9})
    cuerpo = r.json()
    assert r.status_code == 400
    assert set(cuerpo) == {"status", "message", "errors"} and cuerpo["status"] == 400
    assert {"demandaKg", "prioridad"} <= cuerpo["errors"].keys()
    assert "Traceback" not in r.text


def test_cuerpo_no_json(client):
    r = client.post(BASE, content="no es json", headers={"Content-Type": "application/json"})
    assert r.status_code == 400


def test_ruta_inexistente(client):
    r = client.get("/api/v1/otra-cosa")
    assert r.status_code == 404 and r.json()["status"] == 404


def test_fallo_interno_sin_informacion_interna(client, monkeypatch):
    from app.pedidos.service import PedidosService

    def _falla(*_a, **_k):
        raise RuntimeError("clave secreta interna /ruta/privada")

    monkeypatch.setattr(PedidosService, "listar", _falla)
    r = client.get(BASE)
    assert r.status_code == 500
    assert r.json() == {"status": 500, "message": "Error interno del servidor"}
    assert "secreta" not in r.text and "privada" not in r.text


def test_openapi_documenta_los_tres_endpoints(client):
    rutas = client.get("/openapi.json").json()["paths"]
    assert set(rutas["/api/v1/pedidos"]) == {"post", "get"}
    assert "get" in rutas["/api/v1/pedidos/{pedido_id}"]
    assert client.get("/docs").status_code == 200
