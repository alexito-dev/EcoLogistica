"""Calcula la puntuacion SUS (System Usability Scale) de las respuestas de una encuesta.

Entrada: CSV con columnas P1..P10 (escala Likert 1-5), una fila por participante.
Salida: puntuacion por persona, media, desviacion, minimo, maximo e interpretacion.
Solo usa la biblioteca estandar. Uso: python scripts/usabilidad/procesar_sus.py respuestas.csv

Puntuacion estandar: impares (valor - 1), pares (5 - valor); suma x 2,5 (rango 0-100).
Interpretacion segun la guia de laboratorio: > 68 buena, 50-68 aceptable, < 50 baja.
Sprint 4: ademas se informa el grado A-F (curva de Sauro y Lewis, 2016) y, con --markdown, la tabla de
respuestas con el calculo paso a paso, lista para pegar en docs/03 Implementacion/Sprint 04/04 Usabilidad.
Uso: python scripts/usabilidad/procesar_sus.py respuestas.csv [--markdown]
"""

import csv
import statistics
import sys

COLUMNAS = [f"P{i}" for i in range(1, 11)]


def puntuacion_sus(respuestas: list[int]) -> float:
    if len(respuestas) != 10 or any(r not in (1, 2, 3, 4, 5) for r in respuestas):
        raise ValueError("Se requieren 10 respuestas con valores enteros de 1 a 5")
    suma = sum((r - 1) if i % 2 == 1 else (5 - r) for i, r in enumerate(respuestas, start=1))
    return suma * 2.5


# Curva de calificacion de Sauro y Lewis (2016): limite inferior de cada grado y adjetivo asociado.
GRADOS = [
    (84.1, "A+", "Excelente"),
    (80.8, "A", "Excelente"),
    (78.9, "A-", "Excelente"),
    (77.2, "B+", "Bueno"),
    (74.1, "B", "Bueno"),
    (72.6, "B-", "Bueno"),
    (71.1, "C+", "Aceptable"),
    (65.0, "C", "Aceptable"),
    (62.7, "C-", "Aceptable"),
    (51.7, "D", "Pobre"),
    (0.0, "F", "Inaceptable"),
]
UMBRAL_ACEPTACION = 68


def grado(media: float) -> tuple[str, str]:
    """Devuelve (grado, adjetivo) para una puntuacion SUS de 0 a 100."""
    if not 0 <= media <= 100:
        raise ValueError("La puntuacion SUS debe estar entre 0 y 100")
    for minimo, letra, adjetivo in GRADOS:
        if media >= minimo:
            return letra, adjetivo
    raise AssertionError("inalcanzable: el ultimo grado acepta desde 0")


def contribuciones(respuestas: list[int]) -> list[int]:
    """Contribucion (0-4) de cada item: impares valor-1, pares 5-valor."""
    if len(respuestas) != 10 or any(r not in (1, 2, 3, 4, 5) for r in respuestas):
        raise ValueError("Se requieren 10 respuestas con valores enteros de 1 a 5")
    return [(r - 1) if i % 2 == 1 else (5 - r) for i, r in enumerate(respuestas, start=1)]


def interpretar(media: float) -> str:
    if media > 68:
        return "Usabilidad BUENA"
    if media >= 50:
        return "Usabilidad ACEPTABLE"
    return "Usabilidad BAJA"


def leer_respuestas(ruta: str) -> list[list[int]]:
    with open(ruta, encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)
        faltantes = [c for c in COLUMNAS if c not in (lector.fieldnames or [])]
        if faltantes:
            raise ValueError(f"Faltan columnas: {', '.join(faltantes)}")
        return [[int(fila[c]) for c in COLUMNAS] for fila in lector if any((fila[c] or "").strip() for c in COLUMNAS)]


def resumen(puntuaciones: list[float]) -> dict:
    return {
        "participantes": len(puntuaciones),
        "media": round(statistics.mean(puntuaciones), 2),
        "desviacion": round(statistics.stdev(puntuaciones), 2) if len(puntuaciones) > 1 else 0.0,
        "minimo": min(puntuaciones),
        "maximo": max(puntuaciones),
        "interpretacion": interpretar(statistics.mean(puntuaciones)),
    }


def informe_markdown(respuestas: list[list[int]]) -> str:
    """Tablas Markdown: respuestas brutas, calculo paso a paso por participante y resumen global."""
    puntuaciones = [puntuacion_sus(r) for r in respuestas]
    media = statistics.mean(puntuaciones)
    letra, adjetivo = grado(media)
    lineas = ["### Respuestas brutas (escala 1-5)", ""]
    lineas.append("| Participante | " + " | ".join(COLUMNAS) + " |")
    lineas.append("|---|" + "---|" * len(COLUMNAS))
    for i, fila in enumerate(respuestas, start=1):
        lineas.append(f"| P{i:02d} | " + " | ".join(str(v) for v in fila) + " |")
    lineas += ["", "### Calculo paso a paso (impares: valor - 1; pares: 5 - valor; suma x 2,5)", ""]
    lineas.append("| Participante | " + " | ".join(f"C{i}" for i in range(1, 11)) + " | Suma | SUS = suma x 2,5 |")
    lineas.append("|---|" + "---|" * 10 + "---|---|")
    for i, fila in enumerate(respuestas, start=1):
        c = contribuciones(fila)
        lineas.append(f"| P{i:02d} | " + " | ".join(str(v) for v in c) + f" | {sum(c)} | {sum(c)} x 2,5 = {puntuaciones[i - 1]:.1f} |")
    r = resumen(puntuaciones)
    cumple = "SI" if media >= UMBRAL_ACEPTACION else "NO"
    lineas += [
        "",
        "### Resultado global",
        "",
        "| Indicador | Valor |",
        "|---|---|",
        f"| Participantes (n) | {r['participantes']} |",
        f"| SUS promedio | {media:.2f} ({' + '.join(f'{p:.1f}' for p in puntuaciones)}) / {len(puntuaciones)} |",
        f"| Desviacion estandar | {r['desviacion']} |",
        f"| Minimo / maximo | {r['minimo']} / {r['maximo']} |",
        f"| Grado (Sauro y Lewis) | {letra} - {adjetivo} |",
        f"| Cumple el umbral >= {UMBRAL_ACEPTACION} | {cumple} |",
    ]
    return "\n".join(lineas)


def main() -> None:
    argumentos = [a for a in sys.argv[1:] if a != "--markdown"]
    if len(argumentos) != 1:
        raise SystemExit("Uso: python scripts/usabilidad/procesar_sus.py respuestas.csv [--markdown]")
    respuestas = leer_respuestas(argumentos[0])
    if not respuestas:
        raise SystemExit("El archivo no contiene respuestas: aplique la encuesta antes de procesarla.")
    if "--markdown" in sys.argv:
        print(informe_markdown(respuestas))
        return
    puntuaciones = [puntuacion_sus(r) for r in respuestas]
    for i, p in enumerate(puntuaciones, start=1):
        print(f"Participante {i}: {p:.1f}")
    for clave, valor in resumen(puntuaciones).items():
        print(f"{clave}: {valor}")
    letra, adjetivo = grado(statistics.mean(puntuaciones))
    print(f"grado: {letra} ({adjetivo})")


if __name__ == "__main__":
    main()
