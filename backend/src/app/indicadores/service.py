"""Caso de uso: resumir pedidos, flota y la propuesta de rutas de una fecha para el dashboard."""

from collections import Counter
from dataclasses import dataclass
from datetime import date

from app.flota.domain import Combustible, Vehiculo
from app.flota.repository import FlotaRepository
from app.pedidos.domain import EstadoPedido, Pedido
from app.pedidos.repository import PedidosRepository
from app.rutas.planificador import Propuesta
from app.rutas.service import RutasService

_LOTE = 100


@dataclass(frozen=True)
class Indicadores:
    fecha: date
    pedidos: list[Pedido]
    vehiculos: list[Vehiculo]
    propuesta: Propuesta
    vehiculos_aptos: int

    @property
    def por_estado(self) -> list[tuple[EstadoPedido, int]]:
        conteo = Counter(p.estado for p in self.pedidos)
        return [(e, conteo[e]) for e in EstadoPedido]

    @property
    def por_distrito(self) -> list[tuple[str, int, float]]:
        cantidad: Counter[str] = Counter()
        peso: Counter[str] = Counter()
        for p in self.pedidos:
            cantidad[p.ubicacion.distrito] += 1
            peso[p.ubicacion.distrito] += p.demanda_kg
        return [(d, n, peso[d]) for d, n in sorted(cantidad.items(), key=lambda x: (-x[1], x[0]))]

    @property
    def por_prioridad(self) -> list[tuple[int, int]]:
        conteo = Counter(p.prioridad for p in self.pedidos)
        return [(nivel, conteo[nivel]) for nivel in (4, 3, 2, 1)]

    @property
    def por_combustible(self) -> list[tuple[Combustible, int]]:
        conteo = Counter(v.combustible for v in self.vehiculos)
        return [(c, conteo[c]) for c in Combustible if conteo[c]]


class IndicadoresService:
    def __init__(self, pedidos: PedidosRepository, flota: FlotaRepository, rutas: RutasService) -> None:
        self._pedidos = pedidos
        self._flota = flota
        self._rutas = rutas

    def _todos_los_pedidos(self) -> list[Pedido]:
        encontrados: list[Pedido] = []
        pagina = 1
        while True:
            lote, total = self._pedidos.listar(None, pagina, _LOTE)
            encontrados += lote
            if pagina * _LOTE >= total or not lote:
                return encontrados
            pagina += 1

    def calcular(self, fecha: date) -> Indicadores:
        propuesta, aptos = self._rutas.vista_previa(fecha)
        return Indicadores(
            fecha=fecha,
            pedidos=self._todos_los_pedidos(),
            vehiculos=self._flota.listar(fecha),
            propuesta=propuesta,
            vehiculos_aptos=aptos,
        )
