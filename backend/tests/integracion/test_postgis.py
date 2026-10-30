"""Pruebas reales de integración de repositorios contra PostgreSQL/PostGIS aislado.

Requieren ECO_TEST_DATABASE_URL y una base de pruebas con migraciones Alembic aplicadas.
No usamos DATABASE_URL de producción ni ejecutamos escrituras sin una URL explícita de pruebas.
"""

import os
from datetime import date, datetime, time, timezone
from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, text

from app.flota.domain import Combustible, DisponibilidadVehiculo, EstadoVehiculo, Vehiculo
from app.flota.postgres_repository import FlotaPostgresRepository
from app.pedidos.domain import Ambito, EstadoPedido, Pedido, Ubicacion
from app.pedidos.postgres_repository import PedidosPostgresRepository


@pytest.fixture
def engine_postgis():
    url = os.environ.get("ECO_TEST_DATABASE_URL")
    if not url:
        pytest.skip("Solo se permite PostgreSQL de pruebas mediante ECO_TEST_DATABASE_URL")
    from sqlalchemy.engine import make_url

    nombre_base = make_url(url).database or ""
    if not nombre_base.endswith("_test"):
        pytest.fail("ECO_TEST_DATABASE_URL debe apuntar a una base terminada en _test")
    engine = create_engine(url, pool_pre_ping=True)
    try:
        with engine.connect() as conexion:
            assert conexion.execute(text("SELECT PostGIS_Version()")).scalar_one()
        yield engine
    finally:
        engine.dispose()


def test_pedido_y_coordenadas_persisten_entre_instancias(engine_postgis):
    repositorio = PedidosPostgresRepository(engine_postgis)
    ambito = Ambito(-12.20, -11.95, -75.35, -75.10, ("Huancayo",))
    pedido = Pedido.crear(
        codigo=f"TEST-{uuid4().hex[:12].upper()}",
        ubicacion=Ubicacion("Jr. Real 123", "Huancayo", -12.06, -75.20),
        demanda_kg=10.0,
        demanda_m3=0.5,
        tiempo_servicio_min=10,
        ventana_inicio=datetime(2026, 10, 30, 8, tzinfo=timezone.utc),
        ventana_fin=datetime(2026, 10, 30, 12, tzinfo=timezone.utc),
        prioridad=2,
        ambito=ambito,
    )
    try:
        repositorio.guardar(pedido)
        nuevo_repositorio = PedidosPostgresRepository(engine_postgis)
        recuperado = nuevo_repositorio.obtener(pedido.id)
        assert recuperado is not None
        assert recuperado.codigo == pedido.codigo
        assert recuperado.estado == EstadoPedido.PENDIENTE
        assert recuperado.ubicacion.latitud == pytest.approx(-12.06)
        assert recuperado.ubicacion.longitud == pytest.approx(-75.20)
        assert nuevo_repositorio.obtener_por_codigo(pedido.codigo).id == pedido.id
    finally:
        with engine_postgis.begin() as conexion:
            conexion.execute(text("DELETE FROM pedidos WHERE id=:id"), {"id": pedido.id})
            conexion.execute(text("DELETE FROM ubicaciones WHERE id=:id"), {"id": pedido.id})


def test_vehiculo_y_disponibilidad_persisten_entre_instancias(engine_postgis):
    repositorio = FlotaPostgresRepository(engine_postgis)
    vehiculo = Vehiculo(
        id=uuid4(),
        placa=f"T{uuid4().hex[:6].upper()}",
        tipo="Furgón de prueba",
        capacidad_kg=Decimal("700.00"),
        capacidad_m3=Decimal("6.500"),
        combustible=Combustible.DIESEL,
        consumo_base_por_100km=Decimal("12.5000"),
        factor_emision_kgco2e_unidad=None,
        anio=2022,
        estado=EstadoVehiculo.DISPONIBLE,
        creado_en=None,
        actualizado_en=None,
    )
    fecha = date(2026, 10, 30)
    try:
        repositorio.crear(vehiculo)
        repositorio.guardar_disponibilidad(
            vehiculo.id,
            DisponibilidadVehiculo(fecha, time(8), time(17), True, None),
        )
        nuevo_repositorio = FlotaPostgresRepository(engine_postgis)
        recuperado = nuevo_repositorio.obtener(vehiculo.id, fecha)
        assert recuperado is not None
        assert recuperado.placa == vehiculo.placa
        assert recuperado.elegible_para_planificar
        assert recuperado.disponibilidad.fecha == fecha
        assert any(v.id == vehiculo.id for v in nuevo_repositorio.listar(fecha))
    finally:
        with engine_postgis.begin() as conexion:
            conexion.execute(
                text("DELETE FROM disponibilidad_vehiculos WHERE vehiculo_id=:id"),
                {"id": vehiculo.id},
            )
            conexion.execute(text("DELETE FROM vehiculos WHERE id=:id"), {"id": vehiculo.id})


