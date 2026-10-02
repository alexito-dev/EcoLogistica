import { useMemo, useState, type CSSProperties } from 'react'
import {
  ChevronLeft,
  ChevronRight,
  ChevronRight as Flecha,
  Clock,
  Eye,
  Inbox,
  ListFilter,
  MapPin,
  RefreshCw,
  Search,
  SearchX,
  TriangleAlert,
  Weight,
} from 'lucide-react'
import type { EstadoPedido, Pedido } from '../api/pedidos'
import { useMediaQuery } from '../hooks/useMediaQuery'
import { ventanaCorta } from '../lib/fechas'
import { ETIQUETA_ESTADO, ETIQUETA_PRIORIDAD, formatoNumero } from '../lib/estados'

const POR_PAGINA = 8

interface Props {
  pedidos: Pedido[]
  cargando: boolean
  error: string | null
  resaltadoId?: string | null
  onReintentar: () => void
  onVer: (pedido: Pedido) => void
  onNuevo?: () => void
}

function Insignias({ p }: { p: Pedido }) {
  return (
    <>
      <span className={`prioridad prioridad--${p.prioridad}`}>{ETIQUETA_PRIORIDAD[p.prioridad]}</span>
      <span className={`insignia insignia--${p.estado.toLowerCase()}`}>{ETIQUETA_ESTADO[p.estado]}</span>
    </>
  )
}

