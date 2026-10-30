import { useCallback, useEffect, useState } from 'react'
import { CircleAlert, Clock, Gauge, Leaf, PackageCheck, RefreshCw } from 'lucide-react'
import { ApiError } from '../api/http'
import { obtenerIndicadores, type Indicadores } from '../api/indicadores'
import Hero from '../components/Hero'
import StatCard from '../components/StatCard'
import { ETIQUETA_COMBUSTIBLE, ETIQUETA_ESTADO, ETIQUETA_PRIORIDAD, formatoNumero } from '../lib/estados'
import { fechaCorta, fechaLocal } from '../lib/fechas'

interface Barra {
  etiqueta: string
  valor: number
  detalle?: string
}

/** Barras horizontales accesibles: cada fila se lee como texto y la barra es decorativa. */
function Barras({ filas, unidad = '' }: { filas: Barra[]; unidad?: string }) {
  const maximo = Math.max(...filas.map((f) => f.valor), 0)
  if (maximo === 0) return <p className="indicador__vacio">Sin datos para mostrar.</p>
  return (
    <ul className="barras">
      {filas.map((f) => (
        <li key={f.etiqueta}>
          <span className="barras__etiqueta">{f.etiqueta}</span>
          <span className="barras__pista" aria-hidden="true">
            <span style={{ width: `${(f.valor / maximo) * 100}%` }} />
          </span>
          <span className="barras__valor">
            {formatoNumero(f.valor)}
            {unidad}
            {f.detalle && <small> · {f.detalle}</small>}
          </span>
        </li>
      ))}
    </ul>
  )
}

export default function PaginaIndicadores() {
  const [fecha, setFecha] = useState(() => fechaLocal(1))
  const [datos, setDatos] = useState<Indicadores | null>(null)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')

  const consultar = useCallback(
    () =>
      obtenerIndicadores(fecha)
        .then(setDatos)
        .catch((e: unknown) => setError(e instanceof ApiError ? e.message : 'No se pudieron calcular los indicadores.'))
        .finally(() => setCargando(false)),
    [fecha],
  )
  const cargar = () => {
    setCargando(true)
    setError('')
    void consultar()
  }
  useEffect(() => {
    void consultar()
  }, [consultar])
  const cambiarFecha = (valor: string) => {
    if (!valor) return
    setCargando(true)
    setError('')
    setFecha(valor)
  }

  const dia = datos?.dia
  const ahorroKm = dia ? dia.distanciaBaseKm - dia.distanciaKm : 0

  return (
    <>
      <Hero
        titulo="Indicadores"
        subtitulo="Operación y sostenibilidad de la planificación: emisiones, puntualidad y uso de la flota."
        accion={
          <div className="rutas-filtro">
            <label>
              <span>Fecha de reparto</span>
              <input type="date" value={fecha} onChange={(e) => cambiarFecha(e.target.value)} />
            </label>
            <button type="button" className="boton boton--claro" onClick={cargar} disabled={cargando}>
              <RefreshCw size={18} aria-hidden="true" className={cargando ? 'girando' : undefined} />
              Actualizar
            </button>
          </div>
        }
      />

      <section className="stats" aria-label={`Indicadores del ${fechaCorta(fecha)}`}>
        <StatCard titulo="Ahorro de CO₂e" valor={dia?.ahorroCo2Pct ?? 0} sufijo="%" detalle={dia ? `${formatoNumero(dia.co2Kg)} de ${formatoNumero(dia.co2BaseKg)} kg sin optimizar` : 'Frente al despacho sin optimizar'} icono={Leaf} indice={0} />
        <StatCard titulo="Puntualidad" valor={dia?.paradasATiempoPct ?? 0} sufijo="%" detalle="Paradas dentro de su ventana" icono={Clock} indice={1} />
        <StatCard titulo="Uso de capacidad" valor={dia?.usoCapacidadPct ?? 0} sufijo="%" detalle={datos ? `${formatoNumero(dia?.demandaKg ?? 0)} de ${formatoNumero(datos.flota.capacidadAptaKg)} kg` : 'Carga sobre capacidad apta'} icono={Gauge} indice={2} />
        <StatCard titulo="Pedidos del día" valor={dia?.asignados ?? 0} sufijo={dia ? `/ ${dia.pedidos}` : undefined} detalle="Asignados a una ruta" icono={PackageCheck} indice={3} />
      </section>

      {error && (
        <div role="alert" className="aviso aviso--error rutas-aviso">
          <CircleAlert size={20} aria-hidden="true" />
          <div>
            <strong>{error}</strong>
          </div>
          <button type="button" className="boton boton--secundario" onClick={cargar}>
            Reintentar
          </button>
        </div>
      )}

      {datos && dia && (
        <div className="indicadores aparecer">
          <article className="tarjeta indicador indicador--ancho">
            <h2>Emisiones del {fechaCorta(datos.fecha)}</h2>
            <p className="indicador__nota">
              {dia.pedidos === 0
                ? 'No hay pedidos planificables en esta fecha.'
                : `La propuesta de rutas recorre ${formatoNumero(dia.distanciaKm)} km${ahorroKm > 0 ? `, ${formatoNumero(Math.round(ahorroKm * 100) / 100)} km menos que sin optimizar` : ''}, y prioriza los vehículos que menos emiten.`}
            </p>
            <Barras
              unidad=" kg CO₂e"
              filas={[
                { etiqueta: 'Sin optimizar', valor: dia.co2BaseKg },
                { etiqueta: 'Propuesta', valor: dia.co2Kg },
              ]}
            />
          </article>

          <article className="tarjeta indicador">
            <h2>Pedidos por estado</h2>
            <p className="indicador__nota">{datos.pedidos.total} registrados · {formatoNumero(datos.pedidos.pesoKg)} kg en total</p>
            <Barras filas={datos.pedidos.porEstado.filter((e) => e.cantidad > 0).map((e) => ({ etiqueta: ETIQUETA_ESTADO[e.estado], valor: e.cantidad }))} />
          </article>

          <article className="tarjeta indicador">
            <h2>Pedidos por distrito</h2>
            <p className="indicador__nota">Dónde se concentra la demanda</p>
            <Barras filas={datos.pedidos.porDistrito.map((d) => ({ etiqueta: d.distrito, valor: d.cantidad, detalle: `${formatoNumero(d.pesoKg)} kg` }))} />
          </article>

          <article className="tarjeta indicador">
            <h2>Pedidos por prioridad</h2>
            <p className="indicador__nota">Los urgentes se asignan primero</p>
            <Barras filas={datos.pedidos.porPrioridad.map((p) => ({ etiqueta: ETIQUETA_PRIORIDAD[p.prioridad], valor: p.cantidad }))} />
          </article>

          <article className="tarjeta indicador">
            <h2>Flota por combustible</h2>
            <p className="indicador__nota">{datos.flota.aptos} de {datos.flota.total} vehículos con turno el {fechaCorta(datos.fecha)}</p>
            <Barras filas={datos.flota.porCombustible.map((c) => ({ etiqueta: ETIQUETA_COMBUSTIBLE[c.combustible], valor: c.cantidad }))} />
          </article>
        </div>
      )}
    </>
  )
}
