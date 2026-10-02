"""Casos de uso de pedidos."""

from dataclasses import replace
from uuid import UUID

from app.pedidos.domain import (
    Ambito,
    EstadoPedido,
    Pedido,
    PedidoNoEncontradoError,
    Ubicacion,
)
from app.pedidos.repository import PedidosRepository
from app.pedidos.schemas import PedidoCrear


class PedidosService:
    def __init__(self, repositorio: PedidosRepository, ambito: Ambito) -> None:
        self._repo = repositorio
        self._ambito = ambito

    def registrar(self, datos: PedidoCrear) -> Pedido:
        pedido = Pedido.crear(
            codigo=datos.codigo or "GENERADO",
            ubicacion=Ubicacion(
                direccion_referencial=datos.direccion,
                distrito=datos.distrito,
                latitud=datos.latitud,
                longitud=datos.longitud,
            ),
            destinatario_alias=datos.destinatario_alias,
            demanda_kg=datos.demanda_kg,
            demanda_m3=datos.demanda_m3,
            tiempo_servicio_min=datos.tiempo_servicio_min,
            ventana_inicio=datos.ventana_inicio,
            ventana_fin=datos.ventana_fin,
            prioridad=datos.prioridad,
            observacion_operativa=datos.observacion_operativa,
            ambito=self._ambito,
        )
        if not datos.codigo:
            # El correlativo se consume solo si el pedido ya pasó las validaciones.
            pedido = replace(pedido, codigo=self._resolver_codigo(None))
        self._repo.guardar(pedido)  # lanza CodigoDuplicadoError si el código ya existe
        return pedido

    def obtener(self, pedido_id: UUID) -> Pedido:
        pedido = self._repo.obtener(pedido_id)
        if pedido is None:
            raise PedidoNoEncontradoError(pedido_id)
        return pedido

    def listar(
        self, estado: EstadoPedido | None, pagina: int, limite: int
    ) -> tuple[list[Pedido], int]:
        return self._repo.listar(estado, pagina, limite)

    def _resolver_codigo(self, codigo: str | None) -> str:
        """Usa el código enviado (normalizado) o genera `PED-000001`, `PED-000002`, ..."""
        if codigo:
            return Pedido.normalizar_codigo(codigo)
        while True:
            generado = f"PED-{self._repo.siguiente_correlativo():06d}"
            if self._repo.obtener_por_codigo(generado) is None:
                return generado
