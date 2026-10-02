import { useCallback, useEffect, useMemo, useState, type ReactNode } from 'react'
import { cerrarSesion, obtenerSesion, type Usuario } from '../api/auth'
import { alVencerSesion } from '../api/http'
import { AuthContext, type EstadoSesion } from './contexto'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [estado, setEstado] = useState<EstadoSesion>('cargando')
  const [usuario, setUsuario] = useState<Usuario | null>(null)
  const [aviso, setAviso] = useState<string | null>(null)

  useEffect(() => {
    let activo = true
    obtenerSesion()
      .then((u) => {
        if (!activo) return
        setUsuario(u)
        setEstado(u ? 'autenticado' : 'anonimo')
      })
      .catch(() => {
        if (!activo) return
        setAviso('No se pudo conectar con el servidor. Verifique que la API esté en ejecución.')
        setEstado('anonimo')
      })
    return () => {
      activo = false
    }
  }, [])

  useEffect(
    () =>
      alVencerSesion(() => {
        setUsuario(null)
        setEstado('anonimo')
        setAviso('Su sesión venció. Inicie sesión nuevamente.')
      }),
    [],
  )

  const entrar = useCallback((u: Usuario) => {
    setUsuario(u)
    setAviso(null)
    setEstado('autenticado')
  }, [])

  const salir = useCallback(async () => {
    try {
      await cerrarSesion()
    } finally {
      setUsuario(null)
      setAviso('Sesión cerrada correctamente.')
      setEstado('anonimo')
    }
  }, [])

  const valor = useMemo(() => ({ estado, usuario, aviso, entrar, salir }), [estado, usuario, aviso, entrar, salir])
  return <AuthContext.Provider value={valor}>{children}</AuthContext.Provider>
}
