"""Rutas de autenticación: contraseña, segundo factor, sesión y cierre de sesión."""

from typing import Annotated

from fastapi import APIRouter, Cookie, Response, status
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from app.auth.dependencias import (
    COOKIE_MFA,
    COOKIE_SESION,
    RUTA_COOKIE_MFA,
    RUTA_COOKIE_SESION,
    ServicioAuthDep,
    UsuarioActual,
    poner_cookie_sesion,
)
from app.auth.domain import VIGENCIA_COMPROBANTE_MFA, PasoAcceso, Rol, Usuario
from app.config import get_settings
from app.pedidos.schemas import ErrorOut

router = APIRouter(prefix="/auth", tags=["Autenticación"])


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="forbid")


class LoginIn(_Base):
    correo: str = Field(min_length=3, max_length=254)
    clave: str = Field(min_length=1, max_length=256)


class LoginOut(_Base):
    paso: PasoAcceso
    clave_mfa: str | None = Field(default=None, description="Clave Base32 para ingreso manual (solo al enrolar)")
    otpauth_uri: str | None = Field(default=None, description="URI para el código QR (solo al enrolar)")


class MfaIn(_Base):
    codigo: str = Field(pattern=r"^\d{6}$", description="Código de 6 dígitos de la app autenticadora")


class UsuarioOut(_Base):
    nombre: str
    correo: str
    rol: Rol

    @classmethod
    def desde_dominio(cls, u: Usuario) -> "UsuarioOut":
        return cls(nombre=u.nombre, correo=u.correo, rol=u.rol)


def _errores(*codigos: int) -> dict:
    return {c: {"model": ErrorOut} for c in codigos}


@router.post("/login", response_model=LoginOut, summary="Paso 1: correo y contraseña", responses=_errores(400, 401, 429))
def login(datos: LoginIn, response: Response, servicio: ServicioAuthDep) -> LoginOut:
    resultado = servicio.iniciar(datos.correo, datos.clave)
    response.set_cookie(
        COOKIE_MFA,
        resultado.comprobante,
        max_age=int(VIGENCIA_COMPROBANTE_MFA.total_seconds()),
        path=RUTA_COOKIE_MFA,
        httponly=True,
        samesite="strict",
        secure=get_settings().cookie_secure,
    )
    return LoginOut(paso=resultado.paso, clave_mfa=resultado.secreto, otpauth_uri=resultado.uri)


@router.post("/mfa", response_model=UsuarioOut, summary="Paso 2: código TOTP", responses=_errores(400, 401))
def verificar_mfa(
    datos: MfaIn,
    response: Response,
    servicio: ServicioAuthDep,
    eco_mfa: Annotated[str | None, Cookie()] = None,
) -> UsuarioOut:
    sesion = servicio.verificar_mfa(eco_mfa, datos.codigo)
    response.delete_cookie(COOKIE_MFA, path=RUTA_COOKIE_MFA)
    poner_cookie_sesion(response, sesion.token)
    return UsuarioOut.desde_dominio(sesion.usuario)


@router.get("/sesion", response_model=UsuarioOut, summary="Sesión actual", responses=_errores(401))
def sesion_actual(usuario: UsuarioActual) -> UsuarioOut:
    return UsuarioOut.desde_dominio(usuario)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, summary="Cerrar sesión", responses=_errores(401))
def logout(usuario: UsuarioActual, servicio: ServicioAuthDep) -> Response:
    servicio.cerrar_sesion(usuario)
    respuesta = Response(status_code=status.HTTP_204_NO_CONTENT)
    respuesta.delete_cookie(COOKIE_SESION, path=RUTA_COOKIE_SESION)
    return respuesta
