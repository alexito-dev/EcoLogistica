"""Adaptador PostgreSQL de asignaciones y eventos de parada (tablas de la migracion 20261113_01)."""

from datetime import date
from uuid import UUID

from sqlalchemy import Engine, text

from app.conduccion.domain import EstadoParada, EventoParada


def _evento(fila) -> EventoParada:
    return EventoParada(
        id=fila["id"],
        fecha=fila["fecha"],
        pedido_id=fila["pedido_id"],
        estado=EstadoParada(fila["estado"]),
        nota=fila["nota"],
        usuario_id=str(fila["usuario_id"]) if fila["usuario_id"] else None,
        creado_en=fila["creado_en"],
    )


_COLUMNAS = "id, fecha, pedido_id, estado, nota, usuario_id, creado_en"


class ConduccionPostgresRepository:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def asignar(self, fecha: date, vehiculo_id: UUID, conductor_id: str, asignado_por: str | None) -> None:
        with self._engine.begin() as conexion:
            conexion.execute(
                text("""
                    INSERT INTO asignaciones_ruta (fecha, vehiculo_id, conductor_id, asignado_por, asignado_en)
                    VALUES (:fecha, :vehiculo, :conductor, :por, now())
                    ON CONFLICT (fecha, vehiculo_id) DO UPDATE SET conductor_id = EXCLUDED.conductor_id,
                        asignado_por = EXCLUDED.asignado_por, asignado_en = now()
                """),
                {
                    "fecha": fecha,
                    "vehiculo": vehiculo_id,
                    "conductor": UUID(conductor_id),
                    "por": UUID(asignado_por) if asignado_por else None,
                },
            )

    def asignaciones(self, fecha: date) -> dict[UUID, str]:
        with self._engine.connect() as conexion:
            filas = conexion.execute(
                text("SELECT vehiculo_id, conductor_id FROM asignaciones_ruta WHERE fecha = :fecha"),
                {"fecha": fecha},
            ).all()
        return {fila[0]: str(fila[1]) for fila in filas}

    def registrar_evento(self, evento: EventoParada) -> None:
        with self._engine.begin() as conexion:
            conexion.execute(
                text("""
                    INSERT INTO eventos_parada (id, fecha, pedido_id, estado, nota, usuario_id, creado_en)
                    VALUES (:id, :fecha, :pedido, :estado, :nota, :usuario, :creado)
                """),
                {
                    "id": evento.id,
                    "fecha": evento.fecha,
                    "pedido": evento.pedido_id,
                    "estado": evento.estado.value,
                    "nota": evento.nota,
                    "usuario": UUID(evento.usuario_id) if evento.usuario_id else None,
                    "creado": evento.creado_en,
                },
            )

    def ultimos_eventos(self, fecha: date) -> dict[UUID, EventoParada]:
        with self._engine.connect() as conexion:
            filas = (
                conexion.execute(
                    text(f"""
                        SELECT DISTINCT ON (pedido_id) {_COLUMNAS}
                        FROM eventos_parada WHERE fecha = :fecha
                        ORDER BY pedido_id, creado_en DESC, id DESC
                    """),
                    {"fecha": fecha},
                )
                .mappings()
                .all()
            )
        return {fila["pedido_id"]: _evento(fila) for fila in filas}

    def historial(self, fecha: date, pedido_id: UUID) -> list[EventoParada]:
        with self._engine.connect() as conexion:
            filas = (
                conexion.execute(
                    text(f"""
                        SELECT {_COLUMNAS} FROM eventos_parada
                        WHERE fecha = :fecha AND pedido_id = :pedido ORDER BY creado_en, id
                    """),
                    {"fecha": fecha, "pedido": pedido_id},
                )
                .mappings()
                .all()
            )
        return [_evento(f) for f in filas]
