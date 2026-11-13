"""API de Conduccion: ruta asignada, avance de entregas e incidencias (HU-005, HU-010) y reoptimizacion (HU-006)."""

from datetime import date
from functools import lru_cache
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth.dependencias import get_repositorio_usuarios, requerir_rol
from app.auth.domain import Rol, Usuario
from app.auth.repository import UsuariosRepository
from app.conduccion.memory_repository import ConduccionMemoryRepository
from app.conduccion.postgres_repository import ConduccionPostgresRepository
from app.conduccion.repository import ConduccionRepository
from app.conduccion.schemas import (
    AsignacionIn,
    EstadoIn,
    EventoOut,
    FechaIn,
    MiRutaOut,
    ParadaEjecucionOut,
    ReoptimizacionOut,
    SeguimientoOut,
)
from app.conduccion.service import ConduccionService, ParadaNoAsignadaError, RutaNoGuardadaError
from app.config import get_settings
from app.database import get_engine
from app.pedidos.repository import PedidosRepository
from app.pedidos.router import get_repositorio
from app.pedidos.schemas import ErrorOut
from app.rutas.router import get_repositorio_guardadas

router = APIRouter(prefix="/conduccion", tags=["Conducción"])
ROLES_PLANIFICACION = (Rol.PLANIFICADOR, Rol.ADMIN)

_ERRORES = {
    400: {"model": ErrorOut, "description": "Datos con formato inválido"},
    401: {"model": ErrorOut, "description": "Sin sesión válida"},
    403: {"model": ErrorOut, "description": "Rol sin permiso"},
    404: {"model": ErrorOut, "description": "Sin rutas guardadas o parada no asignada"},
    422: {"model": ErrorOut, "description": "Regla de negocio incumplida"},
}


@lru_cache
def get_repositorio_conduccion() -> ConduccionRepository:
    if get_settings().database_url:
        return ConduccionPostgresRepository(get_engine())
    return ConduccionMemoryRepository()


def get_servicio_conduccion(
    guardadas: Annotated[object, Depends(get_repositorio_guardadas)],
    conduccion: Annotated[ConduccionRepository, Depends(get_repositorio_conduccion)],
    pedidos: Annotated[PedidosRepository, Depends(get_repositorio)],
    usuarios: Annotated[UsuariosRepository, Depends(get_repositorio_usuarios)],
) -> ConduccionService:
    return ConduccionService(guardadas, conduccion, pedidos, usuarios)


ServicioDep = Annotated[ConduccionService, Depends(get_servicio_conduccion)]
FechaQuery = Annotated[date, Query(description="Fecha de reparto (AAAA-MM-DD)")]
Conductor = Annotated[Usuario, Depends(requerir_rol(Rol.CONDUCTOR))]
Planificacion = Annotated[Usuario, Depends(requerir_rol(*ROLES_PLANIFICACION))]


def _no_encontrado(mensaje: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=mensaje)


@router.get(
    "/mi-ruta",
    response_model=MiRutaOut,
    summary="Consultar la ruta asignada a quien conduce",
    responses={k: _ERRORES[k] for k in (400, 401, 403, 404)},
)
def mi_ruta(servicio: ServicioDep, conductor: Conductor, fecha: FechaQuery) -> MiRutaOut:
    try:
        return MiRutaOut.model_validate(servicio.mi_ruta(fecha, conductor))
    except RutaNoGuardadaError as error:
        raise _no_encontrado("No hay rutas guardadas para esta fecha") from error


@router.post(
    "/paradas/{pedido_id}/estado",
    response_model=ParadaEjecucionOut,
    summary="Registrar el avance de una entrega",
    description=(
        "Quien conduce marca En ruta, Entregado, Incidencia (con descripción) o Cancelado. "
        "Solo se permiten las transiciones válidas y solo sobre paradas de su ruta."
    ),
    responses={k: _ERRORES[k] for k in (400, 401, 403, 404, 422)},
)
def registrar_estado(pedido_id: UUID, datos: EstadoIn, servicio: ServicioDep, conductor: Conductor) -> ParadaEjecucionOut:
    try:
        return ParadaEjecucionOut.model_validate(
            servicio.registrar_estado(datos.fecha, pedido_id, datos.estado, datos.nota, conductor)
        )
    except (RutaNoGuardadaError, ParadaNoAsignadaError) as error:
        raise _no_encontrado("La parada no pertenece a una ruta asignada a usted") from error


@router.get(
    "/seguimiento",
    response_model=SeguimientoOut,
    summary="Seguimiento de las rutas del día para Planificación",
    responses={k: _ERRORES[k] for k in (400, 401, 403, 404)},
)
def seguimiento(servicio: ServicioDep, _: Planificacion, fecha: FechaQuery) -> SeguimientoOut:
    try:
        return SeguimientoOut.model_validate(servicio.seguimiento(fecha))
    except RutaNoGuardadaError as error:
        raise _no_encontrado("No hay rutas guardadas para esta fecha") from error


@router.put(
    "/asignaciones",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Asignar un conductor a la ruta de un vehículo",
    responses={k: _ERRORES[k] for k in (400, 401, 403, 404, 422)},
)
def asignar(datos: AsignacionIn, servicio: ServicioDep, usuario: Planificacion) -> None:
    try:
        servicio.asignar(datos.fecha, datos.vehiculo_id, datos.conductor_id, usuario)
    except RutaNoGuardadaError as error:
        raise _no_encontrado("No hay rutas guardadas para esta fecha") from error


@router.get(
    "/paradas/{pedido_id}/historial",
    response_model=list[EventoOut],
    summary="Historial de avances de una parada",
    responses={k: _ERRORES[k] for k in (400, 401, 403)},
)
def historial(pedido_id: UUID, servicio: ServicioDep, _: Planificacion, fecha: FechaQuery) -> list[EventoOut]:
    return [
        EventoOut(estado=e.estado, nota=e.nota, usuario_id=e.usuario_id, creado_en=e.creado_en)
        for e in servicio.historial(fecha, pedido_id)
    ]


@router.post(
    "/paradas/{pedido_id}/reprogramar",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Reprogramar una parada con incidencia",
    description="Devuelve el pedido a Pendiente para planificarlo de nuevo; la incidencia y su historial se conservan.",
    responses={k: _ERRORES[k] for k in (400, 401, 403, 404, 422)},
)
def reprogramar(pedido_id: UUID, datos: FechaIn, servicio: ServicioDep, usuario: Planificacion) -> None:
    try:
        servicio.reprogramar(datos.fecha, pedido_id, usuario)
    except (RutaNoGuardadaError, ParadaNoAsignadaError) as error:
        raise _no_encontrado("La parada no existe en las rutas guardadas") from error


@router.post(
    "/reoptimizar",
    response_model=ReoptimizacionOut,
    summary="Reordenar las paradas pendientes tras una incidencia",
    description=(
        "Reordena solo las paradas aún no atendidas desde la última entrega y recalcula sus llegadas. "
        "No altera paradas entregadas, canceladas, reprogramadas ni con incidencia."
    ),
    responses={k: _ERRORES[k] for k in (400, 401, 403, 404)},
)
def reoptimizar(datos: FechaIn, servicio: ServicioDep, usuario: Planificacion) -> ReoptimizacionOut:
    try:
        return ReoptimizacionOut.model_validate(servicio.reoptimizar(datos.fecha, usuario))
    except RutaNoGuardadaError as error:
        raise _no_encontrado("No hay rutas guardadas para esta fecha") from error
