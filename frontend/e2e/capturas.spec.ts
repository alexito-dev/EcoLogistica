import { join } from 'node:path'
import { expect, test } from '@playwright/test'
import { cerrarSesion, iniciarSesion, irA } from './ayudas'

/**
 * Evidencias multimedia de la demostración del Sprint 4 (capturas de pantalla del recorrido real).
 * No forma parte de la suite habitual: se ejecuta solo con ECO_CAPTURAS=1.
 *   $env:ECO_CAPTURAS='1'; npx playwright test e2e/capturas.spec.ts --project=chromium
 */
const SALIDA = process.env.ECO_CAPTURAS_DIR ?? join(process.cwd(), '..', 'docs', '03 Implementación', 'Sprint 04', 'evidencias')

test.skip(!process.env.ECO_CAPTURAS, 'Capturas de la demostración: defina ECO_CAPTURAS=1')

test('capturas del recorrido Planificación → Conducción → Indicadores', async ({ page }) => {
  test.setTimeout(240_000)
  await page.emulateMedia({ reducedMotion: 'reduce' })
  await page.setViewportSize({ width: 1366, height: 820 })
  const foto = (nombre: string) => page.screenshot({ path: join(SALIDA, `demo-${nombre}.png`) })

  await iniciarSesion(page, 'planificador')
  await expect(page.getByRole('heading', { name: 'Pedidos', level: 1 })).toBeVisible()
  await foto('01-pedidos-planificador')

  await irA(page, 'Rutas')
  const fecha = await page.getByLabel('Fecha de reparto').inputValue()
  await expect(page.getByRole('heading', { name: 'Mapa de rutas' })).toBeVisible()
  await page.getByRole('button', { name: 'Guardar rutas' }).click()
  await expect(page.getByRole('status').filter({ hasText: 'Rutas guardadas' })).toBeVisible()
  await page.waitForTimeout(1500) // tiles del mapa
  await foto('02-rutas-guardadas-con-mapa')

  await irA(page, 'Seguimiento')
  await page.getByLabel('Fecha de reparto').fill(fecha)
  const selectores = page.getByLabel(/Conductor asignado al vehículo/)
  await expect(selectores.first()).toBeVisible()
  for (let i = 0; i < (await selectores.count()); i++) {
    await selectores.nth(i).selectOption({ label: 'Conductor de ruta' })
    await expect(selectores.nth(i)).not.toHaveValue('')
  }
  await foto('03-seguimiento-conductor-asignado')
  await cerrarSesion(page)

  await iniciarSesion(page, 'conductor')
  await expect(page.getByRole('heading', { name: 'Mi ruta', level: 1 })).toBeVisible()
  await page.getByLabel('Fecha de reparto').fill(fecha)
  const paradas = page.locator('.parada-ejecucion')
  await expect(paradas.first()).toBeVisible()
  await page.waitForTimeout(1500)
  await foto('04-mi-ruta-conductor')

  await paradas.nth(0).getByRole('button', { name: /Salir hacia la parada/ }).click()
  await paradas.nth(0).getByRole('button', { name: /Marcar entregado/ }).click()
  await expect(paradas.nth(0)).toContainText('Entregado')
  await paradas.nth(1).getByRole('button', { name: /Salir hacia la parada/ }).click()
  await paradas.nth(1).getByRole('button', { name: /Reportar incidencia/ }).click()
  await page.getByLabel(/Describa la incidencia/).fill('Cliente ausente en el domicilio')
  await foto('05-incidencia-por-reportar')
  await page.getByRole('button', { name: 'Enviar incidencia' }).click()
  await expect(paradas.nth(1)).toContainText('Incidencia')
  await foto('06-entrega-e-incidencia-registradas')
  await cerrarSesion(page)

  await iniciarSesion(page, 'planificador')
  await irA(page, 'Seguimiento')
  await page.getByLabel('Fecha de reparto').fill(fecha)
  await expect(page.getByRole('heading', { name: /Incidencias abiertas \(1\)/ })).toBeVisible()
  await page.getByRole('button', { name: /Reprogramar pedido/ }).click()
  await foto('07-seguimiento-incidencia-confirmar-reprogramar')
  await page.getByRole('button', { name: /Confirmar reprogramación del pedido/ }).click()
  await expect(page.getByRole('heading', { name: /Incidencias abiertas \(0\)/ })).toBeVisible()

  await irA(page, 'Indicadores')
  await page.getByLabel('Fecha de reparto').fill(fecha)
  await expect(page.getByRole('heading', { name: 'Resultados observados de la ejecución' })).toBeVisible()
  await page.waitForTimeout(800)
  await foto('08-indicadores-resultados-observados')
})
