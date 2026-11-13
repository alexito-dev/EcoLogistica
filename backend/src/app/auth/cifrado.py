"""Cifrado en reposo de los secretos TOTP (ECO-21, OWASP A02:2025).

Usa Fernet (AES-128-CBC + HMAC-SHA256) con una clave propia, distinta de la clave de firma de las sesiones.
Un secreto TOTP en base de datos solo es util con la clave: una copia filtrada de la tabla no permite
generar codigos de acceso.
"""

from cryptography.fernet import Fernet, InvalidToken


class ClaveDeCifradoInvalidaError(RuntimeError):
    """La clave configurada no es una clave Fernet valida o no corresponde a los datos guardados."""


class CifradorSecretos:
    def __init__(self, clave: str) -> None:
        if not clave:
            raise ClaveDeCifradoInvalidaError(
                "Defina TOTP_CLAVE_CIFRADO. Genere una con: "
                'python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"'
            )
        try:
            self._fernet = Fernet(clave.encode())
        except (ValueError, TypeError) as error:
            raise ClaveDeCifradoInvalidaError("TOTP_CLAVE_CIFRADO no es una clave Fernet valida") from error

    def cifrar(self, texto: str | None) -> str | None:
        return None if texto is None else self._fernet.encrypt(texto.encode()).decode()

    def descifrar(self, token: str | None) -> str | None:
        if token is None:
            return None
        try:
            return self._fernet.decrypt(token.encode()).decode()
        except InvalidToken as error:
            raise ClaveDeCifradoInvalidaError(
                "No se pudo descifrar un secreto TOTP: la clave TOTP_CLAVE_CIFRADO cambio o los datos se alteraron"
            ) from error
