"""Huella de carbono por módulo (vista) de la interfaz, ANTES y DESPUÉS de la optimización Green IT.

Para cada vista se suma lo que el navegador descarga al entrar por primera vez (sin caché): HTML, JavaScript y CSS del
arranque, el logotipo de la barra lateral y los fragmentos (chunks) de esa vista. Todo se mide comprimido con Gzip, como lo
sirve `vite preview` en ambas mediciones. Luego se aplica el modelo SWDM v4 de `calcular_swdm.py`.

Uso (desde la raíz del repositorio):
    vite build --manifest   (en la versión ANTES y en la versión DESPUÉS)
    python scripts/calcular_swdm_modulos.py <frontend_antes> <frontend_despues> [salida.json]

Límite declarado: es transferencia estática; no incluye las respuestas de la API (muy pequeñas y comprimidas con Brotli o Gzip).
"""

import gzip
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from calcular_swdm import co2e_gramos, energia_kwh  # noqa: E402

# Vista -> clave del módulo en el manifiesto de Vite. «Pedidos» vive en el paquete de arranque.
VISTAS = {
    "Pedidos (arranque)": None,
    "Flota": "src/pages/PaginaFlota.tsx",
    "Rutas": "src/pages/PaginaRutas.tsx",
    "Indicadores": "src/pages/PaginaIndicadores.tsx",
    "Seguimiento": "src/pages/PaginaSeguimiento.tsx",
    "Mi ruta": "src/pages/PaginaMiRuta.tsx",
}


def gz(ruta: Path) -> int:
    """Tamaño Gzip; un CSS que el build incrusta en el HTML ya no existe como archivo y se cuenta en `index.html`."""
    return len(gzip.compress(ruta.read_bytes(), 6)) if ruta.exists() else 0


def logo(dist: Path) -> int:
    """Logotipo de la barra lateral: PNG original (no comprimible) o la versión AVIF de 64 px."""
    avif = dist / "img" / "logo-64.avif"
    if avif.exists():
        return avif.stat().st_size
    return (dist / "logo_ecologistica.png").stat().st_size


def cierre(manifiesto: dict, clave: str, visto: set, con_dinamicos: bool) -> None:
    if clave in visto or clave not in manifiesto:
        return
    visto.add(clave)
    nodo = manifiesto[clave]
    for hijo in nodo.get("imports", []):
        cierre(manifiesto, hijo, visto, con_dinamicos)
    if con_dinamicos:
        for hijo in nodo.get("dynamicImports", []):
            if "Mapa" in hijo or "leaflet" in hijo:
                cierre(manifiesto, hijo, visto, con_dinamicos)


def archivos(manifiesto: dict, claves: set) -> set:
    salida = set()
    for k in claves:
        nodo = manifiesto[k]
        salida.add(nodo["file"])
        salida.update(nodo.get("css", []))
    return salida


def medir(frontend: Path) -> dict:
    dist = frontend / "dist"
    manifiesto = json.loads((dist / ".vite" / "manifest.json").read_text(encoding="utf8"))
    base = set()
    cierre(manifiesto, "index.html", base, False)
    comun = archivos(manifiesto, base)
    comun_bytes = gz(dist / "index.html") + sum(gz(dist / f) for f in comun) + logo(dist)
    resultado = {}
    for vista, clave in VISTAS.items():
        if clave is None:
            resultado[vista] = comun_bytes
            continue
        if clave not in manifiesto:
            resultado[vista] = None  # la vista no existía en esa versión
            continue
        propios = set()
        cierre(manifiesto, clave, propios, True)
        extra = archivos(manifiesto, propios) - comun
        resultado[vista] = comun_bytes + sum(gz(dist / f) for f in extra)
    return resultado


def main() -> None:
    antes, despues = medir(Path(sys.argv[1])), medir(Path(sys.argv[2]))
    filas = []
    print("| Módulo | ANTES (B) | DESPUÉS (B) | Reducción | CO₂e ANTES (g) | CO₂e DESPUÉS (g) | Energía DESPUÉS (kWh) |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for vista in VISTAS:
        a, d = antes[vista], despues[vista]
        fila = {"modulo": vista, "bytes_antes": a, "bytes_despues": d}
        if a is None:
            print(f"| {vista} | no existía | {d:,} | — | — | {co2e_gramos(d):.4f} | {energia_kwh(d):.7f} |".replace(",", " "))
        else:
            fila["co2e_antes_g"], fila["co2e_despues_g"] = co2e_gramos(a), co2e_gramos(d)
            print(
                f"| {vista} | {a:,} | {d:,} | −{(1 - d / a) * 100:.1f} % | {co2e_gramos(a):.4f} | {co2e_gramos(d):.4f} | {energia_kwh(d):.7f} |".replace(",", " ")
            )
        filas.append(fila)
    if len(sys.argv) > 3:
        Path(sys.argv[3]).write_text(json.dumps(filas, indent=2, ensure_ascii=False), encoding="utf8")


if __name__ == "__main__":
    main()