def test_postgis_pedidos_filtrado_paginacion_duplicados_y_correlativo(engine_postgis):
    """Verificamos filtros, ausencia, paginación y atomicidad ante código repetido."""
    from dataclasses import replace
    from app.pedidos.domain import CodigoDuplicadoError

    repo = PedidosPostgresRepository(engine_postgis)
    ambito = Ambito(-12.20, -11.95, -75.35, -75.10, ("Huancayo",))
    pedido = Pedido.crear(
        codigo=f"INTEG-{uuid4().hex[:12].upper()}",
        ubicacion=Ubicacion("Av. Giráldez 456", "Huancayo", -12.065, -75.205),
        demanda_kg=18, demanda_m3=0.7, tiempo_servicio_min=12,
        ventana_inicio=datetime(2026, 10, 30, 8, tzinfo=timezone.utc),
        ventana_fin=datetime(2026, 10, 30, 14, tzinfo=timezone.utc),
        prioridad=3, ambito=ambito,
    )
    try:
        repo.guardar(pedido)
        assert repo.obtener(uuid4()) is None
        assert repo.obtener_por_codigo(f"AUSENTE-{uuid4().hex}") is None
        pendientes, total = repo.listar(EstadoPedido.PENDIENTE, pagina=1, limite=100)
        assert total >= 1
        assert any(p.id == pedido.id for p in pendientes)
        entregados, _ = repo.listar(EstadoPedido.ENTREGADO, pagina=1, limite=100)
        assert all(p.estado == EstadoPedido.ENTREGADO for p in entregados)
        todos, _ = repo.listar(None, pagina=1, limite=100)
        assert any(p.id == pedido.id for p in todos)
        assert repo.siguiente_correlativo() > 0
        repetido = replace(pedido, id=uuid4())
        with pytest.raises(CodigoDuplicadoError):
            repo.guardar(repetido)
        assert repo.obtener(repetido.id) is None
    finally:
        with engine_postgis.begin() as conexion:
            conexion.execute(text("DELETE FROM pedidos WHERE id=:id"), {"id": pedido.id})
            conexion.execute(text("DELETE FROM ubicaciones WHERE id=:id"), {"id": pedido.id})


def test_postgis_flota_actualizacion_duplicados_y_upsert_de_turno(engine_postgis):
    """Comprobamos restricciones SQL y el cambio persistente de turno de la misma fecha."""
    from dataclasses import replace
    from app.flota.domain import PlacaDuplicadaError

    repo = FlotaPostgresRepository(engine_postgis)
    primero = Vehiculo(
        id=uuid4(), placa=f"T{uuid4().hex[:6].upper()}", tipo="Camión",
        capacidad_kg=Decimal("800"), capacidad_m3=Decimal("9"),
        combustible=Combustible.DIESEL, consumo_base_por_100km=Decimal("14"),
        factor_emision_kgco2e_unidad=None, anio=2023,
        estado=EstadoVehiculo.DISPONIBLE, creado_en=None, actualizado_en=None,
    )
    segundo = replace(primero, id=uuid4(), placa=f"T{uuid4().hex[:6].upper()}")
    fecha = date(2026, 10, 30)
    try:
        repo.crear(primero)
        repo.crear(segundo)
        assert repo.obtener(uuid4()) is None
        assert repo.actualizar(replace(primero, id=uuid4())) is None
        assert repo.guardar_disponibilidad(
            uuid4(), DisponibilidadVehiculo(fecha, time(8), time(17), True, None)
        ) is None
        with pytest.raises(PlacaDuplicadaError):
            repo.crear(replace(primero, id=uuid4()))
        with pytest.raises(PlacaDuplicadaError):
            repo.actualizar(replace(segundo, placa=primero.placa))

        modificado = repo.actualizar(replace(primero, tipo="Furgón", capacidad_kg=Decimal("950")))
        assert modificado is not None
        assert modificado.tipo == "Furgón"
        assert modificado.capacidad_kg == Decimal("950")
        assert modificado.actualizado_en is not None

        inicial = DisponibilidadVehiculo(fecha, time(8), time(17), True, None)
        repo.guardar_disponibilidad(primero.id, inicial)
        nuevo = DisponibilidadVehiculo(fecha, time(9), time(16), False, "Revisión técnica")
        repo.guardar_disponibilidad(primero.id, nuevo)
        almacenado = FlotaPostgresRepository(engine_postgis).obtener(primero.id, fecha)
        assert almacenado is not None
        assert almacenado.disponibilidad is not None
        assert almacenado.disponibilidad.turno_inicio == time(9)
        assert almacenado.disponibilidad.disponible is False
        assert almacenado.disponibilidad.restriccion_circulacion == "Revisión técnica"
        assert any(v.id == primero.id for v in repo.listar())
    finally:
        with engine_postgis.begin() as conexion:
            for vehiculo in (primero, segundo):
                conexion.execute(
                    text("DELETE FROM disponibilidad_vehiculos WHERE vehiculo_id=:id"),
                    {"id": vehiculo.id},
                )
                conexion.execute(text("DELETE FROM vehiculos WHERE id=:id"), {"id": vehiculo.id})
