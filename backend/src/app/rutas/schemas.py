"""Contratos JSON de la vista previa de rutas (camelCase)."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.flota.domain import Combustible
from app.rutas.planificador import SUPUESTOS, Propuesta, Ruta


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


def _r(valor: float, decimales: int = 2) -> float:
    return round(valor, decimales)


class PuntoOut(_Base):
    nombre: str
    latitud: float
    longitud: float


class VehiculoRutaOut(_Base):
    id: UUID
    placa: str
    tipo: str
    combustible: Combustible
    capacidad_kg: float
    capacidad_m3: float


class ParadaOut(_Base):
    orden: int
    pedido_id: UUID
    codigo: str
    destinatario_alias: str | None
    direccion: str
    distrito: str
    latitud: float
    longitud: float
    demanda_kg: float
    prioridad: int
    ventana_inicio: datetime
    ventana_fin: datetime
    llegada_estimada: datetime
    dentro_de_ventana: bool


class RutaOut(_Base):
    vehiculo: VehiculoRutaOut
    paradas: list[ParadaOut]
    distancia_km: float
    duracion_min: int
    carga_kg: float
    uso_capacidad_pct: float
    co2_kg: float

    @classmethod
    def desde_dominio(cls, ruta: Ruta) -> "RutaOut":
        v = ruta.vehiculo
        return cls(
            vehiculo=VehiculoRutaOut(
                id=v.id,
                placa=v.placa,
                tipo=v.tipo,
                combustible=v.combustible,
                capacidad_kg=float(v.capacidad_kg),
                capacidad_m3=float(v.capacidad_m3),
            ),
            paradas=[
                ParadaOut(
                    orden=i,
                    pedido_id=p.pedido.id,
                    codigo=p.pedido.codigo,
                    destinatario_alias=p.pedido.destinatario_alias,
                    direccion=p.pedido.ubicacion.direccion_referencial,
                    distrito=p.pedido.ubicacion.distrito,
                    latitud=p.pedido.ubicacion.latitud,
                    longitud=p.pedido.ubicacion.longitud,
                    demanda_kg=p.pedido.demanda_kg,
                    prioridad=p.pedido.prioridad,
                    ventana_inicio=p.pedido.ventana_inicio,
                    ventana_fin=p.pedido.ventana_fin,
                    llegada_estimada=p.llegada,
                    dentro_de_ventana=p.dentro_de_ventana,
                )
                for i, p in enumerate(ruta.paradas, start=1)
            ],
            distancia_km=_r(ruta.distancia_km),
            duracion_min=round(ruta.duracion_min),
            carga_kg=_r(ruta.carga_kg),
            uso_capacidad_pct=_r(ruta.carga_kg / float(v.capacidad_kg) * 100, 1),
            co2_kg=_r(ruta.co2_kg),
        )


class SinAsignarOut(_Base):
    pedido_id: UUID
    codigo: str
    demanda_kg: float
    motivo: str


class ResumenOut(_Base):
    pedidos: int
    asignados: int
    vehiculos_usados: int
    vehiculos_disponibles: int
    distancia_km: float
    distancia_base_km: float
    co2_kg: float
    co2_base_kg: float
    ahorro_co2_pct: float
    paradas_fuera_de_ventana: int
    paradas_fuera_de_ventana_base: int


class VistaPreviaOut(_Base):
    fecha: date
    deposito: PuntoOut
    rutas: list[RutaOut]
    sin_asignar: list[SinAsignarOut]
    resumen: ResumenOut
    supuestos: list[str]

    @classmethod
    def desde_dominio(cls, propuesta: Propuesta, nombre_deposito: str, vehiculos_disponibles: int) -> "VistaPreviaOut":
        rutas = [RutaOut.desde_dominio(r) for r in propuesta.rutas]
        co2 = sum(r.co2_kg for r in propuesta.rutas)
        co2_base = propuesta.base.co2_kg
        asignados = sum(len(r.paradas) for r in propuesta.rutas)
        return cls(
            fecha=propuesta.fecha,
            deposito=PuntoOut(
                nombre=nombre_deposito,
                latitud=propuesta.deposito.latitud,
                longitud=propuesta.deposito.longitud,
            ),
            rutas=rutas,
            sin_asignar=[
                SinAsignarOut(pedido_id=s.pedido.id, codigo=s.pedido.codigo, demanda_kg=s.pedido.demanda_kg, motivo=s.motivo)
                for s in propuesta.sin_asignar
            ],
            resumen=ResumenOut(
                pedidos=asignados + len(propuesta.sin_asignar),
                asignados=asignados,
                vehiculos_usados=len(rutas),
                vehiculos_disponibles=vehiculos_disponibles,
                distancia_km=_r(sum(r.distancia_km for r in propuesta.rutas)),
                distancia_base_km=_r(propuesta.base.distancia_km),
                co2_kg=_r(co2),
                co2_base_kg=_r(co2_base),
                ahorro_co2_pct=_r((1 - co2 / co2_base) * 100, 1) if co2_base > 0 else 0.0,
                paradas_fuera_de_ventana=sum(
                    1 for r in propuesta.rutas for p in r.paradas if not p.dentro_de_ventana
                ),
                paradas_fuera_de_ventana_base=propuesta.base.fuera_de_ventana,
            ),
            supuestos=list(SUPUESTOS),
        )
