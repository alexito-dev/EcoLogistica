"""Adaptador en memoria (pruebas y desarrollo sin base de datos)."""

from datetime import date
from threading import RLock
from uuid import UUID

from app.conduccion.domain import EventoParada


class ConduccionMemoryRepository:
    def __init__(self) -> None:
        self._asignaciones: dict[tuple[date, UUID], str] = {}
        self._eventos: list[EventoParada] = []
        self._lock = RLock()

    def asignar(self, fecha: date, vehiculo_id: UUID, conductor_id: str, asignado_por: str | None) -> None:
        with self._lock:
            self._asignaciones[(fecha, vehiculo_id)] = conductor_id

    def asignaciones(self, fecha: date) -> dict[UUID, str]:
        with self._lock:
            return {v: c for (f, v), c in self._asignaciones.items() if f == fecha}

    def registrar_evento(self, evento: EventoParada) -> None:
        with self._lock:
            self._eventos.append(evento)

    def ultimos_eventos(self, fecha: date) -> dict[UUID, EventoParada]:
        with self._lock:
            ultimos: dict[UUID, EventoParada] = {}
            for evento in self._eventos:
                if evento.fecha == fecha:
                    ultimos[evento.pedido_id] = evento  # el orden de insercion es cronologico
            return ultimos

    def historial(self, fecha: date, pedido_id: UUID) -> list[EventoParada]:
        with self._lock:
            return [e for e in self._eventos if e.fecha == fecha and e.pedido_id == pedido_id]
