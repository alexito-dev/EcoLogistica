/** Cliente de la API de pedidos. Las reglas de negocio las decide el backend. */

import { API_URL, ApiError, solicitar } from './http'

export { ApiError } from './http'

export type EstadoPedido =
  | 'PENDIENTE'
  | 'VALIDADO'
  | 'ASIGNADO'
  | 'EN_RUTA'
  | 'ENTREGADO'
  | 'FALLIDO'
  | 'CANCELADO'

export interface Pedido {
  id: string
  codigo: string
  direccion: string
  distrito: string
  latitud: number
  longitud: number
  destinatarioAlias: string | null
  demandaKg: number
  demandaM3: number
  tiempoServicioMin: number
  ventanaInicio: string
  ventanaFin: string
  prioridad: number
  estado: EstadoPedido
  observacionOperativa: string | null
  creadoEn: string
  actualizadoEn: string
}

export type PedidoCrear = Partial<
  Pick<Pedido, 'direccion' | 'distrito' | 'latitud' | 'longitud' | 'ventanaInicio' | 'ventanaFin'>
> &
  Partial<
    Pick<
      Pedido,
      | 'demandaKg'
      | 'demandaM3'
      | 'tiempoServicioMin'
      | 'prioridad'
      | 'destinatarioAlias'
      | 'observacionOperativa'
    >
  > & { codigo?: string }

export interface ListadoPedidos {
  items: Pedido[]
  total: number
  pagina: number
  limite: number
}

export function crearPedido(datos: PedidoCrear): Promise<Pedido> {
  return solicitar<Pedido>('/pedidos', { method: 'POST', body: JSON.stringify(datos) })
}

/** Registros por página: bloques pequeños reducen el JSON, la memoria del navegador y el consumo de red. */
export const PEDIDOS_POR_PAGINA = 12

export function listarPedidos(
  pagina = 1,
  limite = PEDIDOS_POR_PAGINA,
  estado?: EstadoPedido,
): Promise<ListadoPedidos> {
  const filtro = estado ? `&estado=${estado}` : ''
  return solicitar<ListadoPedidos>(`/pedidos?pagina=${pagina}&limite=${limite}${filtro}`)
}

export interface ResultadoImportacion {
  importados: number
  codigos: string[]
}

/** Importa pedidos desde el contenido de la plantilla CSV (todo o nada; ECO-18). */
export function importarPedidos(contenido: string): Promise<ResultadoImportacion> {
  return solicitar<ResultadoImportacion>('/pedidos/importar', { method: 'POST', body: JSON.stringify({ contenido }) })
}

/** Texto de la plantilla CSV con los encabezados esperados. */
export async function obtenerPlantilla(): Promise<string> {
  const respuesta = await fetch(`${API_URL}/pedidos/plantilla`, { credentials: 'include' })
  if (!respuesta.ok) throw new ApiError(respuesta.status, 'No se pudo descargar la plantilla.')
  return respuesta.text()
}
