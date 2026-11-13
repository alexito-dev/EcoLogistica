"""Escenarios de Conduccion: ruta asignada, avance de entregas, incidencias y reoptimizacion (Sprint 4)."""

from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from app.auth.archivo_repository import UsuariosArchivoRepository
from app.auth.dependencias import get_repositorio_usuarios, usuario_actual
from app.auth.domain import Rol
from app.auth.siembra import sembrar_usuarios_demo
from app.conduccion.memory_repository import ConduccionMemoryRepository
from app.conduccion.router import get_repositorio_conduccion
from app.flota.memory_repository import FlotaMemoryRepository
from app.flota.router import get_repositorio_flota
from app.flota.siembra import sembrar_vehiculos_demo
from app.main import app
from app.pedidos.memory_repository import PedidosMemoryRepository
from app.pedidos.router import get_repositorio
from app.pedidos.siembra import sembrar_pedidos_demo
from app.rutas.guardadas import RutasGuardadasArchivo
from app.rutas.router import get_repositorio_guardadas
from tests.pedidos.test_siembra import AMBITO

AHORA = datetime(2026, 10, 9, 10, 0, tzinfo=timezone(timedelta(hours=-5)))
FECHA = "2026-10-10"
ORIGEN = {"Origin": "http://localhost:3000"}


class Entorno:
    def __init__(self, tmp_path):
        self.pedidos = PedidosMemoryRepository()
        self.flota = FlotaMemoryRepository()
        self.usuarios = UsuariosArchivoRepository(tmp_path / "usuarios.json")
        sembrar_usuarios_demo(self.usuarios, "clave-de-pruebas-demo")
        self.conduccion = ConduccionMemoryRepository()
        self.guardadas = RutasGuardadasArchivo(tmp_path / "rutas.json")
        def por_cabecera(request: Request):
            return self.usuario(Rol(request.headers["x-rol-prueba"]))

        app.dependency_overrides[usuario_actual] = por_cabecera
        app.dependency_overrides[get_repositorio] = lambda: self.pedidos
        app.dependency_overrides[get_repositorio_flota] = lambda: self.flota
        app.dependency_overrides[get_repositorio_usuarios] = lambda: self.usuarios
        app.dependency_overrides[get_repositorio_conduccion] = lambda: self.conduccion
        app.dependency_overrides[get_repositorio_guardadas] = lambda: self.guardadas
        sembrar_pedidos_demo(self.pedidos, AMBITO, AHORA)
        sembrar_vehiculos_demo(self.flota, AHORA)

    def usuario(self, rol: Rol):
        return self.usuarios.listar_por_rol(rol)[0]

    def como(self, rol: Rol) -> TestClient:
        """Cliente que actúa con el usuario del rol indicado (varios clientes pueden coexistir)."""
        return TestClient(app, raise_server_exceptions=False, headers={**ORIGEN, "X-Rol-Prueba": rol.value})

    def preparar_rutas(self) -> dict:
        """Planificación guarda las rutas y asigna al conductor demo a la primera."""
        planificador = self.como(Rol.PLANIFICADOR)
        guardada = planificador.post("/api/v1/rutas/guardar", params={"fecha": FECHA})
        assert guardada.status_code == 201, guardada.text
        ruta = guardada.json()["vista"]["rutas"][0]
        respuesta = planificador.put(
            "/api/v1/conduccion/asignaciones",
            json={"fecha": FECHA, "vehiculoId": ruta["vehiculo"]["id"], "conductorId": self.usuario(Rol.CONDUCTOR).id},
        )
        assert respuesta.status_code == 204, respuesta.text
        return ruta


@pytest.fixture
def entorno(tmp_path):
    yield Entorno(tmp_path)
    app.dependency_overrides.clear()


def estado(cliente, pedido_id, nuevo, nota=None):
    return cliente.post(
        f"/api/v1/conduccion/paradas/{pedido_id}/estado", json={"fecha": FECHA, "estado": nuevo, "nota": nota}
    )


def test_conductor_ve_solo_la_ruta_asignada_con_paradas_pendientes(entorno):
    ruta = entorno.preparar_rutas()
    respuesta = entorno.como(Rol.CONDUCTOR).get("/api/v1/conduccion/mi-ruta", params={"fecha": FECHA})
    assert respuesta.status_code == 200, respuesta.text
    rutas = respuesta.json()["rutas"]
    assert len(rutas) == 1 and rutas[0]["vehiculo"]["id"] == ruta["vehiculo"]["id"]
    assert [p["orden"] for p in rutas[0]["paradas"]] == list(range(1, len(ruta["paradas"]) + 1))
    assert {p["estado"] for p in rutas[0]["paradas"]} == {"PENDIENTE"}
    assert rutas[0]["avance"]["entregadas"] == 0


