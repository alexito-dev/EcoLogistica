"""Guardar y volver a abrir las rutas de una fecha (criterio 3 del Sprint 3)."""

from app.auth.domain import Rol
from app.main import app
from app.rutas.guardadas import RutasGuardadasArchivo
from app.rutas.router import get_repositorio_guardadas
from tests.rutas.test_api import MANANA, sembrar

GUARDAR = "/api/v1/rutas/guardar"
GUARDADA = "/api/v1/rutas/guardada"


def test_guarda_y_vuelve_a_abrir_las_rutas(cliente_con_rol):
    cliente = cliente_con_rol(Rol.PLANIFICADOR)
    sembrar()
    creada = cliente.post(GUARDAR, params={"fecha": MANANA})
    assert creada.status_code == 201, creada.text
    abierta = cliente.get(GUARDADA, params={"fecha": MANANA})
    assert abierta.status_code == 200
    assert abierta.json()["vista"]["rutas"] == creada.json()["vista"]["rutas"]
    assert abierta.json()["guardadaPor"] == "Prueba"
    assert abierta.json()["fecha"] == MANANA


def test_las_rutas_guardadas_sobreviven_al_reinicio(cliente_con_rol, tmp_path):
    cliente = cliente_con_rol(Rol.ADMIN)
    sembrar()
    cliente.post(GUARDAR, params={"fecha": MANANA})
    # Un almacén nuevo sobre el mismo archivo equivale a reiniciar la API.
    app.dependency_overrides[get_repositorio_guardadas] = lambda: RutasGuardadasArchivo(tmp_path / "rutas.json")
    abierta = cliente.get(GUARDADA, params={"fecha": MANANA})
    assert abierta.status_code == 200
    assert abierta.json()["vista"]["resumen"]["asignados"] > 0


def test_guardar_de_nuevo_reemplaza_las_rutas_de_la_fecha(cliente_con_rol):
    cliente = cliente_con_rol(Rol.PLANIFICADOR)
    sembrar()
    primera = cliente.post(GUARDAR, params={"fecha": MANANA}).json()["guardadaEn"]
    segunda = cliente.post(GUARDAR, params={"fecha": MANANA}).json()["guardadaEn"]
    assert segunda >= primera
    assert cliente.get(GUARDADA, params={"fecha": MANANA}).json()["guardadaEn"] == segunda


def test_fecha_sin_rutas_guardadas_responde_404(cliente_con_rol):
    cliente = cliente_con_rol(Rol.PLANIFICADOR)
    sembrar()
    assert cliente.get(GUARDADA, params={"fecha": MANANA}).status_code == 404


def test_no_guarda_si_no_hay_rutas_que_guardar(cliente_con_rol):
    cliente = cliente_con_rol(Rol.PLANIFICADOR)
    sembrar()
    respuesta = cliente.post(GUARDAR, params={"fecha": "2026-12-01"})
    assert respuesta.status_code == 422
    assert "fecha" in respuesta.json()["errors"]
    assert cliente.get(GUARDADA, params={"fecha": "2026-12-01"}).status_code == 404


def test_solo_planificacion_y_administracion_guardan_y_abren(cliente_con_rol):
    sembrar()
    for rol in (Rol.CONDUCTOR, Rol.GERENTE, Rol.AUDITOR):
        cliente = cliente_con_rol(rol)
        assert cliente.post(GUARDAR, params={"fecha": MANANA}).status_code == 403
        assert cliente.get(GUARDADA, params={"fecha": MANANA}).status_code == 403


def test_fecha_invalida_responde_400(cliente_con_rol):
    cliente = cliente_con_rol(Rol.PLANIFICADOR)
    assert cliente.post(GUARDAR, params={"fecha": "no-es-fecha"}).status_code == 400
