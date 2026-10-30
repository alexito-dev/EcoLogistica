"""Rutas REST de la vista previa de rutas."""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.auth.dependencias import requerir_rol
from app.auth.domain import Rol
from app.config import get_settings
from app.flota.repository import FlotaRepository
from app.flota.router import get_repositorio_flota
from app.pedidos.repository import PedidosRepository
from app.pedidos.router import get_repositorio
from app.pedidos.schemas import ErrorOut
from app.rutas.planificador import Punto
from app.rutas.schemas import VistaPreviaOut
from app.rutas.service import RutasService

router = APIRouter(prefix="/rutas", tags=["Rutas"])


def get_servicio_rutas(
    pedidos: Annotated[PedidosRepository, Depends(get_repositorio)],
    flota: Annotated[FlotaRepository, Depends(get_repositorio_flota)],
) -> RutasService:
    settings = get_settings()
    return RutasService(pedidos, flota, Punto(settings.deposito_lat, settings.deposito_lon))


@router.get(
    "/vista-previa",
    response_model=VistaPreviaOut,
    summary="Vista previa de rutas del día",
    description=(
        "Agrupa los pedidos pendientes o validados de la fecha en los vehículos aptos para planificar, "
        "respetando su capacidad, y ordena cada ruta para acortar el recorrido. No guarda nada."
    ),
    responses={
        400: {"model": ErrorOut, "description": "Fecha con formato inválido"},
        401: {"model": ErrorOut, "description": "Sin sesión válida"},
        403: {"model": ErrorOut, "description": "Rol sin permiso"},
    },
    dependencies=[Depends(requerir_rol(Rol.PLANIFICADOR, Rol.ADMIN))],
)
def vista_previa(
    servicio: Annotated[RutasService, Depends(get_servicio_rutas)],
    fecha: Annotated[date, Query(description="Fecha de reparto (AAAA-MM-DD)")],
) -> VistaPreviaOut:
    propuesta, disponibles = servicio.vista_previa(fecha)
    return VistaPreviaOut.desde_dominio(propuesta, get_settings().deposito_nombre, disponibles)
