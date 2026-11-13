"""Calcula la puntuacion SUS (System Usability Scale) de las respuestas de una encuesta.

Entrada: CSV con columnas P1..P10 (escala Likert 1-5), una fila por participante.
Salida: puntuacion por persona, media, desviacion, minimo, maximo e interpretacion.
Solo usa la biblioteca estandar. Uso: python scripts/usabilidad/procesar_sus.py respuestas.csv

Puntuacion estandar: impares (valor - 1), pares (5 - valor); suma x 2,5 (rango 0-100).
Interpretacion segun la guia de laboratorio: > 68 buena, 50-68 aceptable, < 50 baja.
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


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python scripts/usabilidad/procesar_sus.py respuestas.csv")
    respuestas = leer_respuestas(sys.argv[1])
    if not respuestas:
        raise SystemExit("El archivo no contiene respuestas: aplique la encuesta antes de procesarla.")
    puntuaciones = [puntuacion_sus(r) for r in respuestas]
    for i, p in enumerate(puntuaciones, start=1):
        print(f"Participante {i}: {p:.1f}")
    for clave, valor in resumen(puntuaciones).items():
        print(f"{clave}: {valor}")


if __name__ == "__main__":
    main()
