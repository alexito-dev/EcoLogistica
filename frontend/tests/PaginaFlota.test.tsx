import { fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import PaginaFlota from '../src/pages/PaginaFlota'
import * as api from '../src/api/flota'
import { ApiError } from '../src/api/http'

const unidad: api.Vehiculo = {
  id: 'v-100', placa: 'W3A-123', tipo: 'Furgón',
  capacidadKg: 700, capacidadM3: 8, combustible: 'DIESEL',
  consumoBasePor100km: 11, factorEmisionKgco2eUnidad: null,
  anio: 2022, estado: 'DISPONIBLE',
  creadoEn: '2026-10-01T09:00:00Z', actualizadoEn: null,
  disponibilidad: { fecha: '2026-10-30', turnoInicio: '08:00:00', turnoFin: '17:00:00', disponible: true, restriccionCirculacion: null },
  elegibleParaPlanificar: true,
}
const sinTurno: api.Vehiculo = { ...unidad, id: 'v-101', placa: 'W3A-124', disponibilidad: null, elegibleParaPlanificar: false, anio: null, combustible: 'ELECTRICO' }
const inactivo: api.Vehiculo = { ...unidad, id: 'v-102', placa: 'W3A-125', estado: 'MANTENIMIENTO', disponibilidad: null, elegibleParaPlanificar: false, combustible: 'GNV' }

beforeEach(() => {
  vi.spyOn(api, 'listarVehiculos').mockResolvedValue({ items: [] })
})
afterEach(() => vi.restoreAllMocks())

describe('Flota: formularios, permisos y fallos de red', () => {
  it('muestra un estado vacío con instrucciones para planificación', async () => {
    render(<PaginaFlota puedeAdministrar={false} puedePlanificar />)
    expect(await screen.findByText('Aún no hay vehículos')).toBeInTheDocument()
    expect(screen.getByText(/Solicite a Administración/)).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Nuevo vehículo' })).not.toBeInTheDocument()
  })

  it('presenta vehículos elegibles, sin turno, en mantenimiento y emisiones', async () => {
    vi.mocked(api.listarVehiculos).mockResolvedValue({ items: [unidad, sinTurno, inactivo] })
    render(<PaginaFlota puedeAdministrar puedePlanificar />)
    expect(await screen.findByText('W3A-123')).toBeInTheDocument()
    expect(screen.getByText('W3A-124')).toBeInTheDocument()
    expect(screen.getByText('W3A-125')).toBeInTheDocument()
    expect(screen.getByText('Apto para planificar')).toBeInTheDocument()
    expect(screen.getByText('Sin turno declarado')).toBeInTheDocument()
    expect(screen.getByText('Mantenimiento')).toBeInTheDocument()
    expect(screen.getByText('Furgón · 2022')).toBeInTheDocument()
    expect(screen.getByRole('region', { name: 'Resumen de flota' })).toBeInTheDocument()
  })

  it('cambia la fecha y vuelve a pedir la disponibilidad', async () => {
    render(<PaginaFlota puedeAdministrar={false} puedePlanificar />)
    await screen.findByText('Aún no hay vehículos')
    fireEvent.change(screen.getByLabelText('Fecha de turno'), { target: { value: '2026-11-01' } })
    await waitFor(() => expect(api.listarVehiculos).toHaveBeenCalledWith('2026-11-01'))
    expect(screen.getByText(/01\/11\/2026/)).toBeInTheDocument()
  })

  it('reintenta cuando el servicio falla y se recupera', async () => {
    vi.mocked(api.listarVehiculos)
      .mockRejectedValueOnce(new ApiError(503, 'Servicio temporalmente indisponible'))
      .mockResolvedValue({ items: [unidad] })
    render(<PaginaFlota puedeAdministrar puedePlanificar />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Servicio temporalmente indisponible')
    await userEvent.click(screen.getByRole('button', { name: 'Reintentar' }))
    expect(await screen.findByText('W3A-123')).toBeInTheDocument()
  })

  it('registra un vehículo normalizando placa y convirtiendo datos numéricos', async () => {
    const guardar = vi.spyOn(api, 'crearVehiculo').mockResolvedValue(unidad)
    const usuario = userEvent.setup()
    render(<PaginaFlota puedeAdministrar puedePlanificar={false} />)
    await screen.findByText('Aún no hay vehículos')
    await usuario.click(screen.getByRole('button', { name: 'Nuevo vehículo' }))
    const panel = screen.getByRole('dialog', { name: 'Registrar vehículo' })
    fireEvent.change(within(panel).getByLabelText('Placa *'), { target: { value: 'w3a-123' } })
    fireEvent.change(within(panel).getByLabelText('Tipo de vehículo *'), { target: { value: 'Furgón' } })
    fireEvent.change(within(panel).getByLabelText('Capacidad (kg) *'), { target: { value: '700' } })
    fireEvent.change(within(panel).getByLabelText('Capacidad (m³) *'), { target: { value: '8' } })
    fireEvent.change(within(panel).getByLabelText('Consumo por 100 km *'), { target: { value: '11' } })
    fireEvent.change(within(panel).getByLabelText('Año'), { target: { value: '2022' } })
    fireEvent.change(within(panel).getByLabelText('Factor de emisión (opcional)'), { target: { value: '2.5' } })
    await usuario.click(within(panel).getByRole('button', { name: 'Registrar vehículo' }))
    await waitFor(() => expect(guardar).toHaveBeenCalledWith(expect.objectContaining({
      placa: 'W3A-123', tipo: 'Furgón', capacidadKg: 700, capacidadM3: 8, anio: 2022,
      factorEmisionKgco2eUnidad: 2.5,
    })))
    expect(await screen.findByRole('status')).toHaveTextContent('Vehículo registrado')
  })

  it('muestra errores por campo y conserva el formulario para corregirlos', async () => {
    vi.spyOn(api, 'crearVehiculo').mockRejectedValue(new ApiError(422, 'Datos inválidos', { placa: 'Placa duplicada' }))
    const usuario = userEvent.setup()
    render(<PaginaFlota puedeAdministrar puedePlanificar={false} />)
    await screen.findByText('Aún no hay vehículos')
    await usuario.click(screen.getByRole('button', { name: 'Nuevo vehículo' }))
    const panel = screen.getByRole('dialog', { name: 'Registrar vehículo' })
    fireEvent.change(within(panel).getByLabelText('Placa *'), { target: { value: 'W3A-123' } })
    fireEvent.change(within(panel).getByLabelText('Tipo de vehículo *'), { target: { value: 'Furgón' } })
    fireEvent.change(within(panel).getByLabelText('Capacidad (kg) *'), { target: { value: '700' } })
    fireEvent.change(within(panel).getByLabelText('Capacidad (m³) *'), { target: { value: '8' } })
    fireEvent.change(within(panel).getByLabelText('Consumo por 100 km *'), { target: { value: '11' } })
    await usuario.click(within(panel).getByRole('button', { name: 'Registrar vehículo' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('Placa duplicada')
    expect(screen.getByRole('dialog', { name: 'Registrar vehículo' })).toBeInTheDocument()
  })

  it('edita una unidad preexistente y permite cancelar sin guardar', async () => {
    vi.mocked(api.listarVehiculos).mockResolvedValue({ items: [unidad] })
    const actualizar = vi.spyOn(api, 'actualizarVehiculo').mockResolvedValue({ ...unidad, placa: 'W3A-999' })
    const usuario = userEvent.setup()
    render(<PaginaFlota puedeAdministrar puedePlanificar={false} />)
    await screen.findByText('W3A-123')
    await usuario.click(screen.getByRole('button', { name: 'Editar vehículo' }))
    let panel = screen.getByRole('dialog', { name: 'Editar vehículo' })
    expect(within(panel).getByLabelText('Placa *')).toHaveValue('W3A-123')
    await usuario.click(within(panel).getByRole('button', { name: 'Cancelar' }))
    expect(actualizar).not.toHaveBeenCalled()
    await usuario.click(screen.getByRole('button', { name: 'Editar vehículo' }))
    panel = screen.getByRole('dialog', { name: 'Editar vehículo' })
    fireEvent.change(within(panel).getByLabelText('Placa *'), { target: { value: 'W3A-999' } })
    await usuario.click(within(panel).getByRole('button', { name: 'Guardar cambios' }))
    await waitFor(() => expect(actualizar).toHaveBeenCalledWith('v-100', expect.objectContaining({ placa: 'W3A-999' })))
    expect(await screen.findByRole('status')).toHaveTextContent('Vehículo actualizado')
  })

  it('configura un turno no disponible con motivo registrado y permite volver a cargar', async () => {
    vi.mocked(api.listarVehiculos).mockResolvedValue({ items: [unidad] })
    const guardar = vi.spyOn(api, 'guardarDisponibilidad').mockResolvedValue(unidad)
    const usuario = userEvent.setup()
    render(<PaginaFlota puedeAdministrar={false} puedePlanificar />)
    await screen.findByText('W3A-123')
    await usuario.click(screen.getByRole('button', { name: 'Configurar turno' }))
    const panel = screen.getByRole('dialog', { name: 'Turno · W3A-123' })
    fireEvent.click(within(panel).getByLabelText('Disponible para planificar'))
    fireEvent.change(within(panel).getByLabelText('Motivo o restricción *'), { target: { value: '  mantenimiento preventivo  ' } })
    await usuario.click(within(panel).getByRole('button', { name: 'Guardar disponibilidad' }))
    await waitFor(() => expect(guardar).toHaveBeenCalledWith('v-100', expect.objectContaining({
      disponible: false, restriccionCirculacion: 'mantenimiento preventivo',
    })))
    expect(await screen.findByRole('status')).toHaveTextContent('Disponibilidad guardada')
  })

  it('informa fallo al guardar un turno sin perder el formulario', async () => {
    vi.mocked(api.listarVehiculos).mockResolvedValue({ items: [unidad] })
    vi.spyOn(api, 'guardarDisponibilidad').mockRejectedValue(new ApiError(422, 'Rango inválido', { turnoFin: 'Debe ser posterior' }))
    const usuario = userEvent.setup()
    render(<PaginaFlota puedeAdministrar={false} puedePlanificar />)
    await screen.findByText('W3A-123')
    await usuario.click(screen.getByRole('button', { name: 'Configurar turno' }))
    await usuario.click(screen.getByRole('dialog', { name: 'Turno · W3A-123' }).querySelector('button[type="submit"]')!)
    expect(await screen.findByRole('alert')).toHaveTextContent('Debe ser posterior')
    expect(screen.getByRole('dialog', { name: 'Turno · W3A-123' })).toBeInTheDocument()
  })
})
