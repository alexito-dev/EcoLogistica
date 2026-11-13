"""Integracion real contra PostgreSQL/PostGIS aislado: cuentas con TOTP cifrado, rutas guardadas y conduccion (ECO-21).

Requieren ECO_TEST_DATABASE_URL (base terminada en _test) con las migraciones aplicadas.
"""

import os
from datetime import date, datetime, timedelta, timezone
from uuid import uuid4

import pytest
from cryptography.fernet import Fernet
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from app.auth.cifrado import CifradorSecretos, ClaveDeCifradoInvalidaError
from app.auth.domain import EstadoUsuario, RegistroIntentos, Rol, Usuario
from app.auth.postgres_repository import UsuariosPostgresRepository
from app.conduccion.domain import EstadoParada, EventoParada
from app.conduccion.postgres_repository import ConduccionPostgresRepository
from app.pedidos.domain import Ambito, EstadoPedido, Pedido, Ubicacion
from app.pedidos.postgres_repository import PedidosPostgresRepository
from app.rutas.guardadas_postgres import RutasGuardadasPostgres


@pytest.fixture
def engine_pg():
    url = os.environ.get("ECO_TEST_DATABASE_URL")
    if not url:
        pytest.skip("Solo se permite PostgreSQL de pruebas mediante ECO_TEST_DATABASE_URL")
    if not (make_url(url).database or "").endswith("_test"):
        pytest.fail("ECO_TEST_DATABASE_URL debe apuntar a una base terminada en _test")
    engine = create_engine(url, pool_pre_ping=True)
    try:
        yield engine
    finally:
        engine.dispose()


def _usuario(rol=Rol.CONDUCTOR, **extra) -> Usuario:
    sufijo = uuid4().hex[:10]
    return Usuario(id=str(uuid4()), correo=f"it-{sufijo}@ecologistica.test", nombre=f"IT {sufijo}", rol=rol,
                   clave_hash="hash-de-prueba", **extra)


def _borrar_usuario(engine, usuario: Usuario) -> None:
    with engine.begin() as conexion:
        conexion.execute(text("DELETE FROM asignaciones_ruta WHERE conductor_id = :id"), {"id": usuario.id})
        conexion.execute(text("DELETE FROM eventos_parada WHERE usuario_id = :id"), {"id": usuario.id})
        conexion.execute(text("DELETE FROM intentos_acceso WHERE correo = :c"), {"c": usuario.correo})
        conexion.execute(text("DELETE FROM usuarios WHERE id = :id"), {"id": usuario.id})


def test_secreto_totp_se_guarda_cifrado_y_se_recupera(engine_pg):
    cifrador = CifradorSecretos(Fernet.generate_key().decode())
    repo = UsuariosPostgresRepository(engine_pg, cifrador)
    usuario = _usuario(mfa_secreto="JBSWY3DPEHPK3PXP", mfa_pendiente="PENDIENTE12345678", mfa_ultimo_paso=42)
    try:
        repo.guardar(usuario)
        with engine_pg.connect() as conexion:
            crudo = conexion.execute(
                text("SELECT mfa_secreto_cifrado, mfa_pendiente_cifrado FROM usuarios WHERE id = :id"),
                {"id": usuario.id},
            ).one()
        assert "JBSWY3DPEHPK3PXP" not in crudo[0] and "PENDIENTE12345678" not in crudo[1]

        recuperado = UsuariosPostgresRepository(engine_pg, cifrador).obtener(usuario.id)
        assert recuperado is not None
        assert (recuperado.mfa_secreto, recuperado.mfa_pendiente, recuperado.mfa_ultimo_paso) == (
            "JBSWY3DPEHPK3PXP", "PENDIENTE12345678", 42)
        assert repo.obtener_por_correo(usuario.correo).id == usuario.id
        assert repo.obtener("no-es-uuid") is None

        # Con otra clave los datos no son legibles.
        with pytest.raises(ClaveDeCifradoInvalidaError):
            UsuariosPostgresRepository(engine_pg, CifradorSecretos(Fernet.generate_key().decode())).obtener(usuario.id)

        actualizado = recuperado
        actualizado.estado = EstadoUsuario.BLOQUEADO
        actualizado.version_sesion = 2
        repo.guardar(actualizado)
        assert repo.obtener(usuario.id).version_sesion == 2
        assert repo.contar() >= 1
        assert usuario.id not in [u.id for u in repo.listar_por_rol(Rol.CONDUCTOR)]  # bloqueado: no es asignable
    finally:
        _borrar_usuario(engine_pg, usuario)


def test_intentos_de_acceso_persisten_y_se_limpian(engine_pg):
    repo = UsuariosPostgresRepository(engine_pg, CifradorSecretos(Fernet.generate_key().decode()))
    correo = f"intentos-{uuid4().hex[:8]}@ecologistica.test"
    ahora = datetime.now(timezone.utc)
    try:
        assert repo.intentos(correo).fallos == []
        registro = RegistroIntentos(fallos=[ahora - timedelta(minutes=1), ahora], bloqueado_hasta=ahora + timedelta(minutes=15))
        repo.guardar_intentos(correo, registro)
        leido = repo.intentos(correo)
        assert len(leido.fallos) == 2 and leido.bloqueado(ahora)
        repo.limpiar_intentos(correo)
        assert repo.intentos(correo).fallos == []
    finally:
        repo.limpiar_intentos(correo)


