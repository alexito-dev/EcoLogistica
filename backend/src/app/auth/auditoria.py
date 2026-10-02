"""Eventos de acceso (base de RF-11.2): una línea JSON por evento, sin secretos."""

import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger("ecologistica.auditoria")

ACCIONES = {
    "LOGIN_OK",
    "LOGIN_FALLIDO",
    "BLOQUEO",
    "MFA_ENROLADO",
    "MFA_FALLIDO",
    "LOGOUT",
    "ACCESO_DENEGADO",
}


def registrar_evento(accion: str, correo: str | None, resultado: str) -> None:
    if accion not in ACCIONES:
        raise ValueError(f"Acción de auditoría desconocida: {accion}")
    logger.info(
        json.dumps(
            {
                "instante": datetime.now(timezone.utc).isoformat(),
                "accion": accion,
                "correo": correo,
                "resultado": resultado,
            },
            ensure_ascii=False,
        )
    )
