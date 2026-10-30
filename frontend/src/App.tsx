import { lazy, Suspense, useEffect, useState } from 'react'
import { ShieldX } from 'lucide-react'
import { AuthProvider } from './auth/AuthContext'
import { useAuth } from './auth/useAuth'
import LoginPage from './auth/LoginPage'
import AppShell from './components/AppShell'
import AvisoSesion from './components/AvisoSesion'
import { NAVEGACION, vistasDelRol, type Vista } from './lib/navegacion'
import PaginaPedidos from './pages/PaginaPedidos'

// Flota, Rutas (con Leaflet) e Indicadores se descargan solo al abrirlas: carga inicial ligera para 2G/3G (RES-06).
const PaginaFlota = lazy(() => import('./pages/PaginaFlota'))
const PaginaRutas = lazy(() => import('./pages/PaginaRutas'))
const PaginaIndicadores = lazy(() => import('./pages/PaginaIndicadores'))

function CargandoVista() {
  return (
    <div className="pantalla-carga pantalla-carga--vista" role="status" aria-live="polite">
      <span className="girador" aria-hidden="true" />
      <span>Cargando…</span>
    </div>
  )
}

/** Título de la pestaña según lo que se ve (WCAG 2.4.2): la app es de una sola página. */
function tituloDePagina(estado: string, conSesion: boolean, vista: Vista | undefined): string | null {
  if (estado === 'cargando') return null
  if (!conSesion) return 'Iniciar sesión'
  if (!vista) return 'Acceso no autorizado'
  return NAVEGACION.find((n) => n.vista === vista)?.texto ?? null
}

function Raiz() {
  const { estado, usuario, salir } = useAuth()
  const [elegida, setVista] = useState<Vista | null>(null)

  // Cada rol abre su primera vista permitida; una vista ajena nunca se muestra (RBAC, documento 08).
  const permitidas = usuario ? vistasDelRol(usuario.rol) : []
  const vista = elegida && permitidas.includes(elegida) ? elegida : permitidas[0]
  const titulo = tituloDePagina(estado, estado !== 'anonimo' && !!usuario, vista)
  useEffect(() => {
    if (titulo) document.title = `${titulo} · EcoLogística Huancayo`
  }, [titulo])

  if (estado === 'cargando') {
    return (
      <div className="pantalla-carga" role="status" aria-live="polite">
        <span className="girador" aria-hidden="true" />
        <span>Verificando sesión…</span>
      </div>
    )
  }

  if (estado === 'anonimo' || !usuario) return <LoginPage />

  if (!vista) {
    return (
      <AppShell usuario={usuario} onSalir={salir} vista="pedidos" onVistaChange={setVista}>
        <section className="tarjeta sin-acceso aparecer" aria-labelledby="titulo-sin-acceso">
          <span className="vacio__icono">
            <ShieldX size={34} aria-hidden="true" />
          </span>
          <h1 id="titulo-sin-acceso">Acceso no autorizado</h1>
          <p>Su rol aún no tiene vistas en esta versión. Estarán disponibles en próximas iteraciones.</p>
        </section>
      </AppShell>
    )
  }

  return (
    <AppShell usuario={usuario} onSalir={salir} vista={vista} onVistaChange={setVista}>
      <AvisoSesion />
      <Suspense fallback={<CargandoVista />}>
        {vista === 'pedidos' && <PaginaPedidos puedeRegistrar={usuario.rol === 'PLANIFICADOR'} />}
        {vista === 'flota' && (
          <PaginaFlota puedeAdministrar={usuario.rol === 'ADMIN'} puedePlanificar={usuario.rol === 'PLANIFICADOR'} />
        )}
        {vista === 'rutas' && <PaginaRutas />}
        {vista === 'indicadores' && <PaginaIndicadores />}
      </Suspense>
    </AppShell>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <Raiz />
    </AuthProvider>
  )
}
