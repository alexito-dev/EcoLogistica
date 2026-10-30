import { useEffect, useRef } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const TILES = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
const ATRIBUCION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
const CENTRO_HUANCAYO: L.LatLngTuple = [-12.0651, -75.2049]

interface Props {
  latitud: number | undefined
  longitud: number | undefined
  onElegir: (latitud: number, longitud: number) => void
}

const marcador = () =>
  L.divIcon({ className: '', html: '<span class="marcador-destino" aria-hidden="true"></span>', iconSize: [28, 36], iconAnchor: [14, 34] })

/** Mapa pequeño para ubicar el destino con un clic; también refleja las coordenadas escritas a mano. */
export default function SelectorUbicacion({ latitud, longitud, onElegir }: Props) {
  const contenedor = useRef<HTMLDivElement>(null)
  const mapa = useRef<L.Map | null>(null)
  const pin = useRef<L.Marker | null>(null)
  const elegir = useRef(onElegir)

  useEffect(() => {
    elegir.current = onElegir
  }, [onElegir])

  useEffect(() => {
    if (!contenedor.current) return
    const m = L.map(contenedor.current, { center: CENTRO_HUANCAYO, zoom: 13 })
    L.tileLayer(TILES, { attribution: ATRIBUCION, maxZoom: 19 }).addTo(m)
    m.on('click', (e: L.LeafletMouseEvent) => elegir.current(redondear(e.latlng.lat), redondear(e.latlng.lng)))
    mapa.current = m
    return () => {
      m.remove()
      mapa.current = null
      pin.current = null
    }
  }, [])

  useEffect(() => {
    const m = mapa.current
    if (!m) return
    const valido = latitud !== undefined && longitud !== undefined && Math.abs(latitud) <= 90 && Math.abs(longitud) <= 180
    if (!valido) {
      pin.current?.remove()
      pin.current = null
      return
    }
    const punto: L.LatLngTuple = [latitud, longitud]
    if (pin.current) {
      pin.current.setLatLng(punto)
    } else {
      pin.current = L.marker(punto, { icon: marcador(), draggable: true, keyboard: false })
        .on('dragend', (e) => {
          const { lat, lng } = (e.target as L.Marker).getLatLng()
          elegir.current(redondear(lat), redondear(lng))
        })
        .addTo(m)
    }
    if (!m.getBounds().contains(punto)) m.panTo(punto)
  }, [latitud, longitud])

  return (
    <div className="selector-ubicacion campo--completo">
      <div ref={contenedor} className="selector-ubicacion__mapa" role="application" aria-label="Mapa para ubicar el destino" />
      <p className="ayuda">Haga clic en el mapa para completar latitud y longitud; luego puede arrastrar el marcador.</p>
    </div>
  )
}

function redondear(valor: number): number {
  return Math.round(valor * 1e6) / 1e6
}
