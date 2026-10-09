import { useCallback, useEffect, useState, type CSSProperties } from 'react'
import { CircleAlert, Info, Leaf, MapPinned, PackageCheck, RefreshCw, Route, Truck } from 'lucide-react'
import { ApiError } from '../api/http'
import { obtenerVistaPrevia, type Ruta, type VistaPrevia } from '../api/rutas'
import Hero from '../components/Hero'
import MapaRutas from '../components/MapaRutas'
import { COLORES_RUTA } from '../lib/colores'
import StatCard from '../components/StatCard'
import { formatoNumero } from '../lib/estados'
import { fechaCorta, fechaLocal } from '../lib/fechas'

const hora = new Intl.DateTimeFormat('es-PE', { timeZone: 'America/Lima', hour: '2-digit', minute: '2-digit', hour12: false })

function duracion(min: number): string {
  const h = Math.floor(min / 60)
  return h ? `${h} h ${String(min % 60).padStart(2, '0')} min` : `${min} min`
}

export default function PaginaRutas() {
  const [fecha, setFecha] = useState(() => fechaLocal(1))
  const [vista, setVista] = useState<VistaPrevia | null>(null)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')
  const [seleccion, setSeleccion] = useState<number | null>(null)

  const consultar = useCallback(
    () =>
      obtenerVistaPrevia(fecha)
        .then(setVista)
        .catch((e: unknown) => setError(e instanceof ApiError ? e.message : 'No se pudo calcular la vista previa de rutas.'))
        .finally(() => setCargando(false)),
    [fecha],
  )
  const cargar = useCallback(() => {
    setCargando(true)
    setError('')
    setSeleccion(null)
    return consultar()
  }, [consultar])
  useEffect(() => {
    void consultar()
  }, [consultar])
  const cambiarFecha = (valor: string) => {
    if (!valor) return
    setCargando(true)
    setSeleccion(null)
    setFecha(valor)
  }

  const r = vista?.resumen
  const sinDatos = vista && vista.rutas.length === 0 && vista.sinAsignar.length === 0

  return (
    <>
      <Hero
        titulo="Rutas"
        subtitulo="Vista previa de las rutas del día con los pedidos registrados y los vehículos con turno."
        accion={
          <div className="rutas-filtro">
            <label>
              <span>Fecha de reparto</span>
              <input type="date" value={fecha} onChange={(e) => cambiarFecha(e.target.value)} />
            </label>
            <button type="button" className="boton boton--claro" onClick={() => void cargar()} disabled={cargando}>
              <RefreshCw size={18} aria-hidden="true" className={cargando ? 'girando' : undefined} />
              Recalcular
            </button>
          </div>
        }
      />

      <section className="stats" aria-label="Resumen de la propuesta">
        <StatCard titulo="Pedidos en ruta" valor={r?.asignados ?? 0} sufijo={r ? `/ ${r.pedidos}` : undefined} detalle={r && r.pedidos > r.asignados ? `${r.pedidos - r.asignados} sin asignar` : 'Todos asignados'} icono={PackageCheck} indice={0} />
        <StatCard titulo="Vehículos" valor={r?.vehiculosUsados ?? 0} sufijo={r ? `/ ${r.vehiculosDisponibles}` : undefined} detalle="Usados / con turno" icono={Truck} indice={1} />
        <StatCard titulo="Distancia" valor={r?.distanciaKm ?? 0} sufijo="km" detalle={r ? `Sin optimizar: ${formatoNumero(r.distanciaBaseKm)} km` : 'Recorrido total'} icono={Route} indice={2} />
        <StatCard titulo="Emisiones" valor={r?.co2Kg ?? 0} sufijo="kg CO₂e" detalle={r && r.ahorroCo2Pct > 0 ? `${formatoNumero(r.ahorroCo2Pct)} % menos que sin optimizar` : 'Estimadas por combustible'} icono={Leaf} indice={3} />
      </section>

      {error && (
        <div role="alert" className="aviso aviso--error rutas-aviso">
          <CircleAlert size={20} aria-hidden="true" />
          <div>
            <strong>{error}</strong>
          </div>
          <button type="button" className="boton boton--secundario" onClick={() => void cargar()}>
            Reintentar
          </button>
        </div>
      )}

      {sinDatos && !cargando && (
        <section className="tarjeta vacio aparecer">
          <span className="vacio__icono">
            <MapPinned size={34} aria-hidden="true" />
          </span>
          <h2>No hay pedidos para el {fechaCorta(fecha)}</h2>
          <p>Registre pedidos con ventana horaria en esa fecha y declare el turno de los vehículos en Flota.</p>
        </section>
      )}

      {vista && !sinDatos && (
        <div className="rutas-layout aparecer">
          <section className="tarjeta rutas-mapa" aria-labelledby="titulo-mapa">
            <header className="rutas-mapa__cabecera">
              <h2 id="titulo-mapa">Mapa de rutas</h2>
              <p>
                {r && r.paradasFueraDeVentana === 0
                  ? `Todas las paradas llegan dentro de su ventana${r.paradasFueraDeVentanaBase ? ` (sin optimizar: ${r.paradasFueraDeVentanaBase} tarde)` : ''}.`
                  : `${r?.paradasFueraDeVentana} parada(s) llegarían fuera de su ventana.`}
              </p>
            </header>
            <MapaRutas vista={vista} seleccion={seleccion} onSeleccion={setSeleccion} />
            <ul className="rutas-leyenda" aria-label="Leyenda">
              <li><span className="marcador-deposito marcador-deposito--chico" aria-hidden="true" /> Depósito</li>
              <li><span className="marcador-parada marcador-parada--chico" style={{ '--color': COLORES_RUTA[0] } as CSSProperties} aria-hidden="true">1</span> Orden de visita</li>
              <li><span className="marcador-parada marcador-parada--chico marcador-parada--tarde" style={{ '--color': COLORES_RUTA[0] } as CSSProperties} aria-hidden="true">!</span> Fuera de ventana</li>
            </ul>
          </section>

          <section className="rutas-panel" aria-label="Rutas por vehículo">
            {vista.rutas.map((ruta, i) => (
              <TarjetaRuta key={ruta.vehiculo.id} ruta={ruta} color={COLORES_RUTA[i % COLORES_RUTA.length]} indice={i} activa={seleccion === i} onClick={() => setSeleccion(seleccion === i ? null : i)} />
            ))}

            {vista.sinAsignar.length > 0 && (
              <article className="tarjeta rutas-sin-asignar">
                <h3>
                  <CircleAlert size={18} aria-hidden="true" /> Sin asignar ({vista.sinAsignar.length})
                </h3>
                <ul>
                  {vista.sinAsignar.map((s) => (
                    <li key={s.pedidoId}>
                      <strong>{s.codigo}</strong> · {formatoNumero(s.demandaKg)} kg — {s.motivo}
                    </li>
                  ))}
                </ul>
              </article>
            )}

            <details className="tarjeta rutas-supuestos">
              <summary>
                <Info size={18} aria-hidden="true" /> ¿Cómo se calcula?
              </summary>
              <p>
                Es una vista previa: agrupa los pedidos en los vehículos según su capacidad y busca el orden que cumple
                las ventanas horarias con menos emisiones. El motor de optimización completo llegará en una próxima
                iteración.
              </p>
              <ul>
                {vista.supuestos.map((s) => (
                  <li key={s}>{s}</li>
                ))}
              </ul>
            </details>
          </section>
        </div>
      )}
    </>
  )
}

