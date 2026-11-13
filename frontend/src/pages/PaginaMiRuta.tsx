import { useCallback, useEffect, useMemo, useState, type FormEvent } from 'react'
import { CheckCircle2, CircleAlert, MapPinned, Navigation, TriangleAlert, XCircle } from 'lucide-react'
import {
  comoVistaPrevia,
  ETIQUETA_PARADA,
  obtenerMiRuta,
  registrarEstado,
  type EstadoParada,
  type MiRuta,
  type ParadaEjecucion,
} from '../api/conduccion'
import { ApiError } from '../api/http'
import Hero from '../components/Hero'
import MapaRutas from '../components/MapaRutas'
import { fechaCorta, fechaLocal, ventanaCorta } from '../lib/fechas'
import { formatoNumero } from '../lib/estados'

/** Acciones que quien conduce puede tomar según el estado actual de la parada (HU-010). */
const ACCIONES: Record<EstadoParada, { estado: EstadoParada; texto: string }[]> = {
  PENDIENTE: [
    { estado: 'EN_RUTA', texto: 'Salir hacia la parada' },
    { estado: 'CANCELADO', texto: 'Cancelar' },
  ],
  EN_RUTA: [
    { estado: 'ENTREGADO', texto: 'Marcar entregado' },
    { estado: 'INCIDENCIA', texto: 'Reportar incidencia' },
    { estado: 'CANCELADO', texto: 'Cancelar' },
  ],
  INCIDENCIA: [
    { estado: 'EN_RUTA', texto: 'Reintentar entrega' },
    { estado: 'CANCELADO', texto: 'Cancelar' },
  ],
  ENTREGADO: [],
  CANCELADO: [],
  REPROGRAMADO: [],
}

function TarjetaParada({
  parada,
  onCambiar,
  ocupada,
}: {
  parada: ParadaEjecucion
  onCambiar: (parada: ParadaEjecucion, estado: EstadoParada, nota?: string) => Promise<void>
  ocupada: boolean
}) {
  const [reportando, setReportando] = useState(false)
  const [nota, setNota] = useState('')
  const acciones = ACCIONES[parada.estado]
  const idNota = `nota-${parada.pedidoId}`

  const enviarIncidencia = async (e: FormEvent) => {
    e.preventDefault()
    await onCambiar(parada, 'INCIDENCIA', nota)
    setReportando(false)
    setNota('')
  }

  return (
    <li className={`parada-ejecucion parada-ejecucion--${parada.estado.toLowerCase()}`}>
      <div className="parada-ejecucion__cabecera">
        <span className="parada-ejecucion__orden" aria-hidden="true">
          {parada.orden}
        </span>
        <div>
          <p className="parada-ejecucion__titulo">
            <strong>{parada.codigo}</strong>{' '}
            <span className={`insignia insignia--${parada.estado.toLowerCase()}`}>{ETIQUETA_PARADA[parada.estado]}</span>
          </p>
          <p>
            {parada.direccion} · {parada.distrito}
          </p>
          <p className="parada-ejecucion__detalle">
            Ventana {ventanaCorta(parada.ventanaInicio, parada.ventanaFin)} · {formatoNumero(parada.demandaKg)} kg
            {parada.destinatarioAlias ? ` · ${parada.destinatarioAlias}` : ''}
          </p>
          {parada.nota && <p className="parada-ejecucion__nota">Nota: {parada.nota}</p>}
        </div>
      </div>

      {acciones.length > 0 && !reportando && (
        <div className="parada-ejecucion__acciones">
          {acciones.map((a) => (
            <button
              key={a.estado}
              type="button"
              className={`boton boton--chico ${a.estado === 'ENTREGADO' ? 'boton--primario' : 'boton--secundario'}`}
              disabled={ocupada}
              aria-label={`${a.texto}: pedido ${parada.codigo}`}
              onClick={() => (a.estado === 'INCIDENCIA' ? setReportando(true) : void onCambiar(parada, a.estado))}
            >
              {a.texto}
            </button>
          ))}
        </div>
      )}

      {reportando && (
        <form className="parada-ejecucion__incidencia" onSubmit={(e) => void enviarIncidencia(e)}>
          <label htmlFor={idNota}>Describa la incidencia del pedido {parada.codigo} *</label>
          <textarea id={idNota} value={nota} onChange={(e) => setNota(e.target.value)} rows={3} maxLength={500} required />
          <div className="parada-ejecucion__acciones">
            <button type="submit" className="boton boton--primario boton--chico" disabled={ocupada || nota.trim().length < 5}>
              Enviar incidencia
            </button>
            <button type="button" className="boton boton--secundario boton--chico" onClick={() => setReportando(false)}>
              Volver
            </button>
          </div>
        </form>
      )}
    </li>
  )
}

