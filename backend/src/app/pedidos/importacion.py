"""Importacion de pedidos desde una plantilla CSV (ECO-18).

Todo o nada: si alguna fila tiene errores no se registra ninguna y se informan las filas con su campo.
Acepta coma o punto y coma (Excel en espanol) y fechas "AAAA-MM-DD HH:MM" en hora de Lima o ISO 8601 con desfase.
"""

import csv
import io
from datetime import datetime, timedelta, timezone

from pydantic import ValidationError

from app.pedidos.domain import Ambito, Pedido, ReglaDominioError, Ubicacion
from app.pedidos.repository import PedidosRepository
from app.pedidos.schemas import PedidoCrear

LIMA = timezone(timedelta(hours=-5))
MAX_FILAS = 500
MAX_CARACTERES = 1_000_000
MAX_ERRORES = 50

COLUMNAS = [
    "codigo", "direccion", "distrito", "latitud", "longitud", "ventana_inicio", "ventana_fin",
    "demanda_kg", "demanda_m3", "tiempo_servicio_min", "prioridad", "destinatario", "observacion",
]
OBLIGATORIAS = ["direccion", "distrito", "latitud", "longitud", "ventana_inicio", "ventana_fin"]
PLANTILLA_CSV = ",".join(COLUMNAS) + "\n"

_CAMPO_API = {
    "codigo": "codigo", "direccion": "direccion", "distrito": "distrito", "latitud": "latitud",
    "longitud": "longitud", "ventana_inicio": "ventanaInicio", "ventana_fin": "ventanaFin",
    "demanda_kg": "demandaKg", "demanda_m3": "demandaM3", "tiempo_servicio_min": "tiempoServicioMin",
    "prioridad": "prioridad", "destinatario": "destinatarioAlias", "observacion": "observacionOperativa",
}
_DESDE_API = {v: k for k, v in _CAMPO_API.items()}


class ImportacionInvalidaError(ReglaDominioError):
    """El archivo tiene errores (HTTP 422); `errors` indica la fila y el campo."""


def _fecha(texto: str) -> datetime:
    texto = texto.strip().replace("Z", "+00:00")
    for formato in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(texto, formato).replace(tzinfo=LIMA)
        except ValueError:
            continue
    return datetime.fromisoformat(texto)  # ISO 8601 con desfase; lanza ValueError si no es valida


def _numero(texto: str, delimitador: str) -> str:
    return texto.strip().replace(",", ".") if delimitador == ";" else texto.strip()


def _leer(contenido: str) -> tuple[list[dict[str, str]], str]:
    contenido = contenido.lstrip("﻿")
    if not contenido.strip():
        raise ImportacionInvalidaError({"archivo": "El archivo está vacío"})
    if len(contenido) > MAX_CARACTERES:
        raise ImportacionInvalidaError({"archivo": "El archivo supera 1 MB"})
    primera = contenido.splitlines()[0]
    delimitador = ";" if primera.count(";") > primera.count(",") else ","
    lector = csv.DictReader(io.StringIO(contenido), delimiter=delimitador)
    encabezados = [(h or "").strip().lower() for h in (lector.fieldnames or [])]
    faltantes = [c for c in OBLIGATORIAS if c not in encabezados]
    if faltantes:
        raise ImportacionInvalidaError({"archivo": f"Faltan columnas obligatorias: {', '.join(faltantes)}"})
    filas = [
        {(k or "").strip().lower(): (v or "").strip() for k, v in fila.items() if k}
        for fila in lector
    ]
    filas = [f for f in filas if any(f.values())]
    if not filas:
        raise ImportacionInvalidaError({"archivo": "El archivo no tiene filas de pedidos"})
    if len(filas) > MAX_FILAS:
        raise ImportacionInvalidaError({"archivo": f"Máximo {MAX_FILAS} pedidos por archivo"})
    return filas, delimitador


def _datos(fila: dict[str, str], delimitador: str) -> dict:
    datos: dict = {_CAMPO_API[c]: v for c, v in fila.items() if c in _CAMPO_API and v != ""}
    for campo in ("latitud", "longitud", "demandaKg", "demandaM3"):
        if campo in datos:
            datos[campo] = _numero(datos[campo], delimitador)
    for campo in ("ventanaInicio", "ventanaFin"):
        if campo in datos:
            datos[campo] = _fecha(datos[campo])
    return datos


def validar_archivo(contenido: str, ambito: Ambito, repositorio: PedidosRepository) -> list[PedidoCrear]:
    """Devuelve los pedidos validos o lanza `ImportacionInvalidaError` con todas las filas con error."""
    filas, delimitador = _leer(contenido)
    errores: dict[str, str] = {}
    validos: list[PedidoCrear] = []
    codigos: dict[str, int] = {}

    def anotar(numero: int, campo: str, mensaje: str) -> None:
        if len(errores) < MAX_ERRORES:
            errores[f"fila {numero} · {_DESDE_API.get(campo, campo)}"] = mensaje

    for indice, fila in enumerate(filas, start=2):  # la fila 1 es el encabezado
        try:
            datos = _datos(fila, delimitador)
            pedido = PedidoCrear.model_validate(datos)
        except ValueError as error:
            if isinstance(error, ValidationError):
                for detalle in error.errors():
                    campo = str(detalle["loc"][0]) if detalle["loc"] else "fila"
                    anotar(indice, campo, "Valor inválido o faltante")
            else:
                anotar(indice, "ventanaInicio", "Fecha inválida (use AAAA-MM-DD HH:MM)")
            continue
        try:
            Pedido.crear(
                codigo=pedido.codigo or "VALIDACION",
                ubicacion=Ubicacion(pedido.direccion, pedido.distrito, pedido.latitud, pedido.longitud),
                demanda_kg=pedido.demanda_kg, demanda_m3=pedido.demanda_m3,
                tiempo_servicio_min=pedido.tiempo_servicio_min, ventana_inicio=pedido.ventana_inicio,
                ventana_fin=pedido.ventana_fin, prioridad=pedido.prioridad, ambito=ambito,
            )
        except ReglaDominioError as error:
            for campo, mensaje in error.errors.items():
                anotar(indice, campo, mensaje)
            continue
        if pedido.codigo:
            codigo = Pedido.normalizar_codigo(pedido.codigo)
            if codigo in codigos:
                anotar(indice, "codigo", f"Código repetido en la fila {codigos[codigo]}")
                continue
            if repositorio.obtener_por_codigo(codigo) is not None:
                anotar(indice, "codigo", "Ya existe un pedido con este código")
                continue
            codigos[codigo] = indice
        validos.append(pedido)

    if errores:
        raise ImportacionInvalidaError(errores)
    return validos
