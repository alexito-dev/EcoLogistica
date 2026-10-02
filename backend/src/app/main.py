"""Punto de entrada de la API de EcoLogística."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.errors import registrar_manejadores
from app.pedidos.router import router as pedidos_router


def create_app() -> FastAPI:
    settings = get_settings()  # valida el ámbito al arrancar
    app = FastAPI(
        title="EcoLogística Huancayo API",
        version="0.1.0",
        description="API REST de pedidos, flota y optimización de rutas sostenibles.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.cors_origin],
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )
    registrar_manejadores(app)
    app.include_router(pedidos_router, prefix="/api/v1")
    return app


app = create_app()
