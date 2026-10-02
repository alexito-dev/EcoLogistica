"""Primitivas criptográficas: hash Argon2id, TOTP (RFC 6238) y tokens firmados."""

import hmac
from datetime import datetime
from functools import lru_cache
from typing import Any

import jwt
import pyotp
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

_hasher = PasswordHasher()  # Argon2id con los parámetros recomendados por la librería
_ALGORITMO = "HS256"
_PASO_TOTP = 30
EMISOR_TOTP = "EcoLogística Huancayo"


# --- Contraseñas -----------------------------------------------------------

def hash_clave(clave: str) -> str:
    return _hasher.hash(clave)


def verificar_clave(clave_hash: str, clave: str) -> bool:
    try:
        return _hasher.verify(clave_hash, clave)
    except (VerificationError, InvalidHashError):
        return False


@lru_cache
def hash_ficticio() -> str:
    """Hash para verificar cuando el correo no existe e igualar los tiempos de respuesta."""
    return _hasher.hash("clave-ficticia-para-igualar-tiempos")


# --- TOTP ------------------------------------------------------------------

def nuevo_secreto_totp() -> str:
    return pyotp.random_base32()


def uri_aprovisionamiento(secreto: str, correo: str) -> str:
    return pyotp.TOTP(secreto).provisioning_uri(name=correo, issuer_name=EMISOR_TOTP)


def verificar_codigo_totp(secreto: str, codigo: str, ultimo_paso: int, ahora: datetime) -> int | None:
    """Devuelve el paso de tiempo del código si es válido (±1 paso) y posterior al último usado."""
    if len(codigo) != 6 or not codigo.isdigit():
        return None
    totp = pyotp.TOTP(secreto)
    paso_actual = int(ahora.timestamp()) // _PASO_TOTP
    for desfase in (0, -1, 1):
        paso = paso_actual + desfase
        if paso > ultimo_paso and hmac.compare_digest(totp.at(paso * _PASO_TOTP), codigo):
            return paso
    return None


# --- Tokens ----------------------------------------------------------------

def emitir_token(clave: str, datos: dict[str, Any]) -> str:
    return jwt.encode(datos, clave, algorithm=_ALGORITMO)


def leer_token(clave: str, token: str | None, proposito: str) -> dict[str, Any] | None:
    """Valida firma y propósito. La expiración la comprueba el servicio con su reloj."""
    if not token:
        return None
    try:
        datos = jwt.decode(
            token,
            clave,
            algorithms=[_ALGORITMO],
            options={"verify_exp": False, "require": ["sub", "prp", "ver", "exp"]},
        )
    except jwt.PyJWTError:
        return None
    return datos if datos.get("prp") == proposito else None
