"""Adaptador de usuarios en un archivo JSON local (desarrollo; un solo proceso).

El archivo vive en `backend/.data/` y está ignorado por Git: contiene hashes y secretos TOTP.
"""

import json
import os
import tempfile
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from threading import RLock

from app.auth.domain import EstadoUsuario, RegistroIntentos, Rol, Usuario


def _usuario_desde_dict(d: dict) -> Usuario:
    return Usuario(**{**d, "rol": Rol(d["rol"]), "estado": EstadoUsuario(d["estado"])})


def _intentos_a_dict(r: RegistroIntentos) -> dict:
    return {
        "fallos": [f.isoformat() for f in r.fallos],
        "bloqueado_hasta": r.bloqueado_hasta.isoformat() if r.bloqueado_hasta else None,
    }


def _intentos_desde_dict(d: dict) -> RegistroIntentos:
    return RegistroIntentos(
        fallos=[datetime.fromisoformat(f) for f in d.get("fallos", [])],
        bloqueado_hasta=datetime.fromisoformat(d["bloqueado_hasta"]) if d.get("bloqueado_hasta") else None,
    )


class UsuariosArchivoRepository:
    def __init__(self, ruta: Path) -> None:
        self._ruta = Path(ruta)
        self._lock = RLock()
        self._usuarios: dict[str, Usuario] = {}
        self._intentos: dict[str, RegistroIntentos] = {}
        self._cargar()

    def _cargar(self) -> None:
        if not self._ruta.exists():
            return
        datos = json.loads(self._ruta.read_text(encoding="utf-8"))
        self._usuarios = {u["id"]: _usuario_desde_dict(u) for u in datos.get("usuarios", [])}
        self._intentos = {c: _intentos_desde_dict(r) for c, r in datos.get("intentos", {}).items()}

    def _persistir(self) -> None:
        """Escritura atómica: archivo temporal en la misma carpeta y reemplazo."""
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        contenido = json.dumps(
            {
                "usuarios": [{**asdict(u), "rol": u.rol.value, "estado": u.estado.value} for u in self._usuarios.values()],
                "intentos": {c: _intentos_a_dict(r) for c, r in self._intentos.items()},
            },
            ensure_ascii=False,
            indent=2,
        )
        descriptor, temporal = tempfile.mkstemp(dir=self._ruta.parent, suffix=".tmp")
        with os.fdopen(descriptor, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
        os.replace(temporal, self._ruta)

    def obtener(self, usuario_id: str) -> Usuario | None:
        return self._usuarios.get(usuario_id)

    def obtener_por_correo(self, correo: str) -> Usuario | None:
        return next((u for u in self._usuarios.values() if u.correo == correo), None)

    def guardar(self, usuario: Usuario) -> None:
        with self._lock:
            self._usuarios[usuario.id] = usuario
            self._persistir()

    def contar(self) -> int:
        return len(self._usuarios)

    def intentos(self, correo: str) -> RegistroIntentos:
        registro = self._intentos.get(correo)
        return RegistroIntentos(list(registro.fallos), registro.bloqueado_hasta) if registro else RegistroIntentos()

    def guardar_intentos(self, correo: str, registro: RegistroIntentos) -> None:
        with self._lock:
            self._intentos[correo] = registro
            self._persistir()

    def limpiar_intentos(self, correo: str) -> None:
        with self._lock:
            if self._intentos.pop(correo, None) is not None:
                self._persistir()
