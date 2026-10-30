"""Contrato JSON del dashboard de indicadores (camelCase)."""

from datetime import date

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.flota.domain import Combustible
from app.indicadores.service import Indicadores
from app.pedidos.domain import EstadoPedido


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ConteoEstado(_Base):
    estado: EstadoPedido
    cantidad: int


class ConteoDistrito(_Base):
    distrito: str
    cantidad: int
    peso_kg: float


class ConteoPrioridad(_Base):
    prioridad: int
    cantidad: int


class ConteoCombustible(_Base):
    combustible: Combustible
    cantidad: int


class PedidosResumen(_Base):
    total: int
    peso_kg: float
    por_estado: list[ConteoEstado]
    por_distrito: list[ConteoDistrito]
    por_prioridad: list[ConteoPrioridad]


class FlotaResumen(_Base):
    total: int
    aptos: int
    capacidad_apta_kg: float
    por_combustible: list[ConteoCombustible]


class DiaResumen(_Base):
    """Planificación de la fecha consultada, según la vista previa de rutas."""

    pedidos: int
    asignados: int
    demanda_kg: float
    uso_capacidad_pct: float
    distancia_km: float
    distancia_base_km: float
    co2_kg: float
    co2_base_kg: float
    ahorro_co2_pct: float
    paradas_a_tiempo_pct: float


class IndicadoresOut(_Base):
    fecha: date
    pedidos: PedidosResumen
    flota: FlotaResumen
    dia: DiaResumen

    @classmethod
    def desde_dominio(cls, ind: Indicadores) -> "IndicadoresOut":
        propuesta = ind.propuesta
        aptos = [v for v in ind.vehiculos if v.elegible_para_planificar]
        capacidad = sum(float(v.capacidad_kg) for v in aptos)
        paradas = [p for r in propuesta.rutas for p in r.paradas]
        demanda = sum(p.pedido.demanda_kg for p in paradas) + sum(s.pedido.demanda_kg for s in propuesta.sin_asignar)
        carga = sum(r.carga_kg for r in propuesta.rutas)
        co2 = sum(r.co2_kg for r in propuesta.rutas)
        base = propuesta.base.co2_kg
        return cls(
            fecha=ind.fecha,
            pedidos=PedidosResumen(
                total=len(ind.pedidos),
                peso_kg=round(sum(p.demanda_kg for p in ind.pedidos), 2),
                por_estado=[ConteoEstado(estado=e, cantidad=n) for e, n in ind.por_estado],
                por_distrito=[
                    ConteoDistrito(distrito=d, cantidad=n, peso_kg=round(kg, 2)) for d, n, kg in ind.por_distrito
                ],
                por_prioridad=[ConteoPrioridad(prioridad=p, cantidad=n) for p, n in ind.por_prioridad],
            ),
            flota=FlotaResumen(
                total=len(ind.vehiculos),
                aptos=ind.vehiculos_aptos,
                capacidad_apta_kg=round(capacidad, 2),
                por_combustible=[ConteoCombustible(combustible=c, cantidad=n) for c, n in ind.por_combustible],
            ),
            dia=DiaResumen(
                pedidos=len(paradas) + len(propuesta.sin_asignar),
                asignados=len(paradas),
                demanda_kg=round(demanda, 2),
                uso_capacidad_pct=round(carga / capacidad * 100, 1) if capacidad else 0.0,
                distancia_km=round(sum(r.distancia_km for r in propuesta.rutas), 2),
                distancia_base_km=round(propuesta.base.distancia_km, 2),
                co2_kg=round(co2, 2),
                co2_base_kg=round(base, 2),
                ahorro_co2_pct=round((1 - co2 / base) * 100, 1) if base > 0 else 0.0,
                paradas_a_tiempo_pct=(
                    round(sum(p.dentro_de_ventana for p in paradas) / len(paradas) * 100, 1) if paradas else 0.0
                ),
            ),
        )
