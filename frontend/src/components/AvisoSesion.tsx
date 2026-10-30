import { useEffect, useRef, useState } from 'react'
import { Clock } from 'lucide-react'
import { obtenerSesion } from '../api/auth'
import { alHaberActividad } from '../api/http'
import { useAuth } from '../auth/useAuth'

/** El servidor cierra la sesión tras 15 minutos sin actividad (RNF-06). */
const INACTIVIDAD_MS = 15 * 60_000
const AVISO_ANTES_MS = 2 * 60_000

interface Props {
  inactividadMs?: number
  avisoAntesMs?: number
}

/** Avisa antes de que venza la sesión y deja extenderla (WCAG 2.2.1 Tiempo ajustable). */
export default function AvisoSesion({ inactividadMs = INACTIVIDAD_MS, avisoAntesMs = AVISO_ANTES_MS }: Props) {
  const { estado } = useAuth()
  const ultimaActividad = useRef(0)
  const [restanteMs, setRestanteMs] = useState<number | null>(null)

  useEffect(
    () =>
      alHaberActividad(() => {
        ultimaActividad.current = Date.now()
        setRestanteMs(null)
      }),
    [],
  )

  useEffect(() => {
    if (estado !== 'autenticado') return
    ultimaActividad.current = Date.now()
    const reloj = setInterval(() => {
      const restante = inactividadMs - (Date.now() - ultimaActividad.current)
      setRestanteMs(restante <= avisoAntesMs ? Math.max(restante, 0) : null)
    }, 1000)
    return () => clearInterval(reloj)
  }, [estado, inactividadMs, avisoAntesMs])

  if (estado !== 'autenticado' || restanteMs === null) return null

  const minutos = Math.floor(restanteMs / 60_000)
  const segundos = String(Math.floor((restanteMs % 60_000) / 1000)).padStart(2, '0')
  return (
    <div role="alert" className="aviso-sesion">
      <Clock size={20} aria-hidden="true" />
      <p>
        Su sesión vencerá por inactividad en <strong>{minutos}:{segundos}</strong>.
      </p>
      <button type="button" className="boton boton--primario boton--chico" onClick={() => void obtenerSesion().catch(() => undefined)}>
        Seguir conectado
      </button>
    </div>
  )
}
