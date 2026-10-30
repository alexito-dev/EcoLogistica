"""Almacén de rutas guardadas en un archivo JSON local (desarrollo; un solo proceso).

Guarda una foto de la propuesta por fecha de reparto, de modo que sobreviva al reinicio de la API.
El archivo vive en `backend/.data/` y está ignorado por Git.
"""

import json
import os
import tempfile
from datetime import date
from pathlib import Path
from threading import RLock


class RutasGuardadasArchivo:
    def __init__(self, ruta: Path) -> None:
        self._ruta = Path(ruta)
        self._lock = RLock()
        self._registros: dict[str, dict] = {}
        if self._ruta.exists():
            self._registros = json.loads(self._ruta.read_text(encoding="utf-8"))

    def guardar(self, fecha: date, registro: dict) -> None:
        with self._lock:
            clave = fecha.isoformat()
            anterior = self._registros.get(clave)
            self._registros[clave] = registro
            try:
                self._persistir()
            except BaseException:
                if anterior is None:
                    self._registros.pop(clave, None)
                else:
                    self._registros[clave] = anterior
                raise

    def obtener(self, fecha: date) -> dict | None:
        with self._lock:
            return self._registros.get(fecha.isoformat())

    def _persistir(self) -> None:
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporal = tempfile.mkstemp(dir=self._ruta.parent, suffix=".tmp")
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as archivo:
                json.dump(self._registros, archivo, ensure_ascii=False, indent=2)
                archivo.flush()
                os.fsync(archivo.fileno())
            os.replace(temporal, self._ruta)
        except BaseException:
            if os.path.exists(temporal):
                os.unlink(temporal)
            raise
