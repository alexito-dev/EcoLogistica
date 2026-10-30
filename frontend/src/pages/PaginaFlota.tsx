import { useCallback, useEffect, useState } from 'react'
import { CalendarCheck, Fuel, Leaf, Plus, RefreshCw, Truck, Weight } from 'lucide-react'
import { ApiError } from '../api/http'
import {
  actualizarVehiculo,
  crearVehiculo,
  guardarDisponibilidad,
  listarVehiculos,
  type Combustible,
  type EstadoVehiculo,
  type Vehiculo,
  type VehiculoGuardar,
} from '../api/flota'
import Drawer from '../components/Drawer'
import Hero from '../components/Hero'
import StatCard from '../components/StatCard'
import { ETIQUETA_COMBUSTIBLE } from '../lib/estados'

interface Props {
  puedeAdministrar: boolean
  puedePlanificar: boolean
}

const HOY = () => {
  const ahora = new Date()
  return `${ahora.getFullYear()}-${String(ahora.getMonth() + 1).padStart(2, '0')}-${String(ahora.getDate()).padStart(2, '0')}`
}

export default function PaginaFlota({ puedeAdministrar, puedePlanificar }: Props) {
  const [fecha, setFecha] = useState(HOY)
  const [vehiculos, setVehiculos] = useState<Vehiculo[]>([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')
  const [aviso, setAviso] = useState('')
  const [vehiculoForm, setVehiculoForm] = useState<Vehiculo | null | undefined>(undefined)
  const [disponibilidad, setDisponibilidad] = useState<Vehiculo | null>(null)

  const consultar = useCallback(
    () =>
      listarVehiculos(fecha)
        .then((respuesta) => setVehiculos(respuesta.items))
        .catch((e: unknown) => setError(e instanceof ApiError ? e.message : 'No se pudo cargar la flota.'))
        .finally(() => setCargando(false)),
    [fecha],
  )
  const cargar = useCallback(() => {
    setCargando(true)
    setError('')
    return consultar()
  }, [consultar])
  useEffect(() => { void consultar() }, [consultar])
  const cambiarFecha = (valor: string) => {
    if (!valor) return
    setCargando(true)
    setFecha(valor)
  }

  const guardarVehiculo = async (datos: VehiculoGuardar) => {
    try {
      if (vehiculoForm) await actualizarVehiculo(vehiculoForm.id, datos)
      else await crearVehiculo(datos)
      setVehiculoForm(undefined)
      setError('')
      setAviso(vehiculoForm ? 'Vehículo actualizado.' : 'Vehículo registrado.')
      await cargar()
    } catch (e) {
      setError(e instanceof ApiError ? e.message : 'No se pudo guardar el vehículo.')
      if (e instanceof ApiError && Object.keys(e.errors).length) setError(Object.values(e.errors).join(' · '))
    }
  }

  const guardarTurno = async (datos: { fecha: string; turnoInicio: string; turnoFin: string; disponible: boolean; restriccionCirculacion: string | null }) => {
    if (!disponibilidad) return
    try {
      await guardarDisponibilidad(disponibilidad.id, datos)
      setDisponibilidad(null)
      setError('')
      setAviso('Disponibilidad guardada.')
      await cargar()
    } catch (e) {
      setError(e instanceof ApiError ? (Object.values(e.errors).join(' · ') || e.message) : 'No se pudo guardar la disponibilidad.')
    }
  }

  const aptos = vehiculos.filter((v) => v.elegibleParaPlanificar)
  const capacidadApta = aptos.reduce((suma, v) => suma + Number(v.capacidadKg), 0)
  const bajasEmisiones = vehiculos.filter((v) => v.combustible === 'ELECTRICO' || v.combustible === 'HIBRIDO' || v.combustible === 'GNV').length
  return <>
    <Hero
      titulo="Flota"
      subtitulo={puedeAdministrar ? 'Administre los vehículos y consulte su disponibilidad para planificar.' : 'Consulte la flota y declare qué unidades estarán disponibles para planificar.'}
      accion={
        <div className="rutas-filtro">
          <label>
            <span>Fecha de turno</span>
            <input type="date" value={fecha} onChange={(e) => cambiarFecha(e.target.value)} />
          </label>
          {puedeAdministrar && (
            <button type="button" className="boton boton--claro" onClick={() => setVehiculoForm(null)}>
              <Plus size={18} aria-hidden="true" /> Nuevo vehículo
            </button>
          )}
        </div>
      }
    />

    <section className="stats" aria-label="Resumen de flota">
      <StatCard titulo="Vehículos" valor={vehiculos.length} detalle="Registrados en total" icono={Truck} indice={0} />
      <StatCard titulo="Aptos" valor={aptos.length} detalle={`Con turno el ${fecha.split('-').reverse().join('/')}`} icono={CalendarCheck} indice={1} />
      <StatCard titulo="Capacidad apta" valor={capacidadApta} sufijo="kg" detalle="Suma de los vehículos aptos" icono={Weight} indice={2} />
      <StatCard titulo="Bajas emisiones" valor={bajasEmisiones} detalle="Eléctricos, híbridos o GNV" icono={Leaf} indice={3} />
    </section>
    {error && <div className="flota-mensaje flota-mensaje--error" role="alert">{error} <button onClick={() => void cargar()}>Reintentar</button></div>}
    {aviso && <div className="flota-mensaje" role="status">{aviso}<button aria-label="Cerrar aviso" onClick={() => setAviso('')}>×</button></div>}

    <section className="flota-listado" aria-labelledby="flota-listado-titulo">
      <header><div><h2 id="flota-listado-titulo">Vehículos</h2><p>Capacidad, estado y turno configurado para la fecha seleccionada.</p></div><button className="boton boton--secundario" onClick={() => void cargar()} aria-label="Actualizar lista"><RefreshCw size={17} /></button></header>
      {cargando ? <p className="flota-vacio" role="status">Cargando vehículos…</p> : vehiculos.length === 0 ? <div className="flota-vacio"><Truck size={32} /><h3>Aún no hay vehículos</h3><p>{puedeAdministrar ? 'Registre el primero para completar la flota.' : 'Solicite a Administración que registre vehículos para poder configurar sus turnos.'}</p></div> : <div className="flota-tarjetas">{vehiculos.map((v) => <article className="flota-vehiculo" key={v.id}>
        <div className="flota-vehiculo__cabecera"><span className="flota-vehiculo__icono"><Truck size={22} /></span><span className={`estado-vehiculo estado-vehiculo--${v.estado.toLowerCase()}`}>{v.elegibleParaPlanificar ? 'Apto para planificar' : v.estado === 'DISPONIBLE' ? 'Sin turno declarado' : v.estado === 'MANTENIMIENTO' ? 'Mantenimiento' : 'Inactivo'}</span></div>
        <h3>{v.placa}</h3><p className="flota-vehiculo__tipo">{v.tipo}{v.anio ? ` · ${v.anio}` : ''}</p>
        <dl><div><dt>Capacidad</dt><dd>{v.capacidadKg} kg · {v.capacidadM3} m³</dd></div><div><dt>Combustible</dt><dd><Fuel size={14} /> {ETIQUETA_COMBUSTIBLE[v.combustible]}</dd></div><div><dt>Turno</dt><dd>{v.disponibilidad ? `${v.disponibilidad.turnoInicio.slice(0, 5)}–${v.disponibilidad.turnoFin.slice(0, 5)}` : 'Sin declarar'}</dd></div></dl>
        {v.disponibilidad?.restriccionCirculacion && <p className="flota-restriccion">Restricción: {v.disponibilidad.restriccionCirculacion}</p>}
        <div className="flota-acciones">{puedeAdministrar && <button className="boton boton--secundario" onClick={() => setVehiculoForm(v)}>Editar vehículo</button>}{puedePlanificar && <button className="boton boton--primario" onClick={() => setDisponibilidad(v)}>Configurar turno</button>}</div>
      </article>)}</div>}
    </section>

    <Drawer abierto={vehiculoForm !== undefined} titulo={vehiculoForm ? 'Editar vehículo' : 'Registrar vehículo'} descripcion="Ingrese los datos de capacidad y operación de la unidad." onCerrar={() => setVehiculoForm(undefined)}>
      <FormularioVehiculo inicial={vehiculoForm ?? null} onGuardar={(d) => void guardarVehiculo(d)} onCancelar={() => setVehiculoForm(undefined)} />
    </Drawer>
    <Drawer abierto={disponibilidad !== null} titulo={`Turno · ${disponibilidad?.placa ?? ''}`} descripcion="La disponibilidad se guarda por fecha y no aplica automáticamente restricciones legales de circulación." onCerrar={() => setDisponibilidad(null)}>
      {disponibilidad && <FormularioDisponibilidad fechaInicial={fecha} inicial={disponibilidad} onGuardar={(d) => void guardarTurno(d)} onCancelar={() => setDisponibilidad(null)} />}
    </Drawer>
  </>
}

function FormularioVehiculo({ inicial, onGuardar, onCancelar }: { inicial: Vehiculo | null; onGuardar: (d: VehiculoGuardar) => void; onCancelar: () => void }) {
  const [datos, setDatos] = useState<VehiculoGuardar>(() => inicial ? {
    placa: inicial.placa, tipo: inicial.tipo, capacidadKg: inicial.capacidadKg, capacidadM3: inicial.capacidadM3,
    combustible: inicial.combustible, consumoBasePor100km: inicial.consumoBasePor100km,
    factorEmisionKgco2eUnidad: inicial.factorEmisionKgco2eUnidad, anio: inicial.anio, estado: inicial.estado,
  } : { placa: '', tipo: '', capacidadKg: 0, capacidadM3: 0, combustible: 'DIESEL', consumoBasePor100km: 0, factorEmisionKgco2eUnidad: null, anio: null, estado: 'DISPONIBLE' })
  const editar = (campo: keyof VehiculoGuardar, valor: string | number | null) => setDatos((anterior) => ({ ...anterior, [campo]: valor }))
  return <form className="formulario flota-formulario" onSubmit={(e) => { e.preventDefault(); onGuardar(datos) }}>
    <label>Placa *<input required minLength={5} maxLength={10} value={datos.placa} onChange={(e) => editar('placa', e.target.value.toUpperCase())} /></label>
    <label>Tipo de vehículo *<input required maxLength={40} value={datos.tipo} onChange={(e) => editar('tipo', e.target.value)} placeholder="Furgón, camión…" /></label>
    <div className="flota-campos-dobles"><label>Capacidad (kg) *<input required type="number" min="0.01" step="0.01" value={datos.capacidadKg || ''} onChange={(e) => editar('capacidadKg', Number(e.target.value))} /></label><label>Capacidad (m³) *<input required type="number" min="0.001" step="0.001" value={datos.capacidadM3 || ''} onChange={(e) => editar('capacidadM3', Number(e.target.value))} /></label></div>
    <label>Combustible *<select value={datos.combustible} onChange={(e) => editar('combustible', e.target.value as Combustible)}>{Object.entries(ETIQUETA_COMBUSTIBLE).map(([valor, texto]) => <option key={valor} value={valor}>{texto}</option>)}</select></label>
    <div className="flota-campos-dobles"><label>Consumo por 100 km *<input required type="number" min="0.0001" step="0.0001" value={datos.consumoBasePor100km || ''} onChange={(e) => editar('consumoBasePor100km', Number(e.target.value))} /></label><label>Año<input type="number" min="1990" max="2100" value={datos.anio ?? ''} onChange={(e) => editar('anio', e.target.value ? Number(e.target.value) : null)} /></label></div>
    <label>Factor de emisión (opcional)<input type="number" min="0.000001" step="0.000001" value={datos.factorEmisionKgco2eUnidad ?? ''} onChange={(e) => editar('factorEmisionKgco2eUnidad', e.target.value ? Number(e.target.value) : null)} /></label>
    <label>Estado<select value={datos.estado} onChange={(e) => editar('estado', e.target.value as EstadoVehiculo)}><option value="DISPONIBLE">Disponible</option><option value="MANTENIMIENTO">Mantenimiento</option><option value="INACTIVO">Inactivo</option></select></label>
    <div className="formulario__acciones"><button type="button" className="boton boton--secundario" onClick={onCancelar}>Cancelar</button><button className="boton boton--primario">{inicial ? 'Guardar cambios' : 'Registrar vehículo'}</button></div>
  </form>
}

function FormularioDisponibilidad({ fechaInicial, inicial, onGuardar, onCancelar }: { fechaInicial: string; inicial: Vehiculo; onGuardar: (d: { fecha: string; turnoInicio: string; turnoFin: string; disponible: boolean; restriccionCirculacion: string | null }) => void; onCancelar: () => void }) {
  const actual = inicial.disponibilidad
  const [fecha, setFecha] = useState(actual?.fecha ?? fechaInicial)
  const [inicio, setInicio] = useState(actual?.turnoInicio.slice(0, 5) ?? '08:00')
  const [fin, setFin] = useState(actual?.turnoFin.slice(0, 5) ?? '17:00')
  const [disponible, setDisponible] = useState(actual?.disponible ?? true)
  const [restriccion, setRestriccion] = useState(actual?.restriccionCirculacion ?? '')
  return <form className="formulario flota-formulario" onSubmit={(e) => { e.preventDefault(); onGuardar({ fecha, turnoInicio: inicio, turnoFin: fin, disponible, restriccionCirculacion: restriccion.trim() || null }) }}>
    <label>Fecha *<input required type="date" value={fecha} onChange={(e) => setFecha(e.target.value)} /></label>
    <div className="flota-campos-dobles"><label>Inicio del turno *<input required type="time" value={inicio} onChange={(e) => setInicio(e.target.value)} /></label><label>Fin del turno *<input required type="time" value={fin} onChange={(e) => setFin(e.target.value)} /></label></div>
    <label className="flota-checkbox"><input type="checkbox" checked={disponible} onChange={(e) => setDisponible(e.target.checked)} /> Disponible para planificar</label>
    {!disponible && <label>Motivo o restricción *<textarea required maxLength={500} value={restriccion} onChange={(e) => setRestriccion(e.target.value)} /></label>}
    <p className="flota-ayuda">El sistema conserva la nota ingresada; no valida reglas de circulación externas.</p>
    <div className="formulario__acciones"><button type="button" className="boton boton--secundario" onClick={onCancelar}>Cancelar</button><button className="boton boton--primario">Guardar disponibilidad</button></div>
  </form>
}
