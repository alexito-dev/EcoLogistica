"""Casos de uso de autenticación: contraseña + TOTP, sesión deslizante y cierre de sesión."""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone

from app.auth import seguridad
from app.auth.auditoria import registrar_evento
from app.auth.domain import (
    DURACION_MAXIMA_SESION,
    INACTIVIDAD_SESION,
    MAX_CODIGOS_FALLIDOS,
    VIGENCIA_COMPROBANTE_MFA,
    CodigoInvalidoError,
    ComprobanteInvalidoError,
    CredencialesInvalidasError,
    CuentaBloqueadaError,
    EstadoUsuario,
    NoAutenticadoError,
    PasoAcceso,
    Usuario,
)
from app.auth.repository import UsuariosRepository


def _ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class ResultadoLogin:
    paso: PasoAcceso
    comprobante: str
    secreto: str | None = None
    uri: str | None = None


@dataclass(frozen=True)
class SesionValida:
    usuario: Usuario
    token: str  # token renovado (inactividad deslizante)


class AutenticacionService:
    def __init__(
        self,
        repositorio: UsuariosRepository,
        clave_firma: str,
        reloj: Callable[[], datetime] = _ahora_utc,
    ) -> None:
        self._repo = repositorio
        self._clave = clave_firma
        self._reloj = reloj

    # --- Paso 1: contraseña ------------------------------------------------

    def iniciar(self, correo: str, clave: str) -> ResultadoLogin:
        ahora = self._reloj()
        correo = Usuario.normalizar_correo(correo)
        intentos = self._repo.intentos(correo)
        if intentos.bloqueado(ahora):
            registrar_evento("BLOQUEO", correo, "rechazado: cuenta bloqueada temporalmente")
            raise CuentaBloqueadaError()

        usuario = self._repo.obtener_por_correo(correo)
        # Se verifica siempre un hash (real o ficticio) para no revelar si el correo existe.
        clave_correcta = seguridad.verificar_clave(usuario.clave_hash if usuario else seguridad.hash_ficticio(), clave)
        if not (usuario and clave_correcta and usuario.estado == EstadoUsuario.ACTIVO):
            bloqueo = intentos.registrar_fallo(ahora)
            self._repo.guardar_intentos(correo, intentos)
            registrar_evento("LOGIN_FALLIDO", correo, "credenciales inválidas")
            if bloqueo:
                registrar_evento("BLOQUEO", correo, "5 intentos fallidos: bloqueo de 15 minutos")
            raise CredencialesInvalidasError()

        self._repo.limpiar_intentos(correo)
        usuario.mfa_fallidos = 0
        if usuario.mfa_secreto:
            paso = PasoAcceso.MFA
            secreto = uri = None
        else:
            paso = PasoAcceso.ENROLAR
            usuario.mfa_pendiente = seguridad.nuevo_secreto_totp()
            secreto = usuario.mfa_pendiente
            uri = seguridad.uri_aprovisionamiento(secreto, usuario.correo)
        self._repo.guardar(usuario)

        comprobante = seguridad.emitir_token(
            self._clave,
            {
                "sub": usuario.id,
                "prp": "mfa",
                "ver": usuario.version_sesion,
                "exp": int((ahora + VIGENCIA_COMPROBANTE_MFA).timestamp()),
            },
        )
        return ResultadoLogin(paso=paso, comprobante=comprobante, secreto=secreto, uri=uri)

    # --- Paso 2: segundo factor ---------------------------------------------

    def verificar_mfa(self, comprobante: str | None, codigo: str) -> SesionValida:
        ahora = self._reloj()
        datos = seguridad.leer_token(self._clave, comprobante, "mfa")
        if not datos or datos["exp"] <= ahora.timestamp():
            raise ComprobanteInvalidoError()
        usuario = self._repo.obtener(datos["sub"])
        if not usuario or usuario.estado != EstadoUsuario.ACTIVO or datos["ver"] != usuario.version_sesion:
            raise ComprobanteInvalidoError()

        enrolando = usuario.mfa_secreto is None
        secreto = usuario.mfa_pendiente if enrolando else usuario.mfa_secreto
        if not secreto:
            raise ComprobanteInvalidoError()

        paso = seguridad.verificar_codigo_totp(secreto, codigo, usuario.mfa_ultimo_paso, ahora)
        if paso is None:
            usuario.mfa_fallidos += 1
            if usuario.mfa_fallidos >= MAX_CODIGOS_FALLIDOS:
                usuario.mfa_fallidos = 0
                usuario.version_sesion += 1  # invalida el comprobante: hay que volver a la contraseña
            self._repo.guardar(usuario)
            registrar_evento("MFA_FALLIDO", usuario.correo, "código incorrecto o repetido")
            raise CodigoInvalidoError()

        usuario.mfa_ultimo_paso = paso
        usuario.mfa_fallidos = 0
        if enrolando:
            usuario.mfa_secreto = usuario.mfa_pendiente
            usuario.mfa_pendiente = None
            registrar_evento("MFA_ENROLADO", usuario.correo, "segundo factor activado")
        self._repo.guardar(usuario)
        registrar_evento("LOGIN_OK", usuario.correo, "acceso concedido")
        return SesionValida(usuario, self._token_sesion(usuario, inicio=ahora, ahora=ahora))

    # --- Sesión ---------------------------------------------------------------

    def _token_sesion(self, usuario: Usuario, inicio: datetime, ahora: datetime) -> str:
        expira = min(ahora + INACTIVIDAD_SESION, inicio + DURACION_MAXIMA_SESION)
        return seguridad.emitir_token(
            self._clave,
            {
                "sub": usuario.id,
                "prp": "sesion",
                "ver": usuario.version_sesion,
                "auth": int(inicio.timestamp()),
                "exp": int(expira.timestamp()),
            },
        )

    def validar_sesion(self, token: str | None) -> SesionValida:
        ahora = self._reloj()
        datos = seguridad.leer_token(self._clave, token, "sesion")
        if not datos or "auth" not in datos or datos["exp"] <= ahora.timestamp():
            raise NoAutenticadoError()
        inicio = datetime.fromtimestamp(datos["auth"], timezone.utc)
        if ahora - inicio >= DURACION_MAXIMA_SESION:
            raise NoAutenticadoError()
        usuario = self._repo.obtener(datos["sub"])
        # El estado y la versión se leen del registro en cada solicitud (RF-11.1, ABAC-01).
        if not usuario or usuario.estado != EstadoUsuario.ACTIVO or datos["ver"] != usuario.version_sesion:
            raise NoAutenticadoError()
        return SesionValida(usuario, self._token_sesion(usuario, inicio=inicio, ahora=ahora))

    def cerrar_sesion(self, usuario: Usuario) -> None:
        usuario.version_sesion += 1  # todos los tokens emitidos antes dejan de valer
        self._repo.guardar(usuario)
        registrar_evento("LOGOUT", usuario.correo, "sesión cerrada")
