import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ApiError } from '../src/api/http'
import PaginaIndicadores from '../src/pages/PaginaIndicadores'
import * as api from '../src/api/indicadores'
import { vistasDelRol } from '../src/lib/navegacion'

const datos: api.Indicadores = {
  fecha: '2026-10-10',
  pedidos: {
    total: 6,
    pesoKg: 498,
    porEstado: [
      { estado: 'PENDIENTE', cantidad: 6 },
      { estado: 'ENTREGADO', cantidad: 0 },
    ],
    porDistrito: [
      { distrito: 'El Tambo', cantidad: 2, pesoKg: 258 },
      { distrito: 'Huancayo', cantidad: 1, pesoKg: 35 },
    ],
    porPrioridad: [
      { prioridad: 4, cantidad: 1 },
      { prioridad: 3, cantidad: 2 },
      { prioridad: 2, cantidad: 2 },
      { prioridad: 1, cantidad: 1 },
    ],
  },
  flota: { total: 3, aptos: 3, capacidadAptaKg: 1070, porCombustible: [{ combustible: 'ELECTRICO', cantidad: 1 }] },
  dia: {
    pedidos: 6,
    asignados: 6,
    demandaKg: 498,
    usoCapacidadPct: 46.5,
    distanciaKm: 49.23,
    distanciaBaseKm: 36.72,
    co2Kg: 6.08,
    co2BaseKg: 11.32,
    ahorroCo2Pct: 46.3,
    paradasATiempoPct: 100,
  },
}

afterEach(() => vi.restoreAllMocks())

describe('PaginaIndicadores', () => {
  it('muestra los indicadores clave y los gráficos', async () => {
    vi.spyOn(api, 'obtenerIndicadores').mockResolvedValue(datos)
    render(<PaginaIndicadores />)
    expect(screen.getByRole('heading', { name: 'Indicadores', level: 1 })).toBeInTheDocument()
    expect(await screen.findByText('Emisiones estimadas del 10/10/2026')).toBeInTheDocument()
    expect(screen.getByText('6.08 de 11.32 kg sin optimizar')).toBeInTheDocument()
    expect(screen.getByText('El Tambo')).toBeInTheDocument()
    expect(screen.getByText('Reducción estimada de CO₂e')).toBeInTheDocument()
    expect(screen.getByText('Puntualidad prevista')).toBeInTheDocument()
    expect(screen.getByText(/resultados observados con las entregas que Conducción registró/)).toBeInTheDocument()
    expect(screen.getByText('Urgente')).toBeInTheDocument()
    expect(screen.getByText('Eléctrico')).toBeInTheDocument()
    // Los estados sin pedidos no ocupan una fila.
    expect(screen.queryByText('Entregado')).not.toBeInTheDocument()
  })

  it('explica cuando la fecha no tiene pedidos', async () => {
    vi.spyOn(api, 'obtenerIndicadores').mockResolvedValue({ ...datos, dia: { ...datos.dia, pedidos: 0, asignados: 0 } })
    render(<PaginaIndicadores />)
    expect(await screen.findByText(/No hay pedidos planificables en esta fecha/)).toBeInTheDocument()
  })
})

describe('menú por rol', () => {
  it('cada rol ve solo sus vistas', () => {
    expect(vistasDelRol('PLANIFICADOR')).toEqual(['pedidos', 'flota', 'rutas', 'seguimiento', 'indicadores'])
    expect(vistasDelRol('ADMIN')).toEqual(['pedidos', 'flota', 'rutas', 'seguimiento', 'indicadores'])
    expect(vistasDelRol('GERENTE')).toEqual(['indicadores'])
    expect(vistasDelRol('CONDUCTOR')).toEqual(['miruta'])
    expect(vistasDelRol('AUDITOR')).toEqual([])
  })
})