def test_sin_rutas_guardadas_responde_404(entorno):
    assert entorno.como(Rol.CONDUCTOR).get("/api/v1/conduccion/mi-ruta", params={"fecha": FECHA}).status_code == 404


def test_avance_se_conserva_y_actualiza_el_pedido(entorno):
    ruta = entorno.preparar_rutas()
    conductor = entorno.como(Rol.CONDUCTOR)
    pedido_id = ruta["paradas"][0]["pedidoId"]
    assert estado(conductor, pedido_id, "EN_RUTA").status_code == 200
    respuesta = estado(conductor, pedido_id, "ENTREGADO")
    assert respuesta.status_code == 200 and respuesta.json()["estado"] == "ENTREGADO"
    assert entorno.pedidos.obtener(UUID(pedido_id)).estado.value == "ENTREGADO"
    rutas = conductor.get("/api/v1/conduccion/mi-ruta", params={"fecha": FECHA}).json()["rutas"]
    assert rutas[0]["paradas"][0]["estado"] == "ENTREGADO"
    assert rutas[0]["avance"]["entregadas"] == 1


def test_transiciones_invalidas_y_incidencia_sin_descripcion(entorno):
    pedido_id = entorno.preparar_rutas()["paradas"][0]["pedidoId"]
    conductor = entorno.como(Rol.CONDUCTOR)
    saltar = estado(conductor, pedido_id, "ENTREGADO")  # PENDIENTE -> ENTREGADO no se permite
    assert saltar.status_code == 422 and "estado" in saltar.json()["errors"]
    estado(conductor, pedido_id, "EN_RUTA")
    sin_nota = estado(conductor, pedido_id, "INCIDENCIA")
    assert sin_nota.status_code == 422 and "nota" in sin_nota.json()["errors"]
    assert estado(conductor, pedido_id, "REPROGRAMADO").status_code == 422  # solo lo decide Planificación
    estado(conductor, pedido_id, "ENTREGADO")
    assert estado(conductor, pedido_id, "EN_RUTA").status_code == 422  # ENTREGADO es final


def test_una_parada_ajena_no_se_puede_modificar(entorno):
    entorno.preparar_rutas()
    guardada = entorno.guardadas.obtener(datetime(2026, 10, 10).date())
    rutas = guardada["vista"]["rutas"]
    if len(rutas) < 2:
        pytest.skip("los datos de demostración generan una sola ruta")
    ajeno = rutas[1]["paradas"][0]["pedidoId"]
    assert estado(entorno.como(Rol.CONDUCTOR), ajeno, "EN_RUTA").status_code == 404


def test_permisos_por_rol(entorno):
    ruta = entorno.preparar_rutas()
    pedido_id = ruta["paradas"][0]["pedidoId"]
    assert estado(entorno.como(Rol.PLANIFICADOR), pedido_id, "EN_RUTA").status_code == 403
    assert entorno.como(Rol.CONDUCTOR).get("/api/v1/conduccion/seguimiento", params={"fecha": FECHA}).status_code == 403
    assert entorno.como(Rol.CONDUCTOR).post("/api/v1/conduccion/reoptimizar", json={"fecha": FECHA}).status_code == 403
    assert entorno.como(Rol.AUDITOR).get("/api/v1/conduccion/mi-ruta", params={"fecha": FECHA}).status_code == 403


def test_asignar_exige_un_conductor_y_un_vehiculo_con_ruta(entorno):
    ruta = entorno.preparar_rutas()
    planificador = entorno.como(Rol.PLANIFICADOR)
    no_conductor = planificador.put(
        "/api/v1/conduccion/asignaciones",
        json={"fecha": FECHA, "vehiculoId": ruta["vehiculo"]["id"], "conductorId": entorno.usuario(Rol.ADMIN).id},
    )
    assert no_conductor.status_code == 422 and "conductorId" in no_conductor.json()["errors"]
    sin_ruta = planificador.put(
        "/api/v1/conduccion/asignaciones",
        json={"fecha": FECHA, "vehiculoId": "00000000-0000-0000-0000-000000000000", "conductorId": entorno.usuario(Rol.CONDUCTOR).id},
    )
    assert sin_ruta.status_code == 422 and "vehiculoId" in sin_ruta.json()["errors"]


