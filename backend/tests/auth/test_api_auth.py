"""Escenarios de openspec/changes/autenticacion-mfa/specs/autenticacion/spec.md (API)."""

import pyotp

from app.auth.domain import Rol
from tests.conftest import CLAVE_DEMO

LOGIN = "/api/v1/auth/login"
MFA = "/api/v1/auth/mfa"
SESION = "/api/v1/auth/sesion"
LOGOUT = "/api/v1/auth/logout"
PEDIDOS = "/api/v1/pedidos"
CORREO = "planificador@ecologistica.test"


def _acceder(client, correo=CORREO):
    r = client.post(LOGIN, json={"correo": correo, "clave": CLAVE_DEMO})
    assert r.status_code == 200, r.text
    clave_mfa = r.json()["claveMfa"]
    r2 = client.post(MFA, json={"codigo": pyotp.TOTP(clave_mfa).now()})
    assert r2.status_code == 200, r2.text
    return clave_mfa


def test_acceso_completo_con_enrolamiento(cliente_real):
    r = cliente_real.post(LOGIN, json={"correo": CORREO, "clave": CLAVE_DEMO})
    cuerpo = r.json()
    assert r.status_code == 200 and cuerpo["paso"] == "ENROLAR"
    assert cuerpo["otpauthUri"].startswith("otpauth://") and cuerpo["claveMfa"]
    cookie_mfa = r.headers["set-cookie"]
    assert "eco_mfa=" in cookie_mfa and "HttpOnly" in cookie_mfa and "SameSite=strict" in cookie_mfa
    assert "eco_sesion" not in cookie_mfa
    assert cliente_real.get(SESION).status_code == 401  # aún sin sesión

    r2 = cliente_real.post(MFA, json={"codigo": pyotp.TOTP(cuerpo["claveMfa"]).now()})
    assert r2.status_code == 200
    assert r2.json() == {"nombre": "Planificación", "correo": CORREO, "rol": "PLANIFICADOR"}
    assert "eco_sesion=" in r2.headers["set-cookie"] and "HttpOnly" in r2.headers["set-cookie"]
    assert cliente_real.get(SESION).json()["rol"] == "PLANIFICADOR"


def test_segundo_acceso_pide_mfa_sin_clave(cliente_real):
    _acceder(cliente_real)
    cliente_real.post(LOGOUT)
    r = cliente_real.post(LOGIN, json={"correo": CORREO, "clave": CLAVE_DEMO})
    assert r.json()["paso"] == "MFA" and r.json()["claveMfa"] is None


def test_credenciales_incorrectas_mensaje_unico(cliente_real):
    a = cliente_real.post(LOGIN, json={"correo": CORREO, "clave": "mala"})
    b = cliente_real.post(LOGIN, json={"correo": "nadie@ecologistica.test", "clave": "mala"})
    assert a.status_code == b.status_code == 401
    assert a.json() == b.json() == {"status": 401, "message": "Correo o contraseña incorrectos"}


def test_bloqueo_responde_429(cliente_real):
    for _ in range(5):
        cliente_real.post(LOGIN, json={"correo": CORREO, "clave": "mala"})
    r = cliente_real.post(LOGIN, json={"correo": CORREO, "clave": CLAVE_DEMO})
    assert r.status_code == 429


def test_codigo_incorrecto_indica_el_campo(cliente_real):
    cliente_real.post(LOGIN, json={"correo": CORREO, "clave": CLAVE_DEMO})
    r = cliente_real.post(MFA, json={"codigo": "000000"})
    if r.status_code == 200:  # coincidencia improbable con el código real
        return
    assert r.status_code == 401 and "codigo" in r.json()["errors"]


def test_codigo_mal_formado_400(cliente_real):
    cliente_real.post(LOGIN, json={"correo": CORREO, "clave": CLAVE_DEMO})
    assert cliente_real.post(MFA, json={"codigo": "12ab"}).status_code == 400


def test_mfa_sin_comprobante(cliente_real):
    assert cliente_real.post(MFA, json={"codigo": "123456"}).status_code == 401


def test_cerrar_sesion_invalida_la_cookie_copiada(cliente_real):
    _acceder(cliente_real)
    copia = cliente_real.cookies.get("eco_sesion")
    r = cliente_real.post(LOGOUT)
    assert r.status_code == 204
    assert cliente_real.get(SESION, cookies={"eco_sesion": copia}).status_code == 401


def test_cookie_alterada(cliente_real):
    _acceder(cliente_real)
    token = cliente_real.cookies.get("eco_sesion")
    cliente_real.cookies.clear()
    assert cliente_real.get(SESION, cookies={"eco_sesion": token[:-3] + "abc"}).status_code == 401


def test_pedidos_sin_sesion_401(cliente_real, pedido_valido):
    assert cliente_real.get(PEDIDOS).status_code == 401
    r = cliente_real.post(PEDIDOS, json=pedido_valido)
    assert r.status_code == 401 and "items" not in r.text


def test_planificador_registra_con_sesion_real(cliente_real, pedido_valido):
    _acceder(cliente_real)
    assert cliente_real.post(PEDIDOS, json=pedido_valido).status_code == 201
    assert cliente_real.get(PEDIDOS).json()["total"] == 1


def test_conductor_real_recibe_403(cliente_real):
    _acceder(cliente_real, "conductor@ecologistica.test")
    r = cliente_real.get(PEDIDOS)
    assert r.status_code == 403 and "items" not in r.text


def test_origen_no_permitido(cliente_real):
    r = cliente_real.post(
        LOGIN,
        json={"correo": CORREO, "clave": CLAVE_DEMO},
        headers={"Origin": "https://sitio-malicioso.example"},
    )
    assert r.status_code == 403


def test_matriz_de_roles_en_pedidos(cliente_con_rol, pedido_valido):
    esperado_registrar = {Rol.PLANIFICADOR: 201}
    esperado_listar = {Rol.PLANIFICADOR: 200, Rol.ADMIN: 200}
    for rol in Rol:
        c = cliente_con_rol(rol)
        assert c.post(PEDIDOS, json=pedido_valido).status_code == esperado_registrar.get(rol, 403), rol
        assert c.get(PEDIDOS).status_code == esperado_listar.get(rol, 403), rol


def test_openapi_documenta_autenticacion(client):
    rutas = client.get("/openapi.json").json()["paths"]
    for ruta in ("/api/v1/auth/login", "/api/v1/auth/mfa", "/api/v1/auth/sesion", "/api/v1/auth/logout"):
        assert ruta in rutas
