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
