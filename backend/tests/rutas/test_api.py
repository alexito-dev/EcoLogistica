"""Escenarios HTTP de la vista previa de rutas."""

from datetime import datetime, timedelta, timezone

from app.auth.domain import Rol
from app.flota.router import get_repositorio_flota
from app.flota.siembra import VEHICULOS_DEMO, sembrar_vehiculos_demo
from app.main import app
from app.pedidos.router import get_repositorio
from app.pedidos.siembra import PEDIDOS_DEMO, sembrar_pedidos_demo
from tests.pedidos.test_siembra import AMBITO

BASE = "/api/v1/rutas/vista-previa"
AHORA = datetime(2026, 10, 9, 10, 0, tzinfo=timezone(timedelta(hours=-5)))
MANANA = "2026-10-10"


def sembrar():
    sembrar_pedidos_demo(app.dependency_overrides[get_repositorio](), AMBITO, AHORA)
    sembrar_vehiculos_demo(app.dependency_overrides[get_repositorio_flota](), AHORA)


def test_propone_rutas_con_los_datos_de_demostracion(cliente_con_rol):
    cliente = cliente_con_rol(Rol.PLANIFICADOR)
    sembrar()
    respuesta = cliente.get(BASE, params={"fecha": MANANA})
    assert respuesta.status_code == 200, respuesta.text
    cuerpo = respuesta.json()
    resumen = cuerpo["resumen"]
    assert resumen["pedidos"] == len(PEDIDOS_DEMO)
    assert resumen["asignados"] == len(PEDIDOS_DEMO)
    assert resumen["vehiculosDisponibles"] == len(VEHICULOS_DEMO)
    assert resumen["co2Kg"] <= resumen["co2BaseKg"]
    assert cuerpo["deposito"]["latitud"] < 0
    assert cuerpo["supuestos"]
    for ruta in cuerpo["rutas"]:
        assert ruta["cargaKg"] <= ruta["vehiculo"]["capacidadKg"]
        assert [p["orden"] for p in ruta["paradas"]] == list(range(1, len(ruta["paradas"]) + 1))


def test_otra_fecha_no_tiene_pedidos(cliente_con_rol):
    cliente = cliente_con_rol(Rol.ADMIN)
    sembrar()
    cuerpo = cliente.get(BASE, params={"fecha": "2026-12-01"}).json()
    assert cuerpo["rutas"] == []
    assert cuerpo["resumen"]["pedidos"] == 0
    assert cuerpo["resumen"]["ahorroCo2Pct"] == 0


def test_sin_turno_declarado_los_pedidos_quedan_sin_asignar(cliente_con_rol):
    cliente = cliente_con_rol(Rol.PLANIFICADOR)
    sembrar_pedidos_demo(app.dependency_overrides[get_repositorio](), AMBITO, AHORA)
    cuerpo = cliente.get(BASE, params={"fecha": MANANA}).json()
    assert len(cuerpo["sinAsignar"]) == len(PEDIDOS_DEMO)


def test_fecha_obligatoria_y_valida(cliente_con_rol):
    cliente = cliente_con_rol(Rol.PLANIFICADOR)
    assert cliente.get(BASE).status_code == 400
    assert cliente.get(BASE, params={"fecha": "mañana"}).status_code == 400


def test_roles_sin_permiso(cliente_con_rol):
    assert cliente_con_rol(Rol.CONDUCTOR).get(BASE, params={"fecha": MANANA}).status_code == 403
