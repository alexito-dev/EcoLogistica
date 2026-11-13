import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import PaginaMiRuta from '../src/pages/PaginaMiRuta'
import PaginaSeguimiento from '../src/pages/PaginaSeguimiento'
import * as api from '../src/api/conduccion'
import { ApiError } from '../src/api/http'

// El mapa necesita un navegador real; sus propias pruebas están en PaginaRutas.
vi.mock('../src/components/MapaRutas', () => ({ default: () => <div data-testid="mapa" /> }))

const base = {
  orden: 1,
  pedidoId: 'p1',
  codigo: 'DR-1001',
  destinatarioAlias: 'Bodega Santa Rosa',
  direccion: 'Jr. Real 455',
  distrito: 'Huancayo',
  latitud: -12.0686,
  longitud: -75.2103,
  demandaKg: 35,
  prioridad: 2,
  ventanaInicio: '2026-10-10T13:00:00Z',
  ventanaFin: '2026-10-10T15:00:00Z',
  llegadaEstimada: '2026-10-10T13:00:00Z',
  dentroDeVentana: true,
  nota: null,
  actualizadoEn: null,
}

function ruta(paradas: api.ParadaEjecucion[], conductorId: string | null = 'c1'): api.RutaConduccion {
  return {
    vehiculo: { id: 'v1', placa: 'ECO-103', tipo: 'Moto', combustible: 'ELECTRICO', capacidadKg: 120, capacidadM3: 1.2 },
    conductorId,
    conductorNombre: conductorId ? 'Conductor de ruta' : null,
    paradas,
    distanciaKm: 12,
    avance: {
      total: paradas.length,
      entregadas: paradas.filter((p) => p.estado === 'ENTREGADO').length,
      incidencias: paradas.filter((p) => p.estado === 'INCIDENCIA').length,
      canceladas: 0,
      reprogramadas: 0,
    },
  }
}

const deposito = { nombre: 'Centro de distribución Huancayo', latitud: -12.0651, longitud: -75.2049 }
const miRuta = (paradas: api.ParadaEjecucion[]): api.MiRuta => ({ fecha: '2026-10-10', deposito, rutas: [ruta(paradas)] })

afterEach(() => vi.restoreAllMocks())

