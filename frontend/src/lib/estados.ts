import type { Combustible } from '../api/flota'
import type { EstadoPedido } from '../api/pedidos'

export const ETIQUETA_ESTADO: Record<EstadoPedido, string> = {
  PENDIENTE: 'Pendiente',
  VALIDADO: 'Validado',
  ASIGNADO: 'Asignado',
  EN_RUTA: 'En ruta',
  ENTREGADO: 'Entregado',
  FALLIDO: 'Fallido',
  CANCELADO: 'Cancelado',
}

export const ETIQUETA_PRIORIDAD: Record<number, string> = {
  1: 'Baja',
  2: 'Normal',
  3: 'Alta',
  4: 'Urgente',
}

export const ETIQUETA_COMBUSTIBLE: Record<Combustible, string> = {
  DIESEL: 'Diésel',
  GASOLINA: 'Gasolina',
  GNV: 'GNV',
  ELECTRICO: 'Eléctrico',
  HIBRIDO: 'Híbrido',
}

/** Formato corto de la ventana: "05/10 08:00 – 12:00" (hora de Lima). */
export function formatoNumero(valor: number): string {
  return new Intl.NumberFormat('es-PE', { maximumFractionDigits: 2 }).format(valor)
}
