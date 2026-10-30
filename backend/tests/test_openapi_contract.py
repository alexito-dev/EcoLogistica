"""Contrato OpenAPI y controles de autorización para los incrementos Sprint 1–3.

Esta suite verifica que las rutas públicas documentadas estén presentes, que los
contratos HTTP publiquen respuestas de error y que los roles no permitidos reciban
403. No reemplaza pruebas de navegador ni pruebas de despliegue.
"""
from app.auth.domain import Rol
from app.main import app


def test_openapi_publica_operaciones_de_los_tres_sprints():
    esquema = app.openapi()
    assert esquema["openapi"].startswith("3.")
    assert esquema["info"]["title"] == "EcoLogística Huancayo API"
    operaciones = {
        "/api/v1/auth/login": "post",
        "/api/v1/auth/mfa": "post",
        "/api/v1/auth/sesion": "get",
        "/api/v1/pedidos": "post",
        "/api/v1/vehiculos": "get",
        "/api/v1/rutas/vista-previa": "get",
        "/api/v1/rutas/guardar": "post",
        "/api/v1/rutas/guardada": "get",
        "/api/v1/indicadores": "get",
    }
    for ruta, metodo in operaciones.items():
        assert ruta in esquema["paths"], ruta
        assert metodo in esquema["paths"][ruta], (ruta, metodo)
        respuestas = esquema["paths"][ruta][metodo]["responses"]
        assert respuestas, (ruta, metodo)


def test_openapi_documenta_errores_de_autorizacion_y_validacion():
    esquema = app.openapi()
    for ruta, metodo in (
        ("/api/v1/rutas/vista-previa", "get"),
        ("/api/v1/rutas/guardar", "post"),
        ("/api/v1/rutas/guardada", "get"),
    ):
        respuestas = esquema["paths"][ruta][metodo]["responses"]
        assert "401" in respuestas
        assert "403" in respuestas


def test_un_conductor_no_puede_planificar_ni_ver_indicadores(cliente_con_rol):
    cliente = cliente_con_rol(Rol.CONDUCTOR)
    assert cliente.get("/api/v1/rutas/vista-previa", params={"fecha": "2026-10-30"}).status_code == 403
    assert cliente.post("/api/v1/rutas/guardar", params={"fecha": "2026-10-30"}).status_code == 403
    assert cliente.get("/api/v1/rutas/guardada", params={"fecha": "2026-10-30"}).status_code == 403
    assert cliente.get("/api/v1/indicadores", params={"fecha": "2026-10-30"}).status_code == 403
