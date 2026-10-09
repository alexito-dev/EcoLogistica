"""Manejo uniforme de errores: { status, message, errors } sin trazas internas (RNF-07)."""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.auth.domain import (
    AccesoDenegadoError,
    CodigoInvalidoError,
    ComprobanteInvalidoError,
    CredencialesInvalidasError,
    CuentaBloqueadaError,
    NoAutenticadoError,
)
from app.flota.domain import PlacaDuplicadaError, ReglaFlotaError, VehiculoNoEncontradoError
from app.pedidos.domain import CodigoDuplicadoError, PedidoNoEncontradoError, ReglaDominioError

logger = logging.getLogger("ecologistica")


def _respuesta(status: int, message: str, errors: dict[str, str] | None = None) -> JSONResponse:
    cuerpo: dict = {"status": status, "message": message}
    if errors:
        cuerpo["errors"] = errors
    return JSONResponse(status_code=status, content=cuerpo)


def _mensaje_validacion(error: dict) -> str:
    tipo = error.get("type", "")
    ctx = error.get("ctx") or {}
    if tipo == "missing":
        return "Campo obligatorio"
    if tipo == "extra_forbidden":
        return "Campo no permitido"
    comparaciones = {
        "greater_than_equal": ("mayor o igual que", "ge"),
        "less_than_equal": ("menor o igual que", "le"),
        "greater_than": ("mayor que", "gt"),
        "less_than": ("menor que", "lt"),
    }
    if tipo in comparaciones:
        texto, clave = comparaciones[tipo]
        return f"Debe ser {texto} {ctx.get(clave, '')}".strip()
    if tipo == "timezone_aware":
        return "Debe incluir zona horaria (ISO 8601 con desfase, por ejemplo -05:00)"
    if tipo.startswith("datetime"):
        return "Fecha y hora inválidas (use ISO 8601 con desfase, por ejemplo 2026-10-05T08:00:00-05:00)"
    if tipo.startswith("uuid"):
        return "Debe ser un UUID válido"
    if tipo in ("string_too_short", "string_too_long"):
        return "Longitud fuera del rango permitido"
    if tipo in ("enum", "literal_error"):
        return "Valor no permitido"
    if tipo == "json_invalid":
        return "El cuerpo no es un JSON válido"
    return "Valor inválido"


def registrar_manejadores(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def _validacion(_: Request, exc: RequestValidationError) -> JSONResponse:
        errores: dict[str, str] = {}
        for error in exc.errors():
            ruta = [str(p) for p in error["loc"] if p not in ("body", "query", "path")]
            campo = ".".join(ruta) or "body"
            errores.setdefault(campo, _mensaje_validacion(error))
        return _respuesta(400, "Datos inválidos", errores)

    @app.exception_handler(ReglaDominioError)
    async def _regla(_: Request, exc: ReglaDominioError) -> JSONResponse:
        return _respuesta(422, "No se cumple una regla de negocio", exc.errors)

    @app.exception_handler(CodigoDuplicadoError)
    async def _duplicado(_: Request, exc: CodigoDuplicadoError) -> JSONResponse:
        return _respuesta(409, str(exc), {"codigo": "Ya existe un pedido con este código"})

    @app.exception_handler(PedidoNoEncontradoError)
    async def _no_encontrado(_: Request, __: PedidoNoEncontradoError) -> JSONResponse:
        return _respuesta(404, "Pedido no encontrado")

    @app.exception_handler(VehiculoNoEncontradoError)
    async def _vehiculo_no_encontrado(_: Request, __: VehiculoNoEncontradoError) -> JSONResponse:
        return _respuesta(404, "Vehículo no encontrado")

    @app.exception_handler(ReglaFlotaError)
    async def _regla_flota(_: Request, exc: ReglaFlotaError) -> JSONResponse:
        return _respuesta(422, "No se cumple una regla de flota", exc.errors)

    @app.exception_handler(PlacaDuplicadaError)
    async def _placa_duplicada(_: Request, __: PlacaDuplicadaError) -> JSONResponse:
        return _respuesta(409, "Ya existe un vehículo con esta placa", {"placa": "La placa debe ser única"})

    @app.exception_handler(CredencialesInvalidasError)
    async def _credenciales(_: Request, __: CredencialesInvalidasError) -> JSONResponse:
        return _respuesta(401, "Correo o contraseña incorrectos")

    @app.exception_handler(CuentaBloqueadaError)
    async def _bloqueada(_: Request, __: CuentaBloqueadaError) -> JSONResponse:
        return _respuesta(429, "Demasiados intentos fallidos. Intente nuevamente en 15 minutos.")

    @app.exception_handler(CodigoInvalidoError)
    async def _codigo(_: Request, __: CodigoInvalidoError) -> JSONResponse:
        return _respuesta(401, "Código incorrecto", {"codigo": "El código no es válido o ya fue usado"})

    @app.exception_handler(ComprobanteInvalidoError)
    async def _comprobante(_: Request, __: ComprobanteInvalidoError) -> JSONResponse:
        return _respuesta(401, "El paso de verificación venció. Inicie sesión nuevamente.")

    @app.exception_handler(NoAutenticadoError)
    async def _no_autenticado(_: Request, __: NoAutenticadoError) -> JSONResponse:
        return _respuesta(401, "Sesión no válida o vencida. Inicie sesión.")

    @app.exception_handler(AccesoDenegadoError)
    async def _denegado(_: Request, __: AccesoDenegadoError) -> JSONResponse:
        return _respuesta(403, "No tiene permiso para realizar esta acción")

    @app.exception_handler(StarletteHTTPException)
    async def _http(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        mensaje = "Recurso no encontrado" if exc.status_code == 404 else "Solicitud no válida"
        return _respuesta(exc.status_code, mensaje)

    @app.exception_handler(Exception)
    async def _inesperado(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Error no controlado", exc_info=exc)
        return _respuesta(500, "Error interno del servidor")
