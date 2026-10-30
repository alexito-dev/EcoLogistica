"""Rutas REST de la vista previa de rutas."""

from datetime import date, datetime, timezone
from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth.dependencias import requerir_rol
from app.auth.domain import Rol, Usuario
from app.config import get_settings
from app.flota.repository import FlotaRepository
from app.flota.router import get_repositorio_flota
from app.pedidos.repository import PedidosRepository
from app.pedidos.router import get_repositorio
from app.pedidos.domain import ReglaDominioError
from app.pedidos.schemas import ErrorOut
from app.rutas.planificador import Punto
from app.rutas.guardadas import RutasGuardadasArchivo
from app.rutas.schemas import RutaGuardadaOut, VistaPreviaOut
from app.rutas.service import RutasService

router = APIRouter(prefix="/rutas", tags=["Rutas"])
ROLES_PLANIFICACION = (Rol.PLANIFICADOR, Rol.ADMIN)


@lru_cache
def get_repositorio_guardadas() -> RutasGuardadasArchivo:
    return RutasGuardadasArchivo(get_settings().rutas_archivo)


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


@router.post(
    "/guardar",
    status_code=status.HTTP_201_CREATED,
    response_model=RutaGuardadaOut,
    summary="Guardar las rutas del día",
    description=(
        "Calcula la propuesta de la fecha y la guarda para volver a abrirla después, incluso tras reiniciar la API. "
        "Si ya había rutas guardadas para esa fecha, las reemplaza."
    ),
    responses={
        400: {"model": ErrorOut, "description": "Fecha con formato inválido"},
        401: {"model": ErrorOut, "description": "Sin sesión válida"},
        403: {"model": ErrorOut, "description": "Rol sin permiso"},
        422: {"model": ErrorOut, "description": "No hay rutas que guardar para la fecha"},
    },
)
def guardar(
    servicio: Annotated[RutasService, Depends(get_servicio_rutas)],
    guardadas: Annotated[RutasGuardadasArchivo, Depends(get_repositorio_guardadas)],
    usuario: Annotated[Usuario, Depends(requerir_rol(*ROLES_PLANIFICACION))],
    fecha: Annotated[date, Query(description="Fecha de reparto (AAAA-MM-DD)")],
) -> RutaGuardadaOut:
    propuesta, disponibles = servicio.vista_previa(fecha)
    vista = VistaPreviaOut.desde_dominio(propuesta, get_settings().deposito_nombre, disponibles)
    if not vista.rutas:
        raise ReglaDominioError({"fecha": "No hay rutas que guardar para esta fecha"})
    guardada = RutaGuardadaOut(
        fecha=fecha, guardada_en=datetime.now(timezone.utc), guardada_por=usuario.nombre, vista=vista
    )
    guardadas.guardar(fecha, guardada.model_dump(mode="json", by_alias=True))
    return guardada


@router.get(
    "/guardada",
    response_model=RutaGuardadaOut,
    summary="Abrir las rutas guardadas de una fecha",
    responses={
        400: {"model": ErrorOut, "description": "Fecha con formato inválido"},
        401: {"model": ErrorOut, "description": "Sin sesión válida"},
        403: {"model": ErrorOut, "description": "Rol sin permiso"},
        404: {"model": ErrorOut, "description": "No hay rutas guardadas para la fecha"},
    },
    dependencies=[Depends(requerir_rol(*ROLES_PLANIFICACION))],
)
def guardada(
    guardadas: Annotated[RutasGuardadasArchivo, Depends(get_repositorio_guardadas)],
    fecha: Annotated[date, Query(description="Fecha de reparto (AAAA-MM-DD)")],
) -> RutaGuardadaOut:
    registro = guardadas.obtener(fecha)
    if registro is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return RutaGuardadaOut.model_validate(registro)
