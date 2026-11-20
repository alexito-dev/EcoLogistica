import { expect, test } from '@playwright/test'

/**
 * Disponibilidad y resiliencia (Sprint 4): códigos HTTP esperados, manejo de errores de red y de servidor en la
 * interfaz, y una sonda de disponibilidad (uptime) sobre /health. Corre en Chromium, Firefox y WebKit y también
 * contra un entorno desplegado (ECO_BASE_URL / ECO_API_URL) como prueba de humo posterior al despliegue.
 */
const API = process.env.ECO_API_URL ?? 'http://localhost:8000'
const SONDAS = Number(process.env.ECO_SONDAS ?? 30)

test.describe('códigos de estado HTTP', () => {
  test('la interfaz y la sonda /health responden 200', async ({ request }) => {
    const web = await request.get('/')
    expect(web.status()).toBe(200)
    expect(web.headers()['content-type']).toContain('text/html')

    const salud = await request.get(`${API}/health`)
    expect(salud.status()).toBe(200)
    expect((await salud.json()).status).toBe('ok')
  })

  test('la API rechaza con el código correcto: 401 sin sesión, 404 en ruta inexistente, 405 en método no permitido', async ({ request }) => {
    expect((await request.get(`${API}/api/v1/auth/sesion`)).status()).toBe(401)
    expect((await request.get(`${API}/api/v1/pedidos`)).status()).toBe(401)
    expect((await request.get(`${API}/api/v1/no-existe`)).status()).toBe(404)
    expect((await request.delete(`${API}/api/v1/auth/sesion`)).status()).toBe(405)
  })

  test('la API valida el cuerpo de las solicitudes (422/401) sin filtrar detalles internos', async ({ request }) => {
    const respuesta = await request.post(`${API}/api/v1/auth/login`, { data: { correo: 'no-es-un-correo' } })
    expect([400, 401, 422]).toContain(respuesta.status())
    expect(await respuesta.text()).not.toMatch(/Traceback|File ".*\.py"/)
  })

  test('las cabeceras de seguridad están presentes en la API', async ({ request }) => {
    const r = await request.get(`${API}/api/v1/auth/sesion`)
    expect(r.headers()['x-content-type-options']).toBe('nosniff')
    expect(r.headers()['x-frame-options']).toBe('DENY')
  })
})

test.describe('resiliencia de la interfaz ante fallos', () => {
  async function intentarIngresar(page: import('@playwright/test').Page) {
    await page.goto('/')
    await page.getByLabel('Correo').fill('planificador@ecologistica.test')
    await page.getByLabel('Contraseña', { exact: true }).fill('cualquier-clave-1')
    await page.getByRole('button', { name: 'Continuar' }).click()
  }

  test('un fallo de red al iniciar sesión se informa y la pantalla sigue usable', async ({ page }) => {
    await page.route('**/api/v1/auth/login', (ruta) => ruta.abort('failed'))
    await intentarIngresar(page)

    await expect(page.getByRole('alert')).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Iniciar sesión' })).toBeVisible()
    // El correo se conserva y, al escribir de nuevo la contraseña, se puede reintentar.
    await expect(page.getByLabel('Correo')).toHaveValue('planificador@ecologistica.test')
    await page.getByLabel('Contraseña', { exact: true }).fill('otra-clave-2')
    await expect(page.getByRole('button', { name: 'Continuar' })).toBeEnabled()
  })

  test('un error 500 del servidor se informa sin romper la interfaz', async ({ page }) => {
    const errores: string[] = []
    page.on('pageerror', (e) => errores.push(e.message))
    await page.route('**/api/v1/auth/login', (ruta) =>
      ruta.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 500, message: 'Error interno' }) }),
    )
    await intentarIngresar(page)

    await expect(page.getByRole('alert')).toBeVisible()
    await page.getByLabel('Contraseña', { exact: true }).fill('otra-clave-2')
    await expect(page.getByRole('button', { name: 'Continuar' })).toBeEnabled()
    expect(errores, 'errores de JavaScript no controlados').toEqual([])
  })

  test('una respuesta 503 (servicio no disponible) se informa y permite reintentar', async ({ page }) => {
    let intentos = 0
    await page.route('**/api/v1/auth/login', (ruta) => {
      intentos += 1
      return ruta.fulfill({ status: 503, contentType: 'application/json', body: JSON.stringify({ status: 503, message: 'No disponible' }) })
    })
    await intentarIngresar(page)
    await expect(page.getByRole('alert')).toBeVisible()
    await page.getByLabel('Contraseña', { exact: true }).fill('otra-clave-2')
    await page.getByRole('button', { name: 'Continuar' }).click()
    await expect.poll(() => intentos).toBe(2)
  })
})

test('disponibilidad: la sonda /health responde correctamente en todas las consultas consecutivas', async ({ request }, testInfo) => {
  let correctas = 0
  const tiempos: number[] = []
  for (let i = 0; i < SONDAS; i++) {
    const t0 = Date.now()
    const r = await request.get(`${API}/health`, { timeout: 5_000 }).catch(() => null)
    tiempos.push(Date.now() - t0)
    if (r?.status() === 200) correctas += 1
  }
  const disponibilidad = (correctas / SONDAS) * 100
  const ordenados = [...tiempos].sort((a, b) => a - b)
  const resumen = {
    sondas: SONDAS,
    correctas,
    disponibilidadPorcentaje: Number(disponibilidad.toFixed(2)),
    maximoMs: ordenados.at(-1),
    p95Ms: ordenados[Math.min(ordenados.length - 1, Math.ceil(0.95 * ordenados.length) - 1)],
  }
  await testInfo.attach('disponibilidad.json', { body: JSON.stringify(resumen, null, 2), contentType: 'application/json' })
  console.log(`[disponibilidad:${testInfo.project.name}] ${JSON.stringify(resumen)}`)
  expect(disponibilidad).toBeGreaterThanOrEqual(99)
})
