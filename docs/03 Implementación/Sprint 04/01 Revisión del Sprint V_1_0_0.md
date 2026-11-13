# Revisión del Sprint 4 — EcoLogística Huancayo

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Corte | 13/11/2026 |
| Rama | `sprint-4/green-it-calidad` |
| Propósito | Que Conducción consulte su ruta, marque cada entrega y reporte incidencias, y que Planificación actúe sobre ellas; cerrar la deuda de los Sprints 1–3 y la Inspección 04 (Green IT) |
| Plan de referencia | [05. Plan funcional de sprints](../../02%20Planificaci%C3%B3n/05%20Plan%20funcional%20de%20sprints.md) |

> **Alcance de este documento.** Registra lo implementado y verificado en el repositorio. **No** afirma el estado de las tarjetas de Jira (no se verificó desde este entorno): los identificadores se citan para que el equipo las actualice. Tampoco documenta reuniones, asistencia ni votaciones del equipo que no consten.

## 1. Qué debía poder hacerse y qué se comprobó

| # | Criterio del plan funcional (Sprint 4) | Resultado | Evidencia |
|---|---|---|---|
| 1 | La persona conductora solo ve la ruta asignada y consulta sus paradas en orden | Cumplido | `GET /api/v1/conduccion/mi-ruta`; `backend/tests/conduccion/test_api.py::test_conductor_ve_solo_la_ruta_asignada…`; E2E `sprint4-conduccion.spec.ts` |
| 2 | Marca `En ruta`, `Entregado`, `Incidencia` o `Cancelado` y el cambio se conserva | Cumplido | `POST /conduccion/paradas/{id}/estado`; eventos inmutables; el estado del pedido se actualiza; prueba de persistencia en PostgreSQL (`test_cuentas_rutas_conduccion.py`, se ejecuta en CI) |
| 3 | Una incidencia en ruta activa es visible para Planificación con su descripción; el re-enrutamiento conserva lo entregado | Cumplido | `GET /conduccion/seguimiento`; `POST /conduccion/reoptimizar` (idempotente, no mueve paradas atendidas) |
| 4 | Lo que no se puede reasignar se explica; no se oculta ni se cambia silenciosamente | Cumplido | Transiciones inválidas responden 422 con los estados permitidos; la incidencia exige descripción; `reprogramar` solo aplica a incidencias y conserva el historial |
| 5 | Los indicadores no se rellenan con cifras inventadas | Cumplido | Esta iteración no agrega indicadores nuevos; el avance se muestra como conteo real de eventos |

Especificación: [`openspec/specs/conduccion/spec.md`](../../../openspec/specs/conduccion/spec.md).

## 2. Deuda de los Sprints 1–3 cerrada en este sprint

| Pendiente | Tarjeta | Qué se hizo | Estado |
|---|---|---|---|
| Cuentas y rutas en archivos JSON locales | ECO-21 | Migración `20261113_01`: tablas `usuarios`, `intentos_acceso`, `rutas_guardadas`, `asignaciones_ruta`, `eventos_parada`; adaptadores PostgreSQL; se usan cuando existe `DATABASE_URL` | Implementado; **verificado por pruebas de integración que corren en CI** (no se pudo levantar PostgreSQL en la máquina de desarrollo) |
| Secretos TOTP sin cifrar en reposo | ECO-21 | Cifrado Fernet (`TOTP_CLAVE_CIFRADO`); la API exige la clave si hay base de datos; prueba que el valor guardado no contiene el secreto y que otra clave no lo descifra | Implementado |
| Accesibilidad WCAG 2.2 AA por debajo de 90 % | ECO-24 | Criterios 1.4.4, 1.4.12, 1.4.13, 2.4.5 y 2.4.11 verificados con pruebas en navegador; mapa de navegación como segunda vía; `axe-core` en todas las vistas | Verificado; ver [02 Accesibilidad](02%20Accesibilidad%20WCAG%202.2%20V_1_0_0.md) |
| E2E con Playwright y CI | ECO-27 | Suite de 9 pruebas E2E + trabajo `e2e` en `ci.yml` | Verificado localmente (9/9); pendiente la primera corrida en GitHub Actions |
| Mapa para Conducción | ECO-13 / HU-005 | Vista «Mi ruta» con mapa y paradas | Implementado |
| Estados de entrega | HU-010 | Vista «Mi ruta» y eventos de parada | Implementado |
| Reenrutamiento operativo | ECO-15 / HU-006 | Reprogramar incidencias y reoptimizar pendientes (vecino más cercano desde la última entrega) | Implementado con alcance acotado; no es el motor VRPTW completo (EN-001) |
| Optimizaciones Green IT | Inspección 04 | Ver [informe](../reduccion%20del%20impacto%20ambiental/01%20Informe%20de%20reduccion%20del%20impacto%20ambiental%20V_1_0_0.md) | Entregado |

## 3. Cómo se verificó

- **Backend:** 180 pruebas aprobadas y 8 omitidas (las de PostgreSQL/PostGIS requieren `ECO_TEST_DATABASE_URL`; corren en el job `cobertura-integral` de CI).
- **Frontend:** 125 pruebas aprobadas; `tsc -b`, linter y compilación de producción sin errores ni advertencias.
- **E2E (navegador real, API real):** 9 de 9 aprobadas, incluido el recorrido Planificación → Conducción → incidencia → Planificación.
- **Green IT:** `lhci autorun` aprobado con los umbrales de `lighthouserc.json`.

## 4. Límites y trabajo que sigue abierto

- **PostgreSQL no se ejecutó localmente:** el equipo no tenía Docker disponible. Las pruebas de integración de las tablas nuevas y los adaptadores escriben y leen en CI; hasta ver ese resultado en verde, la persistencia en PostgreSQL de este sprint debe considerarse **no verificada de extremo a extremo**.
- **Re-enrutamiento:** reordena con una heurística local; no recalcula asignación de vehículos ni reintegra pedidos reprogramados automáticamente (Planificación debe volver a guardar rutas).
- **Mi ruta** no usa geolocalización ni modo sin conexión.
- **Usabilidad (SUS y Nielsen):** se entregan instrumentos y procesamiento; **no hay resultados** porque no se aplicó la encuesta a personas usuarias. Ver [04 Usabilidad](04%20Usabilidad%20SUS%20y%20Nielsen%20V_1_0_0.md).
- **Retrospectiva, estimación y Jira:** requieren al equipo; no se redactan aquí.
- **Despliegue:** sigue sin existir despliegue continuo ni entorno productivo.
