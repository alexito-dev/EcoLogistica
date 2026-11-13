import AxeBuilder from '@axe-core/playwright'
import { expect, test, type Page } from '@playwright/test'
import { iniciarSesion, irA } from './ayudas'

/** Criterios WCAG 2.2 AA pendientes del Sprint 3 (ECO-24): 1.4.4, 1.4.12, 1.4.13, 2.4.5, 2.4.11 y axe-core. */

const ETIQUETAS_AXE = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']

async function axe(page: Page) {
  const resultado = await new AxeBuilder({ page }).withTags(ETIQUETAS_AXE).analyze()
  return resultado.violations.map(
    (v) => `${v.id}: ${v.nodes.map((n) => `${n.target.join(' ')} → ${n.any[0]?.message ?? n.failureSummary}`).join(' | ')}`,
  )
}

test.describe('axe-core en las vistas, tema claro y oscuro', () => {
  for (const tema of ['light', 'dark'] as const) {
    test(`sin violaciones en acceso y vistas de planificación (${tema})`, async ({ page }) => {
      // Sin animaciones de entrada: axe mediría colores a medio desvanecer y daría falsos contrastes bajos.
      await page.emulateMedia({ colorScheme: tema, reducedMotion: 'reduce' })
      await page.goto('/')
      await expect(page.getByRole('heading', { name: 'Iniciar sesión' })).toBeVisible()
      expect(await axe(page), 'acceso').toEqual([])

      await iniciarSesion(page, 'planificador')
      for (const vista of ['Pedidos', 'Flota', 'Rutas', 'Seguimiento', 'Indicadores']) {
        await irA(page, vista)
        await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
        await page.waitForLoadState('networkidle')
        expect(await axe(page), vista).toEqual([])
      }
    })
  }
})

test('1.4.4 y 1.4.10: con zoom al 200 % no hay desplazamiento horizontal ni contenido perdido', async ({ page }) => {
  await page.setViewportSize({ width: 640, height: 360 }) // 1280 × 720 ampliado al 200 %
  await iniciarSesion(page, 'planificador')
  for (const vista of ['Pedidos', 'Flota', 'Rutas', 'Seguimiento', 'Indicadores']) {
    await page.setViewportSize({ width: 640, height: 360 })
    const botonMovil = page.getByRole('navigation', { name: 'Navegación móvil' }).getByRole('button', { name: vista })
    await botonMovil.click()
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
    const desborde = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth)
    expect(desborde, `${vista}: desplazamiento horizontal`).toBeLessThanOrEqual(1)
  }
})

test('1.4.12: con el espaciado de texto ampliado no se recorta contenido', async ({ page }) => {
  await iniciarSesion(page, 'planificador')
  for (const vista of ['Pedidos', 'Flota', 'Rutas', 'Seguimiento']) {
    await irA(page, vista)
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
    await page.addStyleTag({
      content: `* { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important; }
                p { margin-bottom: 2em !important; }`,
    })
    const recortados = await page.evaluate(() =>
      Array.from(document.querySelectorAll<HTMLElement>('body *'))
        .filter((el) => {
          const estilo = getComputedStyle(el)
          const oculta = estilo.overflow === 'hidden' || estilo.overflowY === 'hidden'
          return oculta && !el.closest('.solo-lectores') && el.children.length === 0 && el.textContent?.trim() && el.scrollHeight > el.clientHeight + 2 && el.clientHeight > 0
        })
        .map((el) => `${el.tagName.toLowerCase()}.${el.className}`),
    )
    expect(recortados, `${vista}: texto recortado`).toEqual([])
  }
})

test('2.4.11: el foco no queda oculto tras la barra inferior en el celular', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 700 })
  await iniciarSesion(page, 'planificador')
  await page.getByRole('navigation', { name: 'Navegación móvil' }).getByRole('button', { name: 'Pedidos' }).click()
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
  const barra = await page.getByRole('navigation', { name: 'Navegación móvil' }).boundingBox()
  expect(barra).not.toBeNull()
  // Se recorre con Tab: cada elemento enfocado debe quedar sobre la barra fija inferior.
  for (let i = 0; i < 25; i++) {
    await page.keyboard.press('Tab')
    await page.waitForTimeout(400) // el desplazamiento al foco es suave (scroll-behavior: smooth)
    const caja = await page.evaluate(() => {
      const activo = document.activeElement
      if (!activo || activo === document.body || activo.closest('.barra-inferior')) return null // los controles de la propia barra siempre son visibles
      const r = activo?.getBoundingClientRect()
      return r ? { bottom: r.bottom, height: r.height, quien: `${activo!.tagName} ${(activo as HTMLElement).innerText?.slice(0, 40) ?? ''} ${activo!.className}` } : null
    })
    if (caja && caja.height > 0) expect(caja.bottom, `Tab ${i + 1}: ${caja.quien}`).toBeLessThanOrEqual(barra!.y + 1)
  }
})

test('2.4.5: existe una segunda vía de navegación (mapa de navegación en el pie)', async ({ page }) => {
  await iniciarSesion(page, 'planificador')
  const mapa = page.getByRole('navigation', { name: 'Mapa de navegación' })
  await expect(mapa.getByRole('button')).toHaveCount(5)
  await mapa.getByRole('button', { name: 'Ir a Flota' }).click()
  await expect(page.getByRole('heading', { name: 'Flota', level: 1 })).toBeVisible()
})

test('1.4.13: el contenido emergente del mapa se cierra con Esc sin mover el puntero', async ({ page }) => {
  await iniciarSesion(page, 'planificador')
  await irA(page, 'Rutas')
  await expect(page.getByRole('heading', { name: 'Mapa de rutas' })).toBeVisible()
  const marcador = page.locator('.marcador-parada').first()
  await marcador.click()
  const popup = page.locator('.leaflet-popup')
  await expect(popup).toBeVisible()
  await page.keyboard.press('Escape')
  await expect(popup).toHaveCount(0)
})
