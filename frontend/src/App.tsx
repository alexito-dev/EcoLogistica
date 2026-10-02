import { useCallback, useEffect, useMemo, useState } from 'react'
import { Boxes, Clock, Plus, TriangleAlert, Weight } from 'lucide-react'
import { ApiError, listarPedidos, type Pedido } from './api/pedidos'
import AppShell from './components/AppShell'
import Drawer from './components/Drawer'
import Hero from './components/Hero'
import PedidoDetalle from './components/PedidoDetalle'
import PedidoForm from './components/PedidoForm'
import PedidosTable from './components/PedidosTable'
import StatCard from './components/StatCard'
import Toast from './components/Toast'

export default function App() {
  const [pedidos, setPedidos] = useState<Pedido[]>([])
  const [total, setTotal] = useState(0)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [formAbierto, setFormAbierto] = useState(false)
  const [detalle, setDetalle] = useState<Pedido | null>(null)
  const [aviso, setAviso] = useState<string | null>(null)
  const [nuevoId, setNuevoId] = useState<string | null>(null)

  const cargar = useCallback(async () => {
    setCargando(true)
    setError(null)
    try {
      const listado = await listarPedidos(1, 100)
      setPedidos(listado.items)
      setTotal(listado.total)
    } catch (e) {
      setError(e instanceof ApiError ? e.message : 'No se pudo cargar el listado de pedidos.')
    } finally {
      setCargando(false)
    }
  }, [])

  useEffect(() => {
    void cargar()
  }, [cargar])

  const resumen = useMemo(() => {
    const pendientes = pedidos.filter((p) => p.estado === 'PENDIENTE').length
    const urgentes = pedidos.filter((p) => p.prioridad >= 3).length
    const kg = pedidos.reduce((suma, p) => suma + p.demandaKg, 0)
    return { pendientes, urgentes, kg }
  }, [pedidos])

  const cerrarAviso = useCallback(() => setAviso(null), [])
  const abrirFormulario = () => setFormAbierto(true)

  return (
    <AppShell>
      <Hero
        titulo="Pedidos"
        subtitulo="Registre y consulte los pedidos de última milla con su ventana horaria."
        accion={
          <button type="button" className="boton boton--claro" onClick={abrirFormulario}>
            <Plus size={18} aria-hidden="true" />
            Nuevo pedido
          </button>
        }
      />

      <section className="stats" aria-label="Resumen de pedidos">
        <StatCard indice={1} titulo="Pedidos" valor={total} detalle="Registrados en total" icono={Boxes} />
        <StatCard indice={2} titulo="Pendientes" valor={resumen.pendientes} detalle="Esperando planificación" icono={Clock} />
        <StatCard indice={3} titulo="Prioridad alta" valor={resumen.urgentes} detalle="Alta o urgente" icono={TriangleAlert} />
        <StatCard indice={4} titulo="Carga total" valor={resumen.kg} sufijo="kg" detalle="Suma de pesos" icono={Weight} />
      </section>

      <PedidosTable
        pedidos={pedidos}
        cargando={cargando}
        error={error}
        resaltadoId={nuevoId}
        onReintentar={() => void cargar()}
        onVer={setDetalle}
        onNuevo={abrirFormulario}
      />

      <Drawer
        abierto={formAbierto}
        titulo="Registrar pedido"
        descripcion="Los campos con * son obligatorios. Las horas se ingresan en hora de Lima."
        onCerrar={() => setFormAbierto(false)}
      >
        <PedidoForm
          onCancelar={() => setFormAbierto(false)}
          onCreado={(pedido) => {
            setFormAbierto(false)
            setNuevoId(pedido.id)
            setAviso(`Pedido ${pedido.codigo} registrado en estado Pendiente.`)
            void cargar()
          }}
        />
      </Drawer>

      <Drawer
        abierto={detalle !== null}
        titulo={detalle?.codigo ?? ''}
        descripcion="Detalle del pedido"
        onCerrar={() => setDetalle(null)}
      >
        {detalle && <PedidoDetalle pedido={detalle} />}
      </Drawer>

      <Toast mensaje={aviso} onCerrar={cerrarAviso} />
    </AppShell>
  )
}
