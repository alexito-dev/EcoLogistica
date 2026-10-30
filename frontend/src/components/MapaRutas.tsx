import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import type { VistaPrevia } from '../api/rutas'
import { COLORES_RUTA } from '../lib/colores'
import { trazarPorCalles, type Punto } from '../lib/trazado'

const TILES = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
const ATRIBUCION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'

interface Props {
  vista: VistaPrevia
  /** Índice de la ruta resaltada; null muestra todas por igual. */
  seleccion: number | null
  onSeleccion: (indice: number | null) => void
}

/** Recorrido de cada ruta, con las paradas en orden y el regreso al depósito. */
function recorridos(vista: VistaPrevia): Punto[][] {
  const deposito: Punto = [vista.deposito.latitud, vista.deposito.longitud]
  return vista.rutas.map((ruta) => [deposito, ...ruta.paradas.map((p): Punto => [p.latitud, p.longitud]), deposito])
}

/** Trazos por calles de una vista; `lineas[i]` es null si esa ruta se dibuja en línea recta. */
interface Trazado {
  para: VistaPrevia
  lineas: (Punto[] | null)[]
}

function escapar(texto: string): string {
  return texto.replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`)
}

/** Mapa Leaflet + OpenStreetMap (RES-06): depósito, paradas numeradas y recorrido de cada vehículo. */
export default function MapaRutas({ vista, seleccion, onSeleccion }: Props) {
  const contenedor = useRef<HTMLDivElement>(null)
  const mapa = useRef<L.Map | null>(null)
  const capa = useRef<L.LayerGroup | null>(null)
  const encuadrada = useRef<VistaPrevia | null>(null)
  const [trazado, setTrazado] = useState<Trazado | null>(null)

  // Pide a OSRM el camino por calles de cada ruta; mientras llega (o si falla) se ven líneas rectas.
  useEffect(() => {
    const cancelar = new AbortController()
    Promise.all(recorridos(vista).map((puntos) => trazarPorCalles(puntos, cancelar.signal))).then((lineas) => {
      if (!cancelar.signal.aborted) setTrazado({ para: vista, lineas })
    })
    return () => cancelar.abort()
  }, [vista])
  const lineas = trazado?.para === vista ? trazado.lineas : null
  const porCalles = lineas !== null && lineas.length > 0 && lineas.every((l) => l !== null)

  useEffect(() => {
    if (!contenedor.current) return
    const m = L.map(contenedor.current, { zoomControl: true, attributionControl: true })
    L.tileLayer(TILES, { attribution: ATRIBUCION, maxZoom: 19 }).addTo(m)
    capa.current = L.layerGroup().addTo(m)
    mapa.current = m
    return () => {
      m.remove()
      mapa.current = null
      encuadrada.current = null
    }
  }, [])

  useEffect(() => {
    const m = mapa.current
    const grupo = capa.current
    if (!m || !grupo) return
    grupo.clearLayers()

    const deposito: L.LatLngTuple = [vista.deposito.latitud, vista.deposito.longitud]
    const limites = L.latLngBounds([deposito])
    const rectas = recorridos(vista)

    vista.rutas.forEach((ruta, i) => {
      const color = COLORES_RUTA[i % COLORES_RUTA.length]
      const activa = seleccion === null || seleccion === i
      L.polyline(lineas?.[i] ?? rectas[i], {
        color,
        weight: activa ? 5 : 3,
        opacity: activa ? 0.9 : 0.2,
        dashArray: activa ? undefined : '6 8',
        lineJoin: 'round',
      })
        .on('click', () => onSeleccion(seleccion === i ? null : i))
        .addTo(grupo)

      ruta.paradas.forEach((p) => {
        limites.extend([p.latitud, p.longitud])
        const clases = `marcador-parada${activa ? '' : ' marcador-parada--tenue'}${p.dentroDeVentana ? '' : ' marcador-parada--tarde'}`
        L.marker([p.latitud, p.longitud], {
          icon: L.divIcon({
            className: '',
            html: `<span class="${clases}" style="--color:${color}">${p.orden}</span>`,
            iconSize: [30, 30],
            iconAnchor: [15, 15],
          }),
          keyboard: false,
          zIndexOffset: activa ? 500 : 0,
        })
          .bindPopup(
            `<strong>${escapar(p.codigo)}</strong> · ${escapar(ruta.vehiculo.placa)}<br>` +
              `${escapar(p.destinatarioAlias ?? 'Sin alias')}<br>${escapar(p.direccion)}, ${escapar(p.distrito)}<br>` +
              `${p.demandaKg} kg${p.dentroDeVentana ? '' : ' · <em>llega fuera de su ventana</em>'}`,
          )
          .addTo(grupo)
      })
    })

    L.marker(deposito, {
      icon: L.divIcon({ className: '', html: '<span class="marcador-deposito" aria-hidden="true"></span>', iconSize: [34, 34], iconAnchor: [17, 17] }),
      zIndexOffset: 1000,
    })
      .bindPopup(`<strong>${escapar(vista.deposito.nombre)}</strong><br>Punto de salida y regreso`)
      .addTo(grupo)

    // Solo se reencuadra al cambiar los datos, no al resaltar una ruta.
    if (encuadrada.current !== vista) {
      m.fitBounds(limites, { padding: [36, 36], maxZoom: 15 })
      encuadrada.current = vista
    }
  }, [vista, seleccion, onSeleccion, lineas])

  return (
    <div className="mapa-envoltura">
      <div
        ref={contenedor}
        className="mapa"
        role="region"
        aria-label={`Mapa con ${vista.rutas.length} rutas propuestas desde ${vista.deposito.nombre}`}
      />
      {vista.rutas.length > 0 && (
        <p className="mapa__trazado" role="status">
          {lineas === null ? 'Trazando por calles…' : porCalles ? 'Recorrido por calles · OSRM' : 'Líneas rectas: servicio de calles no disponible'}
        </p>
      )}
    </div>
  )
}
