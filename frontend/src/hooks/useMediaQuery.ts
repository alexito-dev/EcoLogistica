import { useSyncExternalStore } from 'react'

/** Devuelve si la media query coincide; `false` donde `matchMedia` no existe (pruebas, SSR). */
export function useMediaQuery(query: string): boolean {
  return useSyncExternalStore(
    (avisar) => {
      if (typeof window === 'undefined' || !window.matchMedia) return () => {}
      const lista = window.matchMedia(query)
      lista.addEventListener('change', avisar)
      return () => lista.removeEventListener('change', avisar)
    },
    () => (typeof window !== 'undefined' && window.matchMedia ? window.matchMedia(query).matches : false),
    () => false,
  )
}

/** El usuario pidió reducir el movimiento, o el entorno no permite saberlo. */
export function prefiereMenosMovimiento(): boolean {
  if (typeof window === 'undefined' || !window.matchMedia) return true
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}
