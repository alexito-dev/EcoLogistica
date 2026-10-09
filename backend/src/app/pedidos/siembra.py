"""Pedidos de demostración (datos sintéticos en el ámbito de Huancayo) para desarrollo y exposiciones.

Usan códigos propios (`DR-1001`…) para no consumir el correlativo `PED-000001` de los pedidos nuevos.
"""

from datetime import datetime, time, timedelta, timezone

from app.pedidos.domain import Ambito, Pedido, Ubicacion
from app.pedidos.repository import PedidosRepository

LIMA = timezone(timedelta(hours=-5))

# código, dirección, distrito, latitud, longitud, destinatario, kg, m3, inicio, fin, prioridad, observación
PEDIDOS_DEMO = [
    ("DR-1001", "Jr. Real 455", "Huancayo", -12.0686, -75.2103, "Bodega Santa Rosa", 35, 0.4, "08:00", "10:00", 2, None),
    ("DR-1002", "Av. Huancavelica 1120", "El Tambo", -12.0553, -75.2189, "Farmacia San Martín", 8, 0.1, "09:00", "10:30", 4,
     "Medicamentos: entregar en mostrador"),
    ("DR-1003", "Av. Ferrocarril 830", "Chilca", -12.0817, -75.2005, "Minimarket Los Andes", 120, 1.6, "10:00", "13:00", 3, None),
    ("DR-1004", "Jr. Lima 210", "Pilcomayo", -12.0478, -75.2462, "Restaurante El Wanka", 60, 0.8, "11:00", "14:00", 2, None),
    ("DR-1005", "Av. Mariscal Castilla 3950", "El Tambo", -12.0396, -75.2245, "Ferretería El Constructor", 250, 2.2, "14:00", "17:00", 1,
     "Carga pesada: requiere dos personas"),
    ("DR-1006", "Plaza principal s/n", "San Agustín de Cajas", -12.0010, -75.2475, "Panadería Cajas", 25, 0.3, "07:00", "08:30", 3, None),
]


def sembrar_pedidos_demo(repositorio: PedidosRepository, ambito: Ambito, ahora: datetime | None = None) -> int:
    """Registra los pedidos de demostración para el día siguiente si el repositorio está vacío."""
    if repositorio.listar(None, 1, 1)[1] > 0:
        return 0
    manana = ((ahora or datetime.now(LIMA)).astimezone(LIMA) + timedelta(days=1)).date()

    def hora(texto: str) -> datetime:
        return datetime.combine(manana, time.fromisoformat(texto), tzinfo=LIMA)

    for codigo, direccion, distrito, lat, lon, alias, kg, m3, ini, fin, prioridad, obs in PEDIDOS_DEMO:
        repositorio.guardar(
            Pedido.crear(
                codigo=codigo,
                ubicacion=Ubicacion(direccion, distrito, lat, lon),
                destinatario_alias=alias,
                demanda_kg=kg,
                demanda_m3=m3,
                tiempo_servicio_min=10,
                ventana_inicio=hora(ini),
                ventana_fin=hora(fin),
                prioridad=prioridad,
                observacion_operativa=obs,
                ambito=ambito,
            )
        )
    return len(PEDIDOS_DEMO)
