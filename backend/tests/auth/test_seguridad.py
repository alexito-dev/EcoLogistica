from datetime import datetime, timedelta, timezone

import pyotp

from app.auth import seguridad

CLAVE = "clave-de-pruebas-suficientemente-larga-0123456789"
AHORA = datetime(2026, 10, 5, 13, 0, tzinfo=timezone.utc)


def test_hash_argon2id_y_verificacion():
    h = seguridad.hash_clave("secreta-123")
    assert h.startswith("$argon2id$")
    assert "secreta-123" not in h
    assert seguridad.verificar_clave(h, "secreta-123")
    assert not seguridad.verificar_clave(h, "otra")
    assert not seguridad.verificar_clave("no-es-un-hash", "secreta-123")


def test_codigo_totp_correcto_y_con_desfase_de_un_paso():
    secreto = seguridad.nuevo_secreto_totp()
    totp = pyotp.TOTP(secreto)
    assert seguridad.verificar_codigo_totp(secreto, totp.at(AHORA), 0, AHORA)
    anterior = totp.at(AHORA - timedelta(seconds=30))
    assert seguridad.verificar_codigo_totp(secreto, anterior, 0, AHORA)


def test_codigo_totp_fuera_de_ventana_o_mal_formado():
    secreto = seguridad.nuevo_secreto_totp()
    totp = pyotp.TOTP(secreto)
    assert seguridad.verificar_codigo_totp(secreto, totp.at(AHORA - timedelta(minutes=2)), 0, AHORA) is None
    assert seguridad.verificar_codigo_totp(secreto, "12345", 0, AHORA) is None
    assert seguridad.verificar_codigo_totp(secreto, "abcdef", 0, AHORA) is None


def test_codigo_totp_no_se_puede_repetir():
    secreto = seguridad.nuevo_secreto_totp()
    codigo = pyotp.TOTP(secreto).at(AHORA)
    paso = seguridad.verificar_codigo_totp(secreto, codigo, 0, AHORA)
    assert paso
    assert seguridad.verificar_codigo_totp(secreto, codigo, paso, AHORA) is None


def test_uri_de_aprovisionamiento():
    uri = seguridad.uri_aprovisionamiento("JBSWY3DPEHPK3PXP", "planificador@ecologistica.test")
    assert uri.startswith("otpauth://totp/")
    assert "issuer=EcoLog" in uri


def test_token_valido_alterado_o_de_otro_proposito():
    datos = {"sub": "1", "prp": "sesion", "ver": 1, "exp": 9999999999}
    token = seguridad.emitir_token(CLAVE, datos)
    assert seguridad.leer_token(CLAVE, token, "sesion")["sub"] == "1"
    assert seguridad.leer_token(CLAVE, token, "mfa") is None
    assert seguridad.leer_token("otra-clave-de-firma-suficientemente-larga-xx", token, "sesion") is None
    assert seguridad.leer_token(CLAVE, token[:-2] + "xx", "sesion") is None
    assert seguridad.leer_token(CLAVE, None, "sesion") is None
