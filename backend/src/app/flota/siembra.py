"""Vehículos de demostración (datos sintéticos) con turno declarado para el día siguiente."""

from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal

from app.flota.domain import Combustible
from app.flota.repository import FlotaRepository
from app.flota.schemas import DisponibilidadGuardar, VehiculoGuardar
from app.flota.service import FlotaService

LIMA = timezone(timedelta(hours=-5))

# placa, tipo, kg, m3, combustible, consumo por 100 km, año
VEHICULOS_DEMO = [
    ("ECO-101", "Furgón mediano", 600, 6.0, Combustible.DIESEL, 11.5, 2021),
    ("ECO-102", "Furgoneta", 350, 3.5, Combustible.GNV, 9.0, 2022),
    ("ECO-103", "Moto carguera eléctrica", 120, 1.2, Combustible.ELECTRICO, 6.0, 2024),
]


def sembrar_vehiculos_demo(repositorio: FlotaRepository, ahora: datetime | None = None) -> int:
    """Registra la flota de demostración y su turno de mañana si aún no hay vehículos."""
    if repositorio.listar():
        return 0
    servicio = FlotaService(repositorio)
    manana: date = ((ahora or datetime.now(LIMA)).astimezone(LIMA) + timedelta(days=1)).date()
    for placa, tipo, kg, m3, combustible, consumo, anio in VEHICULOS_DEMO:
        vehiculo = servicio.crear(
            VehiculoGuardar(
                placa=placa,
                tipo=tipo,
                capacidad_kg=Decimal(str(kg)),
                capacidad_m3=Decimal(str(m3)),
                combustible=combustible,
                consumo_base_por_100km=Decimal(str(consumo)),
                anio=anio,
            )
        )
        servicio.guardar_disponibilidad(
            vehiculo.id,
            DisponibilidadGuardar(fecha=manana, turno_inicio=time(7, 0), turno_fin=time(18, 0)),
        )
    return len(VEHICULOS_DEMO)
