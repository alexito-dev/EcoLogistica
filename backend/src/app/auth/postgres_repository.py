"""Adaptador PostgreSQL de usuarios e intentos de acceso (ECO-21). Los secretos TOTP se guardan cifrados."""

from collections.abc import Mapping
from datetime import datetime
from uuid import UUID

from sqlalchemy import Engine, text

from app.auth.cifrado import CifradorSecretos
from app.auth.domain import EstadoUsuario, RegistroIntentos, Rol, Usuario

_COLUMNAS = (
    "id, correo, nombre, rol, clave_hash, estado, mfa_secreto_cifrado, mfa_pendiente_cifrado, "
    "mfa_ultimo_paso, mfa_fallidos, version_sesion"
)


class UsuariosPostgresRepository:
    def __init__(self, engine: Engine, cifrador: CifradorSecretos) -> None:
        self._engine = engine
        self._cifrador = cifrador

    def _desde_fila(self, fila: Mapping[str, object]) -> Usuario:
        return Usuario(
            id=str(fila["id"]),
            correo=fila["correo"],  # type: ignore[arg-type]
            nombre=fila["nombre"],  # type: ignore[arg-type]
            rol=Rol(fila["rol"]),  # type: ignore[arg-type]
            clave_hash=fila["clave_hash"],  # type: ignore[arg-type]
            estado=EstadoUsuario(fila["estado"]),  # type: ignore[arg-type]
            mfa_secreto=self._cifrador.descifrar(fila["mfa_secreto_cifrado"]),  # type: ignore[arg-type]
            mfa_pendiente=self._cifrador.descifrar(fila["mfa_pendiente_cifrado"]),  # type: ignore[arg-type]
            mfa_ultimo_paso=int(fila["mfa_ultimo_paso"]),  # type: ignore[arg-type]
            mfa_fallidos=int(fila["mfa_fallidos"]),  # type: ignore[arg-type]
            version_sesion=int(fila["version_sesion"]),  # type: ignore[arg-type]
        )

    def obtener(self, usuario_id: str) -> Usuario | None:
        try:
            uuid = UUID(usuario_id)
        except ValueError:
            return None
        with self._engine.connect() as conexion:
            fila = (
                conexion.execute(text(f"SELECT {_COLUMNAS} FROM usuarios WHERE id = :id"), {"id": uuid})
                .mappings()
                .one_or_none()
            )
        return self._desde_fila(fila) if fila else None

    def obtener_por_correo(self, correo: str) -> Usuario | None:
        with self._engine.connect() as conexion:
            fila = (
                conexion.execute(text(f"SELECT {_COLUMNAS} FROM usuarios WHERE correo = :correo"), {"correo": correo})
                .mappings()
                .one_or_none()
            )
        return self._desde_fila(fila) if fila else None

    def listar_por_rol(self, rol: Rol) -> list[Usuario]:
        with self._engine.connect() as conexion:
            filas = (
                conexion.execute(
                    text(f"SELECT {_COLUMNAS} FROM usuarios WHERE rol = :rol AND estado = 'ACTIVO' ORDER BY nombre"),
                    {"rol": rol.value},
                )
                .mappings()
                .all()
            )
        return [self._desde_fila(f) for f in filas]

    def guardar(self, usuario: Usuario) -> None:
        with self._engine.begin() as conexion:
            conexion.execute(
                text("""
                    INSERT INTO usuarios (id, correo, nombre, rol, clave_hash, estado, mfa_secreto_cifrado,
                        mfa_pendiente_cifrado, mfa_ultimo_paso, mfa_fallidos, version_sesion)
                    VALUES (:id, :correo, :nombre, :rol, :clave_hash, CAST(:estado AS estado_usuario), :secreto,
                        :pendiente, :ultimo_paso, :fallidos, :version)
                    ON CONFLICT (id) DO UPDATE SET
                        correo = EXCLUDED.correo, nombre = EXCLUDED.nombre, rol = EXCLUDED.rol,
                        clave_hash = EXCLUDED.clave_hash, estado = EXCLUDED.estado,
                        mfa_secreto_cifrado = EXCLUDED.mfa_secreto_cifrado,
                        mfa_pendiente_cifrado = EXCLUDED.mfa_pendiente_cifrado,
                        mfa_ultimo_paso = EXCLUDED.mfa_ultimo_paso, mfa_fallidos = EXCLUDED.mfa_fallidos,
                        version_sesion = EXCLUDED.version_sesion, actualizado_en = now()
                """),
                {
                    "id": UUID(usuario.id),
                    "correo": usuario.correo,
                    "nombre": usuario.nombre,
                    "rol": usuario.rol.value,
                    "clave_hash": usuario.clave_hash,
                    "estado": usuario.estado.value,
                    "secreto": self._cifrador.cifrar(usuario.mfa_secreto),
                    "pendiente": self._cifrador.cifrar(usuario.mfa_pendiente),
                    "ultimo_paso": usuario.mfa_ultimo_paso,
                    "fallidos": usuario.mfa_fallidos,
                    "version": usuario.version_sesion,
                },
            )

    def contar(self) -> int:
        with self._engine.connect() as conexion:
            return int(conexion.execute(text("SELECT count(*) FROM usuarios")).scalar_one())

    def intentos(self, correo: str) -> RegistroIntentos:
        with self._engine.connect() as conexion:
            fila = conexion.execute(
                text("SELECT fallos, bloqueado_hasta FROM intentos_acceso WHERE correo = :correo"),
                {"correo": correo},
            ).one_or_none()
        if fila is None:
            return RegistroIntentos()
        fallos: list[datetime] = list(fila[0] or [])
        return RegistroIntentos(fallos=fallos, bloqueado_hasta=fila[1])

    def guardar_intentos(self, correo: str, registro: RegistroIntentos) -> None:
        with self._engine.begin() as conexion:
            conexion.execute(
                text("""
                    INSERT INTO intentos_acceso (correo, fallos, bloqueado_hasta)
                    VALUES (:correo, :fallos, :bloqueado)
                    ON CONFLICT (correo) DO UPDATE SET fallos = EXCLUDED.fallos,
                        bloqueado_hasta = EXCLUDED.bloqueado_hasta
                """),
                {"correo": correo, "fallos": registro.fallos, "bloqueado": registro.bloqueado_hasta},
            )

    def limpiar_intentos(self, correo: str) -> None:
        with self._engine.begin() as conexion:
            conexion.execute(text("DELETE FROM intentos_acceso WHERE correo = :correo"), {"correo": correo})
