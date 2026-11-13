import { useCallback, useEffect, useMemo, useState } from 'react'
import { Boxes, Clock, FileUp, Plus, TriangleAlert, Weight } from 'lucide-react'
import { ApiError, listarPedidos, PEDIDOS_POR_PAGINA, type EstadoPedido, type Pedido } from '../api/pedidos'
import Drawer from '../components/Drawer'
import Hero from '../components/Hero'
import ImportarPedidos from '../components/ImportarPedidos'
import PedidoDetalle from '../components/PedidoDetalle'
import PedidoForm from '../components/PedidoForm'
import PedidosTable from '../components/PedidosTable'
import StatCard from '../components/StatCard'
import Toast from '../components/Toast'

interface Props {
  /** Solo el planificador registra pedidos (matriz RBAC); el administrador solo consulta. */
  puedeRegistrar: boolean
}

export default function PaginaPedidos({ puedeRegistrar }: Props) {
  const [pedidos, setPedidos] = useState<Pedido[]>([])
  const [total, setTotal] = useState(0)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [formAbierto, setFormAbierto] = useState(false)
  const [importarAbierto, setImportarAbierto] = useState(false)
  const [detalle, setDetalle] = useState<Pedido | null>(null)
  const [aviso, setAviso] = useState<string | null>(null)
  const [nuevoId, setNuevoId] = useState<string | null>(null)
  const [pagina, setPagina] = useState(1)
  const [estadoFiltro, setEstadoFiltro] = useState<'TODOS' | EstadoPedido>('TODOS')

  // El estado se actualiza al resolver la promesa: el efecto inicial no provoca renders en cascada.
  const consultar = useCallback(
    () =>
      listarPedidos(pagina, PEDIDOS_POR_PAGINA, estadoFiltro === 'TODOS' ? undefined : estadoFiltro)
        .then((listado) => {
          setPedidos(listado.items)
          setTotal(listado.total)
        })
        .catch((e: unknown) => setError(e instanceof ApiError ? e.message : 'No se pudo cargar el listado de pedidos.'))
        .finally(() => setCargando(false)),
    [pagina, estadoFiltro],
  )

  const cargar = useCallback(() => {
    setCargando(true)
    setError(null)
    return consultar()
  }, [consultar])

  useEffect(() => {
    void consultar()
  }, [consultar])

  const resumen = useMemo(() => {
    const pendientes = pedidos.filter((p) => p.estado === 'PENDIENTE').length
    const urgentes = pedidos.filter((p) => p.prioridad >= 3).length
    const kg = pedidos.reduce((suma, p) => suma + p.demandaKg, 0)
    return { pendientes, urgentes, kg }
  }, [pedidos])

  const cerrarAviso = useCallback(() => setAviso(null), [])
  const abrirFormulario = () => setFormAbierto(true)

  return (
    <>
      <Hero
        titulo="Pedidos"
        subtitulo="Registre y consulte los pedidos de última milla con su ventana horaria."
        accion={
          puedeRegistrar ? (
            <>
              <button type="button" className="boton boton--claro" onClick={abrirFormulario}>
                <Plus size={18} aria-hidden="true" />
                Nuevo pedido
              </button>
              <button type="button" className="boton boton--claro" onClick={() => setImportarAbierto(true)}>
                <FileUp size={18} aria-hidden="true" />
                Importar pedidos
              </button>
            </>
          ) : (
            <p className="hero__nota">Modo consulta: solo el planificador registra pedidos.</p>
          )
        }
      />

      <section className="stats" aria-label="Resumen de pedidos">
        <StatCard indice={1} titulo="Pedidos" valor={total} detalle="Registrados en total" icono={Boxes} />
        <StatCard indice={2} titulo="Pendientes" valor={resumen.pendientes} detalle="En esta página" icono={Clock} />
        <StatCard indice={3} titulo="Prioridad alta" valor={resumen.urgentes} detalle="En esta página" icono={TriangleAlert} />
        <StatCard indice={4} titulo="Carga total" valor={resumen.kg} sufijo="kg" detalle="Suma de esta página" icono={Weight} />
      </section>

      <PedidosTable
        pedidos={pedidos}
        cargando={cargando}
        error={error}
        resaltadoId={nuevoId}
        onReintentar={() => void cargar()}
        onVer={setDetalle}
        onNuevo={puedeRegistrar ? abrirFormulario : undefined}
        pagina={pagina}
        limite={PEDIDOS_POR_PAGINA}
        totalRegistros={total}
        onPagina={setPagina}
        estadoFiltro={estadoFiltro}
        onEstadoFiltro={(estado) => {
          setEstadoFiltro(estado)
          setPagina(1)
        }}
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
        abierto={importarAbierto}
        titulo="Importar pedidos"
        descripcion="Carga masiva desde la plantilla CSV"
        onCerrar={() => setImportarAbierto(false)}
      >
        <ImportarPedidos
          onCancelar={() => setImportarAbierto(false)}
          onImportado={(cantidad) => {
            setImportarAbierto(false)
            setAviso(`${cantidad} pedido(s) importado(s) en estado Pendiente.`)
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
    </>
  )
}
