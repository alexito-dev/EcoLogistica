"""Dependencias de FastAPI: servicio de autenticación, usuario actual y autorización por rol."""

from collections.abc import Callable
from functools import lru_cache
from typing import Annotated

from fastapi import Cookie, Depends, Response

from app.auth.archivo_repository import UsuariosArchivoRepository
from app.auth.auditoria import registrar_evento
from app.auth.domain import DURACION_MAXIMA_SESION, AccesoDenegadoError, Rol, Usuario
from app.auth.repository import UsuariosRepository
from app.auth.service import AutenticacionService
from app.auth.siembra import DOMINIO_DEMO, sembrar_usuarios_demo
from app.config import get_settings

COOKIE_SESION = "eco_sesion"
COOKIE_MFA = "eco_mfa"
RUTA_COOKIE_SESION = "/api"
RUTA_COOKIE_MFA = "/api/v1/auth"


@lru_cache
def get_repositorio_usuarios() -> UsuariosRepository:
    settings = get_settings()
    repositorio = UsuariosArchivoRepository(settings.usuarios_archivo)
    generada = sembrar_usuarios_demo(repositorio, settings.demo_clave or None)
    if generada:
        # Solo en desarrollo y una única vez: la contraseña no se guarda en ningún archivo del repositorio.
        print(
            "\n" + "=" * 72
            + f"\n Usuarios de demostración creados (admin, planificador, conductor, gerente, auditor @{DOMINIO_DEMO})"
            + f"\n Contraseña de demostración: {generada}"
            + "\n Guárdela ahora: no se volverá a mostrar. Configure DEMO_CLAVE en .env para fijarla."
            + "\n" + "=" * 72 + "\n",
            flush=True,
        )
    return repositorio


def get_servicio_auth(
    repositorio: Annotated[UsuariosRepository, Depends(get_repositorio_usuarios)],
) -> AutenticacionService:
    return AutenticacionService(repositorio, get_settings().jwt_secret)


ServicioAuthDep = Annotated[AutenticacionService, Depends(get_servicio_auth)]


def poner_cookie_sesion(response: Response, token: str) -> None:
    response.set_cookie(
        COOKIE_SESION,
        token,
        max_age=int(DURACION_MAXIMA_SESION.total_seconds()),
        path=RUTA_COOKIE_SESION,
        httponly=True,
        samesite="strict",
        secure=get_settings().cookie_secure,
    )


def usuario_actual(
    response: Response,
    servicio: ServicioAuthDep,
    eco_sesion: Annotated[str | None, Cookie()] = None,
) -> Usuario:
    """Valida la sesión, renueva el plazo de inactividad y devuelve el usuario (401 si no hay sesión)."""
    sesion = servicio.validar_sesion(eco_sesion)
    poner_cookie_sesion(response, sesion.token)
    return sesion.usuario


UsuarioActual = Annotated[Usuario, Depends(usuario_actual)]


def requerir_rol(*roles: Rol) -> Callable[[Usuario], Usuario]:
    """Dependencia que exige uno de los roles indicados (403 si no lo tiene; deniega por defecto)."""
    permitidos = frozenset(roles)

    def _verificar(usuario: UsuarioActual) -> Usuario:
        if usuario.rol not in permitidos:
            registrar_evento("ACCESO_DENEGADO", usuario.correo, f"rol {usuario.rol.value} sin permiso")
            raise AccesoDenegadoError()
        return usuario

    return _verificar
