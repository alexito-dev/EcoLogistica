# Revisión del sprint

[← Volver al README principal](../../../README.md#93-fase-03-implementación)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla

**Líder del Proyecto:** Zorrilla Apumayta, Alex Jesus

## Historias de Usuario completadas en este Sprint

Alcance del Sprint 4 (Inspección 5): que Conducción consulte su ruta, marque el avance de las entregas y reporte incidencias para que Planificación actúe, y que cada cambio se compruebe y publique de forma automática. Los commits de cierre son los de la rama `sprint-4/cierre-inspeccion-5` y los del Sprint 4 ya integrados: [`1d57b0d`](https://github.com/alexito-dev/EcoLogistica/commit/1d57b0d), [`3bee0be`](https://github.com/alexito-dev/EcoLogistica/commit/3bee0be), [`ac59b73`](https://github.com/alexito-dev/EcoLogistica/commit/ac59b73), [`e1d961f`](https://github.com/alexito-dev/EcoLogistica/commit/e1d961f), [`003b5a7`](https://github.com/alexito-dev/EcoLogistica/commit/003b5a7) y [`5f750bf`](https://github.com/alexito-dev/EcoLogistica/commit/5f750bf).

| Código | Título | Criterios de aceptación verificados | Enlace de cierre y evidencia |
|---|---|---|---|
| HU-005 / ECO-13 | Ver mi ruta en el mapa (Conducción) | La persona conductora solo ve la ruta asignada, con paradas numeradas en orden y mapa | [`1d57b0d`](https://github.com/alexito-dev/EcoLogistica/commit/1d57b0d); `GET /api/v1/conduccion/mi-ruta`; [`sprint4-conduccion.spec.ts`](../../../frontend/e2e/sprint4-conduccion.spec.ts) |
| HU-010 | Marcar el avance de cada entrega | Marca `En ruta`, `Entregado`, `Incidencia` o `Cancelado`; los cambios quedan como eventos inmutables y el estado del pedido se actualiza; las transiciones inválidas responden 422 | [`1d57b0d`](https://github.com/alexito-dev/EcoLogistica/commit/1d57b0d); `POST /conduccion/paradas/{id}/estado`; pruebas en [`backend/tests/conduccion/`](../../../backend/tests/conduccion/) |
| HU-006 / ECO-15 | Atender incidencias y reorganizar la ruta | Planificación ve la incidencia con su descripción, la reprograma con confirmación y reoptimiza solo lo pendiente sin mover lo ya atendido | [`1d57b0d`](https://github.com/alexito-dev/EcoLogistica/commit/1d57b0d); `GET /conduccion/seguimiento`, `POST /conduccion/reoptimizar` |
| ECO-14 / ECO-26 | Indicadores con entregas reales | Puntualidad observada, cumplimiento, incidencias, recorrido y CO₂e solo con avances registrados; sin entregas no se muestran porcentajes | [`3bee0be`](https://github.com/alexito-dev/EcoLogistica/commit/3bee0be) |
| ECO-18 | Importar pedidos por plantilla CSV | Plantilla descargable; importación de todo o nada con errores por fila y columna | [`ac59b73`](https://github.com/alexito-dev/EcoLogistica/commit/ac59b73) |
| ECO-21 | Cuentas y rutas en PostgreSQL con TOTP cifrado | Migración con cinco tablas nuevas aplicada, revertida y reaplicada en PostGIS; secretos TOTP cifrados con Fernet | [`1d57b0d`](https://github.com/alexito-dev/EcoLogistica/commit/1d57b0d); [ejecución de CI](https://github.com/alexito-dev/EcoLogistica/actions/runs/43453357665) |
| ECO-24 | Accesibilidad WCAG 2.2 AA | 45/45 criterios verificados con pruebas en navegador y `axe-core` en todas las vistas | [`1d57b0d`](https://github.com/alexito-dev/EcoLogistica/commit/1d57b0d); [documento 06](06%20Accesibilidad%20WCAG%202.2%20V_1_0_0.md) |
| ECO-27 | Pruebas E2E con Playwright en tres navegadores | Chromium, Firefox y WebKit ejecutan los flujos críticos: acceso con MFA, rol, validación de formularios y recorrido de Conducción | [`003b5a7`](https://github.com/alexito-dev/EcoLogistica/commit/003b5a7), [`5f750bf`](https://github.com/alexito-dev/EcoLogistica/commit/5f750bf); [`playwright.config.ts`](../../../frontend/playwright.config.ts); [documento 03](03%20Analisis%20PlayWrigth%20V_1_0_0.md) |
| EN-006 / ECO-17 | CI/CD en tres flujos independientes | `ci.yml`, `tests.yml` y `deploy-production.yml` con GitHub Secrets; reportes guardados como artefactos | [`003b5a7`](https://github.com/alexito-dev/EcoLogistica/commit/003b5a7); [`.github/workflows/`](../../../.github/workflows/) |
| Inspección 04 | Rendimiento móvil (Green IT) | FCP 0,92 s, LCP 1,22 s, TBT 41 ms, CLS 0; carga de 1 211 513 B a 41 872 B (−96,5 %) | [`4349948`](https://github.com/alexito-dev/EcoLogistica/commit/4349948), [`e1d961f`](https://github.com/alexito-dev/EcoLogistica/commit/e1d961f); [informe Green IT](../reduccion%20del%20impacto%20ambiental/01%20Informe%20de%20reduccion%20del%20impacto%20ambiental%20V_1_1_0.md) |
| Sin tarjeta (nuevo) | Monitoreo de rendimiento y disponibilidad | Web Vitals y tiempos de API por debajo de 500 ms; códigos 200/401/404/405 y fallos 500/503 informados sin romper la interfaz; sonda `GET /health` | [`003b5a7`](https://github.com/alexito-dev/EcoLogistica/commit/003b5a7); [`rendimiento.spec.ts`](../../../frontend/e2e/rendimiento.spec.ts), [`disponibilidad.spec.ts`](../../../frontend/e2e/disponibilidad.spec.ts) |
| Sin tarjeta (nuevo) | Evaluación de usabilidad SUS y heurística | Script de cálculo SUS con grado A–F (26 pruebas) y evaluación heurística de Nielsen con correcciones aplicadas | [`003b5a7`](https://github.com/alexito-dev/EcoLogistica/commit/003b5a7), [`ac59b73`](https://github.com/alexito-dev/EcoLogistica/commit/ac59b73); [documento 04](04%20Usabilidad%20V_1_0_0.md) |

**Definition of Done aplicada:** código en la rama, pruebas automáticas en verde, `ruff`, `oxlint`, `tsc -b` y compilación sin errores, y comprobación en GitHub Actions. Resultado de la verificación: ver la sección 2 del [documento 05](05%20Deuda%20cerrada%20y%20verificaci%C3%B3n%20del%20Sprint%204%20V_1_0_0.md) y el [análisis Playwright](03%20Analisis%20PlayWrigth%20V_1_0_0.md#22-resultados-de-ejecución).

## Demostración del trabajo completado

- **Entorno utilizado:** local, con la API y el build de producción de la interfaz levantados con datos de demostración (`scripts\iniciar-demo.ps1`) y, para la comprobación automática, por Playwright. Todavía no existe un entorno de *staging* ni de producción activo: `deploy-production.yml` está implementado, pero necesita un servicio de alojamiento y sus secretos.
- **Funcionalidades exhibidas** (recorrido de ocho pasos): Planificación revisa los pedidos, guarda las rutas del día y asigna conductor; Conducción abre «Mi ruta», marca una entrega como entregada y reporta una incidencia; Planificación ve la incidencia, la reprograma con confirmación; Indicadores muestra los «Resultados observados». Después se muestran los flujos de GitHub Actions y el informe HTML de Playwright.
- **Evidencias:** capturas del recorrido en [`evidencias/`](evidencias/) (archivos `demo-01` a `demo-08`) y de los informes HTML de Playwright en [Chromium](evidencias/informe-playwright-chromium.png) y [WebKit](evidencias/informe-playwright-webkit.png).
- **Retroalimentación recibida:** la demostración formal ante el docente se realiza en la exposición del 20/11/2026 (14:40–15:00). Hasta la fecha de este documento no consta una sesión con las personas de Planificación y Conducción de DistriRápido S.A.C., por lo que no se registran asistentes, acuerdos ni acta. La retroalimentación obtenida se agregará en la versión 1.1.0 de este documento.

## Pendientes

| Pendiente | Estado y justificación | Tratamiento posterior |
|---|---|---|
| Despliegue a producción con URL operativa | Flujo listo; falta crear el servicio de alojamiento y definir `DEPLOY_HOOK_BACKEND`, `DEPLOY_HOOK_FRONTEND`, `PRODUCTION_URL` y `PRODUCTION_API_URL` | Acción 2 de la [Retrospectiva](02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md#acciones-a-realizar); luego medir disponibilidad en el entorno desplegado |
| Puntuación SUS | Sin respuestas de personas usuarias (**n = 0**): no se estima ni se inventa | Acción 3: aplicar la encuesta a 5 o más personas y publicar el documento 04 en versión 1.1.0 |
| Firefox en la máquina de desarrollo | No arranca localmente (falta el runtime de Visual C++); se verifica en GitHub Actions | Opcional: instalar el runtime para reproducirlo localmente |
| SonarQube en CI | Se activa solo con `SONAR_TOKEN` y `SONAR_HOST_URL` | Acción 4 |
| Protección de `main` y revisión por pares | Deuda desde el Sprint 3 | Acción 5 |
| HU-011 (comparar ruta optimizada con la línea base manual) | No implementada: no hay datos de línea base acordados | Backlog |
| EN-001 completo (motor VRPTW) | El re-enrutamiento usa una heurística acotada (vecino más cercano) | Backlog; ver los [límites del Sprint 4](05%20Deuda%20cerrada%20y%20verificaci%C3%B3n%20del%20Sprint%204%20V_1_0_0.md#4-límites-y-trabajo-que-sigue-abierto) |
| Hallazgos de usabilidad H4, H5 y H9 | Requieren una regla de negocio o decisión de producto | Acción 7 |
| Tarjetas de Jira de este alcance | No creadas para parte del trabajo; sin ellas no se mide la velocidad | Acción 6 |
| Pruebas E2E con PostgreSQL | La suite E2E usa memoria y archivos temporales; PostGIS se prueba en integración | Backlog |
