"""Ruta REST del dashboard de indicadores."""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.auth.dependencias import requerir_rol
from app.auth.domain import Rol
from app.flota.repository import FlotaRepository
from app.flota.router import get_repositorio_flota
from app.indicadores.schemas import IndicadoresOut
from app.indicadores.service import IndicadoresService
from app.pedidos.repository import PedidosRepository
from app.pedidos.router import get_repositorio
from app.pedidos.schemas import ErrorOut
from app.rutas.router import get_servicio_rutas
from app.rutas.service import RutasService

router = APIRouter(prefix="/indicadores", tags=["Indicadores"])


def get_servicio_indicadores(
    pedidos: Annotated[PedidosRepository, Depends(get_repositorio)],
    flota: Annotated[FlotaRepository, Depends(get_repositorio_flota)],
    rutas: Annotated[RutasService, Depends(get_servicio_rutas)],
) -> IndicadoresService:
    return IndicadoresService(pedidos, flota, rutas)


@router.get(
    "",
    response_model=IndicadoresOut,
    summary="Indicadores de operación y sostenibilidad",
    description=(
        "Resume los pedidos registrados (por estado, distrito y prioridad), la flota (aptos y combustibles) "
        "y la planificación de la fecha según la vista previa de rutas: uso de capacidad, puntualidad y CO₂e."
    ),
    responses={
        400: {"model": ErrorOut, "description": "Fecha con formato inválido"},
        401: {"model": ErrorOut, "description": "Sin sesión válida"},
        403: {"model": ErrorOut, "description": "Rol sin permiso"},
    },
    dependencies=[Depends(requerir_rol(Rol.PLANIFICADOR, Rol.ADMIN, Rol.GERENTE))],
)
def indicadores(
    servicio: Annotated[IndicadoresService, Depends(get_servicio_indicadores)],
    fecha: Annotated[date, Query(description="Fecha de reparto (AAAA-MM-DD)")],
) -> IndicadoresOut:
    return IndicadoresOut.desde_dominio(servicio.calcular(fecha))
