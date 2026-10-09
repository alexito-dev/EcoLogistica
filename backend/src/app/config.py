"""Configuración de la aplicación, leída de variables de entorno (.env)."""

import logging
import secrets
from functools import lru_cache
from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.pedidos.domain import Ambito


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    cors_origin: str = "http://localhost:3000"

    # Autenticación (RF-11.1, RNF-06). Sin valores reales en el repositorio.
    jwt_secret: str = ""
    cookie_secure: bool = False  # True cuando se sirve por HTTPS
    demo_clave: str = ""  # vacía: se genera una aleatoria y se muestra una vez en consola
    usuarios_archivo: Path = Path(__file__).resolve().parents[2] / ".data" / "usuarios.json"
    database_url: str | None = None

    # Ámbito geográfico configurable (RF-02.2). Rectángulo de aproximación para
    # desarrollo; debe validarse con el negocio y sustituirse por PostGIS (EN-005).
    ambito_lat_min: float = -12.20
    ambito_lat_max: float = -11.95
    ambito_lon_min: float = -75.35
    ambito_lon_max: float = -75.10
    ambito_distritos: str = "Huancayo,El Tambo,Chilca,Pilcomayo,San Agustín de Cajas"

    @model_validator(mode="after")
    def _validar_ambito(self) -> "Settings":
        if not (-90 <= self.ambito_lat_min < self.ambito_lat_max <= 90):
            raise ValueError("AMBITO_LAT_MIN debe ser menor que AMBITO_LAT_MAX (rango -90..90)")
        if not (-180 <= self.ambito_lon_min < self.ambito_lon_max <= 180):
            raise ValueError("AMBITO_LON_MIN debe ser menor que AMBITO_LON_MAX (rango -180..180)")
        if not self.distritos:
            raise ValueError("AMBITO_DISTRITOS no puede estar vacío")
        if len(self.jwt_secret) < 32 or "change" in self.jwt_secret:
            logging.getLogger("ecologistica").warning(
                "JWT_SECRET ausente o débil: se usa una clave aleatoria (las sesiones se pierden al reiniciar)."
            )
            self.jwt_secret = secrets.token_urlsafe(48)
        return self

    @property
    def distritos(self) -> tuple[str, ...]:
        return tuple(d.strip() for d in self.ambito_distritos.split(",") if d.strip())

    @property
    def ambito(self) -> Ambito:
        return Ambito(
            lat_min=self.ambito_lat_min,
            lat_max=self.ambito_lat_max,
            lon_min=self.ambito_lon_min,
            lon_max=self.ambito_lon_max,
            distritos=self.distritos,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
