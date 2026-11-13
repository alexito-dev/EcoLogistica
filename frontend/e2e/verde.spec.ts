import { expect, test } from '@playwright/test'
import { iniciarSesion, irA } from './ayudas'

/** Evidencia en navegador real de las optimizaciones Green IT de la API (caché condicional y compresión). */
test('la API comprime el listado y el navegador revalida con ETag', async ({ page }) => {
  const respuestas: { url: string; encoding: string | undefined; etag: string | undefined; condicional: boolean }[] = []
  page.on('response', async (r) => {
    if (r.url().includes('/api/v1/pedidos?')) {
      const enviadas = await r.request().allHeaders() // incluye las cabeceras que añade la pila de red (If-None-Match)
      respuestas.push({
        url: r.url(),
        encoding: r.headers()['content-encoding'],
        etag: r.headers()['etag'],
        condicional: 'if-none-match' in enviadas,
      })
    }
  })
  await iniciarSesion(page, 'planificador')
  await expect(page.getByRole('heading', { name: 'Pedidos', level: 1 })).toBeVisible()
  await expect.poll(() => respuestas.length).toBeGreaterThan(0)

  expect(respuestas[0].url).toContain('limite=12') // bloques de 12 registros
  expect(respuestas[0].etag).toMatch(/^W\//)
  expect(['br', 'gzip']).toContain(respuestas[0].encoding)

  // Al volver a la vista, el navegador reenvía el validador y la API responde sin cambios.
  await irA(page, 'Flota')
  await irA(page, 'Pedidos')
  await expect.poll(() => respuestas.length).toBeGreaterThan(1)
  expect(respuestas.at(-1)!.condicional).toBe(true)
})
