"""Green IT: compresión Brotli/Gzip y caché condicional (ETag/304) de la API (W3C WSG 1.0 pautas 2.4 y 3.1)."""

import gzip

import pytest

BASE = "/api/v1/pedidos"


def _registrar_varios(client, pedido_valido, cantidad=25):
    for i in range(cantidad):
        r = client.post(BASE, json={**pedido_valido, "codigo": f"PED-VERDE-{i:03d}"})
        assert r.status_code == 201


def test_lectura_incluye_etag_y_cache_privada(client):
    r = client.get(BASE)
    assert r.status_code == 200
    assert r.headers["etag"].startswith('W/"')
    assert r.headers["cache-control"] == "private, no-cache"
    assert "Cookie" in r.headers["vary"]


def test_revalidacion_con_if_none_match_responde_304_sin_cuerpo(client):
    etag = client.get(BASE).headers["etag"]
    r = client.get(BASE, headers={"If-None-Match": etag})
    assert r.status_code == 304
    assert r.content == b""
    assert r.headers["etag"] == etag


def test_etag_cambia_cuando_cambian_los_datos(client, pedido_valido):
    antes = client.get(BASE).headers["etag"]
    client.post(BASE, json=pedido_valido)
    r = client.get(BASE, headers={"If-None-Match": antes})
    assert r.status_code == 200
    assert r.headers["etag"] != antes


def test_escrituras_y_autenticacion_no_se_cachean(client, pedido_valido):
    assert "etag" not in client.post(BASE, json=pedido_valido).headers
    assert "etag" not in client.get("/api/v1/auth/sesion").headers


@pytest.mark.parametrize("codificacion", ["br", "gzip"])
def test_respuestas_json_grandes_se_comprimen(client, pedido_valido, codificacion):
    _registrar_varios(client, pedido_valido)
    sin = client.get(BASE, params={"limite": 100}, headers={"Accept-Encoding": "identity"})
    con = client.get(BASE, params={"limite": 100}, headers={"Accept-Encoding": codificacion})
    assert len(sin.content) > 1024
    assert con.headers["content-encoding"] == codificacion
    assert con.json() == sin.json()  # httpx descomprime de forma transparente


def test_gzip_reduce_el_tamano_transferido(client, pedido_valido):
    _registrar_varios(client, pedido_valido)
    crudo = client.get(BASE, params={"limite": 100}, headers={"Accept-Encoding": "identity"}).content
    cliente = client.get(BASE, params={"limite": 100}, headers={"Accept-Encoding": "gzip"})
    assert len(gzip.compress(crudo)) < len(crudo) * 0.35
    assert cliente.headers["content-encoding"] == "gzip"


def test_listado_usa_bloques_de_12_por_defecto(client, pedido_valido):
    _registrar_varios(client, pedido_valido, 14)
    cuerpo = client.get(BASE).json()
    assert (len(cuerpo["items"]), cuerpo["total"], cuerpo["limite"]) == (12, 14, 12)
