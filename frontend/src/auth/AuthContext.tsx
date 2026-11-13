import { useCallback, useEffect, useMemo, useState, type ReactNode } from 'react'
import { cerrarSesion, obtenerSesion, type Usuario } from '../api/auth'
import { alVencerSesion } from '../api/http'
import { AuthContext, type EstadoSesion } from './contexto'

const MARCA_SESION = 'eco.sesion'

/**
 * La cookie de sesión es HttpOnly: el navegador no puede saber si existe. Una marca local indica que esta persona
 * ya inició sesión; sin ella se muestra el acceso de inmediato y se evita una solicitud bloqueante a la API
 * (menos tiempo hasta el primer contenido y menos transferencia para quien aún no tiene sesión). El servidor
 * sigue siendo la única autoridad: la marca solo decide si vale la pena preguntarle.
 */
function recordada(): boolean {
  try {
    return localStorage.getItem(MARCA_SESION) === '1'
  } catch {
    return true // sin almacenamiento disponible: se consulta al servidor como antes
  }
}

function recordar(valor: boolean): void {
  try {
    if (valor) localStorage.setItem(MARCA_SESION, '1')
    else localStorage.removeItem(MARCA_SESION)
  } catch {
    /* sin almacenamiento: no pasa nada, solo se consulta al servidor en la próxima carga */
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [estado, setEstado] = useState<EstadoSesion>(() => (recordada() ? 'cargando' : 'anonimo'))
  const [usuario, setUsuario] = useState<Usuario | null>(null)
  const [aviso, setAviso] = useState<string | null>(null)

  useEffect(() => {
    if (!recordada()) return
    let activo = true
    obtenerSesion()
      .then((u) => {
        if (!activo) return
        if (!u) recordar(false)
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
        recordar(false)
        setUsuario(null)
        setEstado('anonimo')
        setAviso('Su sesión venció. Inicie sesión nuevamente.')
      }),
    [],
  )

  const entrar = useCallback((u: Usuario) => {
    recordar(true)
    setUsuario(u)
    setAviso(null)
    setEstado('autenticado')
  }, [])

  const salir = useCallback(async () => {
    try {
      await cerrarSesion()
    } finally {
      recordar(false)
      setUsuario(null)
      setAviso('Sesión cerrada correctamente.')
      setEstado('anonimo')
    }
  }, [])

  const valor = useMemo(() => ({ estado, usuario, aviso, entrar, salir }), [estado, usuario, aviso, entrar, salir])
  return <AuthContext.Provider value={valor}>{children}</AuthContext.Provider>
}
