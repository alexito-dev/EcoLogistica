"""Index orders by state and window start for the daily route planning query.

Revision ID: 20261113_02
Revises: 20261113_01
"""

from alembic import op

revision = "20261113_02"
down_revision = "20261113_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE INDEX ix_pedidos_estado_ventana ON pedidos (estado, ventana_inicio)")


def downgrade() -> None:
    op.execute("DROP INDEX ix_pedidos_estado_ventana")
