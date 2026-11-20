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


@pytest.mark.parametrize(
    "media, letra",
    [(100, "A+"), (84.1, "A+"), (84.0, "A"), (80.8, "A"), (78.9, "A-"), (77.2, "B+"), (74.1, "B"), (72.6, "B-"),
     (71.1, "C+"), (68, "C"), (65, "C"), (62.7, "C-"), (51.7, "D"), (51.6, "F"), (0, "F")],
)
def test_grado_a_f_segun_la_curva_de_sauro_y_lewis(media, letra):
    assert sus.grado(media)[0] == letra


def test_grado_rechaza_puntuaciones_fuera_de_rango():
    for mala in (-0.1, 100.1):
        with pytest.raises(ValueError):
            sus.grado(mala)


def test_contribuciones_suman_la_puntuacion_dividida_entre_2_5():
    respuestas = [4, 2, 5, 1, 4, 2, 5, 2, 4, 1]
    assert sus.contribuciones(respuestas) == [3, 3, 4, 4, 3, 3, 4, 3, 3, 4]
    assert sum(sus.contribuciones(respuestas)) * 2.5 == sus.puntuacion_sus(respuestas) == 85.0


def test_informe_markdown_incluye_calculo_y_resultado_global():
    texto = sus.informe_markdown([[5, 1, 5, 1, 5, 1, 5, 1, 5, 1], [3] * 10])
    assert "| P01 | 5 | 1 | 5 | 1 | 5 | 1 | 5 | 1 | 5 | 1 |" in texto
    assert "40 x 2,5 = 100.0" in texto
    assert "20 x 2,5 = 50.0" in texto
    assert "| SUS promedio | 75.00" in texto
    assert "| Grado (Sauro y Lewis) | B - Bueno |" in texto
    assert "| Cumple el umbral >= 68 | SI |" in texto
