"""Reglas de la vista previa de rutas (RF-04): capacidad, orden, ventanas y emisiones."""

from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from uuid import uuid4

from app.flota.domain import Combustible, DisponibilidadVehiculo, EstadoVehiculo, Vehiculo
from app.pedidos.domain import Ambito, Pedido, Ubicacion
from app.rutas.planificador import Punto, co2_kg, distancia_km, longitud_recorrido, planificar

LIMA = timezone(timedelta(hours=-5))
FECHA = date(2026, 10, 10)
DEPOSITO = Punto(-12.0651, -75.2049)
AMBITO = Ambito(-12.20, -11.95, -75.35, -75.10, ("Huancayo", "El Tambo", "Chilca"))


def pedido(codigo, lat, lon, kg=10.0, prioridad=2, inicio="08:00", fin="18:00", m3=0.1):
    return Pedido.crear(
        codigo=codigo,
        ubicacion=Ubicacion("Jr. Prueba 1", "Huancayo", lat, lon),
        destinatario_alias=None,
        demanda_kg=kg,
        demanda_m3=m3,
        tiempo_servicio_min=10,
        ventana_inicio=datetime.combine(FECHA, time.fromisoformat(inicio), tzinfo=LIMA),
        ventana_fin=datetime.combine(FECHA, time.fromisoformat(fin), tzinfo=LIMA),
        prioridad=prioridad,
        observacion_operativa=None,
        ambito=AMBITO,
        ahora=datetime(2026, 10, 9, 9, 0, tzinfo=LIMA),
    )


def vehiculo(placa, kg, combustible=Combustible.DIESEL, consumo="10", factor=None):
    return Vehiculo(
        id=uuid4(),
        placa=placa,
        tipo="Furgón",
        capacidad_kg=Decimal(kg),
        capacidad_m3=Decimal("10"),
        combustible=combustible,
        consumo_base_por_100km=Decimal(consumo),
        factor_emision_kgco2e_unidad=factor,
        anio=2022,
        estado=EstadoVehiculo.DISPONIBLE,
        creado_en=None,
        actualizado_en=None,
        disponibilidad=DisponibilidadVehiculo(FECHA, time(7, 0), time(18, 0), True, None),
    )


def test_distancia_aplica_factor_de_circuito():
    # Un grado de latitud ≈ 111,2 km en línea recta; × 1,3 por las calles.
    assert abs(distancia_km(Punto(0, 0), Punto(1, 0)) - 111.19 * 1.3) < 0.5


def test_respeta_la_capacidad_y_reporta_lo_que_no_cabe():
    pedidos = [pedido("A", -12.06, -75.21, kg=80), pedido("B", -12.07, -75.20, kg=80)]
    propuesta = planificar(FECHA, DEPOSITO, pedidos, [vehiculo("ECO-1", "100")])
    assert [len(r.paradas) for r in propuesta.rutas] == [1]
    assert propuesta.rutas[0].carga_kg <= 100
    assert len(propuesta.sin_asignar) == 1
    assert propuesta.sin_asignar[0].motivo == "Supera la capacidad libre de la flota"


def test_prioriza_los_urgentes_cuando_falta_capacidad():
    pedidos = [pedido("NORMAL", -12.06, -75.21, kg=80, prioridad=1), pedido("URGENTE", -12.09, -75.19, kg=80, prioridad=4)]
    propuesta = planificar(FECHA, DEPOSITO, pedidos, [vehiculo("ECO-1", "100")])
    assert propuesta.rutas[0].paradas[0].pedido.codigo == "URGENTE"
    assert propuesta.sin_asignar[0].pedido.codigo == "NORMAL"


def test_sin_vehiculos_todos_quedan_sin_asignar():
    propuesta = planificar(FECHA, DEPOSITO, [pedido("A", -12.06, -75.21)], [])
    assert propuesta.rutas == []
    assert propuesta.sin_asignar[0].motivo == "No hay vehículos disponibles para la fecha"


def test_la_ruta_propuesta_es_mas_corta_que_el_orden_de_registro():
    # Registro en zigzag: norte, sur, norte, sur.
    pedidos = [
        pedido("P1", -12.00, -75.24),
        pedido("P2", -12.10, -75.20),
        pedido("P3", -12.01, -75.25),
        pedido("P4", -12.11, -75.19),
    ]
    propuesta = planificar(FECHA, DEPOSITO, pedidos, [vehiculo("ECO-1", "500")])
    ruta = propuesta.rutas[0]
    assert ruta.distancia_km < propuesta.base.distancia_km
    assert ruta.co2_kg < propuesta.base.co2_kg
    orden = [p.pedido for p in ruta.paradas]
    assert abs(longitud_recorrido(DEPOSITO, orden) - ruta.distancia_km) < 1e-9


def test_marca_las_llegadas_fuera_de_ventana():
    tarde = pedido("TARDE", -12.06, -75.21, inicio="06:00", fin="07:01")
    ruta = planificar(FECHA, DEPOSITO, [tarde], [vehiculo("ECO-1", "100")]).rutas[0]
    assert ruta.paradas[0].dentro_de_ventana is False


def test_espera_a_que_abra_la_ventana():
    temprano = pedido("T", -12.06, -75.21, inicio="10:00", fin="11:00")
    parada = planificar(FECHA, DEPOSITO, [temprano], [vehiculo("ECO-1", "100")]).rutas[0].paradas[0]
    assert parada.llegada == temprano.ventana_inicio
    assert parada.dentro_de_ventana is True


def test_emisiones_usan_el_factor_del_vehiculo_o_el_de_referencia():
    diesel = vehiculo("ECO-1", "100", consumo="10")
    assert abs(co2_kg(diesel, 100) - 10 * 2.68) < 1e-9
    propio = vehiculo("ECO-2", "100", consumo="10", factor=Decimal("3"))
    assert abs(co2_kg(propio, 100) - 30) < 1e-9
    electrico = vehiculo("ECO-3", "100", combustible=Combustible.ELECTRICO, consumo="20")
    assert co2_kg(electrico, 100) < co2_kg(diesel, 100)


def test_cumple_una_ventana_temprana_aunque_el_orden_de_registro_no():
    lejos_y_temprano = pedido("C-CAJAS", -12.001, -75.2475, inicio="07:00", fin="07:40")
    pedidos = [pedido("A-SUR", -12.10, -75.20), pedido("B-CENTRO", -12.07, -75.21), lejos_y_temprano]
    propuesta = planificar(FECHA, DEPOSITO, pedidos, [vehiculo("ECO-1", "500")])
    assert all(p.dentro_de_ventana for p in propuesta.rutas[0].paradas)
    assert propuesta.base.fuera_de_ventana == 1


def test_prefiere_el_vehiculo_que_menos_emite():
    diesel = vehiculo("ECO-1", "500", consumo="12")
    electrico = vehiculo("ECO-2", "100", combustible=Combustible.ELECTRICO, consumo="6")
    propuesta = planificar(FECHA, DEPOSITO, [pedido("A", -12.06, -75.21, kg=20)], [diesel, electrico])
    assert propuesta.rutas[0].vehiculo.placa == "ECO-2"


def test_la_duracion_no_cuenta_la_espera_antes_de_salir():
    tarde = pedido("T", -12.06, -75.21, inicio="14:00", fin="16:00")
    ruta = planificar(FECHA, DEPOSITO, [tarde], [vehiculo("ECO-1", "100")]).rutas[0]
    assert ruta.paradas[0].llegada == tarde.ventana_inicio
    assert ruta.duracion_min < 30
