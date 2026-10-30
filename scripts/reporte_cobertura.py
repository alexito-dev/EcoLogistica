#!/usr/bin/env python3
"""Auditoría de cobertura combinada: Cobertura XML (Python) + LCOV (TypeScript).

Criterio proxy transparente: (líneas cubiertas + ramas cubiertas) /
(líneas ejecutables + ramas instrumentadas), sin excluir módulos de aplicación.
No sustituye el valor oficial importado y calculado por SonarQube.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def python_coverage(path: Path) -> dict[str, int]:
    root = ET.parse(path).getroot()
    counts = {"lines": 0, "covered_lines": 0, "branches": 0, "covered_branches": 0}
    for line in root.findall(".//class/lines/line"):
        counts["lines"] += 1
        counts["covered_lines"] += int(int(line.attrib.get("hits", "0")) > 0)
        if line.attrib.get("branch") == "true":
            match = re.search(r"\((\d+)/(\d+)\)", line.attrib.get("condition-coverage", ""))
            if match:
                counts["covered_branches"] += int(match.group(1))
                counts["branches"] += int(match.group(2))
            else:
                raise ValueError("Cobertura condicional sin conteo detallado en línea Python")
    if not counts["lines"] or not counts["branches"]:
        raise ValueError("Se requieren líneas y ramas Python: pytest --cov-branch --cov-report=xml")
    return counts


def typescript_coverage(path: Path) -> dict[str, int]:
    counts = {"lines": 0, "covered_lines": 0, "branches": 0, "covered_branches": 0}
    files = 0
    for record in path.read_text(encoding="utf-8").split("end_of_record"):
        if not record.strip():
            continue
        fields = dict(
            line.split(":", 1) for line in record.splitlines()
            if ":" in line and line.split(":", 1)[0] in {"SF", "LF", "LH", "BRF", "BRH"}
        )
        if not fields.get("SF"):
            continue
        files += 1
        for metric, field in (
            ("lines", "LF"),
            ("covered_lines", "LH"),
            ("branches", "BRF"),
            ("covered_branches", "BRH"),
        ):
            counts[metric] += int(fields.get(field, "0"))
    if files == 0 or counts["lines"] == 0 or counts["branches"] == 0:
        raise ValueError("Faltan métricas de líneas/ramas LCOV del frontend")
    return counts


def pct(num: int, den: int) -> float:
    return round(100 * num / den, 2) if den else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", type=Path, default=Path("backend/coverage.xml"))
    parser.add_argument("--frontend", type=Path, default=Path("frontend/coverage/lcov.info"))
    parser.add_argument("--min", dest="minimum", type=float, default=0.0,
                        help="Umbral combinado para fallar CI; 0: informe diagnóstico")
    args = parser.parse_args()
    backend = python_coverage(args.backend)
    frontend = typescript_coverage(args.frontend)
    total = {k: backend[k] + frontend[k] for k in backend}
    coverage = pct(total["covered_lines"] + total["covered_branches"],
                   total["lines"] + total["branches"])
    rows = [
        "# Cobertura verificable del commit",
        "",
        f"**Commit:** `{os.environ.get('GITHUB_SHA', 'ejecución local')}`",
        "",
        "| Área | Líneas cubiertas | Cobertura líneas | Ramas cubiertas | Cobertura ramas | Cobertura combinada |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for title, counter in [("Backend Python", backend), ("Frontend TypeScript", frontend),
                           ("Total ponderado", total)]:
        rows.append(
            f"| {title} | {counter['covered_lines']}/{counter['lines']} "
            f"| {pct(counter['covered_lines'], counter['lines'])}% "
            f"| {counter['covered_branches']}/{counter['branches']} "
            f"| {pct(counter['covered_branches'], counter['branches'])}% "
            f"| {pct(counter['covered_lines'] + counter['covered_branches'], counter['lines'] + counter['branches'])}% |"
        )
    rows += [
        "",
        f"**Umbral obligatorio del indicador combinado:** {args.minimum}% (objetivo 95%).",
        "",
        "> Indicador técnico de seguimiento basado en XML+LCOV. SonarQube calcula "
        "su propia cobertura después de importar estos informes, y ese resultado "
        "debe contrastarse con el panel en el mismo commit.",
        "",
    ]
    result = "\n".join(rows)
    print(result)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(result + "\n")
    if args.minimum and coverage < args.minimum:
        raise SystemExit(
            f"Cobertura combinada {coverage}% inferior al mínimo requerido {args.minimum}%"
        )


if __name__ == "__main__":
    main()
