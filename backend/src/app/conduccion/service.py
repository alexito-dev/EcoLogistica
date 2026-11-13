"""Casos de uso de Conduccion: consultar la ruta asignada, registrar avances y reoptimizar tras incidencias."""

from datetime import date, datetime, timedelta, timezone
from uuid import UUID, uuid4

from app.auth.domain import Rol, Usuario
from app.auth.repository import UsuariosRepository
from app.conduccion.domain import (
    LONGITUD_MINIMA_NOTA,
    TERMINALES,
    TRANSICIONES_CONDUCTOR,
    EstadoParada,
    EventoParada,
)
from app.conduccion.repository import ConduccionRepository
from app.pedidos.domain import EstadoPedido, PedidoNoEncontradoError, ReglaDominioError
from app.pedidos.repository import PedidosRepository
from app.rutas.planificador import LIMA, VELOCIDAD_KMH, Punto, distancia_km

ESTADO_PEDIDO = {
    EstadoParada.PENDIENTE: EstadoPedido.PENDIENTE,
    EstadoParada.EN_RUTA: EstadoPedido.EN_RUTA,
    EstadoParada.ENTREGADO: EstadoPedido.ENTREGADO,
    EstadoParada.INCIDENCIA: EstadoPedido.FALLIDO,
    EstadoParada.CANCELADO: EstadoPedido.CANCELADO,
    EstadoParada.REPROGRAMADO: EstadoPedido.PENDIENTE,
}


class RutaNoGuardadaError(Exception):
    """No hay rutas guardadas para la fecha (HTTP 404)."""


class ParadaNoAsignadaError(Exception):
    """La parada no existe o no pertenece a una ruta asignada a quien consulta (HTTP 404)."""


def _fecha_hora(texto: str) -> datetime:
    """ISO 8601 con sufijo Z (Python 3.10 no lo admite en fromisoformat)."""
    return datetime.fromisoformat(texto.replace("Z", "+00:00"))


def _como_punto(parada: dict) -> Punto:
    return Punto(parada["latitud"], parada["longitud"])


