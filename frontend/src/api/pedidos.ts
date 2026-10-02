/** Cliente de la API de pedidos. Las reglas de negocio las decide el backend. */

const API_URL: string = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1'

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

/** Error de la API con detalle por campo ({ status, message, errors }). */
export class ApiError extends Error {
  readonly status: number
  readonly errors: Record<string, string>

  constructor(status: number, message: string, errors: Record<string, string> = {}) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.errors = errors
  }
}

async function solicitar<T>(ruta: string, init?: RequestInit): Promise<T> {
  let respuesta: Response
  try {
    respuesta = await fetch(`${API_URL}${ruta}`, {
      ...init,
      headers: { 'Content-Type': 'application/json', ...init?.headers },
    })
  } catch {
    throw new ApiError(0, 'No se pudo conectar con el servidor. Verifique su conexión e intente nuevamente.')
  }

  if (respuesta.ok) return (await respuesta.json()) as T

  let cuerpo: { message?: string; errors?: Record<string, string> } = {}
  try {
    cuerpo = await respuesta.json()
  } catch {
    /* cuerpo no JSON: se usa el mensaje genérico */
  }
  throw new ApiError(
    respuesta.status,
    cuerpo.message ?? 'Ocurrió un error inesperado. Intente nuevamente.',
    cuerpo.errors ?? {},
  )
}

export function crearPedido(datos: PedidoCrear): Promise<Pedido> {
  return solicitar<Pedido>('/pedidos', { method: 'POST', body: JSON.stringify(datos) })
}

export function listarPedidos(pagina = 1, limite = 20): Promise<ListadoPedidos> {
  return solicitar<ListadoPedidos>(`/pedidos?pagina=${pagina}&limite=${limite}`)
}
