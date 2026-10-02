import type { ReactNode } from 'react'

interface Props {
  titulo: string
  subtitulo: string
  accion: ReactNode
}

/** Cabecera con degradado de marca y colinas decorativas (ilustración propia en SVG). */
export default function Hero({ titulo, subtitulo, accion }: Props) {
  return (
    <section className="hero aparecer" aria-labelledby="titulo-pagina">
      <svg className="hero__arte" viewBox="0 0 600 200" preserveAspectRatio="xMaxYMax slice" aria-hidden="true">
        <circle cx="520" cy="46" r="26" className="hero__sol" />
        <path d="M0 170 C 120 120, 220 190, 340 150 S 520 110, 600 140 L 600 200 L 0 200 Z" className="hero__colina hero__colina--atras" />
        <path d="M0 190 C 140 150, 260 200, 400 170 S 540 160, 600 175 L 600 200 L 0 200 Z" className="hero__colina hero__colina--frente" />
        <g className="hero__arbol" transform="translate(452 112)">
          <rect x="-2" y="18" width="4" height="22" rx="2" />
          <circle cx="0" cy="12" r="14" />
        </g>
        <g className="hero__arbol hero__arbol--chico" transform="translate(492 128)">
          <rect x="-1.5" y="12" width="3" height="16" rx="1.5" />
          <circle cx="0" cy="8" r="10" />
        </g>
      </svg>
      <div className="hero__texto">
        <p className="hero__eyebrow">Planificación del día</p>
        <h1 id="titulo-pagina">{titulo}</h1>
        <p className="hero__subtitulo">{subtitulo}</p>
      </div>
      <div className="hero__accion">{accion}</div>
    </section>
  )
}
