/** Cliente del dashboard de indicadores. Los cálculos los hace el backend. */

import type { Combustible } from './flota'
import { solicitar } from './http'
import type { EstadoPedido } from './pedidos'

export interface Indicadores {
  fecha: string
  pedidos: {
    total: number
    pesoKg: number
    porEstado: { estado: EstadoPedido; cantidad: number }[]
    porDistrito: { distrito: string; cantidad: number; pesoKg: number }[]
    porPrioridad: { prioridad: number; cantidad: number }[]
  }
  flota: {
    total: number
    aptos: number
    capacidadAptaKg: number
    porCombustible: { combustible: Combustible; cantidad: number }[]
  }
  dia: {
    pedidos: number
    asignados: number
    demandaKg: number
    usoCapacidadPct: number
    distanciaKm: number
    distanciaBaseKm: number
    co2Kg: number
    co2BaseKg: number
    ahorroCo2Pct: number
    paradasATiempoPct: number
  }
}

export function obtenerIndicadores(fecha: string): Promise<Indicadores> {
  return solicitar(`/indicadores?fecha=${encodeURIComponent(fecha)}`)
}

/** Resultados observados con las entregas que Conducción registró (ECO-14 y ECO-26). */
export interface Ejecucion {
  fecha: string
  paradas: number
  entregadas: number
  incidencias: number
  canceladas: number
  reprogramadas: number
  pendientes: number
  entregasATiempo: number
  entregasTarde: number
  puntualidadPct: number | null
  cumplimientoPct: number | null
  distanciaRecorridaKm: number
  distanciaPrevistaKm: number
  co2RecorridoKg: number
  co2PrevistoKg: number
}

/** Ejecución de la fecha, o null si aún no hay rutas guardadas. */
export async function obtenerEjecucion(fecha: string): Promise<Ejecucion | null> {
  try {
    return await solicitar<Ejecucion>(`/indicadores/ejecucion?fecha=${encodeURIComponent(fecha)}`)
  } catch (e) {
    if (e instanceof Error && 'status' in e && (e as { status: number }).status === 404) return null
    throw e
  }
}
