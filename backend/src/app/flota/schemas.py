"""JSON contracts for fleet APIs (camelCase)."""

from datetime import date, datetime, time
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from pydantic.alias_generators import to_camel

from app.flota.domain import Combustible, EstadoVehiculo, Vehiculo

_Placa = Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=10, pattern=r"^[A-Za-z0-9-]+$")]
_Tipo = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=40)]
_Restriccion = Annotated[str, StringConstraints(strip_whitespace=True, max_length=500)]


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="forbid")


class VehiculoGuardar(_Base):
    placa: _Placa
    tipo: _Tipo
    capacidad_kg: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    capacidad_m3: Decimal = Field(gt=0, max_digits=10, decimal_places=3)
    combustible: Combustible
    consumo_base_por_100km: Decimal = Field(
        gt=0, max_digits=10, decimal_places=4,
        validation_alias="consumoBasePor100km", serialization_alias="consumoBasePor100km",
    )
    factor_emision_kgco2e_unidad: Decimal | None = Field(
        default=None, gt=0, max_digits=14, decimal_places=6,
        validation_alias="factorEmisionKgco2eUnidad", serialization_alias="factorEmisionKgco2eUnidad",
    )
    anio: int | None = Field(default=None, ge=1990, le=2100)
    estado: EstadoVehiculo = EstadoVehiculo.DISPONIBLE


class DisponibilidadGuardar(_Base):
    fecha: date
    turno_inicio: time
    turno_fin: time
    disponible: bool = True
    restriccion_circulacion: _Restriccion | None = None


class DisponibilidadOut(_Base):
    fecha: date
    turno_inicio: time
    turno_fin: time
    disponible: bool
    restriccion_circulacion: str | None


class VehiculoOut(_Base):
    id: UUID
    placa: str
    tipo: str
    capacidad_kg: Decimal
    capacidad_m3: Decimal
    combustible: Combustible
    consumo_base_por_100km: Decimal = Field(
        serialization_alias="consumoBasePor100km", validation_alias="consumoBasePor100km",
    )
    factor_emision_kgco2e_unidad: Decimal | None = Field(
        serialization_alias="factorEmisionKgco2eUnidad", validation_alias="factorEmisionKgco2eUnidad",
    )
    anio: int | None
    estado: EstadoVehiculo
    creado_en: datetime | None
    actualizado_en: datetime | None
    disponibilidad: DisponibilidadOut | None
    elegible_para_planificar: bool

    @classmethod
    def desde_dominio(cls, vehiculo: Vehiculo) -> "VehiculoOut":
        disponibilidad = (
            DisponibilidadOut(
                fecha=vehiculo.disponibilidad.fecha,
                turno_inicio=vehiculo.disponibilidad.turno_inicio,
                turno_fin=vehiculo.disponibilidad.turno_fin,
                disponible=vehiculo.disponibilidad.disponible,
                restriccion_circulacion=vehiculo.disponibilidad.restriccion_circulacion,
            )
            if vehiculo.disponibilidad
            else None
        )
        return cls(
            id=vehiculo.id,
            placa=vehiculo.placa,
            tipo=vehiculo.tipo,
            capacidad_kg=vehiculo.capacidad_kg,
            capacidad_m3=vehiculo.capacidad_m3,
            combustible=vehiculo.combustible,
            consumo_base_por_100km=vehiculo.consumo_base_por_100km,
            factor_emision_kgco2e_unidad=vehiculo.factor_emision_kgco2e_unidad,
            anio=vehiculo.anio,
            estado=vehiculo.estado,
            creado_en=vehiculo.creado_en,
            actualizado_en=vehiculo.actualizado_en,
            disponibilidad=disponibilidad,
            elegible_para_planificar=vehiculo.elegible_para_planificar,
        )


class ListadoVehiculosOut(_Base):
    items: list[VehiculoOut]
