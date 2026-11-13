"""Importación de pedidos por plantilla CSV (ECO-18)."""

import pytest

from app.auth.domain import Rol

BASE = "/api/v1/pedidos"
ENCABEZADO = "codigo,direccion,distrito,latitud,longitud,ventana_inicio,ventana_fin,demanda_kg,demanda_m3,tiempo_servicio_min,prioridad,destinatario,observacion"
FILA_OK = "{cod},Jr. Real 123,Huancayo,-12.0651,-75.2049,2026-11-20 08:00,2026-11-20 12:00,25,0.3,10,2,Bodega Ana,"


def csv(*filas, encabezado=ENCABEZADO):
    return "\n".join([encabezado, *filas]) + "\n"


def test_plantilla_descargable_solo_para_quien_registra(client, cliente_con_rol):
    r = client.get(f"{BASE}/plantilla")
    assert r.status_code == 200 and r.headers["content-type"].startswith("text/csv")
    assert r.text.startswith("codigo,direccion,distrito") and "attachment" in r.headers["content-disposition"]
    assert cliente_con_rol(Rol.ADMIN).get(f"{BASE}/plantilla").status_code == 403


def test_importa_todas_las_filas_validas(client):
    contenido = csv(FILA_OK.format(cod="IMP-1"), FILA_OK.format(cod="IMP-2"), FILA_OK.format(cod=""))
    r = client.post(f"{BASE}/importar", json={"contenido": contenido})
    assert r.status_code == 201, r.text
    cuerpo = r.json()
    assert cuerpo["importados"] == 3 and cuerpo["codigos"][:2] == ["IMP-1", "IMP-2"]
    assert client.get(BASE).json()["total"] == 3
    primero = client.get(BASE, params={"limite": 100}).json()["items"][-1]
    assert primero["ventanaInicio"].startswith("2026-11-20T13:00:00")  # 08:00 de Lima en UTC


def test_acepta_punto_y_coma_y_decimales_con_coma(client):
    contenido = ENCABEZADO.replace(",", ";") + "\n" + "IMP-9;Jr. Real 1;Huancayo;-12,0651;-75,2049;2026-11-20 08:00;2026-11-20 12:00;25,5;0,3;10;2;;\n"
    assert client.post(f"{BASE}/importar", json={"contenido": contenido}).status_code == 201


def test_todo_o_nada_informa_fila_y_campo(client):
    malo = "IMP-3,Jr. Real 123,Huancayo,-12.0651,-75.2049,2026-11-20 12:00,2026-11-20 08:00,25,0.3,10,2,,"
    fuera = "IMP-4,Lima,Huancayo,-12.5,-75.2,2026-11-20 08:00,2026-11-20 12:00,25,0.3,10,2,,"
    r = client.post(f"{BASE}/importar", json={"contenido": csv(FILA_OK.format(cod="IMP-1"), malo, fuera)})
    assert r.status_code == 422
    errores = r.json()["errors"]
    assert "fila 3 · ventana_fin" in errores and "fila 4 · latitud" in errores
    assert client.get(BASE).json()["total"] == 0  # ninguna se registró


def test_codigos_repetidos_y_existentes(client, pedido_valido):
    client.post(BASE, json={**pedido_valido, "codigo": "YA-EXISTE"})
    contenido = csv(FILA_OK.format(cod="IMP-1"), FILA_OK.format(cod="imp-1"), FILA_OK.format(cod="YA-EXISTE"))
    errores = client.post(f"{BASE}/importar", json={"contenido": contenido}).json()["errors"]
    assert "repetido" in errores["fila 3 · codigo"] and "Ya existe" in errores["fila 4 · codigo"]


@pytest.mark.parametrize("contenido, campo", [
    ("   \n", "archivo"),
    ("direccion,distrito\nA,B\n", "archivo"),
    (ENCABEZADO + "\n", "archivo"),
])
def test_archivos_invalidos(client, contenido, campo):
    r = client.post(f"{BASE}/importar", json={"contenido": contenido})
    assert r.status_code == 422 and campo in r.json()["errors"]


def test_fecha_invalida_y_valores_faltantes(client):
    contenido = csv("X1,Jr. Real,Huancayo,abc,-75.2,mañana,2026-11-20 12:00,25,0.3,10,2,,")
    errores = client.post(f"{BASE}/importar", json={"contenido": contenido}).json()["errors"]
    assert any("fila 2" in k for k in errores)


def test_limite_de_filas_y_permisos(client, cliente_con_rol):
    filas = [FILA_OK.format(cod=f"M-{i}") for i in range(501)]
    r = client.post(f"{BASE}/importar", json={"contenido": csv(*filas)})
    assert r.status_code == 422 and "500" in r.json()["errors"]["archivo"]
    assert cliente_con_rol(Rol.CONDUCTOR).post(f"{BASE}/importar", json={"contenido": csv(FILA_OK.format(cod="Z"))}).status_code == 403
