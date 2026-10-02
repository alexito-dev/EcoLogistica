import logging

import pyotp
import pytest

from app.auth.domain import (
    CodigoInvalidoError,
    ComprobanteInvalidoError,
    CredencialesInvalidasError,
    CuentaBloqueadaError,
    EstadoUsuario,
    NoAutenticadoError,
    PasoAcceso,
)
from app.auth.service import AutenticacionService
from app.auth.siembra import sembrar_usuarios_demo
from tests.conftest import CLAVE_DEMO, Reloj

FIRMA = "clave-de-pruebas-suficientemente-larga-0123456789"
CORREO = "planificador@ecologistica.test"


@pytest.fixture
def reloj():
    return Reloj()


@pytest.fixture
def servicio(repo_usuarios, reloj):
    return AutenticacionService(repo_usuarios, FIRMA, reloj)


def _acceder(servicio, reloj, correo=CORREO):
    """Enrola (si hace falta) y devuelve la sesión y el secreto TOTP."""
    r = servicio.iniciar(correo, CLAVE_DEMO)
    secreto = r.secreto or servicio._repo.obtener_por_correo(correo).mfa_secreto
    sesion = servicio.verificar_mfa(r.comprobante, pyotp.TOTP(secreto).at(reloj()))
    return sesion, secreto


def test_siembra_crea_cinco_roles_y_no_sobrescribe(repo_usuarios):
    assert repo_usuarios.contar() == 5
    assert sembrar_usuarios_demo(repo_usuarios, None) is None
    assert repo_usuarios.contar() == 5


def test_siembra_genera_clave_si_no_se_configura(tmp_path):
    from app.auth.archivo_repository import UsuariosArchivoRepository

    repo = UsuariosArchivoRepository(tmp_path / "u.json")
    generada = sembrar_usuarios_demo(repo, None)
    assert generada and len(generada) >= 12
    assert generada not in (tmp_path / "u.json").read_text(encoding="utf-8")


def test_primer_acceso_pide_enrolar_y_luego_mfa(servicio, reloj):
    r = servicio.iniciar("  PLANIFICADOR@ecologistica.test ", CLAVE_DEMO)
    assert r.paso == PasoAcceso.ENROLAR and r.secreto and r.uri.startswith("otpauth://")
    sesion = servicio.verificar_mfa(r.comprobante, pyotp.TOTP(r.secreto).at(reloj()))
    assert sesion.usuario.correo == CORREO and sesion.token
    reloj.avanzar(minutes=1)
    assert servicio.iniciar(CORREO, CLAVE_DEMO).paso == PasoAcceso.MFA


def test_el_secreto_solo_se_activa_al_validar_un_codigo(servicio, repo_usuarios):
    r = servicio.iniciar(CORREO, CLAVE_DEMO)
    u = repo_usuarios.obtener_por_correo(CORREO)
    assert u.mfa_secreto is None and u.mfa_pendiente == r.secreto


@pytest.mark.parametrize("correo,clave", [(CORREO, "incorrecta"), ("nadie@ecologistica.test", CLAVE_DEMO)])
def test_credenciales_invalidas_mismo_error(servicio, correo, clave):
    with pytest.raises(CredencialesInvalidasError):
        servicio.iniciar(correo, clave)


def test_usuario_inactivo_no_accede(servicio, repo_usuarios):
    u = repo_usuarios.obtener_por_correo(CORREO)
    u.estado = EstadoUsuario.INACTIVO
    repo_usuarios.guardar(u)
    with pytest.raises(CredencialesInvalidasError):
        servicio.iniciar(CORREO, CLAVE_DEMO)


@pytest.mark.parametrize("correo", [CORREO, "inexistente@ecologistica.test"])
def test_bloqueo_tras_cinco_fallos_tambien_para_inexistentes(servicio, reloj, correo):
    for _ in range(5):
        with pytest.raises(CredencialesInvalidasError):
            servicio.iniciar(correo, "mala")
    with pytest.raises(CuentaBloqueadaError):
        servicio.iniciar(correo, CLAVE_DEMO)
    reloj.avanzar(minutes=15, seconds=1)
    if correo == CORREO:
        assert servicio.iniciar(correo, CLAVE_DEMO).paso == PasoAcceso.ENROLAR


def test_fallos_fuera_de_la_ventana_no_bloquean(servicio, reloj):
    for _ in range(4):
        with pytest.raises(CredencialesInvalidasError):
            servicio.iniciar(CORREO, "mala")
    reloj.avanzar(minutes=16)
    with pytest.raises(CredencialesInvalidasError):
        servicio.iniciar(CORREO, "mala")
    assert servicio.iniciar(CORREO, CLAVE_DEMO)


