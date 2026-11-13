/** Cliente de Conducción: ruta asignada, avance de entregas, incidencias y reoptimización (Sprint 4). */

import type { Parada, Ruta, VistaPrevia } from './rutas'
import { solicitar } from './http'

export type EstadoParada = 'PENDIENTE' | 'EN_RUTA' | 'ENTREGADO' | 'INCIDENCIA' | 'CANCELADO' | 'REPROGRAMADO'

export const ETIQUETA_PARADA: Record<EstadoParada, string> = {
  PENDIENTE: 'Pendiente',
  EN_RUTA: 'En ruta',
  ENTREGADO: 'Entregado',
  INCIDENCIA: 'Incidencia',
  CANCELADO: 'Cancelado',
  REPROGRAMADO: 'Reprogramado',
}

export interface ParadaEjecucion extends Parada {
  estado: EstadoParada
  nota: string | null
  actualizadoEn: string | null
}

export interface RutaConduccion extends Omit<Ruta, 'paradas' | 'duracionMin' | 'cargaKg' | 'usoCapacidadPct' | 'co2Kg'> {
  conductorId: string | null
  conductorNombre: string | null
  paradas: ParadaEjecucion[]
  avance: { total: number; entregadas: number; incidencias: number; canceladas: number; reprogramadas: number }
}

export interface Deposito {
  nombre: string
  latitud: number
  longitud: number
}

export interface MiRuta {
  fecha: string
  deposito: Deposito
  rutas: RutaConduccion[]
}

export interface Incidencia {
  pedidoId: string
  codigo: string
  direccion: string
  distrito: string
  nota: string | null
  vehiculo: string
  conductorNombre: string | null
  actualizadoEn: string | null
}

export interface Seguimiento extends MiRuta {
  incidencias: Incidencia[]
  conductoresDisponibles: { id: string; nombre: string }[]
}

const q = encodeURIComponent

/** Ruta del conductor en la fecha, o null si Planificación aún no guardó rutas. */
export async function obtenerMiRuta(fecha: string): Promise<MiRuta | null> {
  try {
    return await solicitar<MiRuta>(`/conduccion/mi-ruta?fecha=${q(fecha)}`)
  } catch (e) {
    if (e instanceof Error && 'status' in e && (e as { status: number }).status === 404) return null
    throw e
  }
}

export function registrarEstado(pedidoId: string, fecha: string, estado: EstadoParada, nota?: string): Promise<ParadaEjecucion> {
  return solicitar(`/conduccion/paradas/${pedidoId}/estado`, {
    method: 'POST',
    body: JSON.stringify({ fecha, estado, nota: nota?.trim() || null }),
  })
}

export async function obtenerSeguimiento(fecha: string): Promise<Seguimiento | null> {
  try {
    return await solicitar<Seguimiento>(`/conduccion/seguimiento?fecha=${q(fecha)}`)
  } catch (e) {
    if (e instanceof Error && 'status' in e && (e as { status: number }).status === 404) return null
    throw e
  }
}

export function asignarConductor(fecha: string, vehiculoId: string, conductorId: string): Promise<void> {
  return solicitar('/conduccion/asignaciones', { method: 'PUT', body: JSON.stringify({ fecha, vehiculoId, conductorId }) })
}

export function reprogramarParada(pedidoId: string, fecha: string): Promise<void> {
  return solicitar(`/conduccion/paradas/${pedidoId}/reprogramar`, { method: 'POST', body: JSON.stringify({ fecha }) })
}

export function reoptimizarRutas(fecha: string): Promise<{ rutasReordenadas: number }> {
  return solicitar('/conduccion/reoptimizar', { method: 'POST', body: JSON.stringify({ fecha }) })
}

/** Adapta las rutas de Conducción a la forma que dibuja el mapa de Planificación. */
export function comoVistaPrevia(datos: MiRuta): VistaPrevia {
  return {
    fecha: datos.fecha,
    deposito: datos.deposito,
    rutas: datos.rutas.map((r) => ({
      ...r,
      paradas: r.paradas,
      duracionMin: 0,
      cargaKg: 0,
      usoCapacidadPct: 0,
      co2Kg: 0,
    })),
    sinAsignar: [],
    resumen: {
      pedidos: 0, asignados: 0, vehiculosUsados: datos.rutas.length, vehiculosDisponibles: datos.rutas.length,
      distanciaKm: 0, distanciaBaseKm: 0, co2Kg: 0, co2BaseKg: 0, ahorroCo2Pct: 0,
      paradasFueraDeVentana: 0, paradasFueraDeVentanaBase: 0,
    },
    supuestos: [],
  }
}