describe('Indicadores: condiciones de error, filtros y valores límite', () => {
  it('permite reintentar al fallar el servicio y recupera los gráficos', async () => {
    const obtener = vi.spyOn(api, 'obtenerIndicadores')
      .mockRejectedValueOnce(new ApiError(503, 'API temporalmente no disponible'))
      .mockResolvedValue(datos)
    render(<PaginaIndicadores />)
    expect(await screen.findByRole('alert')).toHaveTextContent('API temporalmente no disponible')
    await userEvent.click(screen.getByRole('button', { name: 'Reintentar' }))
    expect(await screen.findByText('El Tambo')).toBeInTheDocument()
    expect(obtener).toHaveBeenCalledTimes(2)
  })

  it('consulta una fecha nueva tras cambiar el filtro', async () => {
    const obtener = vi.spyOn(api, 'obtenerIndicadores').mockResolvedValue(datos)
    render(<PaginaIndicadores />)
    await screen.findByText('El Tambo')
    fireEvent.change(screen.getByLabelText('Fecha de reparto'), { target: { value: '2026-12-01' } })
    await waitFor(() => expect(obtener).toHaveBeenLastCalledWith('2026-12-01'))
  })

  it('muestra todas las secciones sin datos cuando sus conteos son cero', async () => {
    const vacio: api.Indicadores = {
      ...datos,
      pedidos: { total: 0, pesoKg: 0, porEstado: [], porDistrito: [], porPrioridad: [] },
      flota: { total: 0, aptos: 0, capacidadAptaKg: 0, porCombustible: [] },
      dia: { ...datos.dia, pedidos: 0, asignados: 0, demandaKg: 0, distanciaKm: 0,
        distanciaBaseKm: 0, co2Kg: 0, co2BaseKg: 0, ahorroCo2Pct: 0, paradasATiempoPct: 0,
        usoCapacidadPct: 0 },
    }
    vi.spyOn(api, 'obtenerIndicadores').mockResolvedValue(vacio)
    render(<PaginaIndicadores />)
    expect(await screen.findByText(/No hay pedidos planificables/)).toBeInTheDocument()
    expect(screen.getAllByText('Sin datos para mostrar.')).toHaveLength(5)
  })

  it('no anuncia ahorro de kilómetros cuando la ruta propuesta no mejora la referencia', async () => {
    vi.spyOn(api, 'obtenerIndicadores').mockResolvedValue({
      ...datos, dia: { ...datos.dia, distanciaKm: 55, distanciaBaseKm: 50 },
    })
    render(<PaginaIndicadores />)
    expect(await screen.findByText(/La propuesta de rutas recorre 55 km/)).not.toHaveTextContent('km menos que sin optimizar')
  })

  it('explica un fallo inesperado sin mostrar su traza ni bloquear una nueva consulta', async () => {
    const obtener = vi.spyOn(api, 'obtenerIndicadores').mockRejectedValueOnce(new Error('fallo interno')).mockResolvedValue(datos)
    render(<PaginaIndicadores />)
    expect(await screen.findByRole('alert')).toHaveTextContent('No se pudieron calcular los indicadores.')
    expect(screen.queryByText('fallo interno')).not.toBeInTheDocument()
    await userEvent.click(screen.getByRole('button', { name: 'Reintentar' }))
    await screen.findByText('El Tambo')
    expect(obtener).toHaveBeenCalledTimes(2)
  })
})

describe('resultados observados (ECO-14 y ECO-26)', () => {
  const ejecucion: api.Ejecucion = {
    fecha: '2026-10-10', paradas: 6, entregadas: 3, incidencias: 1, canceladas: 0, reprogramadas: 0, pendientes: 2,
    entregasATiempo: 2, entregasTarde: 1, puntualidadPct: 66.7, cumplimientoPct: 50,
    distanciaRecorridaKm: 12.5, distanciaPrevistaKm: 30, co2RecorridoKg: 2.1, co2PrevistoKg: 5,
  }

  it('muestra puntualidad, cumplimiento, recorrido y CO₂e observados', async () => {
    vi.spyOn(api, 'obtenerIndicadores').mockResolvedValue(datos)
    vi.spyOn(api, 'obtenerEjecucion').mockResolvedValue(ejecucion)
    render(<PaginaIndicadores />)
    const seccion = (await screen.findByRole('heading', { name: 'Resultados observados de la ejecución' })).closest('article')!
    expect(seccion).toHaveTextContent(/66[.,]7 % puntualidad observada/)
    expect(seccion).toHaveTextContent('3 de 6 entregadas')
    expect(seccion).toHaveTextContent(/12[.,]5 km recorridos/)
    expect(seccion).toHaveTextContent(/2[.,]1 kg CO₂e emitidos/)
  })

  it('no inventa porcentajes cuando no hay entregas o rutas', async () => {
    vi.spyOn(api, 'obtenerIndicadores').mockResolvedValue(datos)
    const observados = vi.spyOn(api, 'obtenerEjecucion').mockResolvedValue({ ...ejecucion, entregadas: 0, puntualidadPct: null })
    render(<PaginaIndicadores />)
    expect(await screen.findByText(/ninguna entrega registrada todavía/)).toBeInTheDocument()
    observados.mockResolvedValue(null)
    await userEvent.setup().click(screen.getByRole('button', { name: /Actualizar/ }))
    expect(await screen.findByText(/no hay resultados observados/)).toBeInTheDocument()
  })
})
