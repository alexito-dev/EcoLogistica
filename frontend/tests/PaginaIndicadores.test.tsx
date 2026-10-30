import { render, screen } from '@testing-library/react'
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
    expect(await screen.findByText('Emisiones del 10/10/2026')).toBeInTheDocument()
    expect(screen.getByText('6.08 de 11.32 kg sin optimizar')).toBeInTheDocument()
    expect(screen.getByText('El Tambo')).toBeInTheDocument()
    expect(screen.getByText('Urgente')).toBeInTheDocument()
    expect(screen.getByText('Eléctrico')).toBeInTheDocument()
    // Los estados sin pedidos no ocupan una fila.
    expect(screen.queryByText('Entregado')).not.toBeInTheDocument()
  })

  it('explica cuando la fecha no tiene pedidos', async () => {
    vi.spyOn(api, 'obtenerIndicadores').mockResolvedValue({ ...datos, dia: { ...datos.dia, pedidos: 0, asignados: 0 } })
    render(<PaginaIndicadores />)
    expect(await screen.findByText('No hay pedidos planificables en esta fecha.')).toBeInTheDocument()
  })
})

describe('menú por rol', () => {
  it('cada rol ve solo sus vistas', () => {
    expect(vistasDelRol('PLANIFICADOR')).toEqual(['pedidos', 'flota', 'rutas', 'indicadores'])
    expect(vistasDelRol('ADMIN')).toEqual(['pedidos', 'flota', 'rutas', 'indicadores'])
    expect(vistasDelRol('GERENTE')).toEqual(['indicadores'])
    expect(vistasDelRol('CONDUCTOR')).toEqual([])
    expect(vistasDelRol('AUDITOR')).toEqual([])
  })
})
