import { Boxes, LayoutDashboard, Route, Truck, type LucideIcon } from 'lucide-react'
import type { Rol } from '../api/auth'

export type Vista = 'pedidos' | 'flota' | 'rutas' | 'indicadores'

const OPERACION: Rol[] = ['PLANIFICADOR', 'ADMIN']

/** Menú por rol (matriz RBAC del documento 08): cada rol ve solo las vistas que puede abrir. */
export const NAVEGACION: { texto: string; icono: LucideIcon; vista: Vista; roles: Rol[] }[] = [
  { texto: 'Pedidos', icono: Boxes, vista: 'pedidos', roles: OPERACION },
  { texto: 'Flota', icono: Truck, vista: 'flota', roles: OPERACION },
  { texto: 'Rutas', icono: Route, vista: 'rutas', roles: OPERACION },
  { texto: 'Indicadores', icono: LayoutDashboard, vista: 'indicadores', roles: [...OPERACION, 'GERENTE'] },
]

/** Vistas permitidas para un rol, en el orden del menú. */
export function vistasDelRol(rol: Rol): Vista[] {
  return NAVEGACION.filter((n) => n.roles.includes(rol)).map((n) => n.vista)
}
