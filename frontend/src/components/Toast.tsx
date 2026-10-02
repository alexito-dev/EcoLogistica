import { useEffect } from 'react'
import { CircleCheck, X } from 'lucide-react'

interface Props {
  mensaje: string | null
  onCerrar: () => void
}

/** Aviso temporal de confirmación (se anuncia a lectores de pantalla). */
export default function Toast({ mensaje, onCerrar }: Props) {
  useEffect(() => {
    if (!mensaje) return
    const temporizador = window.setTimeout(onCerrar, 7000)
    return () => window.clearTimeout(temporizador)
  }, [mensaje, onCerrar])

  return (
    <div className="toast-zona" role="status" aria-live="polite">
      {mensaje && (
        <div className="toast">
          <span className="toast__icono">
            <CircleCheck size={20} aria-hidden="true" />
          </span>
          <p>{mensaje}</p>
          <button type="button" className="icono-boton" onClick={onCerrar} aria-label="Cerrar aviso">
            <X size={18} aria-hidden="true" />
          </button>
        </div>
      )}
    </div>
  )
}
