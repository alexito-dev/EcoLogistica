"""PostgreSQL adapter for vehicle master data and daily availability."""

from collections.abc import Mapping
from datetime import date
from uuid import UUID

from sqlalchemy import Engine, text
from sqlalchemy.exc import IntegrityError

from app.flota.domain import (
    Combustible,
    DisponibilidadVehiculo,
    EstadoVehiculo,
    PlacaDuplicadaError,
    Vehiculo,
)


_SELECT = """
SELECT v.id, v.placa, v.tipo, v.capacidad_kg, v.capacidad_m3, v.combustible,
       v.consumo_base_por_100km, v.factor_emision_kgco2e_unidad, v.anio,
       v.estado, v.creado_en, v.actualizado_en,
       d.fecha AS disponibilidad_fecha, d.turno_inicio, d.turno_fin,
       d.disponible AS disponibilidad_activa,
       d.restriccion_circulacion
FROM vehiculos v
LEFT JOIN disponibilidad_vehiculos d
  ON d.vehiculo_id = v.id AND d.fecha = :fecha
"""


class FlotaPostgresRepository:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def listar(self, fecha: date | None = None) -> list[Vehiculo]:
        with self._engine.connect() as connection:
            rows = connection.execute(text(_SELECT + " ORDER BY v.placa"), {"fecha": fecha}).mappings().all()
        return [self._desde_fila(row) for row in rows]

    def obtener(self, vehiculo_id: UUID, fecha: date | None = None) -> Vehiculo | None:
        with self._engine.connect() as connection:
            row = connection.execute(
                text(_SELECT + " WHERE v.id = :id"), {"id": vehiculo_id, "fecha": fecha}
            ).mappings().one_or_none()
        return self._desde_fila(row) if row else None

    def crear(self, vehiculo: Vehiculo) -> Vehiculo:
        try:
            with self._engine.begin() as connection:
                connection.execute(
                    text("""
                        INSERT INTO vehiculos
                            (id, placa, tipo, capacidad_kg, capacidad_m3, combustible,
                             consumo_base_por_100km, factor_emision_kgco2e_unidad,
                             anio, estado)
                        VALUES
                            (:id, :placa, :tipo, :capacidad_kg, :capacidad_m3,
                             :combustible, :consumo, :factor_emision, :anio, :estado)
                    """), self._parametros(vehiculo)
                )
        except IntegrityError as error:
            if self._placa_existe(vehiculo.placa):
                raise PlacaDuplicadaError(vehiculo.placa) from error
            raise
        return self.obtener(vehiculo.id)  # type: ignore[return-value]

    def actualizar(self, vehiculo: Vehiculo) -> Vehiculo | None:
        try:
            with self._engine.begin() as connection:
                result = connection.execute(
                    text("""
                        UPDATE vehiculos SET
                            placa=:placa, tipo=:tipo, capacidad_kg=:capacidad_kg,
                            capacidad_m3=:capacidad_m3, combustible=:combustible,
                            consumo_base_por_100km=:consumo,
                            factor_emision_kgco2e_unidad=:factor_emision,
                            anio=:anio, estado=:estado, actualizado_en=now()
                        WHERE id=:id
                    """), self._parametros(vehiculo)
                )
                if result.rowcount == 0:
                    return None
        except IntegrityError as error:
            if self._placa_existe(vehiculo.placa):
                raise PlacaDuplicadaError(vehiculo.placa) from error
            raise
        return self.obtener(vehiculo.id)

    def guardar_disponibilidad(
        self, vehiculo_id: UUID, disponibilidad: DisponibilidadVehiculo
    ) -> Vehiculo | None:
        with self._engine.begin() as connection:
            existe = connection.execute(
                text("SELECT 1 FROM vehiculos WHERE id=:id"), {"id": vehiculo_id}
            ).scalar_one_or_none()
            if not existe:
                return None
            connection.execute(
                text("""
                    INSERT INTO disponibilidad_vehiculos
                        (vehiculo_id, fecha, turno_inicio, turno_fin, disponible,
                         restriccion_circulacion, actualizado_en)
                    VALUES
                        (:vehiculo_id, :fecha, :turno_inicio, :turno_fin, :disponible,
                         :restriccion, now())
                    ON CONFLICT (vehiculo_id, fecha) DO UPDATE SET
                        turno_inicio=EXCLUDED.turno_inicio,
                        turno_fin=EXCLUDED.turno_fin,
                        disponible=EXCLUDED.disponible,
                        restriccion_circulacion=EXCLUDED.restriccion_circulacion,
                        actualizado_en=now()
                """), {
                    "vehiculo_id": vehiculo_id,
                    "fecha": disponibilidad.fecha,
                    "turno_inicio": disponibilidad.turno_inicio,
                    "turno_fin": disponibilidad.turno_fin,
                    "disponible": disponibilidad.disponible,
                    "restriccion": disponibilidad.restriccion_circulacion,
                }
            )
        return self.obtener(vehiculo_id, disponibilidad.fecha)

    def _placa_existe(self, placa: str) -> bool:
        with self._engine.connect() as connection:
            return bool(connection.execute(
                text("SELECT 1 FROM vehiculos WHERE placa=:placa"), {"placa": placa}
            ).scalar_one_or_none())

    @staticmethod
    def _parametros(v: Vehiculo) -> dict[str, object]:
        return {
            "id": v.id,
            "placa": v.placa,
            "tipo": v.tipo,
            "capacidad_kg": v.capacidad_kg,
            "capacidad_m3": v.capacidad_m3,
            "combustible": v.combustible.value,
            "consumo": v.consumo_base_por_100km,
            "factor_emision": v.factor_emision_kgco2e_unidad,
            "anio": v.anio,
            "estado": v.estado.value,
        }

    @staticmethod
    def _desde_fila(row: Mapping[str, object]) -> Vehiculo:
        disponibilidad = None
        if row["disponibilidad_fecha"] is not None:
            disponibilidad = DisponibilidadVehiculo(
                fecha=row["disponibilidad_fecha"],  # type: ignore[arg-type]
                turno_inicio=row["turno_inicio"],  # type: ignore[arg-type]
                turno_fin=row["turno_fin"],  # type: ignore[arg-type]
                disponible=row["disponibilidad_activa"],  # type: ignore[arg-type]
                restriccion_circulacion=row["restriccion_circulacion"],  # type: ignore[arg-type]
            )
        return Vehiculo(
            id=row["id"],  # type: ignore[arg-type]
            placa=row["placa"],  # type: ignore[arg-type]
            tipo=row["tipo"],  # type: ignore[arg-type]
            capacidad_kg=row["capacidad_kg"],  # type: ignore[arg-type]
            capacidad_m3=row["capacidad_m3"],  # type: ignore[arg-type]
            combustible=Combustible(row["combustible"]),  # type: ignore[arg-type]
            consumo_base_por_100km=row["consumo_base_por_100km"],  # type: ignore[arg-type]
            factor_emision_kgco2e_unidad=row["factor_emision_kgco2e_unidad"],  # type: ignore[arg-type]
            anio=row["anio"],  # type: ignore[arg-type]
            estado=EstadoVehiculo(row["estado"]),  # type: ignore[arg-type]
            creado_en=row["creado_en"],
            actualizado_en=row["actualizado_en"],
            disponibilidad=disponibilidad,
        )
