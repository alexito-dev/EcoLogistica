import { act, renderHook } from '@testing-library/react'
import { useCountUp } from '../src/hooks/useCountUp'
import { prefiereMenosMovimiento, useMediaQuery } from '../src/hooks/useMediaQuery'

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

describe('Accesibilidad: consulta de preferencias reales de movimiento', () => {
  it('aplica una política segura cuando el navegador no proporciona matchMedia', () => {
    vi.stubGlobal('matchMedia', undefined)
    expect(prefiereMenosMovimiento()).toBe(true)
    const { result } = renderHook(() => useMediaQuery('(min-width: 800px)'))
    expect(result.current).toBe(false)
  })

  it('se suscribe a cambios de media query y se desuscribe al desmontar', () => {
    let coinciden = false
    const escuchas = new Set<() => void>()
    const matchMedia = vi.fn().mockImplementation((media: string) => ({
      matches: coinciden, media,
      addEventListener: (_: string, listener: () => void) => escuchas.add(listener),
      removeEventListener: (_: string, listener: () => void) => escuchas.delete(listener),
    }))
    vi.stubGlobal('matchMedia', matchMedia)
    const { result, unmount } = renderHook(() => useMediaQuery('(min-width: 800px)'))
    expect(result.current).toBe(false)
    expect(escuchas.size).toBeGreaterThan(0)
    coinciden = true
    act(() => { for (const avisar of escuchas) avisar() })
    expect(result.current).toBe(true)
    unmount()
    expect(escuchas.size).toBe(0)
  })

  it('identifica el modo de movimiento reducido y evita animar cifras', () => {
    vi.stubGlobal('matchMedia', vi.fn().mockImplementation(() => ({ matches: true, addEventListener() {}, removeEventListener() {} })))
    expect(prefiereMenosMovimiento()).toBe(true)
    const { result, rerender } = renderHook(({ objetivo }) => useCountUp(objetivo), { initialProps: { objetivo: 10 } })
    expect(result.current).toBe(10)
    rerender({ objetivo: 25 })
    expect(result.current).toBe(25)
  })

  it('muestra el valor objetivo inmediatamente al no variar', () => {
    vi.stubGlobal('matchMedia', vi.fn().mockImplementation(() => ({ matches: false, addEventListener() {}, removeEventListener() {} })))
    const animaciones: FrameRequestCallback[] = []
    vi.stubGlobal('requestAnimationFrame', vi.fn((callback: FrameRequestCallback) => {
      animaciones.push(callback)
      return animaciones.length
    }))
    vi.stubGlobal('cancelAnimationFrame', vi.fn())
    const { result, unmount } = renderHook(() => useCountUp(100, 300))
    expect(animaciones.length).toBeGreaterThan(0)
    act(() => { animaciones.shift()?.(performance.now() + 400) })
    expect(result.current).toBe(100)
    unmount()
  })
})
