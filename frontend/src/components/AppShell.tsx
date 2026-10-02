import type { ReactNode } from 'react'
import { Boxes, LayoutDashboard, Leaf, LogOut, Route, Truck } from 'lucide-react'
import { ETIQUETA_ROL, type Usuario } from '../api/auth'
import ThemeToggle from './ThemeToggle'

interface Props {
  children: ReactNode
  usuario: Usuario
  onSalir: () => void
}

const NAVEGACION = [
  { texto: 'Pedidos', icono: Boxes, activo: true },
  { texto: 'Flota', icono: Truck, activo: false },
  { texto: 'Rutas', icono: Route, activo: false },
  { texto: 'Indicadores', icono: LayoutDashboard, activo: false },
]

function Enlaces({ variante }: { variante: 'lateral' | 'inferior' }) {
  return (
    <ul className={variante === 'lateral' ? 'nav' : 'nav-inferior'}>
      {NAVEGACION.map(({ texto, icono: Icono, activo }) => (
        <li key={texto}>
          {activo ? (
            <a className="nav__item nav__item--activo" href="#contenido" aria-current="page">
              <Icono size={20} aria-hidden="true" />
              <span>{texto}</span>
            </a>
          ) : (
            <span className="nav__item nav__item--pronto" aria-disabled="true" title="Disponible próximamente">
              <Icono size={20} aria-hidden="true" />
              <span>{texto}</span>
              {variante === 'lateral' && <span className="nav__pronto">Pronto</span>}
              {variante === 'inferior' && <span className="solo-lectores"> (próximamente)</span>}
            </span>
          )}
        </li>
      ))}
    </ul>
  )
}

export default function AppShell({ children, usuario, onSalir }: Props) {
  const iniciales = usuario.nombre
    .split(/\s+/)
    .map((p) => p[0])
    .join('')
    .slice(0, 2)
    .toUpperCase()
  return (
    <div className="shell">
      <a className="saltar" href="#contenido">
        Saltar al contenido
      </a>

      <aside className="lateral">
        <div className="marca">
          <img src="/logo_ecologistica.png" alt="" width="40" height="40" />
          <div>
            <p className="marca__nombre">EcoLogística</p>
            <p className="marca__lema">Huancayo</p>
          </div>
        </div>
        <nav aria-label="Navegación principal">
          <Enlaces variante="lateral" />
        </nav>
        <div className="lateral__eco">
          <Leaf size={18} aria-hidden="true" />
          <p>Cada ruta optimizada es menos CO₂ en el valle del Mantaro.</p>
        </div>
      </aside>

      <div className="principal">
        <header className="barra">
          <div className="barra__marca">
            <img src="/logo_ecologistica.png" alt="" width="32" height="32" />
            <span>EcoLogística</span>
          </div>
          <p className="barra__contexto">Panel de {ETIQUETA_ROL[usuario.rol].toLowerCase()}</p>
          <div className="barra__acciones">
            <div className="usuario" title={usuario.correo}>
              <span className="usuario__avatar" aria-hidden="true">
                {iniciales}
              </span>
              <span className="usuario__datos">
                <span className="usuario__nombre">{usuario.nombre}</span>
                <span className="usuario__rol">{ETIQUETA_ROL[usuario.rol]}</span>
              </span>
            </div>
            <ThemeToggle />
            <button
              type="button"
              className="icono-boton icono-boton--borde"
              onClick={onSalir}
              aria-label="Cerrar sesión"
              title="Cerrar sesión"
            >
              <LogOut size={20} aria-hidden="true" />
            </button>
          </div>
        </header>
        <main id="contenido" tabIndex={-1}>
          {children}
        </main>
        <footer className="pie">
          <small>Taller de Proyectos 2 · Ingeniería de Sistemas e Informática · 2026</small>
        </footer>
      </div>

      <nav className="barra-inferior" aria-label="Navegación móvil">
        <Enlaces variante="inferior" />
      </nav>
    </div>
  )
}
