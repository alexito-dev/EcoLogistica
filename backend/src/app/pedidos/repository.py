"""Puerto de persistencia de pedidos; admite adaptadores en memoria y PostgreSQL/PostGIS."""

from collections.abc import Collection
from datetime import datetime
from typing import Protocol
from uuid import UUID

from app.pedidos.domain import EstadoPedido, Pedido


class PedidosRepository(Protocol):
    def guardar(self, pedido: Pedido) -> None:
        """Persiste el pedido. Lanza `CodigoDuplicadoError` si el código ya existe."""

    def obtener(self, pedido_id: UUID) -> Pedido | None: ...

    def obtener_por_codigo(self, codigo: str) -> Pedido | None:
        """Busca por código ya normalizado."""

    def listar(
        self, estado: EstadoPedido | None, pagina: int, limite: int
    ) -> tuple[list[Pedido], int]:
        """Pedidos por `creado_en` descendente y total que cumple el filtro."""

    def listar_por_ventana(
        self, desde: datetime, hasta: datetime, estados: Collection[EstadoPedido]
    ) -> list[Pedido]:
        """Pedidos cuya ventana inicia en [desde, hasta) y cuyo estado está en `estados`, por ventana y código."""

    def actualizar_estado(self, pedido_id: UUID, estado: EstadoPedido) -> None:
        """Cambia el estado del pedido (avance de la entrega). Lanza `PedidoNoEncontradoError` si no existe."""

    def siguiente_correlativo(self) -> int: ...
