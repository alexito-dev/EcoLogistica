/** Cliente HTTP común: cookies de sesión, errores uniformes y aviso global de sesión vencida. */

export const API_URL: string = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1'

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

type Oyente = () => void
const oyentes401 = new Set<Oyente>()

/** Suscribe una función que se ejecuta cuando una solicitud protegida responde 401. */
export function alVencerSesion(oyente: Oyente): () => void {
  oyentes401.add(oyente)
  return () => oyentes401.delete(oyente)
}

interface Opciones {
  /** false en los pasos de inicio de sesión, donde un 401 es un error esperado del formulario. */
  avisarSesionVencida?: boolean
}

export async function solicitar<T>(ruta: string, init?: RequestInit, opciones: Opciones = {}): Promise<T> {
  const { avisarSesionVencida = true } = opciones
  let respuesta: Response
  try {
    respuesta = await fetch(`${API_URL}${ruta}`, {
      ...init,
      credentials: 'include',
      headers: { 'Content-Type': 'application/json', ...init?.headers },
    })
  } catch {
    throw new ApiError(0, 'No se pudo conectar con el servidor. Verifique su conexión e intente nuevamente.')
  }

  if (respuesta.status === 204) return undefined as T
  if (respuesta.ok) return (await respuesta.json()) as T

  let cuerpo: { message?: string; errors?: Record<string, string> } = {}
  try {
    cuerpo = await respuesta.json()
  } catch {
    /* cuerpo no JSON: se usa el mensaje genérico */
  }
  if (respuesta.status === 401 && avisarSesionVencida) oyentes401.forEach((o) => o())
  throw new ApiError(
    respuesta.status,
    cuerpo.message ?? 'Ocurrió un error inesperado. Intente nuevamente.',
    cuerpo.errors ?? {},
  )
}
