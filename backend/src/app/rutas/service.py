"""Caso de uso: armar la vista previa de rutas de una fecha con los pedidos y la flota registrados."""

from datetime import date

from app.flota.repository import FlotaRepository
from app.pedidos.domain import EstadoPedido, Pedido
from app.pedidos.repository import PedidosRepository
from app.rutas.planificador import LIMA, Propuesta, Punto, planificar

# Solo se planifican pedidos que aún no salieron a reparto.
ESTADOS_PLANIFICABLES = {EstadoPedido.PENDIENTE, EstadoPedido.VALIDADO}
_LOTE = 100


class RutasService:
    def __init__(self, pedidos: PedidosRepository, flota: FlotaRepository, deposito: Punto) -> None:
        self._pedidos = pedidos
        self._flota = flota
        self._deposito = deposito

    def pedidos_del_dia(self, fecha: date) -> list[Pedido]:
        encontrados: list[Pedido] = []
        pagina = 1
        while True:
            lote, total = self._pedidos.listar(None, pagina, _LOTE)
            encontrados += [
                p
                for p in lote
                if p.estado in ESTADOS_PLANIFICABLES and p.ventana_inicio.astimezone(LIMA).date() == fecha
            ]
            if pagina * _LOTE >= total or not lote:
                return encontrados
            pagina += 1

    def vista_previa(self, fecha: date) -> tuple[Propuesta, int]:
        vehiculos = [v for v in self._flota.listar(fecha) if v.elegible_para_planificar]
        return planificar(fecha, self._deposito, self.pedidos_del_dia(fecha), vehiculos), len(vehiculos)
