"""Persist vehicle master data and date-specific availability.

Revision ID: 20261009_02
Revises: 20261009_01
"""

from alembic import op

revision = "20261009_02"
down_revision = "20261009_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE TYPE estado_vehiculo AS ENUM ('DISPONIBLE','MANTENIMIENTO','INACTIVO')")
    op.execute("""
        CREATE TABLE vehiculos (
            id uuid PRIMARY KEY,
            placa varchar(10) NOT NULL,
            tipo varchar(40) NOT NULL,
            capacidad_kg numeric(10,2) NOT NULL CHECK (capacidad_kg > 0),
            capacidad_m3 numeric(10,3) NOT NULL CHECK (capacidad_m3 > 0),
            combustible varchar(20) NOT NULL
                CHECK (combustible IN ('DIESEL','GASOLINA','GNV','ELECTRICO','HIBRIDO')),
            consumo_base_por_100km numeric(10,4) NOT NULL CHECK (consumo_base_por_100km > 0),
            factor_emision_kgco2e_unidad numeric(14,6)
                CHECK (factor_emision_kgco2e_unidad IS NULL OR factor_emision_kgco2e_unidad > 0),
            anio smallint CHECK (anio IS NULL OR anio BETWEEN 1990 AND 2100),
            estado estado_vehiculo NOT NULL DEFAULT 'DISPONIBLE',
            creado_en timestamptz NOT NULL DEFAULT now(),
            actualizado_en timestamptz NOT NULL DEFAULT now(),
            CONSTRAINT uq_vehiculos_placa UNIQUE (placa),
            CHECK (placa = upper(placa)),
            CHECK (length(placa) BETWEEN 5 AND 10)
        )
    """)
    op.execute("""
        CREATE TABLE disponibilidad_vehiculos (
            vehiculo_id uuid NOT NULL REFERENCES vehiculos(id),
            fecha date NOT NULL,
            turno_inicio time NOT NULL,
            turno_fin time NOT NULL,
            disponible boolean NOT NULL DEFAULT true,
            restriccion_circulacion varchar(500),
            actualizado_en timestamptz NOT NULL DEFAULT now(),
            PRIMARY KEY (vehiculo_id, fecha),
            CHECK (turno_fin > turno_inicio),
            CHECK (disponible OR NULLIF(btrim(restriccion_circulacion), '') IS NOT NULL)
        )
    """)
    op.execute("CREATE INDEX ix_vehiculos_estado_placa ON vehiculos (estado, placa)")
    op.execute("CREATE INDEX ix_disponibilidad_fecha_estado ON disponibilidad_vehiculos (fecha, disponible)")


def downgrade() -> None:
    op.execute("DROP TABLE disponibilidad_vehiculos")
    op.execute("DROP TABLE vehiculos")
    op.execute("DROP TYPE estado_vehiculo")