/** Vista de Conducción: la ruta asignada, sus paradas en orden y el registro de avance e incidencias. */
export default function PaginaMiRuta() {
  const [fecha, setFecha] = useState(() => fechaLocal(0))
  const [datos, setDatos] = useState<MiRuta | null>(null)
  const [cargando, setCargando] = useState(true)
  const [ocupada, setOcupada] = useState(false)
  const [error, setError] = useState('')
  const [aviso, setAviso] = useState('')

  const cargar = useCallback(
    () =>
      obtenerMiRuta(fecha)
        .then(setDatos)
        .catch((e: unknown) => setError(e instanceof ApiError ? e.message : 'No se pudo cargar su ruta.'))
        .finally(() => setCargando(false)),
    [fecha],
  )
  useEffect(() => {
    void cargar()
  }, [cargar])

  const cambiarFecha = (valor: string) => {
    if (!valor) return
    setCargando(true)
    setError('')
    setAviso('')
    setFecha(valor)
  }

  const cambiar = async (parada: ParadaEjecucion, estado: EstadoParada, nota?: string) => {
    setOcupada(true)
    setError('')
    try {
      await registrarEstado(parada.pedidoId, fecha, estado, nota)
      setAviso(`Pedido ${parada.codigo}: ${ETIQUETA_PARADA[estado].toLowerCase()}.`)
      await cargar()
    } catch (e: unknown) {
      setError(e instanceof ApiError ? e.message : 'No se pudo registrar el avance. Intente nuevamente.')
    } finally {
      setOcupada(false)
    }
  }

  const vista = useMemo(() => (datos && datos.rutas.length > 0 ? comoVistaPrevia(datos) : null), [datos])
  const [seleccion, setSeleccion] = useState<number | null>(null)
  const sinRuta = !cargando && (!datos || datos.rutas.length === 0)

  return (
    <>
      <Hero
        titulo="Mi ruta"
        subtitulo="Consulte sus paradas en orden, marque cada entrega y reporte incidencias."
        accion={
          <div className="rutas-filtro">
            <label>
              <span>Fecha de reparto</span>
              <input type="date" value={fecha} onChange={(e) => cambiarFecha(e.target.value)} />
            </label>
          </div>
        }
      />

      {aviso && (
        <p role="status" className="aviso aviso--info">
          <CheckCircle2 size={18} aria-hidden="true" /> {aviso}
        </p>
      )}
      {error && (
        <div role="alert" className="aviso aviso--error">
          <CircleAlert size={20} aria-hidden="true" />
          <div>
            <strong>{error}</strong>
          </div>
        </div>
      )}

      {sinRuta && (
        <section className="tarjeta vacio aparecer">
          <span className="vacio__icono">
            <MapPinned size={34} aria-hidden="true" />
          </span>
          <h2>No tiene una ruta asignada el {fechaCorta(fecha)}</h2>
          <p>Planificación debe guardar las rutas del día y asignarle un vehículo. Vuelva a consultar más tarde.</p>
        </section>
      )}

      {datos && vista && (
        <div className="rutas-layout aparecer">
          <section className="tarjeta rutas-mapa" aria-labelledby="titulo-mapa-ruta">
            <header className="rutas-mapa__cabecera">
              <h2 id="titulo-mapa-ruta">Mapa de mi ruta</h2>
              <p>
                <Navigation size={16} aria-hidden="true" /> Salida desde {datos.deposito.nombre}
              </p>
            </header>
            <MapaRutas vista={vista} seleccion={seleccion} onSeleccion={setSeleccion} />
          </section>

          <section className="rutas-panel" aria-label="Paradas de mi ruta">
            {datos.rutas.map((ruta) => (
              <article key={ruta.vehiculo.id} className="tarjeta">
                <h2>
                  Vehículo {ruta.vehiculo.placa}{' '}
                  <small>
                    {ruta.avance.entregadas} de {ruta.avance.total} entregadas
                    {ruta.avance.incidencias > 0 && (
                      <>
                        {' · '}
                        <TriangleAlert size={14} aria-hidden="true" /> {ruta.avance.incidencias} con incidencia
                      </>
                    )}
                  </small>
                </h2>
                <progress
                  value={ruta.avance.entregadas + ruta.avance.canceladas + ruta.avance.reprogramadas}
                  max={ruta.avance.total}
                  aria-label={`Avance de la ruta del vehículo ${ruta.vehiculo.placa}`}
                />
                <ol className="paradas-ejecucion">
                  {ruta.paradas.map((p) => (
                    <TarjetaParada key={p.pedidoId} parada={p} onCambiar={cambiar} ocupada={ocupada} />
                  ))}
                </ol>
              </article>
            ))}
            <p className="rutas-nota">
              <XCircle size={14} aria-hidden="true" /> Una incidencia queda visible para Planificación; usted puede reintentar la
              entrega o cancelarla.
            </p>
          </section>
        </div>
      )}
    </>
  )
}
