import { useState, type ChangeEvent, type FormEvent } from 'react'
import { CircleAlert, Download, FileUp } from 'lucide-react'
import { ApiError, importarPedidos, obtenerPlantilla } from '../api/pedidos'

interface Props {
  onImportado: (cantidad: number) => void
  onCancelar: () => void
}

/** Lee un archivo como texto (FileReader funciona en todos los navegadores y en las pruebas). */
function leerTexto(archivo: File): Promise<string> {
  return new Promise((resolver, rechazar) => {
    const lector = new FileReader()
    lector.onload = () => resolver(String(lector.result ?? ''))
    lector.onerror = () => rechazar(lector.error)
    lector.readAsText(archivo)
  })
}

/** Carga masiva desde la plantilla CSV (ECO-18): se valida todo y se registra solo si no hay errores. */
export default function ImportarPedidos({ onImportado, onCancelar }: Props) {
  const [contenido, setContenido] = useState('')
  const [nombre, setNombre] = useState('')
  const [enviando, setEnviando] = useState(false)
  const [error, setError] = useState('')
  const [filas, setFilas] = useState<[string, string][]>([])

  const descargarPlantilla = async () => {
    try {
      const texto = await obtenerPlantilla()
      const url = URL.createObjectURL(new Blob([texto], { type: 'text/csv;charset=utf-8' }))
      const enlace = document.createElement('a')
      enlace.href = url
      enlace.download = 'plantilla-pedidos.csv'
      enlace.click()
      URL.revokeObjectURL(url)
    } catch (e) {
      setError(e instanceof ApiError ? e.message : 'No se pudo descargar la plantilla.')
    }
  }

  const elegirArchivo = async (e: ChangeEvent<HTMLInputElement>) => {
    const archivo = e.target.files?.[0]
    setError('')
    setFilas([])
    if (!archivo) return
    setNombre(archivo.name)
    setContenido(await leerTexto(archivo))
  }

  const enviar = async (e: FormEvent) => {
    e.preventDefault()
    setEnviando(true)
    setError('')
    setFilas([])
    try {
      const r = await importarPedidos(contenido)
      onImportado(r.importados)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
        setFilas(Object.entries(err.errors))
      } else {
        setError('No se pudo importar el archivo. Intente nuevamente.')
      }
    } finally {
      setEnviando(false)
    }
  }

  return (
    <form className="importar" onSubmit={(e) => void enviar(e)}>
      <p>
        Descargue la plantilla, complete una fila por pedido y súbala. Las fechas se escriben como{' '}
        <code>AAAA-MM-DD HH:MM</code> en hora de Lima. Se importan todos los pedidos o ninguno.
      </p>
      <button type="button" className="boton boton--secundario" onClick={() => void descargarPlantilla()}>
        <Download size={18} aria-hidden="true" /> Descargar plantilla CSV
      </button>

      <div className="campo">
        <label htmlFor="archivo-pedidos">Archivo CSV de pedidos</label>
        <input id="archivo-pedidos" type="file" accept=".csv,text/csv" onChange={(e) => void elegirArchivo(e)} />
        {nombre && <small>Archivo elegido: {nombre}</small>}
      </div>

      {error && (
        <div role="alert" className="aviso aviso--error">
          <CircleAlert size={20} aria-hidden="true" />
          <div>
            <strong>{error}</strong>
            {filas.length > 0 && (
              <ul className="importar__errores">
                {filas.map(([campo, mensaje]) => (
                  <li key={campo}>
                    <strong>{campo}:</strong> {mensaje}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}

      <div className="parada-ejecucion__acciones">
        <button type="submit" className="boton boton--primario" disabled={enviando || !contenido}>
          <FileUp size={18} aria-hidden="true" /> {enviando ? 'Importando…' : 'Importar pedidos'}
        </button>
        <button type="button" className="boton boton--secundario" onClick={onCancelar}>
          Cancelar
        </button>
      </div>
    </form>
  )
}
