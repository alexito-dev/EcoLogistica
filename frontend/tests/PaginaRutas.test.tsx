import { fireEvent, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import PaginaRutas from '../src/pages/PaginaRutas'
import * as api from '../src/api/rutas'
import * as trazado from '../src/lib/trazado'

const parada: api.Parada = {
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
}

const vista: api.VistaPrevia = {
  fecha: '2026-10-10',
  deposito: { nombre: 'Centro de distribución Huancayo', latitud: -12.0651, longitud: -75.2049 },
  rutas: [
    {
      vehiculo: { id: 'v1', placa: 'ECO-103', tipo: 'Moto carguera eléctrica', combustible: 'ELECTRICO', capacidadKg: 120, capacidadM3: 1.2 },
      paradas: [parada, { ...parada, orden: 2, pedidoId: 'p2', codigo: 'DR-1002', dentroDeVentana: false }],
      distanciaKm: 5.4,
      duracionMin: 75,
      cargaKg: 43,
      usoCapacidadPct: 35.8,
      co2Kg: 0.07,
    },
  ],
  sinAsignar: [{ pedidoId: 'p9', codigo: 'DR-1009', demandaKg: 900, motivo: 'Supera la capacidad libre de la flota' }],
  resumen: {
    pedidos: 3,
    asignados: 2,
    vehiculosUsados: 1,
    vehiculosDisponibles: 3,
    distanciaKm: 5.4,
    distanciaBaseKm: 8.1,
    co2Kg: 0.07,
    co2BaseKg: 2.1,
    ahorroCo2Pct: 96.7,
    paradasFueraDeVentana: 1,
    paradasFueraDeVentanaBase: 2,
  },
  supuestos: ['Velocidad media urbana de 25 km/h para estimar las llegadas.'],
}

// Sin red en las pruebas: el trazado por calles no responde y el mapa usa líneas rectas.
beforeEach(() => vi.spyOn(trazado, 'trazarPorCalles').mockResolvedValue(null))
afterEach(() => vi.restoreAllMocks())

describe('PaginaRutas', () => {
  it('muestra el mapa, el ahorro y las rutas por vehículo', async () => {
    vi.spyOn(api, 'obtenerVistaPrevia').mockResolvedValue(vista)
    render(<PaginaRutas />)
    expect(screen.getByRole('heading', { name: 'Rutas', level: 1 })).toBeInTheDocument()
    expect(await screen.findByRole('region', { name: /Mapa con 1 rutas/ })).toBeInTheDocument()
    expect(screen.getByText('ECO-103')).toBeInTheDocument()
    expect(screen.getByText(/96.7 % menos que sin optimizar/)).toBeInTheDocument()
    expect(screen.getByText('1 parada(s) llegarían fuera de su ventana.')).toBeInTheDocument()
    expect(screen.getByText(/DR-1009/)).toBeInTheDocument()
    expect(screen.getByText('¿Cómo se calcula?')).toBeInTheDocument()
    expect(await screen.findByText('Líneas rectas: servicio de calles no disponible')).toBeInTheDocument()
  })

  it('indica cuando el recorrido sigue las calles', async () => {
    vi.spyOn(api, 'obtenerVistaPrevia').mockResolvedValue(vista)
    vi.mocked(trazado.trazarPorCalles).mockResolvedValue([[-12.0651, -75.2049], [-12.07, -75.21]])
    render(<PaginaRutas />)
    expect(await screen.findByText('Recorrido por calles · OSRM')).toBeInTheDocument()
  })

  it('permite resaltar una ruta', async () => {
    vi.spyOn(api, 'obtenerVistaPrevia').mockResolvedValue(vista)
    render(<PaginaRutas />)
    const boton = await screen.findByRole('button', { name: /ECO-103/ })
    expect(boton).toHaveAttribute('aria-pressed', 'false')
    await userEvent.click(boton)
    expect(boton).toHaveAttribute('aria-pressed', 'true')
  })

  it('explica qué hacer si no hay pedidos para la fecha', async () => {
    vi.spyOn(api, 'obtenerVistaPrevia').mockResolvedValue({ ...vista, rutas: [], sinAsignar: [] })
    render(<PaginaRutas />)
    expect(await screen.findByText(/declare el turno de los vehículos en Flota/)).toBeInTheDocument()
  })

  it('consulta otra fecha al cambiarla', async () => {
    const espia = vi.spyOn(api, 'obtenerVistaPrevia').mockResolvedValue(vista)
    render(<PaginaRutas />)
    await screen.findByText('ECO-103')
    fireEvent.change(screen.getByLabelText('Fecha de reparto'), { target: { value: '2026-12-01' } })
    await screen.findByText('ECO-103')
    expect(espia).toHaveBeenLastCalledWith('2026-12-01')
  })
})
