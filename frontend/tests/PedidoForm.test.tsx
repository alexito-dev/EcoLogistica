import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import PedidoForm from '../src/components/PedidoForm'
import * as api from '../src/api/pedidos'

const creado = { id: 'abc', codigo: 'PED-000001', estado: 'PENDIENTE' } as api.Pedido

async function llenar(user: ReturnType<typeof userEvent.setup>, sobre: Record<string, string> = {}) {
  const valores: Record<string, string> = {
    Dirección: 'Jr. Real 123',
    Distrito: 'Huancayo',
    Latitud: '-12.0651',
    Longitud: '-75.2049',
    'Peso \\(kg\\)': '25',
    'Ventana: inicio': '2026-10-05T08:00',
    'Ventana: fin': '2026-10-05T12:00',
    ...sobre,
  }
  for (const [etiqueta, valor] of Object.entries(valores)) {
    const campo = screen.getByLabelText(new RegExp(`^${etiqueta}`))
    await user.clear(campo)
    await user.type(campo, valor)
  }
}

afterEach(() => vi.restoreAllMocks())

describe('PedidoForm', () => {
  it('ofrece un mapa para ubicar el destino', async () => {
    render(<PedidoForm onCreado={() => {}} onCancelar={() => {}} />)
    expect(await screen.findByRole('application', { name: 'Mapa para ubicar el destino' })).toBeInTheDocument()
    expect(screen.getByText(/Haga clic en el mapa para completar latitud y longitud/)).toBeInTheDocument()
  })

  it('envía la ventana en hora de Lima con desfase y notifica el pedido creado', async () => {
    const espia = vi.spyOn(api, 'crearPedido').mockResolvedValue(creado)
    const onCreado = vi.fn()
    const user = userEvent.setup()
    render(<PedidoForm onCreado={onCreado} onCancelar={vi.fn()} />)
    await llenar(user)
    await user.click(screen.getByRole('button', { name: 'Guardar pedido' }))

    expect(espia).toHaveBeenCalledOnce()
    const enviado = espia.mock.calls[0][0]
    expect(enviado.ventanaInicio).toBe('2026-10-05T08:00:00-05:00')
    expect(enviado.ventanaFin).toBe('2026-10-05T12:00:00-05:00')
    expect(enviado.codigo).toBeUndefined()
    expect(enviado.tiempoServicioMin).toBeUndefined()
    await waitFor(() => expect(onCreado).toHaveBeenCalledWith(creado))
  })

  it('muestra el error junto al campo de hora final y conserva los valores', async () => {
    vi.spyOn(api, 'crearPedido').mockRejectedValue(
      new api.ApiError(422, 'No se cumple una regla de negocio', {
        ventanaFin: 'La hora final debe ser posterior a la hora inicial',
      }),
    )
    const onCreado = vi.fn()
    const user = userEvent.setup()
    render(<PedidoForm onCreado={onCreado} onCancelar={vi.fn()} />)
    await llenar(user, { 'Ventana: fin': '2026-10-05T07:00' })
    await user.click(screen.getByRole('button', { name: 'Guardar pedido' }))

    const campoFin = await screen.findByLabelText(/^Ventana: fin/)
    expect(campoFin).toHaveAttribute('aria-invalid', 'true')
    const idError = campoFin.getAttribute('aria-describedby') as string
    expect(document.getElementById(idError)).toHaveTextContent('posterior a la hora inicial')
    expect(screen.getByRole('alert')).toHaveTextContent('No se cumple una regla de negocio')
    expect(screen.getByLabelText(/^Dirección/)).toHaveValue('Jr. Real 123')
    expect(campoFin).toHaveValue('2026-10-05T07:00')
    expect(onCreado).not.toHaveBeenCalled()
  })

  it('muestra los campos obligatorios que devuelve el backend', async () => {
    vi.spyOn(api, 'crearPedido').mockRejectedValue(
      new api.ApiError(400, 'Datos inválidos', {
        direccion: 'Campo obligatorio',
        distrito: 'Campo obligatorio',
      }),
    )
    const user = userEvent.setup()
    render(<PedidoForm onCreado={vi.fn()} onCancelar={vi.fn()} />)
    await user.click(screen.getByRole('button', { name: 'Guardar pedido' }))
    await waitFor(() =>
      expect(screen.getAllByText('Campo obligatorio').length).toBeGreaterThanOrEqual(2),
    )
    expect(screen.getByLabelText(/^Dirección/)).toHaveAttribute('aria-invalid', 'true')
  })

  it('cada campo tiene etiqueta asociada y se recorre con teclado', async () => {
    const user = userEvent.setup()
    render(<PedidoForm onCreado={vi.fn()} onCancelar={vi.fn()} />)
    const controles = [
      ...screen.getAllByRole('textbox'),
      ...screen.getAllByRole('spinbutton'),
      screen.getByRole('combobox', { name: /Prioridad/ }),
    ]
    expect(controles.length).toBeGreaterThan(8)
    for (const c of controles) expect(c).toHaveAccessibleName()
    screen.getByLabelText(/^Dirección/).focus()
    await user.tab()
    expect(screen.getByLabelText(/^Distrito/)).toHaveFocus()
  })

  it('el botón Cancelar avisa al contenedor', async () => {
    const onCancelar = vi.fn()
    const user = userEvent.setup()
    render(<PedidoForm onCreado={vi.fn()} onCancelar={onCancelar} />)
    await user.click(screen.getByRole('button', { name: 'Cancelar' }))
    expect(onCancelar).toHaveBeenCalledOnce()
  })

  it('informa un error inesperado sin romperse', async () => {
    vi.spyOn(api, 'crearPedido').mockRejectedValue(new Error('boom'))
    const user = userEvent.setup()
    render(<PedidoForm onCreado={vi.fn()} onCancelar={vi.fn()} />)
    await user.click(screen.getByRole('button', { name: 'Guardar pedido' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('error inesperado')
  })
})
