"""In-memory fleet adapter for isolated unit and API tests."""

from datetime import date
from threading import RLock
from uuid import UUID

from app.flota.domain import DisponibilidadVehiculo, PlacaDuplicadaError, Vehiculo


class FlotaMemoryRepository:
    def __init__(self) -> None:
        self._vehiculos: dict[UUID, Vehiculo] = {}
        self._disponibilidad: dict[tuple[UUID, date], DisponibilidadVehiculo] = {}
        self._lock = RLock()

    def listar(self, fecha: date | None = None) -> list[Vehiculo]:
        with self._lock:
            return [self._con_disponibilidad(v, fecha) for v in self._vehiculos.values()]

    def obtener(self, vehiculo_id: UUID, fecha: date | None = None) -> Vehiculo | None:
        with self._lock:
            vehiculo = self._vehiculos.get(vehiculo_id)
            return self._con_disponibilidad(vehiculo, fecha) if vehiculo else None

    def crear(self, vehiculo: Vehiculo) -> Vehiculo:
        with self._lock:
            if any(v.placa == vehiculo.placa for v in self._vehiculos.values()):
                raise PlacaDuplicadaError(vehiculo.placa)
            self._vehiculos[vehiculo.id] = vehiculo
            return vehiculo

    def actualizar(self, vehiculo: Vehiculo) -> Vehiculo | None:
        with self._lock:
            if vehiculo.id not in self._vehiculos:
                return None
            if any(v.id != vehiculo.id and v.placa == vehiculo.placa for v in self._vehiculos.values()):
                raise PlacaDuplicadaError(vehiculo.placa)
            self._vehiculos[vehiculo.id] = vehiculo
            return vehiculo

    def guardar_disponibilidad(
        self, vehiculo_id: UUID, disponibilidad: DisponibilidadVehiculo
    ) -> Vehiculo | None:
        with self._lock:
            if vehiculo_id not in self._vehiculos:
                return None
            self._disponibilidad[(vehiculo_id, disponibilidad.fecha)] = disponibilidad
            return self._con_disponibilidad(self._vehiculos[vehiculo_id], disponibilidad.fecha)

    def _con_disponibilidad(self, vehiculo: Vehiculo, fecha: date | None) -> Vehiculo:
        disponibilidad = self._disponibilidad.get((vehiculo.id, fecha)) if fecha else None
        return Vehiculo(**{**vehiculo.__dict__, "disponibilidad": disponibilidad})
