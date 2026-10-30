"""Benchmark del planificador de rutas (EN-001): tiempo de generación frente al objetivo de 45 s.

Uso, desde `backend/`:
    python scripts/benchmark_rutas.py            # volúmenes por defecto
    python scripts/benchmark_rutas.py 50 150     # volúmenes propios (pedidos)

Los datos son sintéticos y reproducibles (semilla fija) dentro del ámbito de Huancayo.
"""

import random
import sys
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from time import perf_counter
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app.config import get_settings  # noqa: E402
from app.flota.domain import Combustible, DisponibilidadVehiculo, EstadoVehiculo, Vehiculo  # noqa: E402
from app.pedidos.domain import Pedido, Ubicacion  # noqa: E402
from app.rutas.planificador import Punto, planificar  # noqa: E402

LIMA = timezone(timedelta(hours=-5))
OBJETIVO_S = 45.0
VOLUMENES = (25, 50, 100, 150)
FECHA = date(2026, 11, 2)


def pedidos_sinteticos(n: int, azar: random.Random) -> list[Pedido]:
    ambito = get_settings().ambito
    datos = []
    for i in range(n):
        inicio = datetime.combine(FECHA, time(7 + azar.randint(0, 8), 0), tzinfo=LIMA)
        datos.append(
            Pedido.crear(
                codigo=f"BM-{i:04d}",
                ubicacion=Ubicacion(f"Calle {i}", "Huancayo", azar.uniform(-12.12, -12.00), azar.uniform(-75.28, -75.18)),
                destinatario_alias=None,
                demanda_kg=azar.uniform(5, 60),
                demanda_m3=azar.uniform(0.05, 0.6),
                tiempo_servicio_min=10,
                ventana_inicio=inicio,
                ventana_fin=inicio + timedelta(hours=3),
                prioridad=azar.randint(1, 4),
                observacion_operativa=None,
                ambito=ambito,
            )
        )
    return datos


def flota_sintetica(n_pedidos: int) -> list[Vehiculo]:
    cantidad = max(3, n_pedidos // 12)
    return [
        Vehiculo(
            id=uuid4(),
            placa=f"BM{i:03d}",
            tipo="Camioneta",
            capacidad_kg=Decimal(500),
            capacidad_m3=Decimal(6),
            combustible=Combustible.DIESEL,
            consumo_base_por_100km=Decimal(12),
            factor_emision_kgco2e_unidad=None,
            anio=2022,
            estado=EstadoVehiculo.DISPONIBLE,
            creado_en=None,
            actualizado_en=None,
            disponibilidad=DisponibilidadVehiculo(FECHA, time(7, 0), time(19, 0), True, None),
        )
        for i in range(cantidad)
    ]


def main() -> None:
    volumenes = tuple(int(a) for a in sys.argv[1:]) or VOLUMENES
    settings = get_settings()
    deposito = Punto(settings.deposito_lat, settings.deposito_lon)
    print(f"{'Pedidos':>8} {'Vehículos':>10} {'Asignados':>10} {'Tiempo (s)':>11}  Objetivo <= {OBJETIVO_S:g} s")
    for n in volumenes:
        pedidos = pedidos_sinteticos(n, random.Random(2026))
        flota = flota_sintetica(n)
        inicio = perf_counter()
        propuesta = planificar(FECHA, deposito, pedidos, flota)
        segundos = perf_counter() - inicio
        asignados = sum(len(r.paradas) for r in propuesta.rutas)
        print(f"{n:>8} {len(flota):>10} {asignados:>10} {segundos:>11.2f}  {'cumple' if segundos <= OBJETIVO_S else 'NO cumple'}")


if __name__ == "__main__":
    main()