function TarjetaRuta({ ruta, color, indice, activa, onClick }: { ruta: Ruta; color: string; indice: number; activa: boolean; onClick: () => void }) {
  return (
    <article className={`tarjeta ruta aparecer${activa ? ' ruta--activa' : ''}`} style={{ '--color': color, '--i': indice } as CSSProperties}>
      <button type="button" className="ruta__cabecera" onClick={onClick} aria-pressed={activa}>
        <span className="ruta__punto" aria-hidden="true" />
        <strong>{ruta.vehiculo.placa}</strong>
        <span className="ruta__tipo">{ruta.vehiculo.tipo}</span>
        <span className="ruta__ver">{activa ? 'En el mapa' : 'Ver en mapa'}</span>
      </button>
      <p className="ruta__resumen">
        {formatoNumero(ruta.distanciaKm)} km · {duracion(ruta.duracionMin)} · {formatoNumero(ruta.co2Kg)} kg CO₂e
      </p>
      <div className="ruta__capacidad">
        <div className="ruta__carga" aria-hidden="true">
          <span style={{ width: `${Math.min(ruta.usoCapacidadPct, 100)}%` }} />
        </div>
        <span>
          {formatoNumero(ruta.cargaKg)} / {formatoNumero(ruta.vehiculo.capacidadKg)} kg
        </span>
      </div>
      <ol className="ruta__paradas">
        {ruta.paradas.map((p) => (
          <li key={p.pedidoId} className={p.dentroDeVentana ? undefined : 'ruta__parada--tarde'}>
            <span className="ruta__hora" title={`Ventana ${hora.format(new Date(p.ventanaInicio))}–${hora.format(new Date(p.ventanaFin))}`}>
              {hora.format(new Date(p.llegadaEstimada))}
            </span>
            <span className="ruta__parada">
              <span>
                <strong>{p.codigo}</strong>
                {p.destinatarioAlias && ` ${p.destinatarioAlias}`}
              </span>
              <small>
                {p.distrito}
                {!p.dentroDeVentana && ' · fuera de ventana'}
              </small>
            </span>
            <span className="ruta__kg">{formatoNumero(p.demandaKg)} kg</span>
          </li>
        ))}
      </ol>
    </article>
  )
}