export default function PedidosTable({ pedidos, cargando, error, resaltadoId, onReintentar, onVer, onNuevo }: Props) {
  const [busqueda, setBusqueda] = useState('')
  const [estado, setEstado] = useState<'TODOS' | EstadoPedido>('TODOS')
  const [pagina, setPagina] = useState(1)
  const esMovil = useMediaQuery('(max-width: 1099px)')

  const filtrados = useMemo(() => {
    const termino = busqueda.trim().toLowerCase()
    return pedidos.filter((p) => {
      if (estado !== 'TODOS' && p.estado !== estado) return false
      if (!termino) return true
      return [p.codigo, p.direccion, p.distrito, p.destinatarioAlias ?? ''].some((t) =>
        t.toLowerCase().includes(termino),
      )
    })
  }, [pedidos, busqueda, estado])

  const totalPaginas = Math.max(1, Math.ceil(filtrados.length / POR_PAGINA))
  const paginaActual = Math.min(pagina, totalPaginas)
  const visibles = filtrados.slice((paginaActual - 1) * POR_PAGINA, paginaActual * POR_PAGINA)
  const estadosPresentes = Array.from(new Set(pedidos.map((p) => p.estado)))
  const claseFila = (p: Pedido) => `aparecer${p.id === resaltadoId ? ' resaltado' : ''}`

  return (
    <section className="tarjeta aparecer" style={{ '--i': 5 } as CSSProperties} aria-labelledby="titulo-lista">
      <div className="lista-cabecera">
        <div>
          <h2 id="titulo-lista">Pedidos registrados</h2>
          <p className="lista-cabecera__detalle">Del más reciente al más antiguo</p>
        </div>
        <div className="herramientas">
          <div className="buscador">
            <Search size={18} aria-hidden="true" />
            <label htmlFor="busqueda" className="solo-lectores">
              Buscar pedidos por código, dirección o distrito
            </label>
            <input
              id="busqueda"
              type="search"
              placeholder="Buscar pedido…"
              value={busqueda}
              onChange={(e) => {
                setBusqueda(e.target.value)
                setPagina(1)
              }}
            />
          </div>
          <div className="filtro">
            <ListFilter size={18} aria-hidden="true" />
            <label htmlFor="filtro-estado" className="solo-lectores">
              Filtrar por estado
            </label>
            <select
              id="filtro-estado"
              value={estado}
              onChange={(e) => {
                setEstado(e.target.value as 'TODOS' | EstadoPedido)
                setPagina(1)
              }}
            >
              <option value="TODOS">Todos los estados</option>
              {estadosPresentes.map((e) => (
                <option key={e} value={e}>
                  {ETIQUETA_ESTADO[e]}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {error && (
        <div role="alert" className="aviso aviso--error">
          <TriangleAlert size={20} aria-hidden="true" />
          <div>
            <strong>{error}</strong>
          </div>
          <button type="button" className="boton boton--secundario boton--chico" onClick={onReintentar}>
            <RefreshCw size={16} aria-hidden="true" />
            Reintentar
          </button>
        </div>
      )}

      {cargando && pedidos.length === 0 && !error && (
        <div className="esqueleto" aria-busy="true" aria-label="Cargando pedidos">
          <span />
          <span />
          <span />
        </div>
      )}

      {!cargando && pedidos.length === 0 && !error && (
        <div className="vacio">
          <span className="vacio__icono">
            <Inbox size={34} aria-hidden="true" />
          </span>
          <p className="vacio__titulo">Aún no hay pedidos</p>
          <p>Registre el primero para empezar a armar la planificación del día.</p>
          {onNuevo && (
            <button type="button" className="boton boton--primario" onClick={onNuevo}>
              Nuevo pedido
            </button>
          )}
        </div>
      )}

      {pedidos.length > 0 && filtrados.length === 0 && (
        <div className="vacio">
          <span className="vacio__icono">
            <SearchX size={34} aria-hidden="true" />
          </span>
          <p className="vacio__titulo">Sin resultados</p>
          <p>Ningún pedido coincide con la búsqueda o el filtro.</p>
        </div>
      )}

      {visibles.length > 0 && esMovil && (
        <ul className="lista-movil">
          {visibles.map((p, i) => (
            <li key={p.id} className={claseFila(p)} style={{ '--i': i } as CSSProperties}>
              <button
                type="button"
                className="pedido-tarjeta"
                onClick={() => onVer(p)}
                aria-label={`Ver detalle del pedido ${p.codigo}`}
              >
                <span className="pedido-tarjeta__fila">
                  <strong>{p.codigo}</strong>
                  <span className="pedido-tarjeta__insignias">
                    <Insignias p={p} />
                  </span>
                </span>
                <span className="pedido-tarjeta__dato">
                  <MapPin size={16} aria-hidden="true" />
                  {p.direccion} · {p.distrito}
                </span>
                <span className="pedido-tarjeta__fila pedido-tarjeta__fila--suave">
                  <span className="pedido-tarjeta__dato">
                    <Clock size={16} aria-hidden="true" />
                    {ventanaCorta(p.ventanaInicio, p.ventanaFin)}
                  </span>
                  <span className="pedido-tarjeta__dato">
                    <Weight size={16} aria-hidden="true" />
                    {formatoNumero(p.demandaKg)} kg
                  </span>
                  <Flecha size={18} aria-hidden="true" className="pedido-tarjeta__flecha" />
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}

      {visibles.length > 0 && !esMovil && (
        <div className="tabla-contenedor" tabIndex={0} role="region" aria-label="Tabla de pedidos con desplazamiento">
          <table>
            <caption className="solo-lectores">Pedidos registrados, del más reciente al más antiguo</caption>
            <thead>
              <tr>
                <th scope="col">Código</th>
                <th scope="col">Destino</th>
                <th scope="col">Ventana (hora de Lima)</th>
                <th scope="col" className="num">
                  Carga
                </th>
                <th scope="col">Prioridad</th>
                <th scope="col">Estado</th>
                <th scope="col">
                  <span className="solo-lectores">Acciones</span>
                </th>
              </tr>
            </thead>
            <tbody>
              {visibles.map((p, i) => (
                <tr key={p.id} className={claseFila(p)} style={{ '--i': i } as CSSProperties}>
                  <th scope="row" className="codigo">
                    {p.codigo}
                  </th>
                  <td>
                    <span className="destino__direccion">{p.direccion}</span>
                    <span className="destino__distrito">{p.distrito}</span>
                  </td>
                  <td className="num">{ventanaCorta(p.ventanaInicio, p.ventanaFin)}</td>
                  <td className="num">
                    {formatoNumero(p.demandaKg)} kg
                    <span className="destino__distrito">{formatoNumero(p.demandaM3)} m³</span>
                  </td>
                  <td>
                    <span className={`prioridad prioridad--${p.prioridad}`}>{ETIQUETA_PRIORIDAD[p.prioridad]}</span>
                  </td>
                  <td>
                    <span className={`insignia insignia--${p.estado.toLowerCase()}`}>{ETIQUETA_ESTADO[p.estado]}</span>
                  </td>
                  <td>
                    <button
                      type="button"
                      className="icono-boton"
                      onClick={() => onVer(p)}
                      aria-label={`Ver detalle del pedido ${p.codigo}`}
                      title="Ver detalle"
                    >
                      <Eye size={18} aria-hidden="true" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {visibles.length > 0 && (
        <nav className="paginacion" aria-label="Paginación de pedidos">
          <p aria-live="polite">
            Mostrando {(paginaActual - 1) * POR_PAGINA + 1}–{(paginaActual - 1) * POR_PAGINA + visibles.length} de{' '}
            {filtrados.length}
          </p>
          <div>
            <button
              type="button"
              className="icono-boton icono-boton--borde"
              onClick={() => setPagina(paginaActual - 1)}
              disabled={paginaActual === 1}
              aria-label="Página anterior"
            >
              <ChevronLeft size={18} aria-hidden="true" />
            </button>
            <span className="paginacion__pagina">
              {paginaActual} / {totalPaginas}
            </span>
            <button
              type="button"
              className="icono-boton icono-boton--borde"
              onClick={() => setPagina(paginaActual + 1)}
              disabled={paginaActual === totalPaginas}
              aria-label="Página siguiente"
            >
              <ChevronRight size={18} aria-hidden="true" />
            </button>
          </div>
        </nav>
      )}
    </section>
  )
}
