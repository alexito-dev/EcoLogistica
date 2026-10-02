"""Puerto de persistencia de pedidos (el adaptador PostgreSQL llegará con EN-005)."""

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

    def siguiente_correlativo(self) -> int: ...
