"""Puerto de persistencia de usuarios (el adaptador PostgreSQL llegará con EN-005)."""

from typing import Protocol

from app.auth.domain import RegistroIntentos, Usuario


class UsuariosRepository(Protocol):
    def obtener(self, usuario_id: str) -> Usuario | None: ...

    def obtener_por_correo(self, correo: str) -> Usuario | None:
        """Busca por correo ya normalizado."""

    def guardar(self, usuario: Usuario) -> None: ...

    def contar(self) -> int: ...

    def intentos(self, correo: str) -> RegistroIntentos: ...

    def guardar_intentos(self, correo: str, registro: RegistroIntentos) -> None: ...

    def limpiar_intentos(self, correo: str) -> None: ...
