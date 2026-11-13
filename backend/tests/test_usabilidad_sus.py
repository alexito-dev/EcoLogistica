"""El procesamiento SUS de la guía de laboratorio calcula bien la escala estándar."""

import importlib.util
from pathlib import Path

import pytest

RUTA = Path(__file__).resolve().parents[2] / "scripts" / "usabilidad" / "procesar_sus.py"
spec = importlib.util.spec_from_file_location("procesar_sus", RUTA)
sus = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sus)


def test_puntuaciones_extremas_y_neutra():
    assert sus.puntuacion_sus([5, 1, 5, 1, 5, 1, 5, 1, 5, 1]) == 100.0
    assert sus.puntuacion_sus([1, 5, 1, 5, 1, 5, 1, 5, 1, 5]) == 0.0
    assert sus.puntuacion_sus([3] * 10) == 50.0


def test_respuestas_invalidas_se_rechazan():
    for malas in ([3] * 9, [3] * 9 + [6], [3] * 9 + [0]):
        with pytest.raises(ValueError):
            sus.puntuacion_sus(malas)


@pytest.mark.parametrize("media, texto", [(68.1, "BUENA"), (68, "ACEPTABLE"), (50, "ACEPTABLE"), (49.9, "BAJA")])
def test_interpretacion(media, texto):
    assert texto in sus.interpretar(media)


def test_lectura_csv_y_resumen(tmp_path):
    archivo = tmp_path / "r.csv"
    archivo.write_text("P1,P2,P3,P4,P5,P6,P7,P8,P9,P10\n5,1,5,1,5,1,5,1,5,1\n3,3,3,3,3,3,3,3,3,3\n", encoding="utf-8")
    puntuaciones = [sus.puntuacion_sus(r) for r in sus.leer_respuestas(str(archivo))]
    assert puntuaciones == [100.0, 50.0]
    assert sus.resumen(puntuaciones)["media"] == 75.0


def test_csv_sin_columnas_obligatorias(tmp_path):
    archivo = tmp_path / "r.csv"
    archivo.write_text("P1,P2\n1,2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Faltan columnas"):
        sus.leer_respuestas(str(archivo))