def test_incidencia_visible_para_planificacion_y_reprogramacion_conserva_historial(entorno):
    pedido_id = entorno.preparar_rutas()["paradas"][0]["pedidoId"]
    conductor, planificador = entorno.como(Rol.CONDUCTOR), entorno.como(Rol.PLANIFICADOR)
    estado(conductor, pedido_id, "EN_RUTA")
    assert estado(conductor, pedido_id, "INCIDENCIA", "Cliente ausente en el domicilio").status_code == 200
    seguimiento = planificador.get("/api/v1/conduccion/seguimiento", params={"fecha": FECHA}).json()
    assert [i["pedidoId"] for i in seguimiento["incidencias"]] == [pedido_id]
    assert seguimiento["incidencias"][0]["nota"] == "Cliente ausente en el domicilio"
    assert seguimiento["conductoresDisponibles"]
    assert entorno.pedidos.obtener(UUID(pedido_id)).estado.value == "FALLIDO"

    assert planificador.post(f"/api/v1/conduccion/paradas/{pedido_id}/reprogramar", json={"fecha": FECHA}).status_code == 204
    assert entorno.pedidos.obtener(UUID(pedido_id)).estado.value == "PENDIENTE"
    historial = planificador.get(f"/api/v1/conduccion/paradas/{pedido_id}/historial", params={"fecha": FECHA}).json()
    assert [e["estado"] for e in historial] == ["EN_RUTA", "INCIDENCIA", "REPROGRAMADO"]
    # Ya no es una incidencia abierta y no se puede reprogramar dos veces.
    assert planificador.post(f"/api/v1/conduccion/paradas/{pedido_id}/reprogramar", json={"fecha": FECHA}).status_code == 422


def test_reprogramar_exige_incidencia(entorno):
    pedido_id = entorno.preparar_rutas()["paradas"][0]["pedidoId"]
    respuesta = entorno.como(Rol.PLANIFICADOR).post(
        f"/api/v1/conduccion/paradas/{pedido_id}/reprogramar", json={"fecha": FECHA}
    )
    assert respuesta.status_code == 422


def test_reoptimizar_conserva_lo_ejecutado_y_es_idempotente(entorno):
    ruta = entorno.preparar_rutas()
    primera = ruta["paradas"][0]["pedidoId"]
    conductor, planificador = entorno.como(Rol.CONDUCTOR), entorno.como(Rol.PLANIFICADOR)
    estado(conductor, primera, "EN_RUTA")
    estado(conductor, primera, "ENTREGADO")
    primera_vez = planificador.post("/api/v1/conduccion/reoptimizar", json={"fecha": FECHA})
    assert primera_vez.status_code == 200
    segunda_vez = planificador.post("/api/v1/conduccion/reoptimizar", json={"fecha": FECHA}).json()
    assert segunda_vez["rutasReordenadas"] == 0  # el orden ya es el óptimo desde la última entrega
    paradas = conductor.get("/api/v1/conduccion/mi-ruta", params={"fecha": FECHA}).json()["rutas"][0]["paradas"]
    assert paradas[0]["pedidoId"] == primera and paradas[0]["estado"] == "ENTREGADO"
    assert [p["orden"] for p in paradas] == list(range(1, len(paradas) + 1))
    assert sorted(p["pedidoId"] for p in paradas) == sorted(p["pedidoId"] for p in ruta["paradas"])


def test_indicadores_observados_solo_con_entregas_registradas(entorno):
    ruta = entorno.preparar_rutas()
    planificador, conductor = entorno.como(Rol.PLANIFICADOR), entorno.como(Rol.CONDUCTOR)
    url = "/api/v1/indicadores/ejecucion"
    vacio = planificador.get(url, params={"fecha": FECHA}).json()
    assert vacio["entregadas"] == 0 and vacio["puntualidadPct"] is None and vacio["distanciaRecorridaKm"] == 0
    total = sum(len(r["paradas"]) for r in entorno.guardadas.obtener(datetime(2026, 10, 10).date())["vista"]["rutas"])
    assert vacio["paradas"] == total and vacio["pendientes"] == total

    primera, segunda = ruta["paradas"][0]["pedidoId"], ruta["paradas"][-1]["pedidoId"]
    estado(conductor, primera, "EN_RUTA")
    estado(conductor, primera, "ENTREGADO")
    if segunda != primera:
        estado(conductor, segunda, "EN_RUTA")
        estado(conductor, segunda, "INCIDENCIA", "Calle cerrada por obras")
    datos = planificador.get(url, params={"fecha": FECHA}).json()
    assert datos["entregadas"] == 1 and datos["cumplimientoPct"] > 0
    # La ventana de los datos de demostración es futura respecto a la hora real: la entrega cuenta a tiempo.
    assert datos["entregasATiempo"] + datos["entregasTarde"] == 1 and datos["puntualidadPct"] in (0.0, 100.0)
    assert 0 < datos["distanciaRecorridaKm"] <= datos["distanciaPrevistaKm"]
    assert 0 < datos["co2RecorridoKg"] <= datos["co2PrevistoKg"]
    if segunda != primera:
        assert datos["incidencias"] == 1


def test_indicadores_observados_permisos_y_fecha_sin_rutas(entorno):
    assert entorno.como(Rol.CONDUCTOR).get("/api/v1/indicadores/ejecucion", params={"fecha": FECHA}).status_code == 403
    assert entorno.como(Rol.PLANIFICADOR).get("/api/v1/indicadores/ejecucion", params={"fecha": FECHA}).status_code == 404
