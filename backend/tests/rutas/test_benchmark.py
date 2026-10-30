"""EN-001: el benchmark debe funcionar como puerta de calidad, no solo imprimir resultados."""

import sys
from types import SimpleNamespace

import pytest

from scripts import benchmark_rutas as benchmark


def test_benchmark_rechaza_duracion_superior_a_45_segundos(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["benchmark_rutas.py", "1"])
    tiempos = iter([0.0, 46.0])
    monkeypatch.setattr(benchmark, "perf_counter", lambda: next(tiempos))
    monkeypatch.setattr(benchmark, "planificar", lambda *args: SimpleNamespace(rutas=[]))

    with pytest.raises(SystemExit) as error:
        benchmark.main()

    assert error.value.code == 1
    assert "NO cumple" in capsys.readouterr().out


def test_benchmark_termina_si_cumple_umbral(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["benchmark_rutas.py", "1"])
    tiempos = iter([0.0, 0.5])
    monkeypatch.setattr(benchmark, "perf_counter", lambda: next(tiempos))
    monkeypatch.setattr(benchmark, "planificar", lambda *args: SimpleNamespace(rutas=[]))

    benchmark.main()

    assert "cumple" in capsys.readouterr().out
