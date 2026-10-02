from datetime import datetime, timedelta, timezone

import pytest

from app.pedidos.domain import Ambito, EstadoPedido, Pedido, ReglaDominioError, Ubicacion

LIMA = timezone(timedelta(hours=-5))
AMBITO = Ambito(-12.20, -11.95, -75.35, -75.10, ("Huancayo", "El Tambo", "Chilca"))


def _crear(**cambios):
    datos = dict(
        codigo=" ped-001 ",
        ubicacion=Ubicacion("Jr. Real 123", "Huancayo", -12.06, -75.20),
        demanda_kg=10.0,
        demanda_m3=0.0,
        tiempo_servicio_min=10,
        ventana_inicio=datetime(2026, 10, 5, 8, 0, tzinfo=LIMA),
        ventana_fin=datetime(2026, 10, 5, 12, 0, tzinfo=LIMA),
        prioridad=2,
        ambito=AMBITO,
    )
    datos.update(cambios)
    return Pedido.crear(**datos)


def test_crea_pedido_pendiente_con_codigo_normalizado_y_fechas_utc():
    pedido = _crear()
    assert pedido.estado == EstadoPedido.PENDIENTE
    assert pedido.codigo == "PED-001"
    assert pedido.ventana_inicio == datetime(2026, 10, 5, 13, 0, tzinfo=timezone.utc)
    assert pedido.ventana_inicio.utcoffset() == timedelta(0)


@pytest.mark.parametrize("fin_horas", [0, -1])
def test_rechaza_ventana_con_fin_igual_o_anterior_al_inicio(fin_horas):
    inicio = datetime(2026, 10, 5, 8, 0, tzinfo=LIMA)
    with pytest.raises(ReglaDominioError) as e:
        _crear(ventana_inicio=inicio, ventana_fin=inicio + timedelta(hours=fin_horas))
    assert "ventanaFin" in e.value.errors


def test_acepta_ventana_de_un_minuto():
    inicio = datetime(2026, 10, 5, 8, 0, tzinfo=LIMA)
    assert _crear(ventana_inicio=inicio, ventana_fin=inicio + timedelta(minutes=1))


def test_rechaza_fecha_sin_zona_horaria():
    with pytest.raises(ReglaDominioError) as e:
        _crear(ventana_inicio=datetime(2026, 10, 5, 8, 0))
    assert "ventanaInicio" in e.value.errors


def test_rechaza_sin_carga():
    with pytest.raises(ReglaDominioError) as e:
        _crear(demanda_kg=0, demanda_m3=0)
    assert "demandaKg" in e.value.errors


def test_acepta_solo_volumen():
    assert _crear(demanda_kg=0, demanda_m3=0.5)


@pytest.mark.parametrize("campo", ["demanda_kg", "demanda_m3"])
def test_rechaza_demanda_negativa(campo):
    with pytest.raises(ReglaDominioError) as e:
        _crear(**{campo: -1})
    assert ("demandaKg" if campo == "demanda_kg" else "demandaM3") in e.value.errors


@pytest.mark.parametrize("prioridad", [0, 5])
def test_rechaza_prioridad_fuera_de_rango(prioridad):
    with pytest.raises(ReglaDominioError) as e:
        _crear(prioridad=prioridad)
    assert "prioridad" in e.value.errors


@pytest.mark.parametrize("prioridad", [1, 4])
def test_acepta_limites_de_prioridad(prioridad):
    assert _crear(prioridad=prioridad).prioridad == prioridad


def test_rechaza_tiempo_de_servicio_no_positivo():
    with pytest.raises(ReglaDominioError) as e:
        _crear(tiempo_servicio_min=0)
    assert "tiempoServicioMin" in e.value.errors


def test_rechaza_coordenadas_fuera_del_ambito():
    with pytest.raises(ReglaDominioError) as e:
        _crear(ubicacion=Ubicacion("Av. Arequipa", "Huancayo", -12.04, -77.03))
    assert {"latitud", "longitud"} <= e.value.errors.keys() or "longitud" in e.value.errors


def test_rechaza_distrito_no_configurado_ignorando_mayusculas():
    with pytest.raises(ReglaDominioError) as e:
        _crear(ubicacion=Ubicacion("Calle 1", "Lima", -12.06, -75.20))
    assert "distrito" in e.value.errors
    assert _crear(ubicacion=Ubicacion("Calle 1", "  el tambo ", -12.06, -75.20))


def test_acumula_varios_errores():
    with pytest.raises(ReglaDominioError) as e:
        _crear(prioridad=9, demanda_kg=0, demanda_m3=0)
    assert {"prioridad", "demandaKg"} <= e.value.errors.keys()
