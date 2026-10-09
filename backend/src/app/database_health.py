"""Startup checks for an explicitly configured PostgreSQL database."""

from sqlalchemy import inspect, text

from app.database import get_engine


def verificar_base_de_datos() -> None:
    """Fail startup early if PostgreSQL/PostGIS is configured but unavailable."""
    with get_engine().connect() as connection:
        extension = connection.execute(
            text("SELECT extversion FROM pg_extension WHERE extname = 'postgis'")
        ).scalar_one_or_none()
        if extension is None:
            raise RuntimeError("La base configurada no tiene instalada la extension PostGIS")
        tablas = inspect(connection)
        if not tablas.has_table("pedidos") or not tablas.has_table("ubicaciones"):
            raise RuntimeError("Faltan tablas de pedidos; ejecuta las migraciones antes de iniciar la API")
