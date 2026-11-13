"""Indicadores OBSERVADOS de la ejecucion de rutas (ECO-14 y ECO-26).

A diferencia de los indicadores de planificacion (previstos), estos se calculan solo con avances que la
persona conductora registro: entregas a tiempo, incidencias y recorrido hasta la ultima entrega.
La distancia no viene de GPS: se estima con la misma formula de tramos del planificador, solo sobre los
tramos efectivamente completados. Si aun no hay entregas, los porcentajes son nulos (no se inventan).
"""

from datetime import date, datetime
from uuid import UUID

from app.conduccion.domain import EstadoParada
from app.conduccion.repository import ConduccionRepository
from app.rutas.planificador import Punto, distancia_km


class EjecucionNoDisponibleError(Exception):
    """No hay rutas guardadas para la fecha (HTTP 404)."""


def _fecha_hora(texto: str) -> datetime:
    return datetime.fromisoformat(texto.replace("Z", "+00:00"))


def calcular_ejecucion(guardadas, conduccion: ConduccionRepository, fecha: date) -> dict:
    registro = guardadas.obtener(fecha)
    if registro is None:
        raise EjecucionNoDisponibleError()
    eventos = conduccion.ultimos_eventos(fecha)
    deposito = Punto(registro["vista"]["deposito"]["latitud"], registro["vista"]["deposito"]["longitud"])

    conteo = {estado: 0 for estado in EstadoParada}
    a_tiempo = tarde = 0
    km_recorridos = km_previstos = co2_recorrido = co2_previsto = 0.0
    for ruta in registro["vista"]["rutas"]:
        paradas = ruta["paradas"]
        entregadas_idx = []
        for i, parada in enumerate(paradas):
            evento = eventos.get(UUID(parada["pedidoId"]))
            estado = evento.estado if evento else EstadoParada.PENDIENTE
            conteo[estado] += 1
            if estado == EstadoParada.ENTREGADO and evento is not None:
                entregadas_idx.append(i)
                if evento.creado_en <= _fecha_hora(parada["ventanaFin"]):
                    a_tiempo += 1
                else:
                    tarde += 1
        km_ruta = float(ruta["distanciaKm"])
        factor_co2 = float(ruta["co2Kg"]) / km_ruta if km_ruta > 0 else 0.0
        km_previstos += km_ruta
        co2_previsto += float(ruta["co2Kg"])
        if entregadas_idx:
            puntos = [deposito, *(Punto(p["latitud"], p["longitud"]) for p in paradas[: entregadas_idx[-1] + 1])]
            km = sum(distancia_km(a, b) for a, b in zip(puntos, puntos[1:]))
            km_recorridos += km
            co2_recorrido += km * factor_co2

    total = sum(conteo.values())
    entregadas = conteo[EstadoParada.ENTREGADO]
    return {
        "fecha": fecha,
        "paradas": total,
        "entregadas": entregadas,
        "incidencias": conteo[EstadoParada.INCIDENCIA],
        "canceladas": conteo[EstadoParada.CANCELADO],
        "reprogramadas": conteo[EstadoParada.REPROGRAMADO],
        "pendientes": conteo[EstadoParada.PENDIENTE] + conteo[EstadoParada.EN_RUTA],
        "entregasATiempo": a_tiempo,
        "entregasTarde": tarde,
        "puntualidadPct": round(a_tiempo / entregadas * 100, 1) if entregadas else None,
        "cumplimientoPct": round(entregadas / total * 100, 1) if total else None,
        "distanciaRecorridaKm": round(km_recorridos, 2),
        "distanciaPrevistaKm": round(km_previstos, 2),
        "co2RecorridoKg": round(co2_recorrido, 2),
        "co2PrevistoKg": round(co2_previsto, 2),
    }
