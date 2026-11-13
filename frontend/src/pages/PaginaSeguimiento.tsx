import { useCallback, useEffect, useRef, useState } from 'react'
import { CheckCircle2, CircleAlert, MapPinned, RefreshCw, Shuffle, TriangleAlert } from 'lucide-react'
import {
  asignarConductor,
  ETIQUETA_PARADA,
  obtenerSeguimiento,
  reoptimizarRutas,
  reprogramarParada,
  type Seguimiento,
} from '../api/conduccion'
import { ApiError } from '../api/http'
import Hero from '../components/Hero'
import { fechaCorta, fechaLocal, isoAHoraLima } from '../lib/fechas'

/** Vista de Planificación: asigna conductores, sigue el avance de las entregas y atiende las incidencias. */
export default function PaginaSeguimiento() {
  const [fecha, setFecha] = useState(() => fechaLocal(0))
  const [datos, setDatos] = useState<Seguimiento | null>(null)
  const [cargando, setCargando] = useState(true)
  const [ocupada, setOcupada] = useState(false)
  const [error, setError] = useState('')
  const [aviso, setAviso] = useState('')
  // Planificación suele guardar las rutas del día siguiente: si hoy no hay, se ofrece mañana (heurística 1 de Nielsen).
  const buscarCercana = useRef(true)
  const [confirmando, setConfirmando] = useState<string | null>(null)

  const cargar = useCallback(
    () =>
      obtenerSeguimiento(fecha)
        .then(async (d) => {
          if (!d && buscarCercana.current) {
            buscarCercana.current = false
            const manana = fechaLocal(1)
            const siguiente = await obtenerSeguimiento(manana)
            if (siguiente) {
              setFecha(manana)
              setAviso(`No hay rutas para hoy; se muestra el ${fechaCorta(manana)}, que tiene rutas guardadas.`)
              setDatos(siguiente)
              return
            }
          }
          setDatos(d)
        })
        .catch((e: unknown) => setError(e instanceof ApiError ? e.message : 'No se pudo cargar el seguimiento.'))
        .finally(() => setCargando(false)),
    [fecha],
  )
  useEffect(() => {
    void cargar()
  }, [cargar])

  const ejecutar = async (accion: () => Promise<string>) => {
    setOcupada(true)
    setError('')
    try {
      setAviso(await accion())
      await cargar()
    } catch (e: unknown) {
      setError(e instanceof ApiError ? e.message : 'No se pudo completar la acción. Intente nuevamente.')
    } finally {
      setOcupada(false)
    }
  }

  const cambiarFecha = (valor: string) => {
    if (!valor) return
    buscarCercana.current = false
    setCargando(true)
    setError('')
    setAviso('')
    setFecha(valor)
  }

  const sinRutas = !cargando && !datos

  return (
    <>
      <Hero
        titulo="Seguimiento"
        subtitulo="Asigne conductores a las rutas guardadas, revise el avance de las entregas y atienda las incidencias."
        accion={
          <div className="rutas-filtro">
            <label>
              <span>Fecha de reparto</span>
              <input type="date" value={fecha} onChange={(e) => cambiarFecha(e.target.value)} />
            </label>
            <button
              type="button"
              className="boton boton--claro"
              disabled={ocupada || !datos}
              onClick={() =>
                void ejecutar(async () => {
                  const { rutasReordenadas } = await reoptimizarRutas(fecha)
                  return rutasReordenadas === 0
                    ? 'El orden de las paradas pendientes ya es el más corto; no hubo cambios.'
                    : `Se reordenaron las paradas pendientes de ${rutasReordenadas} ruta(s). Lo ya entregado no cambió.`
                })
              }
            >
              <Shuffle size={18} aria-hidden="true" />
              Reoptimizar pendientes
            </button>
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

      {sinRutas && (
        <section className="tarjeta vacio aparecer">
          <span className="vacio__icono">
            <MapPinned size={34} aria-hidden="true" />
          </span>
          <h2>No hay rutas guardadas el {fechaCorta(fecha)}</h2>
          <p>Guarde las rutas del día en la vista Rutas para poder asignarlas a un conductor.</p>
        </section>
      )}

      {datos && (
        <>
          <section className="tarjeta aparecer" aria-labelledby="titulo-incidencias">
            <h2 id="titulo-incidencias">
              <TriangleAlert size={18} aria-hidden="true" /> Incidencias abiertas ({datos.incidencias.length})
            </h2>
            {datos.incidencias.length === 0 ? (
              <p>No hay incidencias abiertas.</p>
            ) : (
              <ul className="incidencias">
                {datos.incidencias.map((i) => (
                  <li key={i.pedidoId}>
                    <p>
                      <strong>{i.codigo}</strong> · {i.direccion}, {i.distrito}
                    </p>
                    <p>
                      Vehículo {i.vehiculo}
                      {i.conductorNombre ? ` · ${i.conductorNombre}` : ''}
                      {i.actualizadoEn ? ` · ${isoAHoraLima(i.actualizadoEn)}` : ''}
                    </p>
                    <p className="parada-ejecucion__nota">{i.nota}</p>
                    {confirmando === i.pedidoId ? (
                      <div className="parada-ejecucion__acciones">
                        <span>¿Devolver el pedido a Pendiente? Esta incidencia quedará cerrada.</span>
                        <button
                          type="button"
                          className="boton boton--primario boton--chico"
                          disabled={ocupada}
                          aria-label={`Confirmar reprogramación del pedido ${i.codigo}`}
                          onClick={() =>
                            void ejecutar(async () => {
                              await reprogramarParada(i.pedidoId, fecha)
                              setConfirmando(null)
                              return `Pedido ${i.codigo} reprogramado: volvió a Pendiente para planificarlo de nuevo.`
                            })
                          }
                        >
                          Confirmar
                        </button>
                        <button type="button" className="boton boton--secundario boton--chico" onClick={() => setConfirmando(null)}>
                          Cancelar
                        </button>
                      </div>
                    ) : (
                      <button
                        type="button"
                        className="boton boton--secundario boton--chico"
                        disabled={ocupada}
                        aria-label={`Reprogramar pedido ${i.codigo}`}
                        onClick={() => setConfirmando(i.pedidoId)}
                      >
                        <RefreshCw size={14} aria-hidden="true" /> Reprogramar
                      </button>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section className="rutas-panel" aria-label="Rutas del día">
            {datos.rutas.map((ruta) => {
              const idSelect = `conductor-${ruta.vehiculo.id}`
              return (
                <article key={ruta.vehiculo.id} className="tarjeta aparecer">
                  <h2>
                    Vehículo {ruta.vehiculo.placa}{' '}
                    <small>
                      {ruta.avance.entregadas} de {ruta.avance.total} entregadas
                      {ruta.avance.incidencias > 0 ? ` · ${ruta.avance.incidencias} con incidencia` : ''}
                    </small>
                  </h2>
                  <progress
                    value={ruta.avance.entregadas + ruta.avance.canceladas + ruta.avance.reprogramadas}
                    max={ruta.avance.total}
                    aria-label={`Avance del vehículo ${ruta.vehiculo.placa}`}
                  />
                  <div className="campo">
                    <label htmlFor={idSelect}>Conductor asignado al vehículo {ruta.vehiculo.placa}</label>
                    <select
                      id={idSelect}
                      value={ruta.conductorId ?? ''}
                      disabled={ocupada}
                      onChange={(e) =>
                        e.target.value &&
                        void ejecutar(async () => {
                          await asignarConductor(fecha, ruta.vehiculo.id, e.target.value)
                          return `Conductor asignado al vehículo ${ruta.vehiculo.placa}.`
                        })
                      }
                    >
                      <option value="">Sin asignar</option>
                      {datos.conductoresDisponibles.map((c) => (
                        <option key={c.id} value={c.id}>
                          {c.nombre}
                        </option>
                      ))}
                    </select>
                  </div>
                  <ol className="paradas-seguimiento">
                    {ruta.paradas.map((p) => (
                      <li key={p.pedidoId}>
                        <span className={`insignia insignia--${p.estado.toLowerCase()}`}>{ETIQUETA_PARADA[p.estado]}</span>{' '}
                        {p.orden}. {p.codigo} · {p.direccion}
                      </li>
                    ))}
                  </ol>
                </article>
              )
            })}
          </section>
        </>
      )}
    </>
  )
}
