import { createContext } from 'react'
import type { Usuario } from '../api/auth'

export type EstadoSesion = 'cargando' | 'anonimo' | 'autenticado'

export interface ValorAuth {
  estado: EstadoSesion
  usuario: Usuario | null
  aviso: string | null
  entrar: (usuario: Usuario) => void
  salir: () => Promise<void>
}

export const AuthContext = createContext<ValorAuth | null>(null)
