"""Fleet entities and business rules."""

from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from uuid import UUID


class Combustible(str, Enum):
    DIESEL = "DIESEL"
    GASOLINA = "GASOLINA"
    GNV = "GNV"
    ELECTRICO = "ELECTRICO"
    HIBRIDO = "HIBRIDO"


class EstadoVehiculo(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    MANTENIMIENTO = "MANTENIMIENTO"
    INACTIVO = "INACTIVO"


@dataclass(frozen=True)
class DisponibilidadVehiculo:
    fecha: date
    turno_inicio: time
    turno_fin: time
    disponible: bool
    restriccion_circulacion: str | None


@dataclass(frozen=True)
class Vehiculo:
    id: UUID
    placa: str
    tipo: str
    capacidad_kg: Decimal
    capacidad_m3: Decimal
    combustible: Combustible
    consumo_base_por_100km: Decimal
    factor_emision_kgco2e_unidad: Decimal | None
    anio: int | None
    estado: EstadoVehiculo
    creado_en: datetime | None
    actualizado_en: datetime | None
    disponibilidad: DisponibilidadVehiculo | None = None

    @property
    def elegible_para_planificar(self) -> bool:
        return (
            self.estado == EstadoVehiculo.DISPONIBLE
            and self.disponibilidad is not None
            and self.disponibilidad.disponible
        )


class ReglaFlotaError(Exception):
    def __init__(self, errors: dict[str, str]):
        self.errors = errors
        super().__init__("No se cumple una regla de flota")


class PlacaDuplicadaError(Exception):
    pass


class VehiculoNoEncontradoError(Exception):
    pass
