"""Vista previa de rutas (RF-04): heurística ligera y determinista, sin dependencias externas.

No reemplaza al motor de optimización VRPTW (OR-Tools) previsto para iteraciones posteriores;
sirve para visualizar en el mapa una propuesta razonable con los pedidos y la flota del día.

Supuestos (se devuelven también en la respuesta para que el usuario los vea):
- Distancia = gran círculo (haversine) × FACTOR_CIRCUITO, aproximación a la red vial urbana.
- Velocidad media urbana constante (VELOCIDAD_KMH) para estimar llegadas.
- Factores de emisión de referencia por tipo de combustible cuando el vehículo no declara uno.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from math import asin, cos, radians, sin, sqrt

from app.flota.domain import Combustible, Vehiculo
from app.pedidos.domain import Pedido

LIMA = timezone(timedelta(hours=-5))
RADIO_TIERRA_KM = 6371.0
FACTOR_CIRCUITO = 1.3
VELOCIDAD_KMH = 25.0
INICIO_TURNO_POR_DEFECTO = time(7, 0)

# kg CO2e por unidad de consumo (L, m³ o kWh). Valores referenciales para la vista previa.
FACTOR_EMISION_REFERENCIA = {
    Combustible.DIESEL: 2.68,
    Combustible.GASOLINA: 2.31,
    Combustible.HIBRIDO: 2.31,
    Combustible.GNV: 1.93,
    Combustible.ELECTRICO: 0.21,
}

SUPUESTOS = (
    f"Distancia en línea recta × {FACTOR_CIRCUITO} para aproximar calles reales.",
    f"Velocidad media urbana de {VELOCIDAD_KMH:g} km/h para estimar las llegadas.",
    "Factores de emisión de referencia: diésel 2,68 · gasolina 2,31 · GNV 1,93 kg CO₂e por unidad; "
    "eléctrico 0,21 kg CO₂e/kWh. Se usa el factor del vehículo si está registrado.",
    "La propuesta prioriza llegar dentro de la ventana horaria y, luego, la menor emisión de CO₂e.",
    "La base de comparación llena los vehículos por placa con los pedidos en orden de registro, sin optimizar.",
)


@dataclass(frozen=True)
class Punto:
    latitud: float
    longitud: float


@dataclass
class Parada:
    pedido: Pedido
    llegada: datetime
    dentro_de_ventana: bool


@dataclass
class Ruta:
    vehiculo: Vehiculo
    paradas: list[Parada]
    distancia_km: float
    duracion_min: float
    carga_kg: float
    carga_m3: float
    co2_kg: float


@dataclass
class Base:
    """Totales del despacho sin optimizar, para medir el ahorro."""

    distancia_km: float = 0.0
    co2_kg: float = 0.0
    fuera_de_ventana: int = 0


@dataclass
class SinAsignar:
    pedido: Pedido
    motivo: str


@dataclass
class Propuesta:
    fecha: date
    deposito: Punto
    rutas: list[Ruta] = field(default_factory=list)
    sin_asignar: list[SinAsignar] = field(default_factory=list)
    base: Base = field(default_factory=Base)


def distancia_km(a: Punto, b: Punto) -> float:
    """Distancia vial aproximada entre dos puntos."""
    lat1, lon1, lat2, lon2 = map(radians, (a.latitud, a.longitud, b.latitud, b.longitud))
    h = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return 2 * RADIO_TIERRA_KM * asin(sqrt(h)) * FACTOR_CIRCUITO


def _punto(pedido: Pedido) -> Punto:
    return Punto(pedido.ubicacion.latitud, pedido.ubicacion.longitud)


def longitud_recorrido(deposito: Punto, pedidos: list[Pedido]) -> float:
    """Depósito → paradas en orden → depósito."""
    puntos = [deposito, *map(_punto, pedidos), deposito]
    return sum(distancia_km(a, b) for a, b in zip(puntos, puntos[1:]))


def _vecino_mas_cercano(deposito: Punto, pedidos: list[Pedido]) -> list[Pedido]:
    pendientes = list(pedidos)
    orden: list[Pedido] = []
    actual = deposito
    while pendientes:
        # Desempate por prioridad (mayor primero) y código, para un resultado determinista.
        siguiente = min(pendientes, key=lambda p: (distancia_km(actual, _punto(p)), -p.prioridad, p.codigo))
        pendientes.remove(siguiente)
        orden.append(siguiente)
        actual = _punto(siguiente)
    return orden


def _dos_opt(orden: list[Pedido], costo: Callable[[list[Pedido]], tuple[int, float]]) -> list[Pedido]:
    """Invierte tramos mientras baje el costo (mejora local clásica 2-opt)."""
    mejor = list(orden)
    mejor_costo = costo(mejor)
    mejora = True
    while mejora:
        mejora = False
        for i in range(len(mejor) - 1):
            for j in range(i + 2, len(mejor) + 1):
                candidato = mejor[:i] + mejor[i:j][::-1] + mejor[j:]
                c = costo(candidato)
                if c[0] < mejor_costo[0] or (c[0] == mejor_costo[0] and c[1] < mejor_costo[1] - 1e-9):
                    mejor, mejor_costo, mejora = candidato, c, True
    return mejor


def _factor_emision(vehiculo: Vehiculo) -> float:
    if vehiculo.factor_emision_kgco2e_unidad is not None:
        return float(vehiculo.factor_emision_kgco2e_unidad)
    return FACTOR_EMISION_REFERENCIA[vehiculo.combustible]


def co2_kg(vehiculo: Vehiculo, km: float) -> float:
    return km / 100 * float(vehiculo.consumo_base_por_100km) * _factor_emision(vehiculo)


def _programar(deposito: Punto, vehiculo: Vehiculo, fecha: date, orden: list[Pedido]) -> tuple[list[Parada], float]:
    inicio_turno = vehiculo.disponibilidad.turno_inicio if vehiculo.disponibilidad else INICIO_TURNO_POR_DEFECTO
    salida = datetime.combine(fecha, inicio_turno, tzinfo=LIMA)
    if orden:
        # No se sale antes de lo necesario: se llega a la primera parada cuando abre su ventana.
        traslado = timedelta(hours=distancia_km(deposito, _punto(orden[0])) / VELOCIDAD_KMH)
        salida = max(salida, orden[0].ventana_inicio - traslado)
    reloj = salida
    actual = deposito
    paradas: list[Parada] = []
    for pedido in orden:
        reloj += timedelta(hours=distancia_km(actual, _punto(pedido)) / VELOCIDAD_KMH)
        llegada = max(reloj, pedido.ventana_inicio)  # si llega antes, espera a que abra la ventana
        paradas.append(Parada(pedido, llegada, llegada <= pedido.ventana_fin))
        reloj = llegada + timedelta(minutes=pedido.tiempo_servicio_min)
        actual = _punto(pedido)
    reloj += timedelta(hours=distancia_km(actual, deposito) / VELOCIDAD_KMH)
    return paradas, (reloj - salida).total_seconds() / 60


def planificar(fecha: date, deposito: Punto, pedidos: list[Pedido], vehiculos: list[Vehiculo]) -> Propuesta:
    """Asigna pedidos a vehículos respetando capacidad y ordena cada ruta para cumplir ventanas y emitir menos."""
    propuesta = Propuesta(fecha=fecha, deposito=deposito)
    flota = sorted(vehiculos, key=lambda v: (-float(v.capacidad_kg), v.placa))
    rutas: dict[str, list[Pedido]] = {v.placa: [] for v in flota}
    carga = {v.placa: [0.0, 0.0] for v in flota}

    def costo(vehiculo: Vehiculo, orden: list[Pedido]) -> tuple[int, float]:
        # Primero cumplir ventanas horarias; luego, la menor emisión (Green VRP).
        tardias = sum(not p.dentro_de_ventana for p in _programar(deposito, vehiculo, fecha, orden)[0])
        return tardias, co2_kg(vehiculo, longitud_recorrido(deposito, orden))

    # Inserción más barata: los urgentes y de ventana temprana se ubican primero.
    for pedido in sorted(pedidos, key=lambda p: (-p.prioridad, p.ventana_inicio, p.codigo)):
        mejor: tuple[tuple[int, float], Vehiculo, list[Pedido]] | None = None
        for v in flota:
            if (
                carga[v.placa][0] + pedido.demanda_kg > float(v.capacidad_kg)
                or carga[v.placa][1] + pedido.demanda_m3 > float(v.capacidad_m3)
            ):
                continue
            actual = costo(v, rutas[v.placa])
            for i in range(len(rutas[v.placa]) + 1):
                orden = rutas[v.placa][:i] + [pedido] + rutas[v.placa][i:]
                nuevo = costo(v, orden)
                delta = (nuevo[0] - actual[0], nuevo[1] - actual[1])
                if mejor is None or delta < mejor[0]:
                    mejor = (delta, v, orden)
        if mejor is None:
            motivo = "No hay vehículos disponibles para la fecha" if not flota else "Supera la capacidad libre de la flota"
            propuesta.sin_asignar.append(SinAsignar(pedido, motivo))
            continue
        _, elegido, orden = mejor
        rutas[elegido.placa] = orden
        carga[elegido.placa][0] += pedido.demanda_kg
        carga[elegido.placa][1] += pedido.demanda_m3

    for vehiculo in flota:
        lote = rutas[vehiculo.placa]
        if not lote:
            continue
        # Pulido final con 2-opt desde la inserción y desde el vecino más cercano.
        inicios = (lote, _vecino_mas_cercano(deposito, lote))
        orden = min((_dos_opt(o, lambda o, v=vehiculo: costo(v, o)) for o in inicios), key=lambda o: costo(vehiculo, o))
        paradas, duracion = _programar(deposito, vehiculo, fecha, orden)
        km = longitud_recorrido(deposito, orden)
        propuesta.rutas.append(
            Ruta(
                vehiculo=vehiculo,
                paradas=paradas,
                distancia_km=km,
                duracion_min=duracion,
                carga_kg=carga[vehiculo.placa][0],
                carga_m3=carga[vehiculo.placa][1],
                co2_kg=co2_kg(vehiculo, km),
            )
        )
    propuesta.base = despacho_sin_optimizar(fecha, deposito, pedidos, vehiculos)
    return propuesta


def despacho_sin_optimizar(fecha: date, deposito: Punto, pedidos: list[Pedido], vehiculos: list[Vehiculo]) -> Base:
    """Referencia de comparación: se llena cada vehículo en orden de placa con los pedidos
    en el orden en que se registraron, y cada uno los visita en ese mismo orden."""
    base = Base()
    flota = sorted(vehiculos, key=lambda v: v.placa)
    lotes: dict[str, list[Pedido]] = {v.placa: [] for v in flota}
    for pedido in sorted(pedidos, key=lambda p: (p.creado_en, p.codigo)):
        for v in flota:
            lote = lotes[v.placa]
            if (
                sum(p.demanda_kg for p in lote) + pedido.demanda_kg <= float(v.capacidad_kg)
                and sum(p.demanda_m3 for p in lote) + pedido.demanda_m3 <= float(v.capacidad_m3)
            ):
                lote.append(pedido)
                break
    for v in flota:
        if lotes[v.placa]:
            km = longitud_recorrido(deposito, lotes[v.placa])
            base.distancia_km += km
            base.co2_kg += co2_kg(v, km)
            base.fuera_de_ventana += sum(
                not p.dentro_de_ventana for p in _programar(deposito, v, fecha, lotes[v.placa])[0]
            )
    return base
