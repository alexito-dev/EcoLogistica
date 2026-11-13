"""Adaptador en memoria del repositorio de pedidos (válido para un único proceso)."""

from dataclasses import replace
from datetime import datetime, timezone
from collections.abc import Collection
from threading import Lock
from uuid import UUID

from app.pedidos.domain import CodigoDuplicadoError, EstadoPedido, Pedido, PedidoNoEncontradoError


class PedidosMemoryRepository:
    def __init__(self) -> None:
        self._por_id: dict[UUID, Pedido] = {}
        self._id_por_codigo: dict[str, UUID] = {}
        self._correlativo = 0
        self._lock = Lock()

    def guardar(self, pedido: Pedido) -> None:
        with self._lock:
            if pedido.codigo in self._id_por_codigo:
                raise CodigoDuplicadoError(pedido.codigo)
            self._por_id[pedido.id] = pedido
            self._id_por_codigo[pedido.codigo] = pedido.id

    def listar_por_ventana(self, desde: datetime, hasta: datetime, estados: Collection[EstadoPedido]) -> list[Pedido]:
        with self._lock:
            pedidos = list(self._por_id.values())
        elegidos = [p for p in pedidos if desde <= p.ventana_inicio < hasta and p.estado in estados]
        return sorted(elegidos, key=lambda p: (p.ventana_inicio, p.codigo))

    def actualizar_estado(self, pedido_id: UUID, estado: EstadoPedido) -> None:
        with self._lock:
            pedido = self._por_id.get(pedido_id)
            if pedido is None:
                raise PedidoNoEncontradoError(pedido_id)
            self._por_id[pedido_id] = replace(pedido, estado=estado, actualizado_en=datetime.now(timezone.utc))

    def obtener(self, pedido_id: UUID) -> Pedido | None:
        return self._por_id.get(pedido_id)

    def obtener_por_codigo(self, codigo: str) -> Pedido | None:
        pedido_id = self._id_por_codigo.get(codigo)
        return self._por_id.get(pedido_id) if pedido_id else None

    def listar(
        self, estado: EstadoPedido | None, pagina: int, limite: int
    ) -> tuple[list[Pedido], int]:
        with self._lock:
            pedidos = list(self._por_id.values())
        if estado is not None:
            pedidos = [p for p in pedidos if p.estado == estado]
        pedidos.reverse()  # orden de inserción = creado_en; invertido da el más reciente primero
        inicio = (pagina - 1) * limite
        return pedidos[inicio : inicio + limite], len(pedidos)

    def siguiente_correlativo(self) -> int:
        with self._lock:
            self._correlativo += 1
            return self._correlativo
