"""PostgreSQL/PostGIS adapter for the order repository."""

from collections.abc import Mapping
from uuid import UUID

from sqlalchemy import Engine, text
from sqlalchemy.exc import IntegrityError

from app.pedidos.domain import CodigoDuplicadoError, EstadoPedido, Pedido, Ubicacion

_SELECT_PEDIDO = """
SELECT p.id, p.codigo, p.destinatario_alias, p.demanda_kg, p.demanda_m3,
       p.tiempo_servicio_min, p.ventana_inicio, p.ventana_fin, p.prioridad,
       p.estado, p.observacion_operativa, p.creado_en, p.actualizado_en,
       u.direccion_referencial, u.distrito,
       ST_Y(u.punto)::double precision AS latitud,
       ST_X(u.punto)::double precision AS longitud
FROM pedidos AS p
JOIN ubicaciones AS u ON u.id = p.ubicacion_id
"""


class PedidosPostgresRepository:
    """Store order and location atomically in the configured PostgreSQL database."""

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def guardar(self, pedido: Pedido) -> None:
        try:
            with self._engine.begin() as connection:
                connection.execute(
                    text("""
                        INSERT INTO ubicaciones
                            (id, etiqueta, direccion_referencial, distrito, punto, fuente)
                        VALUES
                            (:id, :etiqueta, :direccion, :distrito,
                             ST_SetSRID(ST_MakePoint(:longitud, :latitud), 4326), :fuente)
                    """),
                    {
                        "id": pedido.id,
                        "etiqueta": f"Pedido {pedido.codigo}",
                        "direccion": pedido.ubicacion.direccion_referencial,
                        "distrito": pedido.ubicacion.distrito,
                        "longitud": pedido.ubicacion.longitud,
                        "latitud": pedido.ubicacion.latitud,
                        "fuente": pedido.ubicacion.fuente,
                    },
                )
                connection.execute(
                    text("""
                        INSERT INTO pedidos
                            (id, codigo, ubicacion_id, destinatario_alias, demanda_kg,
                             demanda_m3, tiempo_servicio_min, ventana_inicio, ventana_fin,
                             prioridad, estado, observacion_operativa, creado_en, actualizado_en)
                        VALUES
                            (:id, :codigo, :ubicacion_id, :destinatario_alias, :demanda_kg,
                             :demanda_m3, :tiempo_servicio_min, :ventana_inicio, :ventana_fin,
                             :prioridad, CAST(:estado AS estado_pedido), :observacion_operativa,
                             :creado_en, :actualizado_en)
                    """),
                    {
                        "id": pedido.id,
                        "codigo": pedido.codigo,
                        "ubicacion_id": pedido.id,
                        "destinatario_alias": pedido.destinatario_alias,
                        "demanda_kg": pedido.demanda_kg,
                        "demanda_m3": pedido.demanda_m3,
                        "tiempo_servicio_min": pedido.tiempo_servicio_min,
                        "ventana_inicio": pedido.ventana_inicio,
                        "ventana_fin": pedido.ventana_fin,
                        "prioridad": pedido.prioridad,
                        "estado": pedido.estado.value,
                        "observacion_operativa": pedido.observacion_operativa,
                        "creado_en": pedido.creado_en,
                        "actualizado_en": pedido.actualizado_en,
                    },
                )
        except IntegrityError as error:
            if self.obtener_por_codigo(pedido.codigo) is not None:
                raise CodigoDuplicadoError(pedido.codigo) from error
            raise

    def obtener(self, pedido_id: UUID) -> Pedido | None:
        with self._engine.connect() as connection:
            row = connection.execute(
                text(_SELECT_PEDIDO + " WHERE p.id = :id"), {"id": pedido_id}
            ).mappings().one_or_none()
        return self._desde_fila(row) if row else None

    def obtener_por_codigo(self, codigo: str) -> Pedido | None:
        with self._engine.connect() as connection:
            row = connection.execute(
                text(_SELECT_PEDIDO + " WHERE p.codigo = :codigo"), {"codigo": codigo}
            ).mappings().one_or_none()
        return self._desde_fila(row) if row else None

    def listar(
        self, estado: EstadoPedido | None, pagina: int, limite: int
    ) -> tuple[list[Pedido], int]:
        filtro = " WHERE p.estado = CAST(:estado AS estado_pedido)" if estado else ""
        parametros = {"estado": estado.value} if estado else {}
        with self._engine.connect() as connection:
            total = connection.execute(
                text("SELECT count(*) FROM pedidos AS p" + filtro), parametros
            ).scalar_one()
            rows = connection.execute(
                text(
                    _SELECT_PEDIDO
                    + filtro
                    + " ORDER BY p.creado_en DESC, p.id DESC LIMIT :limite OFFSET :offset"
                ),
                {**parametros, "limite": limite, "offset": (pagina - 1) * limite},
            ).mappings().all()
        return [self._desde_fila(row) for row in rows], int(total)

    def siguiente_correlativo(self) -> int:
        with self._engine.begin() as connection:
            return int(
                connection.execute(text("SELECT nextval('pedido_codigo_seq')")).scalar_one()
            )

    @staticmethod
    def _desde_fila(row: Mapping[str, object]) -> Pedido:
        return Pedido(
            id=row["id"],  # type: ignore[arg-type]
            codigo=row["codigo"],  # type: ignore[arg-type]
            ubicacion=Ubicacion(
                direccion_referencial=row["direccion_referencial"],  # type: ignore[arg-type]
                distrito=row["distrito"],  # type: ignore[arg-type]
                latitud=float(row["latitud"]),  # type: ignore[arg-type]
                longitud=float(row["longitud"]),  # type: ignore[arg-type]
                fuente="MANUAL",
            ),
            destinatario_alias=row["destinatario_alias"],  # type: ignore[arg-type]
            demanda_kg=float(row["demanda_kg"]),  # type: ignore[arg-type]
            demanda_m3=float(row["demanda_m3"]),  # type: ignore[arg-type]
            tiempo_servicio_min=row["tiempo_servicio_min"],  # type: ignore[arg-type]
            ventana_inicio=row["ventana_inicio"],  # type: ignore[arg-type]
            ventana_fin=row["ventana_fin"],  # type: ignore[arg-type]
            prioridad=row["prioridad"],  # type: ignore[arg-type]
            estado=EstadoPedido(row["estado"]),  # type: ignore[arg-type]
            observacion_operativa=row["observacion_operativa"],  # type: ignore[arg-type]
            creado_en=row["creado_en"],  # type: ignore[arg-type]
            actualizado_en=row["actualizado_en"],  # type: ignore[arg-type]
        )
