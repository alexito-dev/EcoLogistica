/** Cliente de la vista previa de rutas (RF-04). El backend arma la propuesta; aquí solo se muestra. */

import type { Combustible } from './flota'
import { solicitar } from './http'

export interface Parada {
  orden: number
  pedidoId: string
  codigo: string
  destinatarioAlias: string | null
  direccion: string
  distrito: string
  latitud: number
  longitud: number
  demandaKg: number
  prioridad: number
  ventanaInicio: string
  ventanaFin: string
  llegadaEstimada: string
  dentroDeVentana: boolean
}

export interface Ruta {
  vehiculo: {
    id: string
    placa: string
    tipo: string
    combustible: Combustible
    capacidadKg: number
    capacidadM3: number
  }
  paradas: Parada[]
  distanciaKm: number
  duracionMin: number
  cargaKg: number
  usoCapacidadPct: number
  co2Kg: number
}

export interface VistaPrevia {
  fecha: string
  deposito: { nombre: string; latitud: number; longitud: number }
  rutas: Ruta[]
  sinAsignar: { pedidoId: string; codigo: string; demandaKg: number; motivo: string }[]
  resumen: {
    pedidos: number
    asignados: number
    vehiculosUsados: number
    vehiculosDisponibles: number
    distanciaKm: number
    distanciaBaseKm: number
    co2Kg: number
    co2BaseKg: number
    ahorroCo2Pct: number
    paradasFueraDeVentana: number
    paradasFueraDeVentanaBase: number
  }
  supuestos: string[]
}

export function obtenerVistaPrevia(fecha: string): Promise<VistaPrevia> {
  return solicitar(`/rutas/vista-previa?fecha=${encodeURIComponent(fecha)}`)
}
