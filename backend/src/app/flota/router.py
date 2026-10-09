"""Fleet API: vehicle master data and date-specific availability."""

from datetime import date
from functools import lru_cache
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.auth.dependencias import requerir_rol
from app.auth.domain import Rol
from app.config import get_settings
from app.database import get_engine
from app.flota.memory_repository import FlotaMemoryRepository
from app.flota.postgres_repository import FlotaPostgresRepository
from app.flota.repository import FlotaRepository
from app.flota.schemas import (
    DisponibilidadGuardar,
    ListadoVehiculosOut,
    VehiculoGuardar,
    VehiculoOut,
)
from app.flota.service import FlotaService

router = APIRouter(prefix="/vehiculos", tags=["Flota"])


@lru_cache
def get_repositorio_flota() -> FlotaRepository:
    if get_settings().database_url:
        return FlotaPostgresRepository(get_engine())
    return FlotaMemoryRepository()


def get_servicio_flota(
    repositorio: Annotated[FlotaRepository, Depends(get_repositorio_flota)],
) -> FlotaService:
    return FlotaService(repositorio)


ServicioFlota = Annotated[FlotaService, Depends(get_servicio_flota)]
PuedeConsultar = Depends(requerir_rol(Rol.ADMIN, Rol.PLANIFICADOR))
PuedeAdministrar = Depends(requerir_rol(Rol.ADMIN))
PuedePlanificar = Depends(requerir_rol(Rol.PLANIFICADOR))


@router.get("", response_model=ListadoVehiculosOut, dependencies=[PuedeConsultar])
def listar_vehiculos(
    servicio: ServicioFlota,
    fecha: Annotated[date | None, Query()] = None,
) -> ListadoVehiculosOut:
    return ListadoVehiculosOut(items=[VehiculoOut.desde_dominio(v) for v in servicio.listar(fecha)])


@router.post("", response_model=VehiculoOut, status_code=status.HTTP_201_CREATED, dependencies=[PuedeAdministrar])
def crear_vehiculo(datos: VehiculoGuardar, servicio: ServicioFlota) -> VehiculoOut:
    return VehiculoOut.desde_dominio(servicio.crear(datos))


@router.put("/{vehiculo_id}", response_model=VehiculoOut, dependencies=[PuedeAdministrar])
def actualizar_vehiculo(vehiculo_id: UUID, datos: VehiculoGuardar, servicio: ServicioFlota) -> VehiculoOut:
    return VehiculoOut.desde_dominio(servicio.actualizar(vehiculo_id, datos))


@router.put("/{vehiculo_id}/disponibilidad", response_model=VehiculoOut, dependencies=[PuedePlanificar])
def guardar_disponibilidad(
    vehiculo_id: UUID, datos: DisponibilidadGuardar, servicio: ServicioFlota
) -> VehiculoOut:
    return VehiculoOut.desde_dominio(servicio.guardar_disponibilidad(vehiculo_id, datos))


@router.get("/{vehiculo_id}", response_model=VehiculoOut, dependencies=[PuedeConsultar])
def obtener_vehiculo(
    vehiculo_id: UUID,
    servicio: ServicioFlota,
    fecha: Annotated[date | None, Query()] = None,
) -> VehiculoOut:
    return VehiculoOut.desde_dominio(servicio.obtener(vehiculo_id, fecha))
