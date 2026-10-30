/** Hora de Lima (UTC-5, sin horario de verano): la API exige ISO 8601 con desfase explícito. */

const DESFASE_LIMA = '-05:00'

/** "2026-10-05T08:00" (datetime-local) -> "2026-10-05T08:00:00-05:00". Vacío -> undefined. */
export function limaAIso(valorLocal: string): string | undefined {
  if (!valorLocal) return undefined
  const conSegundos = /T\d{2}:\d{2}$/.test(valorLocal) ? `${valorLocal}:00` : valorLocal
  return `${conSegundos}${DESFASE_LIMA}`
}

const formato = new Intl.DateTimeFormat('es-PE', {
  timeZone: 'America/Lima',
  day: '2-digit',
  month: '2-digit',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
  hour12: false,
})

const formatoCorto = new Intl.DateTimeFormat('es-PE', {
  timeZone: 'America/Lima',
  day: '2-digit',
  month: '2-digit',
  hour: '2-digit',
  minute: '2-digit',
  hour12: false,
})
const formatoDia = new Intl.DateTimeFormat('es-PE', { timeZone: 'America/Lima', day: '2-digit', month: '2-digit', year: 'numeric' })
const formatoHora = new Intl.DateTimeFormat('es-PE', { timeZone: 'America/Lima', hour: '2-digit', minute: '2-digit', hour12: false })

/** "05/10 08:00 – 12:00" si es el mismo día (hora de Lima); si no, "05/10 08:00 → 06/10 11:00". */
export function ventanaCorta(inicioIso: string, finIso: string): string {
  const inicio = new Date(inicioIso)
  const fin = new Date(finIso)
  if (Number.isNaN(inicio.getTime()) || Number.isNaN(fin.getTime())) return `${inicioIso} → ${finIso}`
  const mismoDia = formatoDia.format(inicio) === formatoDia.format(fin)
  return mismoDia
    ? `${formatoCorto.format(inicio).replace(',', '')} – ${formatoHora.format(fin)}`
    : `${formatoCorto.format(inicio).replace(',', '')} → ${formatoCorto.format(fin).replace(',', '')}`
}

/** Instante ISO (UTC) -> "05/10/2026, 08:00" en hora de Lima. */
export function isoAHoraLima(iso: string): string {
  const fecha = new Date(iso)
  return Number.isNaN(fecha.getTime()) ? iso : formato.format(fecha)
}

/** Fecha local en formato AAAA-MM-DD, desplazada en días (1 = mañana, el día que se suele planificar). */
export function fechaLocal(desplazamientoDias = 0): string {
  const d = new Date()
  d.setDate(d.getDate() + desplazamientoDias)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

/** "2026-10-10" -> "10/10/2026". */
export function fechaCorta(iso: string): string {
  return iso.split('-').reverse().join('/')
}
