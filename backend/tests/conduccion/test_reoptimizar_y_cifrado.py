"""Reoptimizacion con datos controlados y cifrado en reposo de secretos TOTP (ECO-21)."""

from datetime import date, datetime, timezone
from uuid import uuid4

import pytest
from cryptography.fernet import Fernet

from app.auth.cifrado import CifradorSecretos, ClaveDeCifradoInvalidaError
from app.auth.domain import Rol, Usuario
from app.conduccion.domain import EstadoParada, EventoParada
from app.conduccion.memory_repository import ConduccionMemoryRepository
from app.conduccion.service import ConduccionService
from app.pedidos.memory_repository import PedidosMemoryRepository

FECHA = date(2026, 10, 10)
AHORA = datetime(2026, 10, 10, 13, 0, tzinfo=timezone.utc)


class Guardadas:
    def __init__(self, registro):
        self.registro = registro

    def obtener(self, fecha):
        return self.registro

    def guardar(self, fecha, registro):
        self.registro = registro


class Usuarios:
    def listar_por_rol(self, rol):
        return []


def parada(orden, codigo, lat, lon):
    return {
        "orden": orden, "pedidoId": str(uuid4()), "codigo": codigo, "latitud": lat, "longitud": lon, "prioridad": 2,
        "ventanaInicio": "2026-10-10T13:00:00Z", "ventanaFin": "2026-10-10T23:00:00Z",
        "llegadaEstimada": "2026-10-10T13:00:00Z", "dentroDeVentana": True,
    }


def servicio(paradas):
    registro = {
        "vista": {
            "deposito": {"nombre": "D", "latitud": -12.0651, "longitud": -75.2049},
            "rutas": [{"vehiculo": {"id": str(uuid4()), "placa": "ABC-123"}, "paradas": paradas, "distanciaKm": 1.0}],
        }
    }
    conduccion = ConduccionMemoryRepository()
    return ConduccionService(Guardadas(registro), conduccion, PedidosMemoryRepository(), Usuarios()), registro, conduccion


def test_reoptimizar_reordena_pendientes_desde_la_ultima_entrega():
    cerca = parada(1, "A", -12.0660, -75.2050)
    lejos = parada(2, "B", -12.1500, -75.3000)
    media = parada(3, "C", -12.0700, -75.2060)
    entregada = parada(1, "E", -12.0651, -75.2049)
    svc, registro, conduccion = servicio([entregada, lejos, media, cerca])
    conduccion.registrar_evento(
        EventoParada(uuid4(), FECHA, __import__("uuid").UUID(entregada["pedidoId"]), EstadoParada.ENTREGADO, None, None, AHORA)
    )
    resultado = svc.reoptimizar(FECHA, Usuario("u", "p@x.test", "Plan", Rol.PLANIFICADOR, "h"), ahora=AHORA)
    assert resultado["rutasReordenadas"] == 1
    codigos = [p["codigo"] for p in registro["vista"]["rutas"][0]["paradas"]]
    assert codigos == ["E", "A", "C", "B"]  # la entregada no se mueve; el resto por cercanía
    assert [p["orden"] for p in registro["vista"]["rutas"][0]["paradas"]] == [1, 2, 3, 4]
    assert registro["reoptimizadaPor"] == "Plan"


def test_cifrador_ida_y_vuelta_y_texto_no_legible():
    cifrador = CifradorSecretos(Fernet.generate_key().decode())
    token = cifrador.cifrar("JBSWY3DPEHPK3PXP")
    assert token != "JBSWY3DPEHPK3PXP" and "JBSWY3DPEHPK3PXP" not in token
    assert cifrador.descifrar(token) == "JBSWY3DPEHPK3PXP"
    assert cifrador.cifrar(None) is None and cifrador.descifrar(None) is None


def test_cifrador_exige_clave_valida_y_detecta_clave_distinta():
    with pytest.raises(ClaveDeCifradoInvalidaError, match="TOTP_CLAVE_CIFRADO"):
        CifradorSecretos("")
    with pytest.raises(ClaveDeCifradoInvalidaError, match="Fernet"):
        CifradorSecretos("no-es-fernet")
    token = CifradorSecretos(Fernet.generate_key().decode()).cifrar("secreto")
    with pytest.raises(ClaveDeCifradoInvalidaError, match="descifrar"):
        CifradorSecretos(Fernet.generate_key().decode()).descifrar(token)
