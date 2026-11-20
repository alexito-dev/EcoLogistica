# Revisión del sprint

[← Volver al README principal](../../../README.md#93-fase-03-implementación)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla

**Líder del Proyecto:** Zorrilla Apumayta, Alex Jesus

## Metadatos del documento

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Corte | 20/11/2026 |
| Sprint | ECO Sprint 5 — CI/CD, calidad con Playwright, rendimiento, disponibilidad y usabilidad SUS |
| Rama | `sprint-5/cicd-playwright-usabilidad` |
| Plan de referencia | [05. Plan funcional de sprints](../../02%20Planificaci%C3%B3n/05%20Plan%20funcional%20de%20sprints.md#qué-tendría-que-poder-hacerse-al-terminar-sprint-5) |
| Documentos del sprint | [02 Retrospectiva](02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) · [03 Análisis Playwright](03%20Analisis%20PlayWrigth%20V_1_0_0.md) · [04 Usabilidad](04%20Usabilidad%20V_1_0_0.md) |

> **Alcance de este documento.** Registra lo implementado y verificado en el repositorio. **No** afirma el estado de las tarjetas de Jira (no se consultó desde este entorno): los identificadores existentes se citan para que el equipo las actualice, y el alcance sin tarjeta se señala como tal. Tampoco documenta reuniones, asistencia ni retroalimentación de stakeholders que no consten.

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 20/11/2026 | Hilario Talavera, Alexander Daniel | Primera emisión de la revisión del Sprint 5. |

## Historias de Usuario completadas en este Sprint

El Sprint 5 no agrega funciones nuevas para Planificación o Conducción: completa el **cierre técnico** del producto (calidad, automatización y medición). Por eso los elementos son habilitadores técnicos (EN) del backlog y no historias de usuario nuevas. Se entregan en los commits [`003b5a7`](https://github.com/alexito-dev/EcoLogistica/commit/003b5a7), [`475af1a`](https://github.com/alexito-dev/EcoLogistica/commit/475af1a) y [`5f750bf`](https://github.com/alexito-dev/EcoLogistica/commit/5f750bf) de la rama del sprint.

| Código | Título | Criterios de aceptación verificados | Evidencia |
|---|---|---|---|
| ECO-27 (continuación) | E2E con Playwright en tres navegadores | La suite corre en Chromium (24/24 pruebas), Firefox (14/14, en CI) y WebKit (14/14); flujos críticos: acceso con MFA, rol, validación de formulario y recorrido de Conducción | [`playwright.config.ts`](../../../frontend/playwright.config.ts), [`criticos.spec.ts`](../../../frontend/e2e/criticos.spec.ts); [informe](03%20Analisis%20PlayWrigth%20V_1_0_0.md#22-resultados-de-ejecución) |
| EN-006 / ECO-17 (continuación) | CI/CD en tres flujos independientes | `ci.yml` (estilo, análisis estático, compilación, dependencias, higiene), `tests.yml` (unitarias, integración PostGIS, E2E ×3 navegadores, artefactos) y `deploy-production.yml` (despliegue con GitHub Secrets tras validar); sintaxis válida y `ci.yml` en verde en GitHub Actions | [`.github/workflows/`](../../../.github/workflows/); [ejecución de CI](https://github.com/alexito-dev/EcoLogistica/actions/runs/44751813750) y [Tests](https://github.com/alexito-dev/EcoLogistica/actions/runs/44755819508) |
| Sin tarjeta (nuevo) | Monitoreo de rendimiento | TTFB 9 ms, FCP 236 ms, LCP 236 ms, CLS 0; API con p95 ≤ 34 ms (umbral 500 ms) | [`rendimiento.spec.ts`](../../../frontend/e2e/rendimiento.spec.ts); [informe, sección 3](03%20Analisis%20PlayWrigth%20V_1_0_0.md#3-monitoreo-de-rendimiento) |
| Sin tarjeta (nuevo) | Disponibilidad y resiliencia | Códigos 200/401/404/405; fallos de red, 500 y 503 informados sin romper la interfaz; sonda `GET /health` y disponibilidad 100 % en 30 sondas | [`disponibilidad.spec.ts`](../../../frontend/e2e/disponibilidad.spec.ts), [`test_salud.py`](../../../backend/tests/test_salud.py); [informe, sección 4](03%20Analisis%20PlayWrigth%20V_1_0_0.md#4-disponibilidad-y-resiliencia) |
| Sin tarjeta (nuevo) | Cálculo SUS con grado A–F | El script entrega puntaje individual, promedio, grado de Sauro y Lewis y tablas Markdown paso a paso; 26 pruebas automáticas | [`procesar_sus.py`](../../../scripts/usabilidad/procesar_sus.py), [`test_usabilidad_sus.py`](../../../backend/tests/test_usabilidad_sus.py); [documento 04](04%20Usabilidad%20V_1_0_0.md) |
| Sin tarjeta (mantenimiento) | Higiene del repositorio y trazabilidad | `.gitignore` excluye dependencias, `.env`, compilados y reportes; el CI falla si se versiona `.gitignore~`, `.env`, `node_modules` o reportes; README con *badges* de los tres flujos e índice del Sprint 5 | [`.gitignore`](../../../.gitignore), [`README.md`](../../../README.md) |
| Sin tarjeta (corrección) | Prueba rota por dependencia nueva | `pyotp` 2.12 rechaza secretos de menos de 112 bits; el test de aprovisionamiento usa uno de 160 bits (el que genera la aplicación) | [commit `003b5a7`](https://github.com/alexito-dev/EcoLogistica/commit/003b5a7) |

**Verificación local (20/11/2026):** backend 221 pruebas aprobadas y 9 omitidas (las de PostgreSQL, que requieren `ECO_TEST_DATABASE_URL` y corren en CI); frontend 134 pruebas aprobadas; `ruff`, `oxlint`, `tsc -b` y la compilación de producción sin errores; E2E 24/24 en Chromium y 14/14 en WebKit.

**Verificación en GitHub Actions** (commit `5f750bf` de la rama del sprint): [`tests.yml` en verde (44755819508)](https://github.com/alexito-dev/EcoLogistica/actions/runs/44755819508) con E2E de Chromium 24/24, Firefox 14/14 y WebKit 14/14, además de pytest con benchmark, Vitest, integración con PostGIS y cobertura integral; `ci.yml` y Green IT también en verde. La primera ejecución (`003b5a7`) falló solo en Firefox y WebKit por el recorrido de Conducción; se corrigió en `5f750bf` (ver el [análisis, sección 2.4](03%20Analisis%20PlayWrigth%20V_1_0_0.md#24-hallazgos-durante-la-construcción-de-la-suite)).

## Demostración del trabajo completado

- **Entorno:** local, con la API y el build de producción de la interfaz levantados por Playwright con datos temporales; la demostración manual usa `scripts\iniciar-demo.ps1`. **No hay entorno de *staging* ni de producción**: `deploy-production.yml` está implementado y validado sintácticamente, pero no se ha ejecutado contra un hosting real porque no existen los servicios ni los secretos.
- **Guion reproducible:**
  1. `npx playwright test --project=chromium` en `frontend/`: recorre 24 pruebas, incluido el recorrido Planificación → Conducción → incidencia → indicadores.
  2. `npx playwright show-report`: abre el informe HTML con las 24 pruebas, las trazas y las capturas.
  3. Revisar los adjuntos `web-vitals.json` y `api-tiempos.json` del informe de rendimiento.
  4. En GitHub, pestaña *Actions*: los flujos CI, Tests y Green IT de la rama.
- **Evidencias multimedia:** capturas de los informes HTML de Playwright en [Chromium](evidencias/informe-playwright-chromium.png) y [WebKit](evidencias/informe-playwright-webkit.png).
- **Retroalimentación de stakeholders:** no registrada. No consta una sesión de demostración con DistriRápido S.A.C. ni con el docente en este sprint, por lo que no se documentan asistentes ni acuerdos. Cuando se realice, se registrará en la versión 1.1.0 con el acta o la evidencia.

## Pendientes

| Pendiente | Estado y motivo | Tratamiento posterior |
|---|---|---|
| Despliegue a producción | Flujo listo; sin hosting ni secretos (`DEPLOY_HOOK_BACKEND`, `DEPLOY_HOOK_FRONTEND`, `PRODUCTION_URL`, `PRODUCTION_API_URL`) | Decisión del equipo (acción 2 de la [Retrospectiva](02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md#acciones-a-realizar)); luego verificar `/health` y la prueba de humo |
| Puntuación SUS | Sin respuestas de personas usuarias: **n = 0**, no se estima | Aplicar a ≥ 5 personas con `procesar_sus.py --markdown` (acción 3); publicar el [documento 04](04%20Usabilidad%20V_1_0_0.md) en versión 1.1.0 |
| Firefox en la máquina de desarrollo | No arranca (falta el runtime de Visual C++); se verifica en CI (14/14) | Opcional: instalar el runtime de Visual C++ para reproducirlo localmente |
| SonarQube en CI | Se activa solo con `SONAR_TOKEN` y `SONAR_HOST_URL` | Acción 4 |
| Protección de `main` y revisión por pares | Pendiente desde el Sprint 3 | Acción 5 |
| HU-011 (comparar ruta optimizada con línea base manual) | No implementada; sin tarjeta ni datos acordados | Backlog |
| EN-001 completo (motor VRPTW) | El re-enrutamiento del Sprint 4 usa una heurística acotada | Backlog; ver [Revisión del Sprint 4](../Sprint%2004/01%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md#4-límites-y-trabajo-que-sigue-abierto) |
| Hallazgos de usabilidad H4, H5 y H9 | Pendientes de regla de negocio o de producto | Acción 7 |
| Tarjetas de Jira de este alcance | No creadas; sin ellas no hay velocidad del sprint | Acción 6 |
| Pruebas E2E con PostgreSQL | La suite E2E usa memoria y archivos temporales; PostGIS se prueba solo en integración | Backlog |
