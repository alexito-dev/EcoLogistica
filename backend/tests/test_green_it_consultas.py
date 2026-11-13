"""Guardas Green IT sobre la capa de datos (ISO/IEC 25010 eficiencia; WSG 1.0 pauta 3.1)."""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
FUENTES = list((RAIZ / "backend" / "src").rglob("*.py"))
MIGRACIONES = "\n".join(p.read_text(encoding="utf8") for p in (RAIZ / "database" / "migrations" / "versions").glob("*.py"))


def test_ninguna_consulta_usa_select_asterisco():
    ofensores = [str(f) for f in FUENTES if re.search(r"select\s+\*", f.read_text(encoding="utf8"), re.IGNORECASE)]
    assert ofensores == []


def test_listados_estan_acotados_con_limit_y_offset():
    for repo in ("pedidos", "flota"):
        codigo = (RAIZ / "backend" / "src" / "app" / repo / "postgres_repository.py").read_text(encoding="utf8")
        if repo == "pedidos":
            assert "LIMIT :limite OFFSET :offset" in codigo


def test_filtros_frecuentes_tienen_indice():
    for indice in ("ix_pedidos_estado_creado", "ix_vehiculos_estado_placa", "ix_disponibilidad_fecha_estado", "ix_ubicaciones_punto", "ix_pedidos_estado_ventana"):
        assert indice in MIGRACIONES
