import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { ApiError } from '../src/api/http'
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
beforeEach(() => {
  vi.spyOn(trazado, 'trazarPorCalles').mockResolvedValue(null)
  vi.spyOn(api, 'obtenerRutasGuardadas').mockResolvedValue(null)
})
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

  it('guarda las rutas y avisa que quedaron guardadas', async () => {
    vi.spyOn(api, 'obtenerVistaPrevia').mockResolvedValue(vista)
    const guardar = vi.spyOn(api, 'guardarRutas').mockResolvedValue({ fecha: vista.fecha, guardadaEn: '2026-10-30T15:00:00Z', guardadaPor: 'Ana Plan', vista })
    render(<PaginaRutas />)
    await screen.findByText('ECO-103')
    await userEvent.click(screen.getByRole('button', { name: 'Guardar rutas' }))
    expect(guardar).toHaveBeenCalledOnce()
    expect(await screen.findByText(/Rutas guardadas\. Puede volver a abrirlas/)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Ver cálculo actual' })).toBeInTheDocument()
  })

  it('abre las rutas guardadas de la fecha y permite volver al cálculo actual', async () => {
    const guardadaVista = { ...vista, rutas: [{ ...vista.rutas[0], vehiculo: { ...vista.rutas[0].vehiculo, placa: 'GUA-001' } }] }
    vi.spyOn(api, 'obtenerVistaPrevia').mockResolvedValue(vista)
    vi.spyOn(api, 'obtenerRutasGuardadas').mockResolvedValue({ fecha: vista.fecha, guardadaEn: '2026-10-30T15:00:00Z', guardadaPor: 'Ana Plan', vista: guardadaVista })
    render(<PaginaRutas />)
    expect(await screen.findByText('GUA-001')).toBeInTheDocument()
    expect(screen.getByText(/Hay rutas guardadas el .* por Ana Plan/)).toBeInTheDocument()
    await userEvent.click(screen.getByRole('button', { name: 'Ver cálculo actual' }))
    expect(screen.getByText('ECO-103')).toBeInTheDocument()
    expect(screen.queryByText('GUA-001')).not.toBeInTheDocument()
  })

  it('no permite guardar si no hay rutas', async () => {
    vi.spyOn(api, 'obtenerVistaPrevia').mockResolvedValue({ ...vista, rutas: [], sinAsignar: [] })
    render(<PaginaRutas />)
    await screen.findByText(/declare el turno de los vehículos en Flota/)
    expect(screen.getByRole('button', { name: 'Guardar rutas' })).toBeDisabled()
  })
})


describe('Rutas: recuperación, fallos de persistencia y decisiones de planificación', () => {
  it('reintenta la vista previa después de un error temporal', async () => {
    const recuperar = vi.spyOn(api, 'obtenerVistaPrevia')
      .mockRejectedValueOnce(new ApiError(503, 'Sin conexión con planificador'))
      .mockResolvedValue(vista)
    render(<PaginaRutas />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Sin conexión con planificador')
    await userEvent.click(screen.getByRole('button', { name: 'Reintentar' }))
    expect(await screen.findByText('ECO-103')).toBeInTheDocument()
    expect(recuperar).toHaveBeenCalledTimes(2)
  })

  it('mantiene la vista para volver a intentar cuando falla el guardado', async () => {
    vi.spyOn(api, 'obtenerVistaPrevia').mockResolvedValue(vista)
    const guardar = vi.spyOn(api, 'guardarRutas').mockRejectedValue(new ApiError(422, 'Sin rutas válidas para guardar'))
    render(<PaginaRutas />)
    await screen.findByText('ECO-103')
    await userEvent.click(screen.getByRole('button', { name: 'Guardar rutas' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('Sin rutas válidas para guardar')
    expect(guardar).toHaveBeenCalledOnce()
    expect(screen.getByRole('button', { name: 'Guardar rutas' })).toBeEnabled()
    expect(screen.getByText('ECO-103')).toBeInTheDocument()
  })

  it('recupera la propuesta calculada aun cuando falla consultar rutas guardadas', async () => {
    vi.spyOn(api, 'obtenerVistaPrevia').mockResolvedValue(vista)
    vi.mocked(api.obtenerRutasGuardadas).mockRejectedValue(new Error('base temporal desconectada'))
    render(<PaginaRutas />)
    expect(await screen.findByText('ECO-103')).toBeInTheDocument()
    expect(screen.queryByLabelText('Rutas guardadas')).not.toBeInTheDocument()
  })

  it('recalcula y permite alternar entre las rutas guardadas y el cálculo actual', async () => {
    const antigua = { ...vista, rutas: [{ ...vista.rutas[0], vehiculo: { ...vista.rutas[0].vehiculo, placa: 'GUA-777' } }] }
    const vistaActual = { ...vista, rutas: [{ ...vista.rutas[0], vehiculo: { ...vista.rutas[0].vehiculo, placa: 'NUE-123' } }] }
    const obtener = vi.spyOn(api, 'obtenerVistaPrevia').mockResolvedValue(vistaActual)
    vi.mocked(api.obtenerRutasGuardadas).mockResolvedValue({
      fecha: vista.fecha, guardadaEn: '2026-10-30T15:00:00Z', guardadaPor: 'Planificador',
      vista: antigua,
    })
    render(<PaginaRutas />)
    await screen.findByText('GUA-777')
    await userEvent.click(screen.getByRole('button', { name: 'Recalcular' }))
    expect(await screen.findByText('NUE-123')).toBeInTheDocument()
    expect(obtener).toHaveBeenCalledTimes(2)
    await userEvent.click(screen.getByRole('button', { name: 'Abrir rutas guardadas' }))
    expect(screen.getByText('GUA-777')).toBeInTheDocument()
  })

  it('muestra la condición de llegada puntual de todas las paradas', async () => {
    vi.spyOn(api, 'obtenerVistaPrevia').mockResolvedValue({
      ...vista,
      resumen: { ...vista.resumen, paradasFueraDeVentana: 0, paradasFueraDeVentanaBase: 1 },
    })
    render(<PaginaRutas />)
    expect(await screen.findByText(/Todas las paradas llegan dentro de su ventana/)).toHaveTextContent('sin optimizar: 1 tarde')
  })

  it('omite la promesa de ahorro si la estimación de emisiones no mejora', async () => {
    vi.spyOn(api, 'obtenerVistaPrevia').mockResolvedValue({
      ...vista, resumen: { ...vista.resumen, ahorroCo2Pct: 0 },
    })
    render(<PaginaRutas />)
    await screen.findByText('ECO-103')
    expect(screen.getByText('Estimadas por combustible')).toBeInTheDocument()
  })

  it('actualiza el filtro y descarta la selección previa al cambiar de fecha', async () => {
    const espia = vi.spyOn(api, 'obtenerVistaPrevia').mockResolvedValue(vista)
    render(<PaginaRutas />)
    const boton = await screen.findByRole('button', { name: /ECO-103/ })
    await userEvent.click(boton)
    expect(boton).toHaveAttribute('aria-pressed', 'true')
    fireEvent.change(screen.getByLabelText('Fecha de reparto'), { target: { value: '2026-12-01' } })
    await waitFor(() => expect(espia).toHaveBeenLastCalledWith('2026-12-01'))
    expect(screen.getByRole('button', { name: /ECO-103/ })).toHaveAttribute('aria-pressed', 'false')
  })
})
