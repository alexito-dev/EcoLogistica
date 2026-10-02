import { ApiError, crearPedido, listarPedidos } from '../src/api/pedidos'

function responder(estado: number, cuerpo: unknown) {
  return vi.fn().mockResolvedValue({
    ok: estado >= 200 && estado < 300,
    status: estado,
    json: async () => cuerpo,
  })
}

afterEach(() => vi.unstubAllGlobals())

describe('cliente de pedidos', () => {
  it('traduce un 422 a ApiError con errores por campo', async () => {
    vi.stubGlobal(
      'fetch',
      responder(422, {
        status: 422,
        message: 'No se cumple una regla',
        errors: { ventanaFin: 'Debe ser posterior' },
      }),
    )
    const error = await crearPedido({}).catch((e) => e)
    expect(error).toBeInstanceOf(ApiError)
    expect(error.status).toBe(422)
    expect(error.errors).toEqual({ ventanaFin: 'Debe ser posterior' })
  })

  it('traduce un 400 a ApiError con errores por campo', async () => {
    vi.stubGlobal(
      'fetch',
      responder(400, {
        status: 400,
        message: 'Datos inválidos',
        errors: { demandaKg: 'Debe ser mayor o igual que 0' },
      }),
    )
    const error = await crearPedido({}).catch((e) => e)
    expect(error.status).toBe(400)
    expect(error.errors.demandaKg).toContain('mayor o igual')
  })

  it('envía el cuerpo JSON por POST y devuelve el pedido creado', async () => {
    const fetchMock = responder(201, { id: '1', codigo: 'PED-000001', estado: 'PENDIENTE' })
    vi.stubGlobal('fetch', fetchMock)
    const pedido = await crearPedido({ direccion: 'Jr. Real 1' })
    expect(pedido.codigo).toBe('PED-000001')
    const [url, init] = fetchMock.mock.calls[0]
    expect(url).toMatch(/\/pedidos$/)
    expect(init.method).toBe('POST')
    expect(JSON.parse(init.body)).toEqual({ direccion: 'Jr. Real 1' })
  })

  it('informa un error de conexión con estado 0', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('fallo de red')))
    const error = await listarPedidos().catch((e) => e)
    expect(error).toBeInstanceOf(ApiError)
    expect(error.status).toBe(0)
  })

  it('usa un mensaje genérico si el cuerpo del error no es JSON', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
        json: async () => {
          throw new Error('no es json')
        },
      }),
    )
    const error = await listarPedidos().catch((e) => e)
    expect(error.status).toBe(500)
    expect(error.message).toBeTruthy()
  })
})
