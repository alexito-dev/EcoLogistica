import type { ReactNode } from 'react'
import { Leaf, LogOut } from 'lucide-react'
import { ETIQUETA_ROL, type Rol, type Usuario } from '../api/auth'
import { NAVEGACION, type Vista } from '../lib/navegacion'
import ThemeToggle from './ThemeToggle'

interface Props {
  children: ReactNode
  usuario: Usuario
  onSalir: () => void
  vista: Vista
  onVistaChange: (vista: Vista) => void
}

function Enlaces({ variante, rol, vista, onVistaChange }: { variante: 'lateral' | 'inferior'; rol: Rol; vista: Vista; onVistaChange: (vista: Vista) => void }) {
  const enlaces = NAVEGACION.filter((n) => n.roles.includes(rol))
  return (
    <ul className={variante === 'lateral' ? 'nav' : 'nav-inferior'} style={variante === 'inferior' ? { gridTemplateColumns: `repeat(${enlaces.length}, 1fr)` } : undefined}>
      {enlaces.map(({ texto, icono: Icono, vista: destino }) => (
        <li key={texto}>
          <button type="button" className={`nav__item${vista === destino ? ' nav__item--activo' : ''}`} onClick={() => onVistaChange(destino)} aria-current={vista === destino ? 'page' : undefined}>
            <Icono size={20} aria-hidden="true" />
            <span>{texto}</span>
          </button>
        </li>
      ))}
    </ul>
  )
}

export default function AppShell({ children, usuario, onSalir, vista, onVistaChange }: Props) {
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
          <Enlaces variante="lateral" rol={usuario.rol} vista={vista} onVistaChange={onVistaChange} />
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
        <Enlaces variante="inferior" rol={usuario.rol} vista={vista} onVistaChange={onVistaChange} />
      </nav>
    </div>
  )
}
