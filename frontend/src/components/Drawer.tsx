import { useEffect, useId, useRef, type ReactNode } from 'react'
import { X } from 'lucide-react'

interface Props {
  abierto: boolean
  titulo: string
  descripcion?: string
  onCerrar: () => void
  children: ReactNode
}

const FOCALIZABLES =
  'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'

/** Panel lateral modal: foco atrapado, Esc cierra y el foco vuelve al elemento que lo abrió. */
export default function Drawer({ abierto, titulo, descripcion, onCerrar, children }: Props) {
  const panelRef = useRef<HTMLDivElement>(null)
  const idTitulo = useId()
  const idDescripcion = useId()
  const onCerrarRef = useRef(onCerrar)
  useEffect(() => {
    onCerrarRef.current = onCerrar
  }, [onCerrar])

  useEffect(() => {
    if (!abierto) return
    const previo = document.activeElement as HTMLElement | null
    const panel = panelRef.current
    document.body.classList.add('sin-scroll')

    const enfocables = () => Array.from(panel?.querySelectorAll<HTMLElement>(FOCALIZABLES) ?? [])
    const primerCampo = panel?.querySelector<HTMLElement>('[data-foco-inicial]') ?? enfocables()[1] ?? panel
    primerCampo?.focus()

    function alPulsar(evento: KeyboardEvent) {
      if (evento.key === 'Escape') {
        evento.stopPropagation()
        onCerrarRef.current()
        return
      }
      if (evento.key !== 'Tab') return
      const lista = enfocables()
      if (lista.length === 0) return
      const primero = lista[0]
      const ultimo = lista[lista.length - 1]
      if (evento.shiftKey && document.activeElement === primero) {
        evento.preventDefault()
        ultimo.focus()
      } else if (!evento.shiftKey && document.activeElement === ultimo) {
        evento.preventDefault()
        primero.focus()
      }
    }

    document.addEventListener('keydown', alPulsar)
    return () => {
      document.removeEventListener('keydown', alPulsar)
      document.body.classList.remove('sin-scroll')
      previo?.focus?.()
    }
  }, [abierto])

  if (!abierto) return null

  return (
    <div className="drawer">
      <div className="drawer__fondo" onClick={onCerrar} aria-hidden="true" />
      <div
        ref={panelRef}
        className="drawer__panel"
        role="dialog"
        aria-modal="true"
        aria-labelledby={idTitulo}
        aria-describedby={descripcion ? idDescripcion : undefined}
        tabIndex={-1}
      >
        <header className="drawer__cabecera">
          <div>
            <h2 id={idTitulo}>{titulo}</h2>
            {descripcion && (
              <p id={idDescripcion} className="drawer__descripcion">
                {descripcion}
              </p>
            )}
          </div>
          <button type="button" className="icono-boton" onClick={onCerrar} aria-label="Cerrar panel">
            <X size={20} aria-hidden="true" />
          </button>
        </header>
        {children}
      </div>
    </div>
  )
}
