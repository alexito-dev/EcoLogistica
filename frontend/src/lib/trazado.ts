/**
 * Trazado de un recorrido por calles reales con OSRM (motor de rutas de código abierto sobre
 * OpenStreetMap, conforme a RES-06). Solo cambia el dibujo del mapa: la propuesta de rutas y sus
 * kilómetros los calcula el backend. Si el servicio no responde, se devuelve null y el mapa usa
 * líneas rectas.
 */

export type Punto = [latitud: number, longitud: number]

/** Servidor OSRM. El público es de demostración; para producción se configura uno propio. */
const OSRM_URL: string = import.meta.env.VITE_OSRM_URL ?? 'https://router.project-osrm.org'
const ESPERA_MAXIMA_MS = 8000

interface RespuestaOsrm {
  code: string
  routes?: { geometry: { coordinates: [number, number][] } }[]
}

export async function trazarPorCalles(puntos: Punto[], senal?: AbortSignal): Promise<Punto[] | null> {
  if (puntos.length < 2) return null
  // OSRM recibe "longitud,latitud" separados por ";".
  const coordenadas = puntos.map(([lat, lon]) => `${lon},${lat}`).join(';')
  const limite = new AbortController()
  const temporizador = setTimeout(() => limite.abort(), ESPERA_MAXIMA_MS)
  const cancelar = () => limite.abort()
  senal?.addEventListener('abort', cancelar)
  try {
    const respuesta = await fetch(`${OSRM_URL}/route/v1/driving/${coordenadas}?overview=full&geometries=geojson`, {
      signal: limite.signal,
    })
    if (!respuesta.ok) return null
    const datos = (await respuesta.json()) as RespuestaOsrm
    const linea = datos.code === 'Ok' ? datos.routes?.[0]?.geometry.coordinates : undefined
    return linea && linea.length > 1 ? linea.map(([lon, lat]) => [lat, lon]) : null
  } catch {
    return null
  } finally {
    clearTimeout(temporizador)
    senal?.removeEventListener('abort', cancelar)
  }
}