def test_acceso_correcto_reinicia_el_contador(servicio, repo_usuarios):
    for _ in range(4):
        with pytest.raises(CredencialesInvalidasError):
            servicio.iniciar(CORREO, "mala")
    servicio.iniciar(CORREO, CLAVE_DEMO)
    assert repo_usuarios.intentos(CORREO).fallos == []


def test_codigo_incorrecto_y_repetido(servicio, reloj):
    _, secreto = _acceder(servicio, reloj)
    r = servicio.iniciar(CORREO, CLAVE_DEMO)
    with pytest.raises(CodigoInvalidoError):
        servicio.verificar_mfa(r.comprobante, "000000" if pyotp.TOTP(secreto).at(reloj()) != "000000" else "111111")
    with pytest.raises(CodigoInvalidoError):  # el código del primer acceso ya fue usado
        servicio.verificar_mfa(r.comprobante, pyotp.TOTP(secreto).at(reloj()))
    reloj.avanzar(seconds=30)
    assert servicio.verificar_mfa(r.comprobante, pyotp.TOTP(secreto).at(reloj()))


def test_cinco_codigos_incorrectos_agotan_el_comprobante(servicio, reloj):
    _, secreto = _acceder(servicio, reloj)
    reloj.avanzar(seconds=30)
    r = servicio.iniciar(CORREO, CLAVE_DEMO)
    correcto = pyotp.TOTP(secreto).at(reloj())
    malo = "000000" if correcto != "000000" else "111111"
    for _ in range(5):
        with pytest.raises(CodigoInvalidoError):
            servicio.verificar_mfa(r.comprobante, malo)
    with pytest.raises(ComprobanteInvalidoError):
        servicio.verificar_mfa(r.comprobante, correcto)


def test_comprobante_vencido_o_alterado(servicio, reloj):
    r = servicio.iniciar(CORREO, CLAVE_DEMO)
    with pytest.raises(ComprobanteInvalidoError):
        servicio.verificar_mfa(r.comprobante + "x", "123456")
    reloj.avanzar(minutes=5, seconds=1)
    with pytest.raises(ComprobanteInvalidoError):
        servicio.verificar_mfa(r.comprobante, pyotp.TOTP(r.secreto).at(reloj()))


def test_sesion_deslizante_inactividad_y_maximo(servicio, reloj):
    sesion, _ = _acceder(servicio, reloj)
    token = sesion.token
    for _ in range(34):  # 34 × 14 min = 7 h 56 min, siempre con actividad
        reloj.avanzar(minutes=14)
        token = servicio.validar_sesion(token).token
    reloj.avanzar(minutes=14)  # 8 h 10 min desde el inicio: supera la duración máxima
    with pytest.raises(NoAutenticadoError):
        servicio.validar_sesion(token)


def test_sesion_vence_por_inactividad(servicio, reloj):
    sesion, _ = _acceder(servicio, reloj)
    reloj.avanzar(minutes=15, seconds=1)
    with pytest.raises(NoAutenticadoError):
        servicio.validar_sesion(sesion.token)


def test_cierre_de_sesion_invalida_tokens_anteriores(servicio, reloj):
    sesion, _ = _acceder(servicio, reloj)
    servicio.cerrar_sesion(sesion.usuario)
    with pytest.raises(NoAutenticadoError):
        servicio.validar_sesion(sesion.token)


def test_desactivacion_con_sesion_abierta(servicio, reloj, repo_usuarios):
    sesion, _ = _acceder(servicio, reloj)
    u = repo_usuarios.obtener_por_correo(CORREO)
    u.estado = EstadoUsuario.INACTIVO
    repo_usuarios.guardar(u)
    with pytest.raises(NoAutenticadoError):
        servicio.validar_sesion(sesion.token)


def test_eventos_sin_secretos(servicio, reloj, caplog):
    caplog.set_level(logging.INFO, logger="ecologistica.auditoria")
    with pytest.raises(CredencialesInvalidasError):
        servicio.iniciar(CORREO, "contraseña-secreta-mala")
    sesion, secreto = _acceder(servicio, reloj)
    texto = caplog.text
    assert "LOGIN_FALLIDO" in texto and "MFA_ENROLADO" in texto and "LOGIN_OK" in texto
    assert "contraseña-secreta-mala" not in texto and CLAVE_DEMO not in texto
    assert secreto not in texto and sesion.token not in texto


def test_persistencia_en_archivo(repo_usuarios, servicio, reloj, tmp_path):
    from app.auth.archivo_repository import UsuariosArchivoRepository

    _acceder(servicio, reloj)
    recargado = UsuariosArchivoRepository(tmp_path / "usuarios.json")
    assert recargado.obtener_por_correo(CORREO).mfa_secreto
