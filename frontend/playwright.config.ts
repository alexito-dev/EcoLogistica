import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { defineConfig, devices } from '@playwright/test'

/**
 * Pruebas E2E (ECO-27, Sprint 5). Levantan la API real (FastAPI, memoria + archivos temporales, sin PostgreSQL ni
 * Docker) y la interfaz, y recorren los flujos de punta a punta en un navegador real.
 *
 * Navegadores (Sprint 5): Chromium ejecuta TODA la suite; Firefox y WebKit ejecutan los flujos críticos
 * (`criticos.spec.ts`, `sprint4-conduccion.spec.ts`) y la disponibilidad/resiliencia (`disponibilidad.spec.ts`). El monitoreo de rendimiento
 * (`rendimiento.spec.ts`) usa las API de Chromium y solo corre allí. Localmente Chromium usa el Chrome instalado;
 * en CI, el Chromium que instala Playwright.
 *
 * Contra un entorno ya desplegado (humo posterior al despliegue): ECO_BASE_URL=https://… ECO_API_URL=https://…
 * no se levanta ningún servidor local.
 */
// Una sola carpeta por ejecución, compartida con los procesos de prueba (que reevalúan este archivo).
const datos = (process.env.ECO_E2E_DIR ??= join(tmpdir(), `eco-e2e-${Date.now()}`))
const CLAVE_DEMO = 'Clave-E2E-solo-pruebas-1'
const BASE_URL = process.env.ECO_BASE_URL ?? 'http://localhost:3000'
const REMOTO = Boolean(process.env.ECO_BASE_URL)
const SOLO_CRITICOS = ['**/criticos.spec.ts', '**/disponibilidad.spec.ts', '**/sprint4-conduccion.spec.ts']

export default defineConfig({
  testDir: './e2e',
  timeout: 90_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 1 : 0,
  // En CI, el reporter «github» deja cada fallo como anotación del trabajo (título y mensaje), visible sin descargar el informe.
  reporter: [['list'], ...(process.env.CI ? [['github'] as const] : []), ['html', { open: 'never', outputFolder: 'playwright-report' }]],
  use: {
    baseURL: BASE_URL,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    locale: 'es-PE',
    timezoneId: 'America/Lima',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'], channel: process.env.CI ? undefined : 'chrome' } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] }, testMatch: SOLO_CRITICOS },
    { name: 'webkit', use: { ...devices['Desktop Safari'] }, testMatch: SOLO_CRITICOS },
  ],
  webServer: REMOTO ? undefined : [
    {
      command: 'python -m uvicorn app.main:app --app-dir src --port 8000',
      cwd: '../backend',
      url: 'http://localhost:8000/docs',
      reuseExistingServer: false,
      timeout: 60_000,
      env: {
        DATABASE_URL: '', // aislado del .env local: nunca usa una base real
        DEMO_PEDIDOS: 'true',
        DEMO_CLAVE: CLAVE_DEMO,
        JWT_SECRET: 'clave-e2e-de-firma-suficientemente-larga-0123456789',
        USUARIOS_ARCHIVO: join(datos, 'usuarios.json'),
        RUTAS_ARCHIVO: join(datos, 'rutas.json'),
        CORS_ORIGIN: 'http://localhost:3000',
      },
    },
    {
      // Se prueba el build de PRODUCCIÓN (con Preact en lugar de React), el que realmente se publica.
      command: 'npm run build && npx vite preview --port 3000 --strictPort',
      url: 'http://localhost:3000',
      reuseExistingServer: false,
      timeout: 120_000,
      env: { VITE_API_URL: 'http://localhost:8000/api/v1' },
    },
  ],
})

export { CLAVE_DEMO }
