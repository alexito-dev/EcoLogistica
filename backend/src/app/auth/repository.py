"""Puerto de persistencia de usuarios (adaptadores: archivo local para pruebas y PostgreSQL con secretos TOTP cifrados)."""

from typing import Protocol

from app.auth.domain import RegistroIntentos, Rol, Usuario


class UsuariosRepository(Protocol):
    def obtener(self, usuario_id: str) -> Usuario | None: ...

    def obtener_por_correo(self, correo: str) -> Usuario | None:
        """Busca por correo ya normalizado."""

    def listar_por_rol(self, rol: Rol) -> list[Usuario]:
        """Usuarios activos de un rol, por nombre."""

    def guardar(self, usuario: Usuario) -> None: ...

    def contar(self) -> int: ...

    def intentos(self, correo: str) -> RegistroIntentos: ...

    def guardar_intentos(self, correo: str, registro: RegistroIntentos) -> None: ...

    def limpiar_intentos(self, correo: str) -> None: ...
