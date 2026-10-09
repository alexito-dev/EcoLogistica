"""Repository contract for vehicle and availability persistence."""

from datetime import date
from typing import Protocol
from uuid import UUID

from app.flota.domain import DisponibilidadVehiculo, Vehiculo


class FlotaRepository(Protocol):
    def listar(self, fecha: date | None = None) -> list[Vehiculo]: ...

    def obtener(self, vehiculo_id: UUID, fecha: date | None = None) -> Vehiculo | None: ...

    def crear(self, vehiculo: Vehiculo) -> Vehiculo: ...

    def actualizar(self, vehiculo: Vehiculo) -> Vehiculo | None: ...

    def guardar_disponibilidad(
        self, vehiculo_id: UUID, disponibilidad: DisponibilidadVehiculo
    ) -> Vehiculo | None: ...
