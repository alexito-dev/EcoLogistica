import { useEffect, useRef, useState } from 'react'
import { prefiereMenosMovimiento } from './useMediaQuery'

/** Anima un número desde su valor anterior hasta `objetivo` (sin animación si se reduce el movimiento). */
export function useCountUp(objetivo: number, duracionMs = 700): number {
  const [valor, setValor] = useState(objetivo)
  const anterior = useRef(prefiereMenosMovimiento() ? objetivo : 0)

  useEffect(() => {
    const desde = anterior.current
    anterior.current = objetivo
    if (prefiereMenosMovimiento() || desde === objetivo) {
      setValor(objetivo)
      return
    }
    let cuadro = 0
    const inicio = performance.now()
    const paso = (ahora: number) => {
      const t = Math.min(1, (ahora - inicio) / duracionMs)
      const suavizado = 1 - Math.pow(1 - t, 3)
      setValor(desde + (objetivo - desde) * suavizado)
      if (t < 1) cuadro = requestAnimationFrame(paso)
    }
    cuadro = requestAnimationFrame(paso)
    return () => cancelAnimationFrame(cuadro)
  }, [objetivo, duracionMs])

  return valor
}
