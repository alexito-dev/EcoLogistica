"""Usuarios de demostración (uno por rol) para desarrollo, sin contraseñas en el repositorio."""

import secrets
import uuid

from app.auth.domain import Rol, Usuario
from app.auth.repository import UsuariosRepository
from app.auth.seguridad import hash_clave

DOMINIO_DEMO = "ecologistica.test"

USUARIOS_DEMO = [
    ("admin", "Administración", Rol.ADMIN),
    ("planificador", "Planificación", Rol.PLANIFICADOR),
    ("conductor", "Conductor de ruta", Rol.CONDUCTOR),
    ("gerente", "Gerencia", Rol.GERENTE),
    ("auditor", "Auditoría", Rol.AUDITOR),
]


def sembrar_usuarios_demo(repositorio: UsuariosRepository, clave_demo: str | None) -> str | None:
    """Crea los usuarios de demostración si el almacén está vacío.

    Devuelve la contraseña generada cuando `clave_demo` no se configuró (para mostrarla una sola vez),
    o None si no se creó nada o se usó la configurada.
    """
    if repositorio.contar() > 0:
        return None
    generada = None if clave_demo else secrets.token_urlsafe(12)
    clave = clave_demo or generada
    for usuario, nombre, rol in USUARIOS_DEMO:
        repositorio.guardar(
            Usuario(
                id=str(uuid.uuid4()),
                correo=f"{usuario}@{DOMINIO_DEMO}",
                nombre=nombre,
                rol=rol,
                clave_hash=hash_clave(clave),
            )
        )
    return generada
