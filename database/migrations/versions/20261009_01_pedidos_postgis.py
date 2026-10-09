"""Persist orders and their destinations with PostGIS.

Revision ID: 20261009_01
Revises:
"""

from alembic import op

revision = "20261009_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.execute("CREATE TYPE estado_pedido AS ENUM ('PENDIENTE','VALIDADO','ASIGNADO','EN_RUTA','ENTREGADO','FALLIDO','CANCELADO')")
    op.execute("CREATE SEQUENCE pedido_codigo_seq START WITH 1 INCREMENT BY 1")
    op.execute("""
        CREATE TABLE ubicaciones (
            id uuid PRIMARY KEY,
            etiqueta varchar(150) NOT NULL,
            direccion_referencial varchar(250),
            distrito varchar(80) NOT NULL,
            punto geometry(Point,4326) NOT NULL,
            precision_m numeric(8,2),
            fuente varchar(80) NOT NULL DEFAULT 'MANUAL',
            es_deposito boolean NOT NULL DEFAULT false,
            creado_en timestamptz NOT NULL DEFAULT now(),
            CHECK (precision_m IS NULL OR precision_m >= 0),
            CHECK (ST_X(punto) BETWEEN -180 AND 180 AND ST_Y(punto) BETWEEN -90 AND 90)
        )
    """)
    op.execute("""
        CREATE TABLE pedidos (
            id uuid PRIMARY KEY,
            codigo varchar(40) NOT NULL CONSTRAINT uq_pedidos_codigo UNIQUE,
            ubicacion_id uuid NOT NULL REFERENCES ubicaciones(id),
            destinatario_alias varchar(120),
            demanda_kg numeric(10,2) NOT NULL DEFAULT 0 CHECK (demanda_kg >= 0),
            demanda_m3 numeric(10,3) NOT NULL DEFAULT 0 CHECK (demanda_m3 >= 0),
            tiempo_servicio_min smallint NOT NULL DEFAULT 10 CHECK (tiempo_servicio_min > 0),
            ventana_inicio timestamptz NOT NULL,
            ventana_fin timestamptz NOT NULL,
            prioridad smallint NOT NULL DEFAULT 2 CHECK (prioridad BETWEEN 1 AND 4),
            estado estado_pedido NOT NULL DEFAULT 'PENDIENTE',
            observacion_operativa varchar(500),
            creado_en timestamptz NOT NULL DEFAULT now(),
            actualizado_en timestamptz NOT NULL DEFAULT now(),
            CHECK (demanda_kg > 0 OR demanda_m3 > 0),
            CHECK (ventana_fin > ventana_inicio)
        )
    """)
    op.execute("CREATE INDEX ix_ubicaciones_punto ON ubicaciones USING GIST (punto)")
    op.execute("CREATE INDEX ix_pedidos_estado_creado ON pedidos (estado, creado_en DESC)")


def downgrade() -> None:
    op.execute("DROP TABLE pedidos")
    op.execute("DROP TABLE ubicaciones")
    op.execute("DROP SEQUENCE pedido_codigo_seq")
    op.execute("DROP TYPE estado_pedido")
