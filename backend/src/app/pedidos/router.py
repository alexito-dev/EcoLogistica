"""Rutas REST de pedidos."""

from functools import lru_cache
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.auth.dependencias import requerir_rol
from app.auth.domain import Rol
from app.config import get_settings
from app.pedidos.domain import EstadoPedido
from app.pedidos.memory_repository import PedidosMemoryRepository
from app.pedidos.repository import PedidosRepository
from app.pedidos.schemas import ErrorOut, ListadoPedidosOut, PedidoCrear, PedidoOut
from app.pedidos.service import PedidosService

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@lru_cache
def get_repositorio() -> PedidosRepository:
    """Repositorio único del proceso. Se sustituirá por el adaptador PostgreSQL (EN-005)."""
    return PedidosMemoryRepository()


def get_servicio(
    repositorio: Annotated[PedidosRepository, Depends(get_repositorio)],
) -> PedidosService:
    return PedidosService(repositorio, get_settings().ambito)


ServicioDep = Annotated[PedidosService, Depends(get_servicio)]

# Matriz RBAC (documento 08): el planificador registra; planificador y administrador consultan.
PUEDE_REGISTRAR = Depends(requerir_rol(Rol.PLANIFICADOR))
PUEDE_CONSULTAR = Depends(requerir_rol(Rol.PLANIFICADOR, Rol.ADMIN))

_ERRORES = {
    400: {"model": ErrorOut, "description": "Datos con formato o tipo inválido"},
    401: {"model": ErrorOut, "description": "Sin sesión válida"},
    403: {"model": ErrorOut, "description": "Rol sin permiso"},
    404: {"model": ErrorOut, "description": "Pedido no encontrado"},
    409: {"model": ErrorOut, "description": "Código de pedido duplicado"},
    422: {"model": ErrorOut, "description": "Regla de negocio incumplida"},
}


@router.post(
    "",
    response_model=PedidoOut,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar pedido",
    responses={k: _ERRORES[k] for k in (400, 401, 403, 409, 422)},
    dependencies=[PUEDE_REGISTRAR],
)
def registrar_pedido(datos: PedidoCrear, servicio: ServicioDep) -> PedidoOut:
    return PedidoOut.desde_dominio(servicio.registrar(datos))


@router.get(
    "",
    response_model=ListadoPedidosOut,
    summary="Listar pedidos",
    responses={k: _ERRORES[k] for k in (400, 401, 403)},
    dependencies=[PUEDE_CONSULTAR],
)
def listar_pedidos(
    servicio: ServicioDep,
    estado: EstadoPedido | None = None,
    pagina: Annotated[int, Query(ge=1)] = 1,
    limite: Annotated[int, Query(ge=1, le=100)] = 20,
) -> ListadoPedidosOut:
    pedidos, total = servicio.listar(estado, pagina, limite)
    return ListadoPedidosOut(
        items=[PedidoOut.desde_dominio(p) for p in pedidos],
        total=total,
        pagina=pagina,
        limite=limite,
    )


@router.get(
    "/{pedido_id}",
    response_model=PedidoOut,
    summary="Consultar pedido por identificador",
    responses={k: _ERRORES[k] for k in (400, 401, 403, 404)},
    dependencies=[PUEDE_CONSULTAR],
)
def obtener_pedido(pedido_id: UUID, servicio: ServicioDep) -> PedidoOut:
    return PedidoOut.desde_dominio(servicio.obtener(pedido_id))
