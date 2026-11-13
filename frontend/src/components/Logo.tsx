interface Props {
  /** Lado en píxeles con el que se muestra (la imagen se sirve a 64 px o 128 px según la densidad). */
  tamano: 32 | 40 | 56
}

/**
 * Logotipo en formatos de nueva generación (AVIF > WebP > PNG) con `srcset` por densidad.
 * Sustituye al PNG original de 1 MB por variantes de 1,5 a 4 KB (Green IT, WSG 1.0 pauta 1.2).
 */
export default function Logo({ tamano }: Props) {
  return (
    <picture>
      <source type="image/avif" srcSet="/img/logo-64.avif 1x, /img/logo-128.avif 2x" />
      <source type="image/webp" srcSet="/img/logo-64.webp 1x, /img/logo-128.webp 2x" />
      <img
        src="/img/logo-64.png"
        srcSet="/img/logo-64.png 1x, /img/logo-128.png 2x"
        alt=""
        width={tamano}
        height={tamano}
        decoding="async"
      />
    </picture>
  )
}