def test_rutas_guardadas_reemplazan_y_sobreviven_a_otra_instancia(engine_pg):
    fecha = date(2031, 1, 15)
    try:
        RutasGuardadasPostgres(engine_pg).guardar(fecha, {"guardadaPor": "Plan", "vista": {"rutas": [1]}})
        RutasGuardadasPostgres(engine_pg).guardar(fecha, {"guardadaPor": "Plan 2", "vista": {"rutas": [1, 2]}})
        leido = RutasGuardadasPostgres(engine_pg).obtener(fecha)
        assert leido == {"guardadaPor": "Plan 2", "vista": {"rutas": [1, 2]}}
        assert RutasGuardadasPostgres(engine_pg).obtener(date(2031, 1, 16)) is None
    finally:
        with engine_pg.begin() as conexion:
            conexion.execute(text("DELETE FROM rutas_guardadas WHERE fecha = :f"), {"f": fecha})


def test_conduccion_asignaciones_eventos_y_estado_del_pedido(engine_pg):
    fecha = date(2031, 2, 20)
    cifrador = CifradorSecretos(Fernet.generate_key().decode())
    usuarios = UsuariosPostgresRepository(engine_pg, cifrador)
    pedidos = PedidosPostgresRepository(engine_pg)
    conduccion = ConduccionPostgresRepository(engine_pg)
    conductor = _usuario()
    vehiculo_id = uuid4()
    pedido = Pedido.crear(
        codigo=f"IT-{uuid4().hex[:10].upper()}",
        ubicacion=Ubicacion("Jr. Real 123", "Huancayo", -12.06, -75.20),
        demanda_kg=10.0, demanda_m3=0.5, tiempo_servicio_min=10,
        ventana_inicio=datetime(2031, 2, 20, 13, tzinfo=timezone.utc),
        ventana_fin=datetime(2031, 2, 20, 17, tzinfo=timezone.utc),
        prioridad=2, ambito=Ambito(-12.20, -11.95, -75.35, -75.10, ("Huancayo",)),
    )
    try:
        usuarios.guardar(conductor)
        pedidos.guardar(pedido)
        with engine_pg.begin() as conexion:
            conexion.execute(
                text("""INSERT INTO vehiculos (id, placa, tipo, capacidad_kg, capacidad_m3, combustible,
                        consumo_base_por_100km, estado)
                        VALUES (:id, :placa, 'Furgón', 500, 3, 'DIESEL', 10, 'DISPONIBLE')"""),
                {"id": vehiculo_id, "placa": f"IT-{uuid4().hex[:6].upper()}"},
            )
        conduccion.asignar(fecha, vehiculo_id, conductor.id, None)
        conduccion.asignar(fecha, vehiculo_id, conductor.id, conductor.id)  # reasignar es idempotente
        assert conduccion.asignaciones(fecha) == {vehiculo_id: conductor.id}

        base = datetime(2031, 2, 20, 14, tzinfo=timezone.utc)
        for i, (estado, nota) in enumerate([
            (EstadoParada.EN_RUTA, None), (EstadoParada.INCIDENCIA, "Cliente ausente"), (EstadoParada.EN_RUTA, None)
        ]):
            conduccion.registrar_evento(EventoParada(uuid4(), fecha, pedido.id, estado, nota, conductor.id, base + timedelta(minutes=i)))
        assert [e.estado for e in conduccion.historial(fecha, pedido.id)] == [
            EstadoParada.EN_RUTA, EstadoParada.INCIDENCIA, EstadoParada.EN_RUTA]
        assert conduccion.ultimos_eventos(fecha)[pedido.id].estado == EstadoParada.EN_RUTA
        assert conduccion.ultimos_eventos(date(2031, 2, 21)) == {}

        # Una incidencia sin descripcion viola la restriccion de la base.
        with pytest.raises(Exception):
            conduccion.registrar_evento(EventoParada(uuid4(), fecha, pedido.id, EstadoParada.INCIDENCIA, " ", None, base))

        pedidos.actualizar_estado(pedido.id, EstadoPedido.ENTREGADO)
        assert pedidos.obtener(pedido.id).estado == EstadoPedido.ENTREGADO
    finally:
        with engine_pg.begin() as conexion:
            conexion.execute(text("DELETE FROM eventos_parada WHERE pedido_id = :id"), {"id": pedido.id})
            conexion.execute(text("DELETE FROM asignaciones_ruta WHERE vehiculo_id = :id"), {"id": vehiculo_id})
            conexion.execute(text("DELETE FROM vehiculos WHERE id = :id"), {"id": vehiculo_id})
            conexion.execute(text("DELETE FROM pedidos WHERE id = :id"), {"id": pedido.id})
            conexion.execute(text("DELETE FROM ubicaciones WHERE id = :id"), {"id": pedido.id})
        _borrar_usuario(engine_pg, conductor)
