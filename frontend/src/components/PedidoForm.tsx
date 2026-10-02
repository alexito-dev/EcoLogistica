import { useEffect, useRef, useState, type FormEvent, type ReactNode } from 'react'
import { CircleAlert, ClipboardList, MapPin, Package, Save, CalendarClock, type LucideIcon } from 'lucide-react'
import { ApiError, crearPedido, type Pedido, type PedidoCrear } from '../api/pedidos'
import { limaAIso } from '../lib/fechas'

const DISTRITOS_SUGERIDOS = ['Huancayo', 'El Tambo', 'Chilca', 'Pilcomayo', 'San Agustín de Cajas']

const PRIORIDADES = [
  { valor: '1', texto: '1 · Baja' },
  { valor: '2', texto: '2 · Normal' },
  { valor: '3', texto: '3 · Alta' },
  { valor: '4', texto: '4 · Urgente' },
]

/** Valores del formulario tal como los escribe la persona (texto). */
interface Valores {
  codigo: string
  direccion: string
  distrito: string
  latitud: string
  longitud: string
  destinatarioAlias: string
  demandaKg: string
  demandaM3: string
  tiempoServicioMin: string
  prioridad: string
  ventanaInicio: string
  ventanaFin: string
  observacionOperativa: string
}

const VACIO: Valores = {
  codigo: '',
  direccion: '',
  distrito: '',
  latitud: '',
  longitud: '',
  destinatarioAlias: '',
  demandaKg: '',
  demandaM3: '',
  tiempoServicioMin: '',
  prioridad: '2',
  ventanaInicio: '',
  ventanaFin: '',
  observacionOperativa: '',
}

const ETIQUETAS: Record<string, string> = {
  codigo: 'Código',
  direccion: 'Dirección',
  distrito: 'Distrito',
  latitud: 'Latitud',
  longitud: 'Longitud',
  destinatarioAlias: 'Destinatario',
  demandaKg: 'Peso (kg)',
  demandaM3: 'Volumen (m³)',
  tiempoServicioMin: 'Tiempo de servicio (min)',
  prioridad: 'Prioridad',
  ventanaInicio: 'Ventana: inicio',
  ventanaFin: 'Ventana: fin',
  observacionOperativa: 'Observación',
}

/** Convierte texto a número; vacío -> undefined para que el backend aplique su valor por defecto. */
function aNumero(texto: string): number | undefined {
  return texto.trim() === '' ? undefined : Number(texto)
}

function aTexto(texto: string): string | undefined {
  return texto.trim() === '' ? undefined : texto.trim()
}

function construirPayload(v: Valores): PedidoCrear {
  return {
    codigo: aTexto(v.codigo),
    direccion: aTexto(v.direccion),
    distrito: aTexto(v.distrito),
    latitud: aNumero(v.latitud),
    longitud: aNumero(v.longitud),
    destinatarioAlias: aTexto(v.destinatarioAlias),
    demandaKg: aNumero(v.demandaKg),
    demandaM3: aNumero(v.demandaM3),
    tiempoServicioMin: aNumero(v.tiempoServicioMin),
    prioridad: aNumero(v.prioridad),
    ventanaInicio: limaAIso(v.ventanaInicio),
    ventanaFin: limaAIso(v.ventanaFin),
    observacionOperativa: aTexto(v.observacionOperativa),
  }
}

function Seccion({ icono: Icono, titulo, children }: { icono: LucideIcon; titulo: string; children: ReactNode }) {
  return (
    <fieldset className="seccion">
      <legend>
        <Icono size={18} aria-hidden="true" />
        {titulo}
      </legend>
      <div className="rejilla">{children}</div>
    </fieldset>
  )
}

interface Props {
  onCreado: (pedido: Pedido) => void
  onCancelar: () => void
}

