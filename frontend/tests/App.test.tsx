import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '../src/App'
import * as api from '../src/api/pedidos'

const pedido: api.Pedido = {
  id: '1',
  codigo: 'PED-000001',
  direccion: 'Jr. Real 123',
  distrito: 'Huancayo',
  latitud: -12.06,
  longitud: -75.2,
  destinatarioAlias: 'Bodega Ana',
  demandaKg: 25,
  demandaM3: 0.3,
  tiempoServicioMin: 10,
  ventanaInicio: '2026-10-05T13:00:00Z',
  ventanaFin: '2026-10-05T17:00:00Z',
  prioridad: 4,
  estado: 'PENDIENTE',
  observacionOperativa: null,
  creadoEn: '2026-10-02T10:00:00Z',
  actualizadoEn: '2026-10-02T10:00:00Z',
}

const otro: api.Pedido = {
  ...pedido,
  id: '2',
  codigo: 'PED-000002',
  direccion: 'Av. Ferrocarril 800',
  distrito: 'El Tambo',
  prioridad: 1,
  estado: 'ENTREGADO',
}

const vacio = { items: [], total: 0, pagina: 1, limite: 100 }
const conPedido = { items: [pedido], total: 1, pagina: 1, limite: 100 }
const conDos = { items: [otro, pedido], total: 2, pagina: 1, limite: 100 }

afterEach(() => vi.restoreAllMocks())

describe('App', () => {
  it('muestra el encabezado, los indicadores y el estado vacío con acción', async () => {
    vi.spyOn(api, 'listarPedidos').mockResolvedValue(vacio)
    render(<App />)
    expect(screen.getByRole('heading', { name: 'Pedidos', level: 1 })).toBeInTheDocument()
    expect(screen.getByRole('region', { name: 'Resumen de pedidos' })).toBeInTheDocument()
    expect(await screen.findByText('Aún no hay pedidos')).toBeInTheDocument()
    expect(screen.getAllByRole('button', { name: /Nuevo pedido/ }).length).toBeGreaterThan(0)
  })

  it('calcula los indicadores con los pedidos cargados', async () => {
    vi.spyOn(api, 'listarPedidos').mockResolvedValue(conDos)
    render(<App />)
    await screen.findByText('PED-000001')
    const resumen = screen.getByRole('region', { name: 'Resumen de pedidos' })
    // Los valores se animan (conteo ascendente): se espera el valor final.
    await waitFor(() => expect(within(resumen).getByText('Pendientes').parentElement).toHaveTextContent('1'))
    await waitFor(() => expect(within(resumen).getByText('Carga total').parentElement).toHaveTextContent('50 kg'))
  })

  it('abre el panel, registra y el pedido aparece en la tabla con aviso de confirmación', async () => {
    const listar = vi.spyOn(api, 'listarPedidos').mockResolvedValueOnce(vacio).mockResolvedValue(conPedido)
    vi.spyOn(api, 'crearPedido').mockResolvedValue(pedido)
    const user = userEvent.setup()
    render(<App />)
    await screen.findByText('Aún no hay pedidos')

    await user.click(screen.getAllByRole('button', { name: /Nuevo pedido/ })[0])
    const panel = await screen.findByRole('dialog', { name: 'Registrar pedido' })
    await user.click(within(panel).getByRole('button', { name: 'Guardar pedido' }))

    const fila = await screen.findByRole('row', { name: /PED-000001/ })
    expect(fila).toHaveTextContent('Pendiente')
    expect(fila).toHaveTextContent('08:00')
    expect(screen.getByRole('status')).toHaveTextContent('PED-000001')
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    expect(listar).toHaveBeenCalledTimes(2)
  })

  it('el panel se cierra con Escape y devuelve el foco al botón que lo abrió', async () => {
    vi.spyOn(api, 'listarPedidos').mockResolvedValue(conPedido)
    const user = userEvent.setup()
    render(<App />)
    await screen.findByText('PED-000001')
    const boton = screen.getAllByRole('button', { name: /Nuevo pedido/ })[0]
    boton.focus()
    await user.click(boton)
    expect(await screen.findByRole('dialog')).toBeInTheDocument()
    await user.keyboard('{Escape}')
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    expect(boton).toHaveFocus()
  })

  it('muestra el detalle de un pedido', async () => {
    vi.spyOn(api, 'listarPedidos').mockResolvedValue(conPedido)
    const user = userEvent.setup()
    render(<App />)
    await user.click(await screen.findByRole('button', { name: 'Ver detalle del pedido PED-000001' }))
    const panel = await screen.findByRole('dialog', { name: 'PED-000001' })
    expect(panel).toHaveTextContent('Jr. Real 123')
    expect(panel).toHaveTextContent('Bodega Ana')
    expect(panel).toHaveTextContent('Prioridad Urgente')
  })

  it('filtra por estado y busca por texto', async () => {
    vi.spyOn(api, 'listarPedidos').mockResolvedValue(conDos)
    const user = userEvent.setup()
    render(<App />)
    await screen.findByText('PED-000001')

    await user.selectOptions(screen.getByLabelText('Filtrar por estado'), 'ENTREGADO')
    expect(screen.getByText('PED-000002')).toBeInTheDocument()
    expect(screen.queryByText('PED-000001')).not.toBeInTheDocument()

    await user.selectOptions(screen.getByLabelText('Filtrar por estado'), 'TODOS')
    await user.type(screen.getByLabelText('Buscar pedidos por código, dirección o distrito'), 'tambo')
    expect(screen.getByText('PED-000002')).toBeInTheDocument()
    expect(screen.queryByText('PED-000001')).not.toBeInTheDocument()

    await user.clear(screen.getByLabelText('Buscar pedidos por código, dirección o distrito'))
    await user.type(screen.getByLabelText('Buscar pedidos por código, dirección o distrito'), 'zzz')
    expect(screen.getByText('Sin resultados')).toBeInTheDocument()
  })

  it('permite reintentar cuando falla la carga del listado', async () => {
    vi.spyOn(api, 'listarPedidos')
      .mockRejectedValueOnce(new api.ApiError(0, 'No se pudo conectar con el servidor.'))
      .mockResolvedValue(conPedido)
    const user = userEvent.setup()
    render(<App />)
    expect(await screen.findByRole('alert')).toHaveTextContent('No se pudo conectar')
    await user.click(screen.getByRole('button', { name: /Reintentar/ }))
    expect(await screen.findByText('PED-000001')).toBeInTheDocument()
  })

  it('alterna entre tema claro y oscuro', async () => {
    vi.spyOn(api, 'listarPedidos').mockResolvedValue(vacio)
    const user = userEvent.setup()
    render(<App />)
    const inicial = document.documentElement.dataset.tema
    await user.click(screen.getByRole('button', { name: /Cambiar a tema/ }))
    expect(document.documentElement.dataset.tema).not.toBe(inicial)
  })
})
