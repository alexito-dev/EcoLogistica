"""Punto de entrada de la API de EcoLogística."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.auth.dependencias import get_repositorio_usuarios
from app.auth.router import router as auth_router
from app.config import get_settings
from app.database_health import verificar_base_de_datos
from app.errors import registrar_manejadores
from app.flota.router import get_repositorio_flota
from app.flota.router import router as flota_router
from app.flota.siembra import sembrar_vehiculos_demo
from app.pedidos.router import get_repositorio
from app.pedidos.router import router as pedidos_router
from app.pedidos.siembra import sembrar_pedidos_demo
from app.indicadores.router import router as indicadores_router
from app.rutas.router import router as rutas_router

METODOS_QUE_CAMBIAN_ESTADO = {"POST", "PUT", "PATCH", "DELETE"}
PREFIJO_API = "/api/v1"
# Cabeceras de endurecimiento (OWASP A02:2025). La CSP estricta solo aplica a la API JSON;
# /docs carga Swagger UI desde un CDN y quedaría inutilizable con ella.
CABECERAS_SEGURIDAD = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
}
CSP_API = "default-src 'none'; frame-ancestors 'none'"


def configurar_registro() -> None:
    """Envía a la consola los eventos de la aplicación y de auditoría de acceso (RF-11.2)."""
    registro = logging.getLogger("ecologistica")
    if not registro.handlers:
        manejador = logging.StreamHandler()
        manejador.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
        registro.addHandler(manejador)
        registro.setLevel(logging.INFO)


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    # Carga el almacén de usuarios al arrancar (y siembra los de demostración si está vacío),
    # para que la contraseña generada aparezca en la consola apenas se inicia el servidor.
    get_repositorio_usuarios()
    settings = get_settings()
    if settings.database_url:
        verificar_base_de_datos()
    if settings.demo_pedidos:
        pedidos = sembrar_pedidos_demo(get_repositorio(), settings.ambito)
        vehiculos = sembrar_vehiculos_demo(get_repositorio_flota())
        logging.getLogger("ecologistica").info(
            "Datos de demostración cargados: %s pedidos, %s vehículos", pedidos, vehiculos
        )
    yield


def create_app() -> FastAPI:
    configurar_registro()
    settings = get_settings()  # valida el ámbito y la clave de firma al arrancar
    app = FastAPI(
        title="EcoLogística Huancayo API",
        version="0.1.0",
        description="API REST de pedidos, flota y optimización de rutas sostenibles.",
        lifespan=ciclo_de_vida,
    )

    @app.middleware("http")
    async def verificar_origen(request: Request, call_next):
        # Defensa CSRF adicional a SameSite=Strict: solo el frontend configurado puede cambiar estado.
        origen = request.headers.get("origin")
        if request.method in METODOS_QUE_CAMBIAN_ESTADO and origen and origen != settings.cors_origin:
            return JSONResponse(status_code=403, content={"status": 403, "message": "Origen no permitido"})
        return await call_next(request)

    @app.middleware("http")
    async def cabeceras_de_seguridad(request: Request, call_next):
        respuesta = await call_next(request)
        respuesta.headers.update(CABECERAS_SEGURIDAD)
        if request.url.path.startswith(PREFIJO_API):
            respuesta.headers["Content-Security-Policy"] = CSP_API
        return respuesta

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.cors_origin],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT"],
        allow_headers=["Content-Type"],
    )
    registrar_manejadores(app)
    for router in (auth_router, pedidos_router, flota_router, rutas_router, indicadores_router):
        app.include_router(router, prefix=PREFIJO_API)
    return app


app = create_app()
