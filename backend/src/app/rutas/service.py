"""Caso de uso: armar la vista previa de rutas de una fecha con los pedidos y la flota registrados."""

from datetime import date, datetime, time, timedelta

from app.flota.repository import FlotaRepository
from app.pedidos.domain import EstadoPedido, Pedido
from app.pedidos.repository import PedidosRepository
from app.rutas.planificador import LIMA, Propuesta, Punto, planificar

# Solo se planifican pedidos que aún no salieron a reparto.
ESTADOS_PLANIFICABLES = {EstadoPedido.PENDIENTE, EstadoPedido.VALIDADO}


class RutasService:
    def __init__(self, pedidos: PedidosRepository, flota: FlotaRepository, deposito: Punto) -> None:
        self._pedidos = pedidos
        self._flota = flota
        self._deposito = deposito

    def pedidos_del_dia(self, fecha: date) -> list[Pedido]:
        # El día se define en hora de Lima; el filtro por fecha y estado lo resuelve el repositorio (índice
        # `ix_pedidos_estado_ventana`) en lugar de recorrer todos los pedidos en Python.
        desde = datetime.combine(fecha, time.min, tzinfo=LIMA)
        return self._pedidos.listar_por_ventana(desde, desde + timedelta(days=1), ESTADOS_PLANIFICABLES)

    def vista_previa(self, fecha: date) -> tuple[Propuesta, int]:
        vehiculos = [v for v in self._flota.listar(fecha) if v.elegible_para_planificar]
        return planificar(fecha, self._deposito, self.pedidos_del_dia(fecha), vehiculos), len(vehiculos)
