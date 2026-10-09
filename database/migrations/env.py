import sys
from pathlib import Path

from alembic import context
from sqlalchemy import create_engine

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend" / "src"))

from app.config import get_settings

config = context.config
database_url = get_settings().database_url
if not database_url:
    raise RuntimeError("Configura DATABASE_URL antes de ejecutar migraciones")
config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))


def run_migrations_offline() -> None:
    context.configure(url=database_url, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(database_url, pool_pre_ping=True)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=None, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()
    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