class ConduccionService:
    def __init__(
        self,
        guardadas,
        conduccion: ConduccionRepository,
        pedidos: PedidosRepository,
        usuarios: UsuariosRepository,
    ) -> None:
        self._guardadas = guardadas
        self._conduccion = conduccion
        self._pedidos = pedidos
        self._usuarios = usuarios

    # --- lectura ---------------------------------------------------------------------------------

    def _registro(self, fecha: date) -> dict:
        registro = self._guardadas.obtener(fecha)
        if registro is None:
            raise RutaNoGuardadaError()
        return registro

    def _rutas_con_estado(self, fecha: date, solo_conductor: str | None = None) -> list[dict]:
        registro = self._registro(fecha)
        asignaciones = self._conduccion.asignaciones(fecha)
        eventos = self._conduccion.ultimos_eventos(fecha)
        nombres = {u.id: u.nombre for u in self._usuarios.listar_por_rol(Rol.CONDUCTOR)}
        salida: list[dict] = []
        for ruta in registro["vista"]["rutas"]:
            vehiculo_id = UUID(ruta["vehiculo"]["id"])
            conductor_id = asignaciones.get(vehiculo_id)
            if solo_conductor is not None and conductor_id != solo_conductor:
                continue
            paradas = []
            for parada in ruta["paradas"]:
                evento = eventos.get(UUID(parada["pedidoId"]))
                paradas.append(
                    {
                        **parada,
                        "estado": (evento.estado if evento else EstadoParada.PENDIENTE).value,
                        "nota": evento.nota if evento else None,
                        "actualizadoEn": evento.creado_en.isoformat() if evento else None,
                    }
                )
            conteo = lambda e: sum(1 for p in paradas if p["estado"] == e)  # noqa: E731
            salida.append(
                {
                    "vehiculo": ruta["vehiculo"],
                    "conductorId": conductor_id,
                    "conductorNombre": nombres.get(conductor_id) if conductor_id else None,
                    "paradas": paradas,
                    "distanciaKm": ruta["distanciaKm"],
                    "avance": {
                        "total": len(paradas),
                        "entregadas": conteo("ENTREGADO"),
                        "incidencias": conteo("INCIDENCIA"),
                        "canceladas": conteo("CANCELADO"),
                        "reprogramadas": conteo("REPROGRAMADO"),
                    },
                }
            )
        return salida

    def mi_ruta(self, fecha: date, conductor: Usuario) -> dict:
        rutas = self._rutas_con_estado(fecha, solo_conductor=conductor.id)
        return {"fecha": fecha, "deposito": self._registro(fecha)["vista"]["deposito"], "rutas": rutas}

    def seguimiento(self, fecha: date) -> dict:
        rutas = self._rutas_con_estado(fecha)
        incidencias = [
            {**p, "vehiculo": r["vehiculo"]["placa"], "conductorNombre": r["conductorNombre"]}
            for r in rutas
            for p in r["paradas"]
            if p["estado"] == "INCIDENCIA"
        ]
        return {
            "fecha": fecha,
            "deposito": self._registro(fecha)["vista"]["deposito"],
            "rutas": rutas,
            "incidencias": incidencias,
            "conductoresDisponibles": [
                {"id": u.id, "nombre": u.nombre} for u in self._usuarios.listar_por_rol(Rol.CONDUCTOR)
            ],
        }

    def historial(self, fecha: date, pedido_id: UUID) -> list[EventoParada]:
        return self._conduccion.historial(fecha, pedido_id)

    # --- escritura -------------------------------------------------------------------------------

    def asignar(self, fecha: date, vehiculo_id: UUID, conductor_id: str, por: Usuario) -> None:
        registro = self._registro(fecha)
        if not any(UUID(r["vehiculo"]["id"]) == vehiculo_id for r in registro["vista"]["rutas"]):
            raise ReglaDominioError({"vehiculoId": "El vehiculo no tiene una ruta guardada en esta fecha"})
        conductor = self._usuarios.obtener(conductor_id)
        if conductor is None or conductor.rol != Rol.CONDUCTOR:
            raise ReglaDominioError({"conductorId": "Seleccione una persona con rol Conductor"})
        self._conduccion.asignar(fecha, vehiculo_id, conductor_id, por.id)

    def _localizar(self, fecha: date, pedido_id: UUID, conductor_id: str | None) -> tuple[dict, dict]:
        for ruta in self._rutas_con_estado(fecha, solo_conductor=conductor_id):
            for parada in ruta["paradas"]:
                if UUID(parada["pedidoId"]) == pedido_id:
                    return ruta, parada
        raise ParadaNoAsignadaError()

    def _registrar(self, fecha: date, pedido_id: UUID, estado: EstadoParada, nota: str | None, por: Usuario, ahora: datetime) -> None:
        evento = EventoParada(uuid4(), fecha, pedido_id, estado, nota, por.id, ahora)
        self._conduccion.registrar_evento(evento)
        try:
            self._pedidos.actualizar_estado(pedido_id, ESTADO_PEDIDO[estado])
        except PedidoNoEncontradoError:
            pass  # el avance se conserva aunque el pedido se hubiera retirado

    def registrar_estado(
        self,
        fecha: date,
        pedido_id: UUID,
        nuevo: EstadoParada,
        nota: str | None,
        conductor: Usuario,
        ahora: datetime | None = None,
    ) -> dict:
        _, parada = self._localizar(fecha, pedido_id, conductor.id)
        actual = EstadoParada(parada["estado"])
        if nuevo not in TRANSICIONES_CONDUCTOR[actual]:
            permitidos = ", ".join(sorted(e.value for e in TRANSICIONES_CONDUCTOR[actual])) or "ninguno (estado final)"
            raise ReglaDominioError({"estado": f"No puede pasar de {actual.value} a {nuevo.value}. Permitidos: {permitidos}"})
        nota_limpia = (nota or "").strip() or None
        if nuevo == EstadoParada.INCIDENCIA and (nota_limpia is None or len(nota_limpia) < LONGITUD_MINIMA_NOTA):
            raise ReglaDominioError({"nota": f"Describa la incidencia (minimo {LONGITUD_MINIMA_NOTA} caracteres)"})
        self._registrar(fecha, pedido_id, nuevo, nota_limpia, conductor, ahora or datetime.now(timezone.utc))
        return self._localizar(fecha, pedido_id, conductor.id)[1]

    def reprogramar(self, fecha: date, pedido_id: UUID, por: Usuario, ahora: datetime | None = None) -> None:
        """Planificacion devuelve el pedido con incidencia a la cola para planificarlo de nuevo."""
        _, parada = self._localizar(fecha, pedido_id, None)
        if parada["estado"] != EstadoParada.INCIDENCIA.value:
            raise ReglaDominioError({"estado": "Solo se reprograma una parada con incidencia"})
        self._registrar(
            fecha, pedido_id, EstadoParada.REPROGRAMADO, "Reprogramado por Planificacion", por,
            ahora or datetime.now(timezone.utc),
        )

    def reoptimizar(self, fecha: date, por: Usuario, ahora: datetime | None = None) -> dict:
        """Reordena las paradas aun no atendidas de cada ruta (vecino mas cercano) sin tocar lo ya ejecutado.

        Las paradas entregadas, canceladas, reprogramadas o con incidencia conservan su lugar y su historial;
        las pendientes y en ruta se reordenan desde la ultima parada entregada (o el deposito) y se recalculan
        sus llegadas estimadas desde `ahora`.
        """
        ahora = ahora or datetime.now(timezone.utc)
        registro = self._registro(fecha)
        deposito = Punto(registro["vista"]["deposito"]["latitud"], registro["vista"]["deposito"]["longitud"])
        estados = {
            UUID(p["pedidoId"]): p["estado"]
            for r in self._rutas_con_estado(fecha)
            for p in r["paradas"]
        }
        reordenadas = 0
        for ruta in registro["vista"]["rutas"]:
            hechas = [p for p in ruta["paradas"] if EstadoParada(estados[UUID(p["pedidoId"])]) in TERMINALES
                      or estados[UUID(p["pedidoId"])] == "INCIDENCIA"]
            por_hacer = [p for p in ruta["paradas"] if p not in hechas]
            if len(por_hacer) < 2:
                continue
            entregadas = [p for p in hechas if estados[UUID(p["pedidoId"])] == "ENTREGADO"]
            actual = _como_punto(entregadas[-1]) if entregadas else deposito
            orden: list[dict] = []
            restantes = list(por_hacer)
            while restantes:
                siguiente = min(
                    restantes,
                    key=lambda p, desde=actual: (distancia_km(desde, _como_punto(p)), -p["prioridad"], p["codigo"]),
                )
                restantes.remove(siguiente)
                orden.append(siguiente)
                actual = _como_punto(siguiente)
            if [p["pedidoId"] for p in orden] == [p["pedidoId"] for p in por_hacer]:
                continue
            reloj = ahora
            previo = _como_punto(entregadas[-1]) if entregadas else deposito
            nuevas = []
            for parada in orden:
                reloj += timedelta(hours=distancia_km(previo, _como_punto(parada)) / VELOCIDAD_KMH)
                inicio = _fecha_hora(parada["ventanaInicio"])
                fin = _fecha_hora(parada["ventanaFin"])
                llegada = max(reloj, inicio)
                pedido = self._pedidos.obtener(UUID(parada["pedidoId"]))
                reloj = llegada + timedelta(minutes=pedido.tiempo_servicio_min if pedido else 10)
                previo = _como_punto(parada)
                nuevas.append({**parada, "llegadaEstimada": llegada.astimezone(LIMA).isoformat(), "dentroDeVentana": llegada <= fin})
            ruta["paradas"] = [*hechas, *nuevas]
            for i, parada in enumerate(ruta["paradas"], start=1):
                parada["orden"] = i
            reordenadas += 1
        if reordenadas:
            registro["reoptimizadaEn"] = ahora.isoformat()
            registro["reoptimizadaPor"] = por.nombre
            self._guardadas.guardar(fecha, registro)
        return {"rutasReordenadas": reordenadas}
