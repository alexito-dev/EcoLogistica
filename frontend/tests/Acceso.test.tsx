import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '../src/App'
import * as auth from '../src/api/auth'
import * as pedidos from '../src/api/pedidos'
import { ApiError } from '../src/api/http'

const planificador: auth.Usuario = { nombre: 'Planificación', correo: 'planificador@ecologistica.test', rol: 'PLANIFICADOR' }
const vacio = { items: [], total: 0, pagina: 1, limite: 100 }

beforeEach(() => {
  vi.spyOn(pedidos, 'listarPedidos').mockResolvedValue(vacio)
})
afterEach(() => vi.restoreAllMocks())

async function llenarCredenciales(user: ReturnType<typeof userEvent.setup>, clave = 'clave-correcta') {
  await user.type(await screen.findByLabelText('Correo'), planificador.correo)
  await user.type(screen.getByLabelText('Contraseña'), clave)
  await user.click(screen.getByRole('button', { name: 'Continuar' }))
}

describe('Acceso con MFA', () => {
  it('sin sesión muestra la pantalla de inicio de sesión', async () => {
    vi.spyOn(auth, 'obtenerSesion').mockResolvedValue(null)
    render(<App />)
    expect(await screen.findByRole('heading', { name: 'Iniciar sesión' })).toBeInTheDocument()
    expect(screen.getByLabelText('Contraseña')).toHaveAttribute('type', 'password')
  })

  it('con sesión vigente muestra pedidos con nombre y rol', async () => {
    vi.spyOn(auth, 'obtenerSesion').mockResolvedValue(planificador)
    render(<App />)
    expect(await screen.findByRole('heading', { name: 'Pedidos', level: 1 })).toBeInTheDocument()
    expect(screen.getByText('Planificación')).toBeInTheDocument()
    expect(screen.getAllByText('Planificador').length).toBeGreaterThan(0)
  })

  it('flujo completo: contraseña, código y entrada a la app', async () => {
    vi.spyOn(auth, 'obtenerSesion').mockResolvedValue(null)
    const login = vi.spyOn(auth, 'iniciarSesion').mockResolvedValue({ paso: 'MFA', claveMfa: null, otpauthUri: null })
    const mfa = vi.spyOn(auth, 'verificarCodigo').mockResolvedValue(planificador)
    const user = userEvent.setup()
    render(<App />)
    await llenarCredenciales(user)

    expect(login).toHaveBeenCalledWith(planificador.correo, 'clave-correcta')
    const campo = await screen.findByLabelText('Código de verificación')
    expect(campo).toHaveFocus()
    await user.type(campo, '12a3456')
    expect(campo).toHaveValue('123456')
    await user.click(screen.getByRole('button', { name: 'Verificar y entrar' }))

    expect(mfa).toHaveBeenCalledWith('123456')
    expect(await screen.findByRole('heading', { name: 'Pedidos', level: 1 })).toBeInTheDocument()
  })

  it('enrolamiento: muestra QR y clave agrupada, y activa con el código', async () => {
    vi.spyOn(auth, 'obtenerSesion').mockResolvedValue(null)
    vi.spyOn(auth, 'iniciarSesion').mockResolvedValue({
      paso: 'ENROLAR',
      claveMfa: 'JBSWY3DPEHPK3PXP',
      otpauthUri: 'otpauth://totp/EcoLog%C3%ADstica:planificador?secret=JBSWY3DPEHPK3PXP',
    })
    vi.spyOn(auth, 'verificarCodigo').mockResolvedValue(planificador)
    const user = userEvent.setup()
    render(<App />)
    await llenarCredenciales(user)

    expect(await screen.findByRole('heading', { name: /Active la verificación/ })).toBeInTheDocument()
    expect(await screen.findByAltText(/Código QR/)).toBeInTheDocument()
    expect(screen.getByLabelText('Clave para ingreso manual')).toHaveTextContent('JBSW Y3DP EHPK 3PXP')
    await user.type(screen.getByLabelText('Código de verificación'), '654321')
    await user.click(screen.getByRole('button', { name: 'Activar y entrar' }))
    expect(await screen.findByRole('heading', { name: 'Pedidos', level: 1 })).toBeInTheDocument()
  })

  it('credenciales incorrectas: mensaje genérico, conserva el correo y vacía la contraseña', async () => {
    vi.spyOn(auth, 'obtenerSesion').mockResolvedValue(null)
    vi.spyOn(auth, 'iniciarSesion').mockRejectedValue(new ApiError(401, 'Correo o contraseña incorrectos'))
    const user = userEvent.setup()
    render(<App />)
    await llenarCredenciales(user, 'mala')
    expect(await screen.findByRole('alert')).toHaveTextContent('Correo o contraseña incorrectos')
    expect(screen.getByLabelText('Correo')).toHaveValue(planificador.correo)
    expect(screen.getByLabelText('Contraseña')).toHaveValue('')
  })

  it('código incorrecto muestra el error y permite reintentar', async () => {
    vi.spyOn(auth, 'obtenerSesion').mockResolvedValue(null)
    vi.spyOn(auth, 'iniciarSesion').mockResolvedValue({ paso: 'MFA', claveMfa: null, otpauthUri: null })
    vi.spyOn(auth, 'verificarCodigo').mockRejectedValue(
      new ApiError(401, 'Código incorrecto', { codigo: 'El código no es válido o ya fue usado' }),
    )
    const user = userEvent.setup()
    render(<App />)
    await llenarCredenciales(user)
    await user.type(await screen.findByLabelText('Código de verificación'), '000000')
    await user.click(screen.getByRole('button', { name: 'Verificar y entrar' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('ya fue usado')
    expect(screen.getByLabelText('Código de verificación')).toHaveValue('')
  })

  it('comprobante vencido vuelve a pedir la contraseña', async () => {
    vi.spyOn(auth, 'obtenerSesion').mockResolvedValue(null)
    vi.spyOn(auth, 'iniciarSesion').mockResolvedValue({ paso: 'MFA', claveMfa: null, otpauthUri: null })
    vi.spyOn(auth, 'verificarCodigo').mockRejectedValue(new ApiError(401, 'El paso de verificación venció.'))
    const user = userEvent.setup()
    render(<App />)
    await llenarCredenciales(user)
    await user.type(await screen.findByLabelText('Código de verificación'), '123456')
    await user.click(screen.getByRole('button', { name: 'Verificar y entrar' }))
    expect(await screen.findByRole('heading', { name: 'Iniciar sesión' })).toBeInTheDocument()
    expect(screen.getByRole('alert')).toHaveTextContent('venció')
  })

  it('cerrar sesión vuelve a la pantalla de acceso', async () => {
    vi.spyOn(auth, 'obtenerSesion').mockResolvedValue(planificador)
    const cerrar = vi.spyOn(auth, 'cerrarSesion').mockResolvedValue()
    const user = userEvent.setup()
    render(<App />)
    await user.click(await screen.findByRole('button', { name: 'Cerrar sesión' }))
    expect(cerrar).toHaveBeenCalled()
    expect(await screen.findByRole('heading', { name: 'Iniciar sesión' })).toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveTextContent('Sesión cerrada')
  })

  it('un 401 durante el uso vuelve al acceso con aviso de sesión vencida', async () => {
    vi.spyOn(auth, 'obtenerSesion').mockResolvedValue(planificador)
    vi.restoreAllMocks()
    vi.spyOn(auth, 'obtenerSesion').mockResolvedValue(planificador)
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({ ok: false, status: 401, json: async () => ({ status: 401, message: 'Sesión no válida' }) }),
    )
    render(<App />)
    expect(await screen.findByRole('heading', { name: 'Iniciar sesión' })).toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveTextContent('Su sesión venció')
    vi.unstubAllGlobals()
  })

  it('un rol sin permiso ve el aviso de acceso no autorizado', async () => {
    vi.spyOn(auth, 'obtenerSesion').mockResolvedValue({ ...planificador, nombre: 'Conductor de ruta', rol: 'CONDUCTOR' })
    render(<App />)
    expect(await screen.findByRole('heading', { name: 'Acceso no autorizado' })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Pedidos', level: 1 })).not.toBeInTheDocument()
  })

  it('el administrador consulta pedidos sin botón de registro', async () => {
    vi.spyOn(auth, 'obtenerSesion').mockResolvedValue({ ...planificador, nombre: 'Administración', rol: 'ADMIN' })
    render(<App />)
    expect(await screen.findByRole('heading', { name: 'Pedidos', level: 1 })).toBeInTheDocument()
    await waitFor(() => expect(screen.queryByRole('button', { name: /Nuevo pedido/ })).not.toBeInTheDocument())
  })

  it('alterna entre tema claro y oscuro', async () => {
    vi.spyOn(auth, 'obtenerSesion').mockResolvedValue(null)
    const user = userEvent.setup()
    render(<App />)
    const inicial = document.documentElement.dataset.tema
    await user.click(await screen.findByRole('button', { name: /Cambiar a tema/ }))
    expect(document.documentElement.dataset.tema).not.toBe(inicial)
  })
})

describe('Cliente HTTP', () => {
  beforeEach(() => vi.restoreAllMocks())
  afterEach(() => vi.unstubAllGlobals())

  it('envía las cookies de sesión en cada solicitud', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => vacio })
    vi.stubGlobal('fetch', fetchMock)
    await pedidos.listarPedidos()
    expect(fetchMock.mock.calls[0][1].credentials).toBe('include')
  })

  it('obtenerSesion devuelve null ante 401 sin avisar sesión vencida', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 401, json: async () => ({}) }))
    await expect(auth.obtenerSesion()).resolves.toBeNull()
  })

  it('cerrarSesion acepta la respuesta 204 sin cuerpo', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, status: 204, json: async () => { throw new Error('sin cuerpo') } }))
    await expect(auth.cerrarSesion()).resolves.toBeUndefined()
  })
})
