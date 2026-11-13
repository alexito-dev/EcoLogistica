"""Contratos JSON de Conduccion (camelCase)."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from app.conduccion.domain import EstadoParada
from app.rutas.schemas import PuntoOut, VehiculoRutaOut


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ParadaEjecucionOut(_Base):
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
    estado: EstadoParada
    nota: str | None
    actualizado_en: datetime | None


class AvanceOut(_Base):
    total: int
    entregadas: int
    incidencias: int
    canceladas: int
    reprogramadas: int


class RutaConduccionOut(_Base):
    vehiculo: VehiculoRutaOut
    conductor_id: str | None
    conductor_nombre: str | None
    paradas: list[ParadaEjecucionOut]
    distancia_km: float
    avance: AvanceOut


class MiRutaOut(_Base):
    fecha: date
    deposito: PuntoOut
    rutas: list[RutaConduccionOut]


class IncidenciaOut(_Base):
    pedido_id: UUID
    codigo: str
    direccion: str
    distrito: str
    nota: str | None
    vehiculo: str
    conductor_nombre: str | None
    actualizado_en: datetime | None


class ConductorOut(_Base):
    id: str
    nombre: str


class SeguimientoOut(_Base):
    fecha: date
    deposito: PuntoOut
    rutas: list[RutaConduccionOut]
    incidencias: list[IncidenciaOut]
    conductores_disponibles: list[ConductorOut]


class EstadoIn(_Base):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="forbid")

    fecha: date
    estado: EstadoParada
    nota: str | None = Field(default=None, max_length=500)


class AsignacionIn(_Base):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="forbid")

    fecha: date
    vehiculo_id: UUID
    conductor_id: str = Field(min_length=1, max_length=64)


class FechaIn(_Base):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="forbid")

    fecha: date


class ReoptimizacionOut(_Base):
    rutas_reordenadas: int


class EventoOut(_Base):
    estado: EstadoParada
    nota: str | None
    usuario_id: str | None
    creado_en: datetime
