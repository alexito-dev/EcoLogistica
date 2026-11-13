from uuid import uuid4

import pytest

from app.pedidos.domain import (
    Ambito,
    CodigoDuplicadoError,
    EstadoPedido,
    PedidoNoEncontradoError,
)
from app.pedidos.memory_repository import PedidosMemoryRepository
from app.pedidos.schemas import PedidoCrear
from app.pedidos.service import PedidosService

AMBITO = Ambito(-12.20, -11.95, -75.35, -75.10, ("Huancayo",))


def _datos(**extra) -> PedidoCrear:
    base = {
        "direccion": "Jr. Real 123",
        "distrito": "Huancayo",
        "latitud": -12.06,
        "longitud": -75.20,
        "demandaKg": 5,
        "ventanaInicio": "2026-10-05T08:00:00-05:00",
        "ventanaFin": "2026-10-05T12:00:00-05:00",
    }
    base.update(extra)
    return PedidoCrear.model_validate(base)


@pytest.fixture
def servicio():
    return PedidosService(PedidosMemoryRepository(), AMBITO)


def test_genera_codigos_correlativos(servicio):
    assert servicio.registrar(_datos()).codigo == "PED-000001"
    assert servicio.registrar(_datos()).codigo == "PED-000002"


def test_el_generado_no_colisiona_con_uno_manual(servicio):
    servicio.registrar(_datos(codigo="ped-000001"))
    assert servicio.registrar(_datos()).codigo == "PED-000002"


def test_valores_por_defecto(servicio):
    pedido = servicio.registrar(_datos())
    assert pedido.tiempo_servicio_min == 10
    assert pedido.prioridad == 2
    assert pedido.estado == EstadoPedido.PENDIENTE


def test_codigo_duplicado_ignora_mayusculas_y_espacios(servicio):
    servicio.registrar(_datos(codigo="ABC-1"))
    with pytest.raises(CodigoDuplicadoError):
        servicio.registrar(_datos(codigo="  abc-1 "))
    assert servicio.listar(None, 1, 20)[1] == 1


def test_obtener_inexistente(servicio):
    with pytest.raises(PedidoNoEncontradoError):
        servicio.obtener(uuid4())


def test_listado_ordenado_filtrado_y_paginado(servicio):
    creados = [servicio.registrar(_datos()) for _ in range(5)]
    items, total = servicio.listar(None, 1, 2)
    assert total == 5
    assert [p.id for p in items] == [creados[4].id, creados[3].id]
    pagina_3, _ = servicio.listar(None, 3, 2)
    assert [p.id for p in pagina_3] == [creados[0].id]
    assert servicio.listar(EstadoPedido.ENTREGADO, 1, 20) == ([], 0)
    assert servicio.listar(EstadoPedido.PENDIENTE, 1, 20)[1] == 5


def test_un_rechazo_no_consume_correlativo(servicio):
    from app.pedidos.domain import ReglaDominioError

    with pytest.raises(ReglaDominioError):
        servicio.registrar(_datos(ventanaFin="2026-10-05T07:00:00-05:00"))
    assert servicio.registrar(_datos()).codigo == "PED-000001"


def test_listar_por_ventana_filtra_dia_de_lima_y_estado():
    """El filtro de planificación se resuelve en el repositorio: borde del día en hora de Lima y estados."""
    from datetime import datetime, timedelta, timezone
    from dataclasses import replace

    from app.pedidos.domain import EstadoPedido
    from app.pedidos.memory_repository import PedidosMemoryRepository
    from tests.pedidos.test_siembra import AMBITO
    from app.pedidos.siembra import sembrar_pedidos_demo

    lima = timezone(timedelta(hours=-5))
    repo = PedidosMemoryRepository()
    sembrar_pedidos_demo(repo, AMBITO, datetime(2026, 10, 9, 10, 0, tzinfo=lima))
    desde = datetime(2026, 10, 10, 0, 0, tzinfo=lima)
    dia = repo.listar_por_ventana(desde, desde + timedelta(days=1), {EstadoPedido.PENDIENTE})
    assert len(dia) == 6
    assert [p.ventana_inicio for p in dia] == sorted(p.ventana_inicio for p in dia)
    assert repo.listar_por_ventana(desde, desde + timedelta(days=1), set()) == []
    assert repo.listar_por_ventana(desde, desde + timedelta(days=1), {EstadoPedido.ENTREGADO}) == []
    # El día anterior y el siguiente no incluyen estos pedidos.
    assert repo.listar_por_ventana(desde - timedelta(days=1), desde, {EstadoPedido.PENDIENTE}) == []
    repo._por_id[dia[0].id] = replace(dia[0], estado=EstadoPedido.ENTREGADO)
    assert len(repo.listar_por_ventana(desde, desde + timedelta(days=1), {EstadoPedido.PENDIENTE})) == 5
