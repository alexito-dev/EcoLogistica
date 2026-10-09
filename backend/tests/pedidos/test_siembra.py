from datetime import datetime, timedelta, timezone

from app.pedidos.domain import Ambito, EstadoPedido
from app.pedidos.memory_repository import PedidosMemoryRepository
from app.pedidos.schemas import PedidoCrear
from app.pedidos.service import PedidosService
from app.pedidos.siembra import PEDIDOS_DEMO, sembrar_pedidos_demo

AMBITO = Ambito(-12.20, -11.95, -75.35, -75.10, ("Huancayo", "El Tambo", "Chilca", "Pilcomayo", "San Agustín de Cajas"))
AHORA = datetime(2026, 10, 2, 10, 0, tzinfo=timezone(timedelta(hours=-5)))


def test_siembra_valida_e_idempotente():
    repo = PedidosMemoryRepository()
    assert sembrar_pedidos_demo(repo, AMBITO, AHORA) == len(PEDIDOS_DEMO)
    assert sembrar_pedidos_demo(repo, AMBITO, AHORA) == 0
    items, total = repo.listar(None, 1, 100)
    assert total == len(PEDIDOS_DEMO)
    assert all(p.estado == EstadoPedido.PENDIENTE for p in items)
    assert items[-1].ventana_inicio.date().isoformat() == "2026-10-03"


def test_la_siembra_no_consume_el_correlativo():
    repo = PedidosMemoryRepository()
    sembrar_pedidos_demo(repo, AMBITO, AHORA)
    nuevo = PedidosService(repo, AMBITO).registrar(
        PedidoCrear.model_validate(
            {
                "direccion": "Jr. Real 123",
                "distrito": "Huancayo",
                "latitud": -12.06,
                "longitud": -75.20,
                "demandaKg": 5,
                "ventanaInicio": "2026-10-05T08:00:00-05:00",
                "ventanaFin": "2026-10-05T12:00:00-05:00",
            }
        )
    )
    assert nuevo.codigo == "PED-000001"
