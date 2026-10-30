"""Ramas negativas y transiciones reales de flota y verificación PostGIS.

Pruebas aisladas: no escriben en bases productivas ni cambian datos de demostración.
"""

from datetime import date, time
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.flota.domain import (
    Combustible, DisponibilidadVehiculo, EstadoVehiculo, PlacaDuplicadaError,
    ReglaFlotaError, Vehiculo, VehiculoNoEncontradoError,
)
from app.flota.memory_repository import FlotaMemoryRepository
from app.flota.service import FlotaService
from app import database_health


def _vehiculo(placa="W3A-123", estado=EstadoVehiculo.DISPONIBLE):
    return Vehiculo(
        id=uuid4(), placa=placa, tipo="Furgón", capacidad_kg=Decimal("700"),
        capacidad_m3=Decimal("8"), combustible=Combustible.DIESEL,
        consumo_base_por_100km=Decimal("11"),
        factor_emision_kgco2e_unidad=None, anio=None, estado=estado,
        creado_en=None, actualizado_en=None,
    )


def _datos(**cambios):
    argumentos = dict(
        placa="W3A-999", tipo="Furgón", capacidad_kg=Decimal("500"),
        capacidad_m3=Decimal("6"), combustible=Combustible.DIESEL,
        consumo_base_por_100km=Decimal("10"),
        factor_emision_kgco2e_unidad=None, anio=None,
        estado=EstadoVehiculo.DISPONIBLE,
    )
    argumentos.update(cambios)
    return SimpleNamespace(**argumentos)


def _turno(**cambios):
    argumentos = dict(
        fecha=date(2026, 10, 30), turno_inicio=time(8, 0),
        turno_fin=time(17, 0), disponible=True,
        restriccion_circulacion=None,
    )
    argumentos.update(cambios)
    return SimpleNamespace(**argumentos)


def test_service_obtener_actualizar_y_turno_de_vehiculo_inexistente():
    servicio = FlotaService(FlotaMemoryRepository())
    inexistente = uuid4()
    with pytest.raises(VehiculoNoEncontradoError):
        servicio.obtener(inexistente)
    with pytest.raises(VehiculoNoEncontradoError):
        servicio.actualizar(inexistente, _datos())
    with pytest.raises(VehiculoNoEncontradoError):
        servicio.guardar_disponibilidad(inexistente, _turno())


def test_service_guarda_catalogo_y_transiciones_de_estado():
    repositorio = FlotaMemoryRepository()
    servicio = FlotaService(repositorio)
    creado = servicio.crear(_datos(placa=" abc-123 ", tipo=" Furgón "))
    assert creado.placa == "ABC-123"
    assert creado.tipo == "Furgón"
    editado = servicio.actualizar(creado.id, _datos(placa="abc-999", estado=EstadoVehiculo.MANTENIMIENTO))
    assert editado.placa == "ABC-999"
    assert editado.estado == EstadoVehiculo.MANTENIMIENTO
    assert servicio.obtener(creado.id).id == creado.id
    with pytest.raises(ReglaFlotaError, match=""):
        servicio.guardar_disponibilidad(creado.id, _turno(disponible=True))


def test_service_rechaza_turno_invertido_y_sin_restriccion_en_mismo_error():
    repositorio = FlotaMemoryRepository()
    servicio = FlotaService(repositorio)
    creado = servicio.crear(_datos())
    with pytest.raises(ReglaFlotaError) as error:
        servicio.guardar_disponibilidad(
            creado.id, _turno(turno_inicio=time(18), turno_fin=time(8),
                              disponible=False, restriccion_circulacion=None)
        )
    assert "turnoFin" in error.value.errors
    assert "restriccionCirculacion" in error.value.errors


def test_service_acepta_turno_no_disponible_con_razon_y_consulta_por_fecha():
    repositorio = FlotaMemoryRepository()
    servicio = FlotaService(repositorio)
    creado = servicio.crear(_datos())
    final = servicio.guardar_disponibilidad(
        creado.id, _turno(disponible=False, restriccion_circulacion="Mantenimiento preventivo")
    )
    assert final.disponibilidad.disponible is False
    assert final.disponibilidad.restriccion_circulacion == "Mantenimiento preventivo"
    assert servicio.obtener(creado.id, date(2026, 10, 30)).disponibilidad is not None
    assert servicio.obtener(creado.id, date(2026, 11, 1)).disponibilidad is None
    assert len(servicio.listar(date(2026, 10, 30))) == 1


def test_repositorio_rechaza_placas_repetidas_y_actualizacion_sin_id():
    repo = FlotaMemoryRepository()
    primero = _vehiculo()
    repo.crear(primero)
    with pytest.raises(PlacaDuplicadaError):
        repo.crear(_vehiculo())
    segundo = _vehiculo("W3A-124")
    repo.crear(segundo)
    with pytest.raises(PlacaDuplicadaError):
        repo.actualizar(Vehiculo(**{**segundo.__dict__, "placa": primero.placa}))
    assert repo.actualizar(_vehiculo("W3A-125")) is None
    assert repo.guardar_disponibilidad(
        uuid4(), DisponibilidadVehiculo(date(2026, 10, 30), time(8), time(17), True, None)
    ) is None


def test_health_falla_si_no_existe_postgis(monkeypatch):
    class Conexion:
        def __enter__(self): return self
        def __exit__(self, *_): return False
        def execute(self, _): return SimpleNamespace(scalar_one_or_none=lambda: None)
    monkeypatch.setattr(database_health, "get_engine", lambda: SimpleNamespace(connect=lambda: Conexion()))
    with pytest.raises(RuntimeError, match="PostGIS"):
        database_health.verificar_base_de_datos()


@pytest.mark.parametrize("tablas, correcto", [
    ({"pedidos", "ubicaciones"}, True),
    ({"pedidos"}, False),
    ({"ubicaciones"}, False),
])
def test_health_verifica_ambas_tablas_obligatorias(monkeypatch, tablas, correcto):
    class Conexion:
        def __enter__(self): return self
        def __exit__(self, *_): return False
        def execute(self, _): return SimpleNamespace(scalar_one_or_none=lambda: "3.5")
    monkeypatch.setattr(database_health, "get_engine", lambda: SimpleNamespace(connect=lambda: Conexion()))
    monkeypatch.setattr(database_health, "inspect", lambda _: SimpleNamespace(has_table=lambda tabla: tabla in tablas))
    if correcto:
        database_health.verificar_base_de_datos()
    else:
        with pytest.raises(RuntimeError, match="migraciones"):
            database_health.verificar_base_de_datos()
