"""Fleet use cases and validation."""

from datetime import date
from uuid import uuid4

from app.flota.domain import (
    DisponibilidadVehiculo,
    EstadoVehiculo,
    ReglaFlotaError,
    Vehiculo,
    VehiculoNoEncontradoError,
)
from app.flota.repository import FlotaRepository


class FlotaService:
    def __init__(self, repositorio: FlotaRepository) -> None:
        self._repo = repositorio

    def listar(self, fecha: date | None = None) -> list[Vehiculo]:
        return self._repo.listar(fecha)

    def obtener(self, vehiculo_id, fecha: date | None = None) -> Vehiculo:
        vehiculo = self._repo.obtener(vehiculo_id, fecha)
        if vehiculo is None:
            raise VehiculoNoEncontradoError()
        return vehiculo

    def crear(self, datos) -> Vehiculo:
        vehiculo = Vehiculo(
            id=uuid4(),
            placa=datos.placa.strip().upper(),
            tipo=datos.tipo.strip(),
            capacidad_kg=datos.capacidad_kg,
            capacidad_m3=datos.capacidad_m3,
            combustible=datos.combustible,
            consumo_base_por_100km=datos.consumo_base_por_100km,
            factor_emision_kgco2e_unidad=datos.factor_emision_kgco2e_unidad,
            anio=datos.anio,
            estado=datos.estado,
            creado_en=None,
            actualizado_en=None,
        )
        return self._repo.crear(vehiculo)

    def actualizar(self, vehiculo_id, datos) -> Vehiculo:
        anterior = self._repo.obtener(vehiculo_id)
        if anterior is None:
            raise VehiculoNoEncontradoError()
        actualizado = Vehiculo(
            **{
                **anterior.__dict__,
                "placa": datos.placa.strip().upper(),
                "tipo": datos.tipo.strip(),
                "capacidad_kg": datos.capacidad_kg,
                "capacidad_m3": datos.capacidad_m3,
                "combustible": datos.combustible,
                "consumo_base_por_100km": datos.consumo_base_por_100km,
                "factor_emision_kgco2e_unidad": datos.factor_emision_kgco2e_unidad,
                "anio": datos.anio,
                "estado": datos.estado,
                "disponibilidad": None,
            }
        )
        guardado = self._repo.actualizar(actualizado)
        if guardado is None:
            raise VehiculoNoEncontradoError()
        return guardado

    def guardar_disponibilidad(self, vehiculo_id, datos) -> Vehiculo:
        vehiculo = self._repo.obtener(vehiculo_id)
        if vehiculo is None:
            raise VehiculoNoEncontradoError()
        errores = {}
        if datos.turno_fin <= datos.turno_inicio:
            errores["turnoFin"] = "La hora final debe ser posterior a la hora inicial"
        if datos.disponible and vehiculo.estado != EstadoVehiculo.DISPONIBLE:
            errores["disponible"] = "El vehículo debe estar en estado Disponible"
        if not datos.disponible and not datos.restriccion_circulacion:
            errores["restriccionCirculacion"] = "Explique por qué no estará disponible"
        if errores:
            raise ReglaFlotaError(errores)
        disponibilidad = DisponibilidadVehiculo(
            fecha=datos.fecha,
            turno_inicio=datos.turno_inicio,
            turno_fin=datos.turno_fin,
            disponible=datos.disponible,
            restriccion_circulacion=datos.restriccion_circulacion,
        )
        guardado = self._repo.guardar_disponibilidad(vehiculo_id, disponibilidad)
        if guardado is None:
            raise VehiculoNoEncontradoError()
        return guardado
