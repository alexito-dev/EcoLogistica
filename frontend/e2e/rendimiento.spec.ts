import { expect, test } from '@playwright/test'
import { iniciarSesion } from './ayudas'

/**
 * Monitoreo de rendimiento (Sprint 5, solo Chromium): Web Vitals de la pantalla de acceso con el build de
 * producción (TTFB, FCP, LCP, CLS) y tiempos de respuesta de la API autenticada. Los valores medidos se adjuntan
 * al informe HTML (`rendimiento.json`) y se imprimen en consola para documentarlos.
 *
 * Los umbrales son los de la rúbrica del curso (API < 500 ms) y los «buenos» de Core Web Vitals, más holgados que
 * los de Lighthouse CI (`lighthouserc.json`) porque aquí se mide en el entorno compartido de pruebas.
 */
const API = process.env.ECO_API_URL ?? 'http://localhost:8000'
const UMBRAL = { ttfbMs: 800, fcpMs: 1800, lcpMs: 2500, cls: 0.1, apiP95Ms: 500 }
const MUESTRAS_API = 20

interface Vitales {
  ttfb: number
  fcp: number
  lcp: number
  cls: number
  cargaMs: number
}

function percentil(valores: number[], p: number): number {
  const o = [...valores].sort((a, b) => a - b)
  return o[Math.min(o.length - 1, Math.ceil((p / 100) * o.length) - 1)]
}

test('Web Vitals de la pantalla de acceso (TTFB, FCP, LCP, CLS)', async ({ page, browserName }, testInfo) => {
  test.skip(browserName !== 'chromium', 'Las métricas LCP/CLS se miden con las API de Chromium')
  // Los observadores deben existir antes de que cargue la página.
  await page.addInitScript(() => {
    const w = window as unknown as { __vitales: { lcp: number; cls: number } }
    w.__vitales = { lcp: 0, cls: 0 }
    new PerformanceObserver((lista) => {
      for (const e of lista.getEntries()) w.__vitales.lcp = e.startTime
    }).observe({ type: 'largest-contentful-paint', buffered: true })
    new PerformanceObserver((lista) => {
      for (const e of lista.getEntries() as unknown as { value: number; hadRecentInput: boolean }[]) {
        if (!e.hadRecentInput) w.__vitales.cls += e.value
      }
    }).observe({ type: 'layout-shift', buffered: true })
  })

  await page.goto('/', { waitUntil: 'load' })
  await expect(page.getByRole('heading', { name: 'Iniciar sesión' })).toBeVisible()
  await page.waitForLoadState('networkidle')

  const v: Vitales = await page.evaluate(() => {
    const nav = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming
    const fcp = performance.getEntriesByName('first-contentful-paint')[0]
    const w = window as unknown as { __vitales: { lcp: number; cls: number } }
    return { ttfb: nav.responseStart, fcp: fcp?.startTime ?? 0, lcp: w.__vitales.lcp, cls: w.__vitales.cls, cargaMs: nav.loadEventEnd }
  })
  const redondeado = {
    ttfbMs: Math.round(v.ttfb),
    fcpMs: Math.round(v.fcp),
    lcpMs: Math.round(v.lcp),
    cls: Number(v.cls.toFixed(4)),
    cargaMs: Math.round(v.cargaMs),
  }
  await testInfo.attach('web-vitals.json', { body: JSON.stringify(redondeado, null, 2), contentType: 'application/json' })
  console.log(`[web-vitals] ${JSON.stringify(redondeado)}`)

  expect(redondeado.fcpMs, 'FCP medido').toBeGreaterThan(0)
  expect(redondeado.ttfbMs, 'TTFB').toBeLessThan(UMBRAL.ttfbMs)
  expect(redondeado.fcpMs, 'FCP').toBeLessThan(UMBRAL.fcpMs)
  expect(redondeado.lcpMs, 'LCP').toBeLessThan(UMBRAL.lcpMs)
  expect(redondeado.cls, 'CLS').toBeLessThan(UMBRAL.cls)
})

test('tiempos de respuesta de la API autenticada (p95 < 500 ms)', async ({ page, browserName }, testInfo) => {
  test.skip(browserName !== 'chromium', 'El monitoreo de la API se ejecuta una sola vez, en Chromium')
  await iniciarSesion(page, 'planificador')

  const manana = new Date(Date.now() + 24 * 3600 * 1000).toISOString().slice(0, 10)
  const endpoints = ['/api/v1/auth/sesion', '/api/v1/pedidos?limite=12', '/api/v1/vehiculos', `/api/v1/indicadores?fecha=${manana}`]
  const resultados: Record<string, { estado: number; medianaMs: number; p95Ms: number; maximoMs: number }> = {}
  for (const ruta of endpoints) {
    const tiempos: number[] = []
    let estado = 0
    for (let i = 0; i < MUESTRAS_API; i++) {
      const t0 = Date.now()
      const r = await page.request.get(`${API}${ruta}`)
      tiempos.push(Date.now() - t0)
      estado = r.status()
    }
    resultados[ruta] = {
      estado,
      medianaMs: percentil(tiempos, 50),
      p95Ms: percentil(tiempos, 95),
      maximoMs: Math.max(...tiempos),
    }
  }
  await testInfo.attach('api-tiempos.json', { body: JSON.stringify(resultados, null, 2), contentType: 'application/json' })
  console.log(`[api-tiempos] ${JSON.stringify(resultados)}`)

  for (const [ruta, r] of Object.entries(resultados)) {
    expect(r.estado, `${ruta} responde 200`).toBe(200)
    expect(r.p95Ms, `${ruta} p95`).toBeLessThan(UMBRAL.apiP95Ms)
  }
})
