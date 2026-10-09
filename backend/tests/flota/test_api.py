"""Fleet API scenarios for HU-003 and HU-009."""

from datetime import date

from app.auth.domain import Rol

BASE = "/api/v1/vehiculos"
VEHICULO = {
    "placa": "ABC-123",
    "tipo": "Furgón",
    "capacidadKg": "900.00",
    "capacidadM3": "8.500",
    "combustible": "DIESEL",
    "consumoBasePor100km": "12.5000",
    "factorEmisionKgco2eUnidad": None,
    "anio": 2022,
    "estado": "DISPONIBLE",
}


def test_admin_registra_vehiculo_con_placa_normalizada(cliente_con_rol):
    admin = cliente_con_rol(Rol.ADMIN)
    respuesta = admin.post(BASE, json={**VEHICULO, "placa": " abc-123 "})
    assert respuesta.status_code == 201, respuesta.text
    assert respuesta.json()["placa"] == "ABC-123"
    assert respuesta.json()["elegibleParaPlanificar"] is False


def test_planificador_declara_disponibilidad_por_fecha(cliente_con_rol):
    admin = cliente_con_rol(Rol.ADMIN)
    creado = admin.post(BASE, json=VEHICULO).json()
    planificador = cliente_con_rol(Rol.PLANIFICADOR)
    fecha = date(2026, 10, 9)

    respuesta = planificador.put(
        f"{BASE}/{creado['id']}/disponibilidad",
        json={
            "fecha": fecha.isoformat(),
            "turnoInicio": "08:00:00",
            "turnoFin": "17:00:00",
            "disponible": True,
            "restriccionCirculacion": "Sin restricciones declaradas",
        },
    )
    assert respuesta.status_code == 200, respuesta.text
    assert respuesta.json()["elegibleParaPlanificar"] is True
    assert respuesta.json()["disponibilidad"]["fecha"] == fecha.isoformat()

    listado = planificador.get(BASE, params={"fecha": fecha.isoformat()})
    assert listado.status_code == 200
    assert listado.json()["items"][0]["placa"] == "ABC-123"
    assert listado.json()["items"][0]["elegibleParaPlanificar"] is True


def test_placa_duplicada_es_conflicto(cliente_con_rol):
    admin = cliente_con_rol(Rol.ADMIN)
    assert admin.post(BASE, json=VEHICULO).status_code == 201
    duplicado = admin.post(BASE, json={**VEHICULO, "tipo": "Camión"})
    assert duplicado.status_code == 409
    assert "placa" in duplicado.json()["errors"]


def test_turno_invertido_se_rechaza(cliente_con_rol):
    admin = cliente_con_rol(Rol.ADMIN)
    creado = admin.post(BASE, json=VEHICULO).json()
    planificador = cliente_con_rol(Rol.PLANIFICADOR)
    respuesta = planificador.put(
        f"{BASE}/{creado['id']}/disponibilidad",
        json={
            "fecha": "2026-10-09",
            "turnoInicio": "17:00:00",
            "turnoFin": "08:00:00",
            "disponible": True,
        },
    )
    assert respuesta.status_code == 422
    assert "turnoFin" in respuesta.json()["errors"]


def test_no_disponible_exige_motivo(cliente_con_rol):
    admin = cliente_con_rol(Rol.ADMIN)
    creado = admin.post(BASE, json=VEHICULO).json()
    planificador = cliente_con_rol(Rol.PLANIFICADOR)
    respuesta = planificador.put(
        f"{BASE}/{creado['id']}/disponibilidad",
        json={
            "fecha": "2026-10-09",
            "turnoInicio": "08:00:00",
            "turnoFin": "17:00:00",
            "disponible": False,
        },
    )
    assert respuesta.status_code == 422
    assert "restriccionCirculacion" in respuesta.json()["errors"]


def test_roles_separan_catalogo_y_disponibilidad(cliente_con_rol):
    planificador = cliente_con_rol(Rol.PLANIFICADOR)
    conductor = cliente_con_rol(Rol.CONDUCTOR)
    assert planificador.post(BASE, json=VEHICULO).status_code == 403
    assert conductor.get(BASE).status_code == 403
