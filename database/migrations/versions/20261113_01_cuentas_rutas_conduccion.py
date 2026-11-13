"""Persist accounts (encrypted TOTP secrets), saved routes and driver execution (ECO-21, Sprint 4).

Revision ID: 20261113_01
Revises: 20261009_02
"""

from alembic import op

revision = "20261113_01"
down_revision = "20261009_02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE TYPE estado_usuario AS ENUM ('ACTIVO','BLOQUEADO','INACTIVO')")
    op.execute("""
        CREATE TABLE usuarios (
            id uuid PRIMARY KEY,
            correo text NOT NULL,
            nombre text NOT NULL,
            rol varchar(20) NOT NULL
                CHECK (rol IN ('ADMIN','PLANIFICADOR','CONDUCTOR','GERENTE','AUDITOR')),
            clave_hash text NOT NULL,
            estado estado_usuario NOT NULL DEFAULT 'ACTIVO',
            mfa_secreto_cifrado text,
            mfa_pendiente_cifrado text,
            mfa_ultimo_paso bigint NOT NULL DEFAULT 0,
            mfa_fallidos integer NOT NULL DEFAULT 0,
            version_sesion integer NOT NULL DEFAULT 1,
            creado_en timestamptz NOT NULL DEFAULT now(),
            actualizado_en timestamptz NOT NULL DEFAULT now(),
            CONSTRAINT uq_usuarios_correo UNIQUE (correo),
            CHECK (correo = lower(correo))
        )
    """)
    op.execute("CREATE INDEX ix_usuarios_rol_estado ON usuarios (rol, estado)")
    op.execute("""
        CREATE TABLE intentos_acceso (
            correo text PRIMARY KEY,
            fallos timestamptz[] NOT NULL DEFAULT '{}',
            bloqueado_hasta timestamptz
        )
    """)
    op.execute("""
        CREATE TABLE rutas_guardadas (
            fecha date PRIMARY KEY,
            registro jsonb NOT NULL,
            guardada_por text NOT NULL,
            guardada_en timestamptz NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE TABLE asignaciones_ruta (
            fecha date NOT NULL,
            vehiculo_id uuid NOT NULL REFERENCES vehiculos(id),
            conductor_id uuid NOT NULL REFERENCES usuarios(id),
            asignado_por uuid REFERENCES usuarios(id),
            asignado_en timestamptz NOT NULL DEFAULT now(),
            PRIMARY KEY (fecha, vehiculo_id)
        )
    """)
    op.execute("CREATE INDEX ix_asignaciones_conductor_fecha ON asignaciones_ruta (conductor_id, fecha)")
    # Historial inmutable de avances: el estado actual de una parada es su ultimo evento.
    op.execute("""
        CREATE TABLE eventos_parada (
            id uuid PRIMARY KEY,
            fecha date NOT NULL,
            pedido_id uuid NOT NULL REFERENCES pedidos(id),
            estado varchar(20) NOT NULL
                CHECK (estado IN ('PENDIENTE','EN_RUTA','ENTREGADO','INCIDENCIA','CANCELADO','REPROGRAMADO')),
            nota text,
            usuario_id uuid REFERENCES usuarios(id),
            creado_en timestamptz NOT NULL DEFAULT now(),
            CHECK (estado <> 'INCIDENCIA' OR NULLIF(btrim(nota), '') IS NOT NULL)
        )
    """)
    op.execute("CREATE INDEX ix_eventos_parada_fecha_pedido ON eventos_parada (fecha, pedido_id, creado_en DESC)")


def downgrade() -> None:
    op.execute("DROP TABLE eventos_parada")
    op.execute("DROP TABLE asignaciones_ruta")
    op.execute("DROP TABLE rutas_guardadas")
    op.execute("DROP TABLE intentos_acceso")
    op.execute("DROP TABLE usuarios")
    op.execute("DROP TYPE estado_usuario")
