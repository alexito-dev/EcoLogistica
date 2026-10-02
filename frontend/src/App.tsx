import { ShieldX } from 'lucide-react'
import type { Rol } from './api/auth'
import { AuthProvider } from './auth/AuthContext'
import { useAuth } from './auth/useAuth'
import LoginPage from './auth/LoginPage'
import AppShell from './components/AppShell'
import PaginaPedidos from './pages/PaginaPedidos'

/** Matriz RBAC del documento 08 para la vista de pedidos. */
const PUEDEN_CONSULTAR_PEDIDOS: Rol[] = ['PLANIFICADOR', 'ADMIN']

function Raiz() {
  const { estado, usuario, salir } = useAuth()

  if (estado === 'cargando') {
    return (
      <div className="pantalla-carga" role="status" aria-live="polite">
        <span className="girador" aria-hidden="true" />
        <span>Verificando sesión…</span>
      </div>
    )
  }

  if (estado === 'anonimo' || !usuario) return <LoginPage />

  return (
    <AppShell usuario={usuario} onSalir={salir}>
      {PUEDEN_CONSULTAR_PEDIDOS.includes(usuario.rol) ? (
        <PaginaPedidos puedeRegistrar={usuario.rol === 'PLANIFICADOR'} />
      ) : (
        <section className="tarjeta sin-acceso aparecer" aria-labelledby="titulo-sin-acceso">
          <span className="vacio__icono">
            <ShieldX size={34} aria-hidden="true" />
          </span>
          <h1 id="titulo-sin-acceso">Acceso no autorizado</h1>
          <p>
            Su rol no tiene permiso para la vista de pedidos. Las vistas de su rol estarán disponibles en próximas
            iteraciones.
          </p>
        </section>
      )}
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
