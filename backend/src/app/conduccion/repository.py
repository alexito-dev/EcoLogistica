"""Puerto de persistencia de asignaciones de conductor y eventos de parada."""

from datetime import date
from typing import Protocol
from uuid import UUID

from app.conduccion.domain import EventoParada


class ConduccionRepository(Protocol):
    def asignar(self, fecha: date, vehiculo_id: UUID, conductor_id: str, asignado_por: str | None) -> None:
        """Asigna (o reemplaza) el conductor de un vehiculo en una fecha."""

    def asignaciones(self, fecha: date) -> dict[UUID, str]:
        """Conductor asignado por vehiculo en la fecha."""

    def registrar_evento(self, evento: EventoParada) -> None: ...

    def ultimos_eventos(self, fecha: date) -> dict[UUID, EventoParada]:
        """Ultimo evento de cada pedido de la fecha."""

    def historial(self, fecha: date, pedido_id: UUID) -> list[EventoParada]:
        """Eventos del pedido en la fecha, del mas antiguo al mas reciente."""
