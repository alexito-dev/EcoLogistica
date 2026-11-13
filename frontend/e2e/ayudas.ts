import { createHmac } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import { expect, type Page } from '@playwright/test'

export const CLAVE_DEMO = 'Clave-E2E-solo-pruebas-1'
const BASE32 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'

/** Código TOTP (RFC 6238, SHA-1, 6 dígitos, 30 s) para la clave base32 que muestra el enrolamiento. */
export function totp(claveBase32: string, ahora = Date.now()): string {
  let bits = ''
  for (const c of claveBase32.replace(/[\s=]/g, '').toUpperCase()) bits += BASE32.indexOf(c).toString(2).padStart(5, '0')
  const clave = Buffer.from(bits.match(/.{8}/g)!.map((b) => parseInt(b, 2)))
  const contador = Buffer.alloc(8)
  contador.writeBigUInt64BE(BigInt(Math.floor(ahora / 1000 / 30)))
  const hmac = createHmac('sha1', clave).update(contador).digest()
  const o = hmac[hmac.length - 1] & 0xf
  const n = ((hmac[o] & 0x7f) << 24) | (hmac[o + 1] << 16) | (hmac[o + 2] << 8) | hmac[o + 3]
  return String(n % 1_000_000).padStart(6, '0')
}

/** Secretos TOTP y último paso usado, en disco: sobreviven al reinicio del proceso de pruebas tras un fallo. */
interface Estado {
  secretos: Record<string, string>
  ultimoPaso: Record<string, number>
}
const archivo = () => join(process.env.ECO_E2E_DIR!, 'autenticadores.json')
function leer(): Estado {
  return existsSync(archivo()) ? (JSON.parse(readFileSync(archivo(), 'utf8')) as Estado) : { secretos: {}, ultimoPaso: {} }
}
function guardar(estado: Estado) {
  mkdirSync(process.env.ECO_E2E_DIR!, { recursive: true })
  writeFileSync(archivo(), JSON.stringify(estado))
}

/** Ingresa con correo + contraseña + TOTP; el primer ingreso de cada cuenta enrola su autenticador. */
export async function iniciarSesion(page: Page, usuario: 'planificador' | 'conductor' | 'admin' | 'gerente' | 'auditor') {
  const correo = `${usuario}@ecologistica.test`
  await page.goto('/')
  await page.getByLabel('Correo').fill(correo)
  await page.getByLabel('Contraseña', { exact: true }).fill(CLAVE_DEMO)
  await page.getByRole('button', { name: 'Continuar' }).click()

  const estado = leer()
  if (!estado.secretos[correo]) {
    estado.secretos[correo] = await page.getByLabel('Clave para ingreso manual').innerText()
  }
  // Un código ya usado se rechaza (un solo uso): si cae en la misma ventana de 30 s, se espera la siguiente.
  const ultimo = estado.ultimoPaso[correo]
  let ahora = Date.now()
  if (ultimo !== undefined && Math.floor(ahora / 30000) <= ultimo) {
    ahora = (ultimo + 1) * 30000 + 500
    await page.waitForTimeout(Math.max(0, ahora - Date.now()))
  }
  estado.ultimoPaso[correo] = Math.floor(ahora / 30000)
  guardar(estado)
  await page.getByLabel('Código de verificación').fill(totp(estado.secretos[correo], ahora))
  await page.getByRole('button', { name: /Activar y entrar|Verificar y entrar/ }).click()
  await expect(page.getByRole('button', { name: 'Cerrar sesión' })).toBeVisible()
}

export async function cerrarSesion(page: Page) {
  await page.getByRole('button', { name: 'Cerrar sesión' }).click()
  await expect(page.getByRole('heading', { name: 'Iniciar sesión' })).toBeVisible()
}

export async function irA(page: Page, vista: string) {
  await page.getByRole('navigation', { name: 'Navegación principal' }).getByRole('button', { name: vista }).click()
}
