"""Almacen de rutas guardadas en PostgreSQL (ECO-21): una fila JSONB por fecha de reparto."""

import json
from datetime import date

from sqlalchemy import Engine, text


class RutasGuardadasPostgres:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def guardar(self, fecha: date, registro: dict) -> None:
        with self._engine.begin() as conexion:
            conexion.execute(
                text("""
                    INSERT INTO rutas_guardadas (fecha, registro, guardada_por, guardada_en)
                    VALUES (:fecha, CAST(:registro AS jsonb), :por, now())
                    ON CONFLICT (fecha) DO UPDATE SET registro = EXCLUDED.registro,
                        guardada_por = EXCLUDED.guardada_por, guardada_en = now()
                """),
                {
                    "fecha": fecha,
                    "registro": json.dumps(registro, ensure_ascii=False),
                    "por": registro.get("guardadaPor", ""),
                },
            )

    def obtener(self, fecha: date) -> dict | None:
        with self._engine.connect() as conexion:
            fila = conexion.execute(
                text("SELECT registro FROM rutas_guardadas WHERE fecha = :fecha"), {"fecha": fecha}
            ).one_or_none()
        return fila[0] if fila else None
