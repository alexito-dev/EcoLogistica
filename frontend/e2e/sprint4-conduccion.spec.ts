import AxeBuilder from '@axe-core/playwright'
import { expect, test } from '@playwright/test'
import { cerrarSesion, iniciarSesion, irA } from './ayudas'

/**
 * Recorrido completo del Sprint 4 en navegador real: Planificación guarda rutas y asigna conductor; Conducción
 * consulta su ruta, marca entregas y reporta una incidencia; Planificación la ve, reprograma y reoptimiza.
 */
test('Planificación y Conducción completan una ruta con una incidencia', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' }) // sin animaciones de entrada: contrastes medidos con colores finales
  // --- Planificación: guardar rutas del día siguiente (datos de demostración) y asignar conductor ---
  await iniciarSesion(page, 'planificador')
  await irA(page, 'Rutas')
  const fecha = await page.getByLabel('Fecha de reparto').inputValue()
  await expect(page.getByRole('heading', { name: 'Mapa de rutas' })).toBeVisible()
  await page.getByRole('button', { name: 'Guardar rutas' }).click()
  await expect(page.getByRole('status').filter({ hasText: 'Rutas guardadas' })).toBeVisible()

  await irA(page, 'Seguimiento')
  await page.getByLabel('Fecha de reparto').fill(fecha)
  const selectores = page.getByLabel(/Conductor asignado al vehículo/)
  await expect(selectores.first()).toBeVisible()
  // Se asigna el mismo conductor a todas las rutas del día; el valor `c1` no es fijo, se elige por nombre.
  for (let i = 0; i < (await selectores.count()); i++) {
    await selectores.nth(i).selectOption({ label: 'Conductor de ruta' })
    await expect(selectores.nth(i)).not.toHaveValue('')
  }
  await expect(page.getByRole('status').filter({ hasText: 'Conductor asignado' })).toBeVisible()
  await cerrarSesion(page)

  // --- Conducción: ver la ruta, entregar la primera parada y reportar incidencia en la segunda ---
  await iniciarSesion(page, 'conductor')
  await expect(page.getByRole('heading', { name: 'Mi ruta', level: 1 })).toBeVisible()
  await page.getByLabel('Fecha de reparto').fill(fecha)
  await expect(page.getByRole('heading', { name: /Vehículo / }).first()).toBeVisible()
  const paradas = page.getByRole('list').filter({ has: page.locator('.parada-ejecucion') }).locator('.parada-ejecucion')
  const total = await paradas.count()
  expect(total).toBeGreaterThanOrEqual(2)
  const axe = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag22aa']).analyze()
  expect(axe.violations.map((v) => v.id), 'accesibilidad de Mi ruta').toEqual([])

  await paradas.nth(0).getByRole('button', { name: /Salir hacia la parada/ }).click()
  await paradas.nth(0).getByRole('button', { name: /Marcar entregado/ }).click()
  await expect(paradas.nth(0)).toContainText('Entregado')

  await paradas.nth(1).getByRole('button', { name: /Salir hacia la parada/ }).click()
  await paradas.nth(1).getByRole('button', { name: /Reportar incidencia/ }).click()
  await expect(page.getByRole('button', { name: 'Enviar incidencia' })).toBeDisabled()
  await page.getByLabel(/Describa la incidencia/).fill('Cliente ausente en el domicilio')
  await page.getByRole('button', { name: 'Enviar incidencia' }).click()
  await expect(paradas.nth(1)).toContainText('Incidencia')
  await expect(paradas.nth(1)).toContainText('Cliente ausente en el domicilio')
  await cerrarSesion(page)

  // --- Planificación: ve la incidencia, la reprograma y reoptimiza lo pendiente ---
  await iniciarSesion(page, 'planificador')
  await irA(page, 'Seguimiento')
  await page.getByLabel('Fecha de reparto').fill(fecha)
  await expect(page.getByRole('heading', { name: /Incidencias abiertas \(1\)/ })).toBeVisible()
  await expect(page.getByText('Cliente ausente en el domicilio').first()).toBeVisible()
  await page.getByRole('button', { name: /Reprogramar pedido/ }).click()
  await expect(page.getByRole('heading', { name: /Incidencias abiertas \(0\)/ })).toBeVisible()
  await page.getByRole('button', { name: /Reoptimizar pendientes/ }).click()
  await expect(page.getByRole('status')).toContainText(/reordenaron|más corto/)

  // Indicadores observados: solo con la entrega registrada por Conducción (ECO-14 y ECO-26).
  await irA(page, 'Indicadores')
  await page.getByLabel('Fecha de reparto').fill(fecha)
  const observados = page.getByRole('article').filter({ has: page.getByRole('heading', { name: 'Resultados observados de la ejecución' }) })
  await expect(observados).toContainText('puntualidad observada')
  await expect(observados).toContainText(/1 de 6 entregadas|1 de \d+ entregadas/)
})

test('un conductor no puede abrir las vistas de Planificación', async ({ page }) => {
  await iniciarSesion(page, 'conductor')
  const menu = page.getByRole('navigation', { name: 'Navegación principal' })
  await expect(menu.getByRole('button', { name: 'Mi ruta' })).toBeVisible()
  await expect(menu.getByRole('button', { name: 'Pedidos' })).toHaveCount(0)
  await expect(menu.getByRole('button', { name: 'Seguimiento' })).toHaveCount(0)
})
