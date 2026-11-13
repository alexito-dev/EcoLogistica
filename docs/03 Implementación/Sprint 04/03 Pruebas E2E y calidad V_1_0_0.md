# Pruebas E2E con Playwright y control de calidad — Sprint 4

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Fecha | 13/11/2026 |
| Tarjeta | ECO-27 (E2E Playwright y CI) |
| Guía | Semana 13 — Playwright (`npm init playwright@latest`, prueba E2E de una transacción) |

## 1. Qué se automatizó

Las pruebas viven en [`frontend/e2e/`](../../../frontend/e2e/) y se configuran en [`frontend/playwright.config.ts`](../../../frontend/playwright.config.ts). Levantan la **API real** (FastAPI con datos de demostración y archivos temporales; `DATABASE_URL` vacío para no tocar nunca una base real) y la interfaz, y operan un navegador real. Las cuentas se enrolan por el flujo verdadero de MFA: el guion lee la clave que muestra la pantalla y calcula el código TOTP (RFC 6238).

| Prueba | Qué recorre |
|---|---|
| `sprint4-conduccion` · transacción completa | Planificación guarda las rutas del día y asigna conductor a cada vehículo → Conducción abre «Mi ruta», sale hacia una parada, marca entregado, reporta una incidencia con descripción → Planificación ve la incidencia, la reprograma y reoptimiza las paradas pendientes |
| `sprint4-conduccion` · permisos | Un conductor solo ve «Mi ruta» en el menú |
| `verde` | Compresión Brotli/Gzip del listado, paginación de 12 y revalidación con `If-None-Match` en Chrome real |
| `accesibilidad` | axe-core en 6 vistas × 2 temas; zoom 200 %; espaciado de texto; foco no oculto; segunda vía de navegación; cierre con `Esc` del globo del mapa |

Resultado local del 13/11/2026: **10 de 10 aprobadas** en Google Chrome (≈ 4 min; el tiempo lo domina la espera de la siguiente ventana TOTP de 30 s, porque un código no puede reutilizarse).

## 2. Ejecución

```powershell
Push-Location frontend
npm.cmd ci
npx.cmd playwright test          # abre API (puerto 8000) y UI (puerto 3000); requiere Python con backend/requirements.txt
npx.cmd playwright show-report   # informe HTML
Pop-Location
```

Localmente se usa el Chrome instalado (`channel: 'chrome'`); en CI, el Chromium que instala `npx playwright install --with-deps chromium`.

## 3. Integración continua

El archivo [`.github/workflows/ci.yml`](../../../.github/workflows/ci.yml) tiene ahora el trabajo `e2e`, junto con `backend`, `migraciones`, `frontend`, `openspec` y `cobertura-integral`. [`green-audit.yml`](../../../.github/workflows/green-audit.yml) audita rendimiento con Lighthouse CI. **Ambos flujos se ejecutaron en GitHub Actions el 13/11/2026 sobre el commit `1d57b0d` y concluyeron con éxito** ([CI](https://github.com/alexito-dev/EcoLogistica/actions/runs/43453357665), [Green IT](https://github.com/alexito-dev/EcoLogistica/actions/runs/43453357841)); el informe de Playwright y los informes de cobertura quedan como artefactos del CI.

## 4. Conjunto de pruebas al corte

| Capa | Aprobadas | Omitidas | Observación |
|---|---:|---:|---|
| Backend (pytest) | 191 | 9 | Las omitidas son de PostgreSQL/PostGIS (`ECO_TEST_DATABASE_URL`); corren en CI |
| Frontend (Vitest) | 127 | 0 | |
| E2E (Playwright) | 10 | 0 | |

## 5. Límites

- Las pruebas E2E usan la API con repositorios en memoria y archivos: **no** ejercitan PostgreSQL. Esa capa la cubren las pruebas de integración del job `cobertura-integral`.
- No existe despliegue continuo ni entorno de pruebas alojado; E2E corre contra servidores locales efímeros.
- No se midió cobertura de las pruebas E2E.
