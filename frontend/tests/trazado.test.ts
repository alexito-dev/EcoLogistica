import { trazarPorCalles } from '../src/lib/trazado'

afterEach(() => vi.restoreAllMocks())

describe('trazarPorCalles', () => {
  it('pide el recorrido a OSRM en orden longitud,latitud y devuelve latitud,longitud', async () => {
    const espia = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ code: 'Ok', routes: [{ geometry: { coordinates: [[-75.2, -12.06], [-75.21, -12.07]] } }] })),
    )
    const linea = await trazarPorCalles([[-12.06, -75.2], [-12.07, -75.21]])
    expect(String(espia.mock.calls[0][0])).toContain('/route/v1/driving/-75.2,-12.06;-75.21,-12.07?overview=full&geometries=geojson')
    expect(linea).toEqual([[-12.06, -75.2], [-12.07, -75.21]])
  })

  it('devuelve null si el servicio falla o no encuentra ruta', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValueOnce(new Error('sin red'))
    expect(await trazarPorCalles([[-12.06, -75.2], [-12.07, -75.21]])).toBeNull()
    vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(new Response(JSON.stringify({ code: 'NoRoute' })))
    expect(await trazarPorCalles([[-12.06, -75.2], [-12.07, -75.21]])).toBeNull()
    vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(new Response('', { status: 429 }))
    expect(await trazarPorCalles([[-12.06, -75.2], [-12.07, -75.21]])).toBeNull()
  })

  it('no consulta con menos de dos puntos', async () => {
    const espia = vi.spyOn(globalThis, 'fetch')
    expect(await trazarPorCalles([[-12.06, -75.2]])).toBeNull()
    expect(espia).not.toHaveBeenCalled()
  })
})
