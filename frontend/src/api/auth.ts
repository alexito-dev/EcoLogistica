/** Cliente de autenticación: contraseña, segundo factor, sesión y cierre de sesión. */

import { ApiError, solicitar } from './http'

export type Rol = 'ADMIN' | 'PLANIFICADOR' | 'CONDUCTOR' | 'GERENTE' | 'AUDITOR'

export interface Usuario {
  nombre: string
  correo: string
  rol: Rol
}

export interface RespuestaLogin {
  paso: 'MFA' | 'ENROLAR'
  claveMfa: string | null
  otpauthUri: string | null
}

export const ETIQUETA_ROL: Record<Rol, string> = {
  ADMIN: 'Administrador',
  PLANIFICADOR: 'Planificador',
  CONDUCTOR: 'Conductor',
  GERENTE: 'Gerente',
  AUDITOR: 'Auditor',
}

export function iniciarSesion(correo: string, clave: string): Promise<RespuestaLogin> {
  return solicitar<RespuestaLogin>(
    '/auth/login',
    { method: 'POST', body: JSON.stringify({ correo, clave }) },
    { avisarSesionVencida: false },
  )
}

export function verificarCodigo(codigo: string): Promise<Usuario> {
  return solicitar<Usuario>('/auth/mfa', { method: 'POST', body: JSON.stringify({ codigo }) }, { avisarSesionVencida: false })
}

/** Usuario de la sesión vigente, o null si no hay sesión. */
export async function obtenerSesion(): Promise<Usuario | null> {
  try {
    return await solicitar<Usuario>('/auth/sesion', undefined, { avisarSesionVencida: false })
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) return null
    throw error
  }
}

export function cerrarSesion(): Promise<void> {
  return solicitar<void>('/auth/logout', { method: 'POST' }, { avisarSesionVencida: false })
}
