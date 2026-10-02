"""Dominio de autenticación: usuarios, roles, reglas y errores (RF-11.1, RNF-05, RNF-07)."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

MAX_INTENTOS = 5
VENTANA_INTENTOS = timedelta(minutes=15)
DURACION_BLOQUEO = timedelta(minutes=15)
INACTIVIDAD_SESION = timedelta(minutes=15)
DURACION_MAXIMA_SESION = timedelta(hours=8)
VIGENCIA_COMPROBANTE_MFA = timedelta(minutes=5)
MAX_CODIGOS_FALLIDOS = 5


class Rol(str, Enum):
    """Roles del documento 08 (matriz RBAC)."""

    ADMIN = "ADMIN"
    PLANIFICADOR = "PLANIFICADOR"
    CONDUCTOR = "CONDUCTOR"
    GERENTE = "GERENTE"
    AUDITOR = "AUDITOR"


class EstadoUsuario(str, Enum):
    """Dominio `estado_usuario` del modelo físico (documento 11)."""

    ACTIVO = "ACTIVO"
    BLOQUEADO = "BLOQUEADO"
    INACTIVO = "INACTIVO"


class PasoAcceso(str, Enum):
    MFA = "MFA"
    ENROLAR = "ENROLAR"


@dataclass
class Usuario:
    id: str
    correo: str
    nombre: str
    rol: Rol
    clave_hash: str
    estado: EstadoUsuario = EstadoUsuario.ACTIVO
    mfa_secreto: str | None = None
    mfa_pendiente: str | None = None
    mfa_ultimo_paso: int = 0
    mfa_fallidos: int = 0
    version_sesion: int = 1

    @staticmethod
    def normalizar_correo(correo: str) -> str:
        return correo.strip().lower()


@dataclass
class RegistroIntentos:
    """Fallos recientes de contraseña para un correo (exista o no la cuenta)."""

    fallos: list[datetime] = field(default_factory=list)
    bloqueado_hasta: datetime | None = None

    def bloqueado(self, ahora: datetime) -> bool:
        return self.bloqueado_hasta is not None and ahora < self.bloqueado_hasta

    def registrar_fallo(self, ahora: datetime) -> bool:
        """Registra un fallo; devuelve True si con él se activa el bloqueo."""
        self.fallos = [f for f in self.fallos if ahora - f < VENTANA_INTENTOS] + [ahora]
        if len(self.fallos) >= MAX_INTENTOS:
            self.bloqueado_hasta = ahora + DURACION_BLOQUEO
            self.fallos = []
            return True
        return False


class CredencialesInvalidasError(Exception):
    """Correo inexistente, contraseña incorrecta o usuario no activo (mismo mensaje)."""


class CuentaBloqueadaError(Exception):
    """Demasiados intentos fallidos (HTTP 429)."""


class CodigoInvalidoError(Exception):
    """Código TOTP incorrecto o repetido (HTTP 401, campo `codigo`)."""


class ComprobanteInvalidoError(Exception):
    """Comprobante del paso MFA vencido, alterado o agotado (HTTP 401)."""


class NoAutenticadoError(Exception):
    """Sin sesión válida (HTTP 401)."""


class AccesoDenegadoError(Exception):
    """El rol no tiene permiso para la acción (HTTP 403)."""