export default function PedidoForm({ onCreado, onCancelar }: Props) {
  const [valores, setValores] = useState<Valores>(VACIO)
  const [errores, setErrores] = useState<Record<string, string>>({})
  const [mensajeError, setMensajeError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)
  const resumenRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (mensajeError) resumenRef.current?.focus()
  }, [mensajeError, errores])

  function cambiar(campo: keyof Valores, valor: string) {
    setValores((previo) => ({ ...previo, [campo]: valor }))
  }

  async function enviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    setEnviando(true)
    setErrores({})
    setMensajeError(null)
    try {
      const pedido = await crearPedido(construirPayload(valores))
      onCreado(pedido)
    } catch (error) {
      // Los valores ingresados se conservan para que la persona corrija solo lo indicado.
      if (error instanceof ApiError) {
        setErrores(error.errors)
        setMensajeError(error.message)
      } else {
        setMensajeError('Ocurrió un error inesperado. Intente nuevamente.')
      }
    } finally {
      setEnviando(false)
    }
  }

  function campo(
    nombre: keyof Valores,
    opciones: {
      tipo?: string
      requerido?: boolean
      ayuda?: string
      paso?: string
      lista?: string
      min?: string
      completo?: boolean
      foco?: boolean
    } = {},
  ) {
    const error = errores[nombre]
    const idError = `${nombre}-error`
    const idAyuda = `${nombre}-ayuda`
    const describe = [error ? idError : null, opciones.ayuda ? idAyuda : null].filter(Boolean).join(' ')
    return (
      <div className={`campo${opciones.completo ? ' campo--completo' : ''}`}>
        <label htmlFor={nombre}>
          {ETIQUETAS[nombre]}
          {opciones.requerido && (
            <span className="requerido" aria-hidden="true">
              {' '}
              *
            </span>
          )}
        </label>
        <input
          id={nombre}
          name={nombre}
          type={opciones.tipo ?? 'text'}
          step={opciones.paso}
          min={opciones.min}
          list={opciones.lista}
          value={valores[nombre]}
          onChange={(e) => cambiar(nombre, e.target.value)}
          aria-required={opciones.requerido || undefined}
          aria-invalid={error ? true : undefined}
          aria-describedby={describe || undefined}
          autoComplete="off"
          data-foco-inicial={opciones.foco ? '' : undefined}
        />
        {opciones.ayuda && (
          <p id={idAyuda} className="ayuda">
            {opciones.ayuda}
          </p>
        )}
        {error && (
          <p id={idError} className="error-campo">
            <CircleAlert size={14} aria-hidden="true" />
            {error}
          </p>
        )}
      </div>
    )
  }

  const camposConError = Object.keys(errores)

  return (
    <form onSubmit={enviar} noValidate className="drawer__form">
      <div className="drawer__cuerpo">
        {mensajeError && (
          <div ref={resumenRef} tabIndex={-1} role="alert" className="aviso aviso--error">
            <CircleAlert size={20} aria-hidden="true" />
            <div>
              <strong>{mensajeError}</strong>
              {camposConError.length > 0 && (
                <ul>
                  {camposConError.map((nombre) => (
                    <li key={nombre}>
                      <a href={`#${nombre}`}>{ETIQUETAS[nombre] ?? nombre}</a>: {errores[nombre]}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        )}

        <Seccion icono={MapPin} titulo="Destino">
          {campo('direccion', { requerido: true, completo: true, foco: true })}
          {campo('distrito', { requerido: true, lista: 'distritos' })}
          <datalist id="distritos">
            {DISTRITOS_SUGERIDOS.map((d) => (
              <option key={d} value={d} />
            ))}
          </datalist>
          {campo('destinatarioAlias')}
          {campo('latitud', { requerido: true, tipo: 'number', paso: 'any', ayuda: 'Ej.: -12.0651' })}
          {campo('longitud', { requerido: true, tipo: 'number', paso: 'any', ayuda: 'Ej.: -75.2049' })}
        </Seccion>

        <Seccion icono={Package} titulo="Carga y servicio">
          {campo('demandaKg', { tipo: 'number', paso: 'any', min: '0', ayuda: 'Al menos peso o volumen' })}
          {campo('demandaM3', { tipo: 'number', paso: 'any', min: '0' })}
          {campo('tiempoServicioMin', { tipo: 'number', paso: '1', min: '1', ayuda: 'Por defecto 10 min' })}
          <div className="campo">
            <label htmlFor="prioridad">{ETIQUETAS.prioridad}</label>
            <select
              id="prioridad"
              name="prioridad"
              value={valores.prioridad}
              onChange={(e) => cambiar('prioridad', e.target.value)}
              aria-invalid={errores.prioridad ? true : undefined}
              aria-describedby={errores.prioridad ? 'prioridad-error' : undefined}
            >
              {PRIORIDADES.map((p) => (
                <option key={p.valor} value={p.valor}>
                  {p.texto}
                </option>
              ))}
            </select>
            {errores.prioridad && (
              <p id="prioridad-error" className="error-campo">
                <CircleAlert size={14} aria-hidden="true" />
                {errores.prioridad}
              </p>
            )}
          </div>
        </Seccion>

        <Seccion icono={CalendarClock} titulo="Ventana horaria (hora de Lima, UTC−5)">
          {campo('ventanaInicio', { requerido: true, tipo: 'datetime-local' })}
          {campo('ventanaFin', { requerido: true, tipo: 'datetime-local' })}
        </Seccion>

        <Seccion icono={ClipboardList} titulo="Identificación y notas">
          {campo('codigo', { ayuda: 'Opcional: si lo deja vacío se genera automáticamente' })}
          {campo('observacionOperativa')}
        </Seccion>
      </div>

      <footer className="drawer__pie">
        <button type="button" className="boton boton--secundario" onClick={onCancelar} disabled={enviando}>
          Cancelar
        </button>
        <button type="submit" className="boton boton--primario" disabled={enviando}>
          <Save size={18} aria-hidden="true" />
          {enviando ? 'Guardando…' : 'Guardar pedido'}
        </button>
      </footer>
    </form>
  )
}
