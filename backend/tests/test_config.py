import pytest
from pydantic import ValidationError

from app.config import Settings


def _settings(**env) -> Settings:
    return Settings(_env_file=None, **env)


def test_valores_por_defecto_incluyen_los_cinco_distritos():
    s = _settings()
    assert s.ambito.distritos == (
        "Huancayo", "El Tambo", "Chilca", "Pilcomayo", "San Agustín de Cajas"
    )
    assert s.ambito.contiene(-12.065, -75.205)


def test_lee_ambito_personalizado():
    s = _settings(ambito_lat_min=-1, ambito_lat_max=1, ambito_lon_min=-1, ambito_lon_max=1,
                  ambito_distritos="A, B")
    assert s.ambito.distritos == ("A", "B")
    assert not s.ambito.contiene(-12, -75)


@pytest.mark.parametrize(
    "env",
    [
        {"ambito_lat_min": 5, "ambito_lat_max": 1},
        {"ambito_lon_min": 0, "ambito_lon_max": 0},
        {"ambito_lat_max": 95},
        {"ambito_distritos": " , "},
    ],
)
def test_configuracion_invalida_impide_el_arranque(env):
    with pytest.raises(ValidationError):
        _settings(**env)


def test_la_auditoria_se_envia_a_la_consola():
    import logging

    from app.main import configurar_registro

    configurar_registro()
    registro = logging.getLogger("ecologistica")
    assert registro.handlers and registro.level == logging.INFO
    assert logging.getLogger("ecologistica.auditoria").getEffectiveLevel() == logging.INFO
