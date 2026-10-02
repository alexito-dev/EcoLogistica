"""Esquemas Pydantic de la API de pedidos (JSON en camelCase)."""

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, StringConstraints
from pydantic.alias_generators import to_camel

from app.pedidos.domain import EstadoPedido, Pedido

_Codigo = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=40)]
_Direccion = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=250)]
_Distrito = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]
_Alias = Annotated[str, StringConstraints(strip_whitespace=True, max_length=120)]
_Observacion = Annotated[str, StringConstraints(strip_whitespace=True, max_length=500)]


class _Base(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )


class PedidoCrear(_Base):
    codigo: _Codigo | None = None
    direccion: _Direccion
    distrito: _Distrito
    latitud: float = Field(ge=-90, le=90)
    longitud: float = Field(ge=-180, le=180)
    destinatario_alias: _Alias | None = None
    demanda_kg: float = Field(default=0, ge=0)
    demanda_m3: float = Field(default=0, ge=0)
    tiempo_servicio_min: int = Field(default=10, gt=0, le=32767)
    ventana_inicio: AwareDatetime
    ventana_fin: AwareDatetime
    prioridad: int = Field(default=2, ge=1, le=4)
    observacion_operativa: _Observacion | None = None


class PedidoOut(_Base):
    id: UUID
    codigo: str
    direccion: str
    distrito: str
    latitud: float
    longitud: float
    destinatario_alias: str | None
    demanda_kg: float
    demanda_m3: float
    tiempo_servicio_min: int
    ventana_inicio: datetime
    ventana_fin: datetime
    prioridad: int
    estado: EstadoPedido
    observacion_operativa: str | None
    creado_en: datetime
    actualizado_en: datetime

    @classmethod
    def desde_dominio(cls, p: Pedido) -> "PedidoOut":
        return cls(
            id=p.id,
            codigo=p.codigo,
            direccion=p.ubicacion.direccion_referencial,
            distrito=p.ubicacion.distrito,
            latitud=p.ubicacion.latitud,
            longitud=p.ubicacion.longitud,
            destinatario_alias=p.destinatario_alias,
            demanda_kg=p.demanda_kg,
            demanda_m3=p.demanda_m3,
            tiempo_servicio_min=p.tiempo_servicio_min,
            ventana_inicio=p.ventana_inicio,
            ventana_fin=p.ventana_fin,
            prioridad=p.prioridad,
            estado=p.estado,
            observacion_operativa=p.observacion_operativa,
            creado_en=p.creado_en,
            actualizado_en=p.actualizado_en,
        )


class ListadoPedidosOut(_Base):
    items: list[PedidoOut]
    total: int
    pagina: int
    limite: int


class ErrorOut(BaseModel):
    status: int
    message: str
    errors: dict[str, str] | None = None
