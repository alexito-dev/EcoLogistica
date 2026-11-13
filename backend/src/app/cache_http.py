"""Caché HTTP condicional (Green IT): ETag + Cache-Control en las lecturas de la API."""

import hashlib

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Los datos dependen de la sesión (cookie): `private` impide cachés compartidas y `no-cache` obliga a
# revalidar con If-None-Match; si no cambió, el servidor responde 304 sin cuerpo y se ahorra la transferencia.
CACHE_CONTROL_LECTURAS = "private, no-cache"
PREFIJOS_NO_CACHEABLES = ("/api/v1/auth",)


def calcular_etag(cuerpo: bytes) -> str:
    return f'W/"{hashlib.sha256(cuerpo).hexdigest()[:32]}"'


def _coincide(if_none_match: str | None, etag: str) -> bool:
    if not if_none_match:
        return False
    candidatos = {c.strip() for c in if_none_match.split(",")}
    return "*" in candidatos or etag in candidatos


class EtagMiddleware(BaseHTTPMiddleware):
    """Añade ETag débil a los GET 200 con JSON y responde 304 cuando el cliente ya tiene la versión."""

    async def dispatch(self, request: Request, call_next):
        respuesta = await call_next(request)
        if (
            request.method != "GET"
            or respuesta.status_code != 200
            or request.url.path.startswith(PREFIJOS_NO_CACHEABLES)
            or "application/json" not in respuesta.headers.get("content-type", "")
        ):
            return respuesta
        cuerpo = b"".join([parte async for parte in respuesta.body_iterator])
        etag = calcular_etag(cuerpo)
        cabeceras = {"ETag": etag, "Cache-Control": CACHE_CONTROL_LECTURAS, "Vary": "Cookie, Accept-Encoding"}
        if _coincide(request.headers.get("if-none-match"), etag):
            return Response(status_code=304, headers=cabeceras)
        encabezados = {
            k: v for k, v in respuesta.headers.items() if k.lower() not in {"content-length", "vary"}
        }
        encabezados.update(cabeceras)
        return Response(content=cuerpo, status_code=200, headers=encabezados, media_type=None)
