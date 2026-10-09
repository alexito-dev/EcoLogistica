import { solicitar } from './http'

export type Combustible = 'DIESEL' | 'GASOLINA' | 'GNV' | 'ELECTRICO' | 'HIBRIDO'
export type EstadoVehiculo = 'DISPONIBLE' | 'MANTENIMIENTO' | 'INACTIVO'

export interface Vehiculo {
  id: string
  placa: string
  tipo: string
  capacidadKg: number
  capacidadM3: number
  combustible: Combustible
  consumoBasePor100km: number
  factorEmisionKgco2eUnidad: number | null
  anio: number | null
  estado: EstadoVehiculo
  creadoEn: string | null
  actualizadoEn: string | null
  disponibilidad: {
    fecha: string
    turnoInicio: string
    turnoFin: string
    disponible: boolean
    restriccionCirculacion: string | null
  } | null
  elegibleParaPlanificar: boolean
}

export interface VehiculoGuardar {
  placa: string
  tipo: string
  capacidadKg: number
  capacidadM3: number
  combustible: Combustible
  consumoBasePor100km: number
  factorEmisionKgco2eUnidad: number | null
  anio: number | null
  estado: EstadoVehiculo
}

export function listarVehiculos(fecha: string): Promise<{ items: Vehiculo[] }> {
  return solicitar(`/vehiculos?fecha=${encodeURIComponent(fecha)}`)
}

export function crearVehiculo(datos: VehiculoGuardar): Promise<Vehiculo> {
  return solicitar('/vehiculos', { method: 'POST', body: JSON.stringify(datos) })
}

export function actualizarVehiculo(id: string, datos: VehiculoGuardar): Promise<Vehiculo> {
  return solicitar(`/vehiculos/${id}`, { method: 'PUT', body: JSON.stringify(datos) })
}

export function guardarDisponibilidad(
  id: string,
  datos: { fecha: string; turnoInicio: string; turnoFin: string; disponible: boolean; restriccionCirculacion: string | null },
): Promise<Vehiculo> {
  return solicitar(`/vehiculos/${id}/disponibilidad`, { method: 'PUT', body: JSON.stringify(datos) })
}