describe('PaginaMiRuta (HU-005 y HU-010)', () => {
  it('muestra las paradas en orden con sus acciones permitidas', async () => {
    vi.spyOn(api, 'obtenerMiRuta').mockResolvedValue(
      miRuta([
        { ...base, estado: 'EN_RUTA' },
        { ...base, orden: 2, pedidoId: 'p2', codigo: 'DR-1002', estado: 'PENDIENTE' },
      ]),
    )
    render(<PaginaMiRuta />)
    expect(await screen.findByText('DR-1001')).toBeInTheDocument()
    expect(screen.getByTestId('mapa')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Marcar entregado: pedido DR-1001' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Reportar incidencia: pedido DR-1001' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Salir hacia la parada: pedido DR-1002' })).toBeInTheDocument()
    // No se puede marcar entregado algo que aún no salió.
    expect(screen.queryByRole('button', { name: 'Marcar entregado: pedido DR-1002' })).not.toBeInTheDocument()
  })

  it('registra el avance y vuelve a consultar la ruta', async () => {
    const consultar = vi
      .spyOn(api, 'obtenerMiRuta')
      .mockResolvedValueOnce(miRuta([{ ...base, estado: 'EN_RUTA' }]))
      .mockResolvedValue(miRuta([{ ...base, estado: 'ENTREGADO' }]))
    const registrar = vi.spyOn(api, 'registrarEstado').mockResolvedValue({ ...base, estado: 'ENTREGADO' })
    const user = userEvent.setup()
    render(<PaginaMiRuta />)
    await user.click(await screen.findByRole('button', { name: 'Marcar entregado: pedido DR-1001' }))
    await waitFor(() => expect(registrar).toHaveBeenCalledWith('p1', expect.any(String), 'ENTREGADO', undefined))
    expect(await screen.findByRole('status')).toHaveTextContent('Pedido DR-1001: entregado.')
    expect(consultar).toHaveBeenCalledTimes(2)
    expect(screen.queryByRole('button', { name: /Marcar entregado/ })).not.toBeInTheDocument()
  })

  it('exige describir la incidencia antes de enviarla', async () => {
    vi.spyOn(api, 'obtenerMiRuta').mockResolvedValue(miRuta([{ ...base, estado: 'EN_RUTA' }]))
    const registrar = vi.spyOn(api, 'registrarEstado').mockResolvedValue({ ...base, estado: 'INCIDENCIA' })
    const user = userEvent.setup()
    render(<PaginaMiRuta />)
    await user.click(await screen.findByRole('button', { name: 'Reportar incidencia: pedido DR-1001' }))
    const enviar = screen.getByRole('button', { name: 'Enviar incidencia' })
    expect(enviar).toBeDisabled()
    await user.type(screen.getByLabelText(/Describa la incidencia del pedido DR-1001/), 'Cliente ausente')
    expect(enviar).toBeEnabled()
    await user.click(enviar)
    await waitFor(() => expect(registrar).toHaveBeenCalledWith('p1', expect.any(String), 'INCIDENCIA', 'Cliente ausente'))
  })

  it('explica cuando no hay ruta asignada', async () => {
    vi.spyOn(api, 'obtenerMiRuta').mockResolvedValue(null)
    render(<PaginaMiRuta />)
    expect(await screen.findByRole('heading', { name: /No tiene una ruta asignada/ })).toBeInTheDocument()
  })

  it('muestra el error del servidor sin ocultarlo', async () => {
    vi.spyOn(api, 'obtenerMiRuta').mockResolvedValue(miRuta([{ ...base, estado: 'PENDIENTE' }]))
    vi.spyOn(api, 'registrarEstado').mockRejectedValue(new ApiError(422, 'No puede pasar de PENDIENTE a ENTREGADO'))
    const user = userEvent.setup()
    render(<PaginaMiRuta />)
    await user.click(await screen.findByRole('button', { name: 'Salir hacia la parada: pedido DR-1001' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('No puede pasar de PENDIENTE')
  })

  it('informa cuando falla la carga', async () => {
    vi.spyOn(api, 'obtenerMiRuta').mockRejectedValue(new ApiError(0, 'No se pudo conectar con el servidor.'))
    render(<PaginaMiRuta />)
    expect(await screen.findByRole('alert')).toHaveTextContent('No se pudo conectar')
  })
})

describe('PaginaSeguimiento (HU-006 y HU-010)', () => {
  const seguimiento = (paradas: api.ParadaEjecucion[], conductorId: string | null = null): api.Seguimiento => ({
    fecha: '2026-10-10',
    deposito,
    rutas: [ruta(paradas, conductorId)],
    incidencias: paradas
      .filter((p) => p.estado === 'INCIDENCIA')
      .map((p) => ({
        pedidoId: p.pedidoId, codigo: p.codigo, direccion: p.direccion, distrito: p.distrito, nota: p.nota,
        vehiculo: 'ECO-103', conductorNombre: 'Conductor de ruta', actualizadoEn: '2026-10-10T15:00:00Z',
      })),
    conductoresDisponibles: [{ id: 'c1', nombre: 'Conductor de ruta' }],
  })

  it('asigna un conductor a la ruta', async () => {
    vi.spyOn(api, 'obtenerSeguimiento').mockResolvedValue(seguimiento([{ ...base, estado: 'PENDIENTE' }]))
    const asignar = vi.spyOn(api, 'asignarConductor').mockResolvedValue()
    const user = userEvent.setup()
    render(<PaginaSeguimiento />)
    await user.selectOptions(await screen.findByLabelText('Conductor asignado al vehículo ECO-103'), 'c1')
    await waitFor(() => expect(asignar).toHaveBeenCalledWith(expect.any(String), 'v1', 'c1'))
    expect(await screen.findByRole('status')).toHaveTextContent('Conductor asignado al vehículo ECO-103.')
  })

  it('muestra la incidencia con su descripción y permite reprogramarla', async () => {
    vi.spyOn(api, 'obtenerSeguimiento').mockResolvedValue(
      seguimiento([{ ...base, estado: 'INCIDENCIA', nota: 'Cliente ausente' }], 'c1'),
    )
    const reprogramar = vi.spyOn(api, 'reprogramarParada').mockResolvedValue()
    const user = userEvent.setup()
    render(<PaginaSeguimiento />)
    const seccion = (await screen.findByRole('heading', { name: /Incidencias abiertas \(1\)/ })).closest('section')!
    expect(within(seccion).getByText('Cliente ausente')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Reprogramar pedido DR-1001' }))
    await waitFor(() => expect(reprogramar).toHaveBeenCalledWith('p1', expect.any(String)))
    expect(await screen.findByRole('status')).toHaveTextContent('volvió a Pendiente')
  })

  it('reoptimiza las paradas pendientes e informa el resultado', async () => {
    vi.spyOn(api, 'obtenerSeguimiento').mockResolvedValue(seguimiento([{ ...base, estado: 'PENDIENTE' }], 'c1'))
    const reoptimizar = vi.spyOn(api, 'reoptimizarRutas').mockResolvedValueOnce({ rutasReordenadas: 1 }).mockResolvedValue({ rutasReordenadas: 0 })
    const user = userEvent.setup()
    render(<PaginaSeguimiento />)
    await user.click(await screen.findByRole('button', { name: /Reoptimizar pendientes/ }))
    expect(await screen.findByRole('status')).toHaveTextContent('Se reordenaron las paradas pendientes de 1 ruta(s)')
    await user.click(screen.getByRole('button', { name: /Reoptimizar pendientes/ }))
    await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('ya es el más corto'))
    expect(reoptimizar).toHaveBeenCalledTimes(2)
  })

  it('indica cuando no hay rutas guardadas', async () => {
    vi.spyOn(api, 'obtenerSeguimiento').mockResolvedValue(null)
    render(<PaginaSeguimiento />)
    expect(await screen.findByRole('heading', { name: /No hay rutas guardadas/ })).toBeInTheDocument()
  })
})
