"""Dominio de la ejecucion de rutas por Conduccion (HU-005, HU-010, HU-006).

El avance de cada parada se guarda como una secuencia de eventos inmutables: el estado actual es el ultimo
evento y el historial completo queda disponible para auditoria.
"""

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from uuid import UUID


class EstadoParada(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_RUTA = "EN_RUTA"
    ENTREGADO = "ENTREGADO"
    INCIDENCIA = "INCIDENCIA"
    CANCELADO = "CANCELADO"
    REPROGRAMADO = "REPROGRAMADO"


# Transiciones permitidas para quien conduce. REPROGRAMADO solo lo decide Planificacion.
TRANSICIONES_CONDUCTOR: dict[EstadoParada, frozenset[EstadoParada]] = {
    EstadoParada.PENDIENTE: frozenset({EstadoParada.EN_RUTA, EstadoParada.CANCELADO}),
    EstadoParada.EN_RUTA: frozenset({EstadoParada.ENTREGADO, EstadoParada.INCIDENCIA, EstadoParada.CANCELADO}),
    EstadoParada.INCIDENCIA: frozenset({EstadoParada.EN_RUTA, EstadoParada.CANCELADO}),
    EstadoParada.ENTREGADO: frozenset(),
    EstadoParada.CANCELADO: frozenset(),
    EstadoParada.REPROGRAMADO: frozenset(),
}

TERMINALES = frozenset({EstadoParada.ENTREGADO, EstadoParada.CANCELADO, EstadoParada.REPROGRAMADO})
LONGITUD_MINIMA_NOTA = 5


@dataclass(frozen=True)
class EventoParada:
    id: UUID
    fecha: date
    pedido_id: UUID
    estado: EstadoParada
    nota: str | None
    usuario_id: str | None
    creado_en: datetime
