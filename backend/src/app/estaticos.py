"""Sirve la interfaz compilada desde la misma API (un solo servicio, un solo origen).

Las cookies de sesión son `HttpOnly` y `SameSite=Strict`: solo viajan si la interfaz y la API comparten origen.
Por eso, en producción FastAPI entrega también los archivos de `frontend/dist` (variable `FRONTEND_DIST`).
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, Response

# Rutas que pertenecen a la API y nunca deben responder con la interfaz.
PREFIJOS_API = ("api/", "docs", "redoc", "openapi.json", "health")
CACHE_INMUTABLE = "public, max-age=31536000, immutable"  # los archivos de /assets llevan hash en el nombre
CACHE_REVALIDAR = "no-cache"


def servir_interfaz(app: FastAPI, carpeta: Path) -> None:
    """Registra la entrega de `carpeta` (build de Vite) con respaldo a `index.html` para las rutas de la SPA."""
    raiz = carpeta.resolve()
    indice = raiz / "index.html"
    if not indice.is_file():
        raise RuntimeError(f"FRONTEND_DIST no contiene index.html: {raiz}")

    @app.get("/{ruta:path}", include_in_schema=False)
    def interfaz(ruta: str) -> Response:
        if ruta.startswith(PREFIJOS_API):
            return JSONResponse(status_code=404, content={"status": 404, "message": "Recurso no encontrado"})
        if ruta:
            candidato = (raiz / ruta).resolve()
            # `is_relative_to` bloquea `..` y rutas absolutas que escapen de la carpeta compilada.
            if candidato.is_file() and candidato.is_relative_to(raiz):
                inmutable = ruta.startswith("assets/")
                return FileResponse(candidato, headers={"Cache-Control": CACHE_INMUTABLE if inmutable else CACHE_REVALIDAR})
            if Path(ruta).suffix:  # un archivo con extensión que no existe es un 404 real, no una ruta de la SPA
                return JSONResponse(status_code=404, content={"status": 404, "message": "Recurso no encontrado"})
        return FileResponse(indice, headers={"Cache-Control": CACHE_REVALIDAR})
