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

## 5. SonarQube en la integración continua

El trabajo `cobertura-integral` de `ci.yml` incluye ahora un paso de **SonarQube con puerta de calidad** (`sonar.qualitygate.wait=true`) que lee la cobertura de Python y de TypeScript generada en el mismo trabajo y la configuración de [`sonar-project.properties`](../../../sonar-project.properties). **Solo se ejecuta si el repositorio define los secretos `SONAR_TOKEN` y `SONAR_HOST_URL`**; sin ellos se omite y el CI no falla.

Para activarlo (lo debe hacer quien administra el repositorio, porque requiere una cuenta y un token propios):

1. Crear el proyecto en SonarCloud (gratuito para repositorios públicos) o en un servidor SonarQube propio, con la clave `ecologistica`. En SonarCloud, añadir también `sonar.organization` en `sonar-project.properties`.
2. En GitHub: *Settings → Secrets and variables → Actions* y crear `SONAR_TOKEN` y `SONAR_HOST_URL` (por ejemplo `https://sonarcloud.io`).
3. Hacer un push: el paso aparecerá en el CI y bloqueará el trabajo si la puerta de calidad falla.

**Estado:** el análisis oficial con el código del Sprint 4 **todavía no se ha ejecutado** porque faltan esas credenciales; el valor de SonarQube del Sprint 3 (commit `9b31dd0`) sigue siendo el último medido. La cobertura combinada del 90 % sí se verifica en cada CI con `scripts/reporte_cobertura.py`.

## 6. Límites

- Las pruebas E2E usan la API con repositorios en memoria y archivos: **no** ejercitan PostgreSQL. Esa capa la cubren las pruebas de integración del job `cobertura-integral`.
- No existe despliegue continuo ni entorno de pruebas alojado; E2E corre contra servidores locales efímeros.
- No se midió cobertura de las pruebas E2E.
- La importación de pedidos por plantilla (ECO-18) se verifica con pruebas de API y de interfaz; no tiene recorrido E2E.
