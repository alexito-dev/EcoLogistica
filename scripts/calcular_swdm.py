"""Calcula la huella de carbono por visita con el Sustainable Web Design Model v4 (SWDM v4).

Constantes de https://sustainablewebdesign.org/estimating-digital-emissions/ (consultadas el 13/11/2026):
energía total 0,300 kWh/GB (operacional 0,194 + incorporada 0,106) e intensidad de red global 494 gCO2e/kWh.
Uso: python scripts/calcular_swdm.py lighthouse-reports/<antes>.report.json <despues>.report.json [visitas_anuales]
"""

import json
import sys

KWH_POR_GB = {"centro_datos": 0.067, "red": 0.072, "dispositivos": 0.161}  # operacional + incorporada
INTENSIDAD_G_KWH = 494.0
BYTES_POR_GB = 1024**3


def energia_kwh(bytes_transferidos: float) -> float:
    return bytes_transferidos / BYTES_POR_GB * sum(KWH_POR_GB.values())


def co2e_gramos(bytes_transferidos: float) -> float:
    return energia_kwh(bytes_transferidos) * INTENSIDAD_G_KWH


def metricas(ruta: str) -> dict:
    with open(ruta, encoding="utf8") as f:
        r = json.load(f)
    a = r["audits"]
    return {
        "rendimiento": round(r["categories"]["performance"]["score"] * 100),
        "accesibilidad": round(r["categories"]["accessibility"]["score"] * 100),
        "buenas_practicas": round(r["categories"]["best-practices"]["score"] * 100),
        "seo": round(r["categories"]["seo"]["score"] * 100),
        "fcp_s": round(a["first-contentful-paint"]["numericValue"] / 1000, 2),
        "lcp_s": round(a["largest-contentful-paint"]["numericValue"] / 1000, 2),
        "tbt_ms": round(a["total-blocking-time"]["numericValue"]),
        "cls": round(a["cumulative-layout-shift"]["numericValue"], 3),
        "bytes": int(a["total-byte-weight"]["numericValue"]),
        "solicitudes": len(a["network-requests"]["details"]["items"]),
    }


def main() -> None:
    antes, despues = metricas(sys.argv[1]), metricas(sys.argv[2])
    visitas = int(sys.argv[3]) if len(sys.argv) > 3 else 500_000
    for nombre, m in (("ANTES", antes), ("DESPUÉS", despues)):
        m["kwh_visita"] = round(energia_kwh(m["bytes"]), 7)
        m["co2e_g_visita"] = round(co2e_gramos(m["bytes"]), 4)
        m["co2e_kg_anual"] = round(m["co2e_g_visita"] * visitas / 1000, 2)
        print(nombre, json.dumps(m, ensure_ascii=False))
    print("Ahorro anual (kg CO2e):", round(antes["co2e_kg_anual"] - despues["co2e_kg_anual"], 2), f"con {visitas} visitas/año")


if __name__ == "__main__":
    main()
