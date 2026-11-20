import { expect, test } from '@playwright/test'
import { CLAVE_DEMO, cerrarSesion, iniciarSesion, irA } from './ayudas'

/**
 * Flujos críticos de negocio (Sprint 4). Se ejecutan en Chromium, Firefox y WebKit: autenticación con MFA,
 * control de acceso por rol y validación del formulario de pedidos hasta guardar un pedido.
 */

test('credenciales incorrectas no abren sesión y se explica el motivo', async ({ page }) => {
  await page.goto('/')
  await page.getByLabel('Correo').fill('planificador@ecologistica.test')
  await page.getByLabel('Contraseña', { exact: true }).fill(`${CLAVE_DEMO}-incorrecta`)
  await page.getByRole('button', { name: 'Continuar' }).click()

  await expect(page.getByRole('alert')).toBeVisible()
  await expect(page.getByRole('button', { name: 'Cerrar sesión' })).toHaveCount(0)
  await expect(page.getByLabel('Contraseña', { exact: true })).toHaveValue('') // nunca se conserva tras un rechazo
})

test('Planificación entra con contraseña y TOTP, y cierra sesión', async ({ page }) => {
  await iniciarSesion(page, 'planificador')
  await expect(page.getByRole('heading', { name: 'Pedidos', level: 1 })).toBeVisible()
  await cerrarSesion(page)
  // Sin sesión, la vista protegida no es accesible.
  await expect(page.getByRole('navigation', { name: 'Navegación principal' })).toHaveCount(0)
})

test('Conducción solo ve su ruta y no las vistas de Planificación', async ({ page }) => {
  await iniciarSesion(page, 'conductor')
  const menu = page.getByRole('navigation', { name: 'Navegación principal' })
  await expect(menu.getByRole('button', { name: 'Mi ruta' })).toBeVisible()
  await expect(menu.getByRole('button', { name: 'Pedidos' })).toHaveCount(0)
  await expect(menu.getByRole('button', { name: 'Seguimiento' })).toHaveCount(0)
})

test('el formulario de pedido valida los campos y guarda un pedido correcto', async ({ page }) => {
  await iniciarSesion(page, 'planificador')
  await irA(page, 'Pedidos')
  await page.getByRole('button', { name: /Nuevo pedido/ }).first().click()
  const form = page.getByRole('dialog')

  // Validación: enviar vacío muestra un resumen de errores enlazado a los campos obligatorios.
  await form.getByRole('button', { name: 'Guardar pedido' }).click()
  const resumen = form.getByRole('alert').filter({ hasText: /Dirección/ })
  await expect(resumen).toBeVisible()
  await expect(resumen.getByRole('link', { name: 'Latitud' })).toBeVisible()

  // Una ventana horaria invertida se rechaza sin guardar nada.
  const direccion = `Jr. Real 123, Huancayo ${test.info().project.name}`
  await form.getByLabel('Dirección').fill(direccion)
  await form.getByLabel('Distrito').fill('Huancayo')
  await form.getByLabel('Latitud').fill('-12.0651')
  await form.getByLabel('Longitud').fill('-75.2049')
  await form.getByLabel('Peso (kg)').fill('12')
  await form.getByLabel('Ventana: inicio').fill('2026-12-01T14:00')
  await form.getByLabel('Ventana: fin').fill('2026-12-01T09:00')
  await form.getByRole('button', { name: 'Guardar pedido' }).click()
  await expect(form.getByRole('alert')).toBeVisible()
  await expect(page.getByText(direccion)).toHaveCount(0)

  // Corregida la ventana, el pedido se guarda y aparece en la lista.
  await form.getByLabel('Ventana: inicio').fill('2026-12-01T09:00')
  await form.getByLabel('Ventana: fin').fill('2026-12-01T14:00')
  await form.getByRole('button', { name: 'Guardar pedido' }).click()
  await expect(page.getByText(direccion).first()).toBeVisible()
})
