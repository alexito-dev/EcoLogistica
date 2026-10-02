"""Dominio de pedidos: entidad y reglas de negocio (RN-001, RF-02.2).

No depende de FastAPI ni de la persistencia.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4


class EstadoPedido(str, Enum):
    """Dominio `estado_pedido` del modelo físico (documento 11)."""

    PENDIENTE = "PENDIENTE"
    VALIDADO = "VALIDADO"
    ASIGNADO = "ASIGNADO"
    EN_RUTA = "EN_RUTA"
    ENTREGADO = "ENTREGADO"
    FALLIDO = "FALLIDO"
    CANCELADO = "CANCELADO"


class ReglaDominioError(Exception):
    """Regla semántica incumplida (HTTP 422). `errors` indica el campo a corregir."""

    def __init__(self, errors: dict[str, str]):
        super().__init__("Regla de negocio incumplida")
        self.errors = errors


class CodigoDuplicadoError(Exception):
    """El código de pedido ya existe (HTTP 409)."""

    def __init__(self, codigo: str):
        super().__init__(f"Ya existe un pedido con el código {codigo}")
        self.codigo = codigo


class PedidoNoEncontradoError(Exception):
    """El pedido no existe (HTTP 404)."""

    def __init__(self, pedido_id: UUID):
        super().__init__("Pedido no encontrado")
        self.pedido_id = pedido_id


@dataclass(frozen=True)
class Ambito:
    """Ámbito geográfico configurado (rectángulo envolvente y distritos)."""

    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    distritos: tuple[str, ...]

    def contiene(self, latitud: float, longitud: float) -> bool:
        return self.lat_min <= latitud <= self.lat_max and self.lon_min <= longitud <= self.lon_max

    def distrito_permitido(self, distrito: str) -> bool:
        return distrito.strip().casefold() in {d.casefold() for d in self.distritos}


@dataclass(frozen=True)
class Ubicacion:
    """Equivale a una fila de `ubicaciones`: punto = POINT(longitud latitud), SRID 4326."""

    direccion_referencial: str
    distrito: str
    latitud: float
    longitud: float
    fuente: str = "MANUAL"


@dataclass(frozen=True)
class Pedido:
    id: UUID
    codigo: str
    ubicacion: Ubicacion
    destinatario_alias: str | None
    demanda_kg: float
    demanda_m3: float
    tiempo_servicio_min: int
    ventana_inicio: datetime
    ventana_fin: datetime
    prioridad: int
    estado: EstadoPedido
    observacion_operativa: str | None
    creado_en: datetime
    actualizado_en: datetime

    @staticmethod
    def normalizar_codigo(codigo: str) -> str:
        return codigo.strip().upper()

    @classmethod
    def crear(
        cls,
        *,
        codigo: str,
        ubicacion: Ubicacion,
        demanda_kg: float,
        demanda_m3: float,
        tiempo_servicio_min: int,
        ventana_inicio: datetime,
        ventana_fin: datetime,
        prioridad: int,
        ambito: Ambito,
        destinatario_alias: str | None = None,
        observacion_operativa: str | None = None,
        ahora: datetime | None = None,
    ) -> "Pedido":
        """Crea un pedido `PENDIENTE` o lanza `ReglaDominioError` con el campo afectado."""
        errores: dict[str, str] = {}

        if demanda_kg < 0:
            errores["demandaKg"] = "No puede ser negativa"
        if demanda_m3 < 0:
            errores["demandaM3"] = "No puede ser negativa"
        if demanda_kg <= 0 and demanda_m3 <= 0 and not errores:
            errores["demandaKg"] = "Al menos una demanda (kg o m3) debe ser mayor que cero"
        if tiempo_servicio_min <= 0:
            errores["tiempoServicioMin"] = "Debe ser mayor que cero"
        if not 1 <= prioridad <= 4:
            errores["prioridad"] = "Debe estar entre 1 (baja) y 4 (urgente)"
        if ventana_inicio.tzinfo is None or ventana_fin.tzinfo is None:
            errores["ventanaInicio"] = "Las fechas deben incluir zona horaria"
        elif ventana_fin <= ventana_inicio:
            errores["ventanaFin"] = "La hora final debe ser posterior a la hora inicial"
        if not ambito.contiene(ubicacion.latitud, ubicacion.longitud):
            errores["latitud"] = "Fuera del ámbito geográfico configurado"
            errores["longitud"] = "Fuera del ámbito geográfico configurado"
        if not ambito.distrito_permitido(ubicacion.distrito):
            errores["distrito"] = "Distrito no incluido en el ámbito configurado"

        if errores:
            raise ReglaDominioError(errores)

        momento = ahora or datetime.now(timezone.utc)
        return cls(
            id=uuid4(),
            codigo=cls.normalizar_codigo(codigo),
            ubicacion=ubicacion,
            destinatario_alias=destinatario_alias,
            demanda_kg=demanda_kg,
            demanda_m3=demanda_m3,
            tiempo_servicio_min=tiempo_servicio_min,
            ventana_inicio=ventana_inicio.astimezone(timezone.utc),
            ventana_fin=ventana_fin.astimezone(timezone.utc),
            prioridad=prioridad,
            estado=EstadoPedido.PENDIENTE,
            observacion_operativa=observacion_operativa,
            creado_en=momento,
            actualizado_en=momento,
        )
