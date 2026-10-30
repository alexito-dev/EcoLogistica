"""Escenarios HTTP del dashboard de indicadores."""

from app.auth.domain import Rol
from app.flota.siembra import VEHICULOS_DEMO
from app.pedidos.siembra import PEDIDOS_DEMO
from tests.rutas.test_api import MANANA, sembrar

BASE = "/api/v1/indicadores"


def test_resume_pedidos_flota_y_planificacion_del_dia(cliente_con_rol):
    cliente = cliente_con_rol(Rol.GERENTE)
    sembrar()
    respuesta = cliente.get(BASE, params={"fecha": MANANA})
    assert respuesta.status_code == 200, respuesta.text
    cuerpo = respuesta.json()

    pedidos = cuerpo["pedidos"]
    assert pedidos["total"] == len(PEDIDOS_DEMO)
    assert pedidos["pesoKg"] == sum(p[6] for p in PEDIDOS_DEMO)
    assert sum(e["cantidad"] for e in pedidos["porEstado"]) == len(PEDIDOS_DEMO)
    assert {"estado": "PENDIENTE", "cantidad": len(PEDIDOS_DEMO)} in pedidos["porEstado"]
    assert pedidos["porDistrito"][0]["distrito"] == "El Tambo"  # el que más pedidos tiene
    assert [p["prioridad"] for p in pedidos["porPrioridad"]] == [4, 3, 2, 1]

    flota = cuerpo["flota"]
    assert flota["total"] == flota["aptos"] == len(VEHICULOS_DEMO)
    assert flota["capacidadAptaKg"] == sum(v[2] for v in VEHICULOS_DEMO)

    dia = cuerpo["dia"]
    assert dia["asignados"] == dia["pedidos"] == len(PEDIDOS_DEMO)
    assert 0 < dia["usoCapacidadPct"] <= 100
    assert dia["co2Kg"] < dia["co2BaseKg"]
    assert dia["paradasATiempoPct"] == 100


def test_fecha_sin_operacion_muestra_ceros(cliente_con_rol):
    cliente = cliente_con_rol(Rol.ADMIN)
    cuerpo = cliente.get(BASE, params={"fecha": "2026-12-01"}).json()
    assert cuerpo["pedidos"]["total"] == 0
    assert cuerpo["dia"] == {
        "pedidos": 0,
        "asignados": 0,
        "demandaKg": 0,
        "usoCapacidadPct": 0,
        "distanciaKm": 0,
        "distanciaBaseKm": 0,
        "co2Kg": 0,
        "co2BaseKg": 0,
        "ahorroCo2Pct": 0,
        "paradasATiempoPct": 0,
    }


def test_permisos(cliente_con_rol):
    assert cliente_con_rol(Rol.PLANIFICADOR).get(BASE, params={"fecha": MANANA}).status_code == 200
    assert cliente_con_rol(Rol.CONDUCTOR).get(BASE, params={"fecha": MANANA}).status_code == 403
    assert cliente_con_rol(Rol.AUDITOR).get(BASE, params={"fecha": MANANA}).status_code == 403
    assert cliente_con_rol(Rol.GERENTE).get(BASE).status_code == 400
