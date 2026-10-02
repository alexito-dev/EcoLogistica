import type { CSSProperties } from 'react'
import type { LucideIcon } from 'lucide-react'
import { useCountUp } from '../hooks/useCountUp'
import { formatoNumero } from '../lib/estados'

interface Props {
  titulo: string
  valor: number
  sufijo?: string
  detalle: string
  icono: LucideIcon
  indice?: number
}

export default function StatCard({ titulo, valor, sufijo, detalle, icono: Icono, indice = 0 }: Props) {
  const animado = useCountUp(valor)
  const mostrado = Number.isInteger(valor) ? Math.round(animado) : animado
  return (
    <article className="stat aparecer" style={{ '--i': indice } as CSSProperties}>
      <span className="stat__icono">
        <Icono size={22} aria-hidden="true" />
      </span>
      <p className="stat__titulo">{titulo}</p>
      <p className="stat__valor">
        {formatoNumero(mostrado)}
        {sufijo && <span className="stat__sufijo"> {sufijo}</span>}
      </p>
      <p className="stat__detalle">{detalle}</p>
    </article>
  )
}
