/** Cliente de la API de pedidos. Las reglas de negocio las decide el backend. */

import { solicitar } from './http'

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

export function listarPedidos(pagina = 1, limite = 20): Promise<ListadoPedidos> {
  return solicitar<ListadoPedidos>(`/pedidos?pagina=${pagina}&limite=${limite}`)
}
