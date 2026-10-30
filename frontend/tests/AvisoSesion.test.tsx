import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { AuthContext, type ValorAuth } from '../src/auth/contexto'
import AvisoSesion from '../src/components/AvisoSesion'
import * as apiAuth from '../src/api/auth'

function conSesion(estado: ValorAuth['estado'] = 'autenticado') {
  const valor: ValorAuth = {
    estado,
    usuario: { nombre: 'Prueba', correo: 'p@x.test', rol: 'PLANIFICADOR' },
    aviso: null,
    entrar: () => undefined,
    salir: async () => undefined,
  }
  return (
    <AuthContext.Provider value={valor}>
      <AvisoSesion inactividadMs={10_000} avisoAntesMs={4_000} />
    </AuthContext.Provider>
  )
}

describe('AvisoSesion', () => {
  beforeEach(() => vi.useFakeTimers({ shouldAdvanceTime: false }))
  afterEach(() => {
    vi.useRealTimers()
    vi.restoreAllMocks()
  })

  it('no aparece mientras queda tiempo', () => {
    render(conSesion())
    act(() => vi.advanceTimersByTime(3_000))
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })

  it('avisa antes de vencer y permite seguir conectado', async () => {
    const espia = vi.spyOn(apiAuth, 'obtenerSesion').mockResolvedValue(null)
    render(conSesion())
    act(() => vi.advanceTimersByTime(7_000))
    expect(screen.getByRole('alert')).toHaveTextContent(/vencerá por inactividad/)
    const boton = screen.getByRole('button', { name: 'Seguir conectado' })
    vi.useRealTimers()
    await userEvent.click(boton)
    expect(espia).toHaveBeenCalledOnce()
  })

  it('no muestra nada sin sesión', () => {
    render(conSesion('anonimo'))
    act(() => vi.advanceTimersByTime(9_000))
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })
})
