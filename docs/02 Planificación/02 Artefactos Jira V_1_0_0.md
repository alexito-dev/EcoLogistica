# 02. Artefactos Jira

[← Volver al README Principal](../../README.md)

## Metadatos

| Campo | Valor |
|---|---|
| Proyecto | EcoLogística Huancayo |
| Herramienta | Atlassian Jira Software — Scrum |
| Versión del entregable | 1.0.0-MVP |
| Fecha | 11 de septiembre de 2026 |
| Responsable de configuración | Isidro Casio, Jose Luis |
| Estado | Especificación y checklist preparados; requiere validación visual en el proyecto Jira del equipo |

## 1. Configuración objetivo

| Elemento | Configuración |
|---|---|
| Tipo de proyecto | Scrum administrado por el equipo |
| Jerarquía | Epic → Story / Task → Sub-task; Bug para incidencias |
| Flujo | To Do → In Progress → In Review / QA → Done |
| Release | `v1.0.0-MVP` |
| Sprint | Sprint 1, duración de 2 semanas |
| Sprint Goal | Publicar la primera planificación sostenible de pedidos, flota y rutas con métricas verificables y trazabilidad documental. |

## 2. Épicas y backlog priorizado

| Prioridad | Tipo | Clave | Resumen | Story Points | Componente |
|---:|---|---|---|---:|---|
| 1 | Epic | EP-01 / SCRUM-5 | Gestión de pedidos | — | Pedidos |
| 2 | Story | HU-001 | Registrar pedido con ventana horaria | 5 | Pedidos |
| 3 | Story | HU-002 | Validar y geocodificar pedido | 3 | Pedidos |
| 4 | Story | HU-008 | Importar pedidos por plantilla | 5 | Pedidos |
| 5 | Epic | EP-02 / SCRUM-6 | Flota y conductores | — | Flota |
| 6 | Story | HU-003 | Configurar vehículo y conductor | 5 | Flota |
| 7 | Story | HU-009 | Parametrizar restricciones vehiculares | 3 | Flota |
| 8 | Epic | EP-03 / SCRUM-7 | Optimización sostenible | — | Motor |
| 9 | Story | HU-004 | Generar ruta VRPTW/Green VRP | 8 | Motor |
| 10 | Task | EN-001 | Benchmark del motor ≤45 s | 5 | Motor |
| 11 | Epic | EP-04 / SCRUM-8 | Seguimiento y re-enrutamiento | — | Mapa |
| 12 | Story | HU-005 | Consultar ruta en mapa | 5 | Mapa |
| 13 | Story | HU-006 | Reoptimizar ante pedido urgente o incidencia | 8 | Mapa |
| 14 | Story | HU-010 | Reportar y consultar estados de entrega | 5 | Mapa |
| 15 | Task | EN-002 | Disponibilidad y recuperación del servicio | 5 | Mapa |
| 16 | Epic | EP-05 / SCRUM-9 | Indicadores y auditoría | — | Dashboard |
| 17 | Story | HU-007 | Consultar KPI de costo, puntualidad y CO₂ | 5 | Dashboard |
| 18 | Story | HU-011 | Comparar ruta optimizada contra línea base manual | 5 | Dashboard |
| 19 | Task | EN-003 | Protección de datos y auditoría | 3 | Dashboard |
| 20 | Task | EN-004 | Hardening OWASP Top 10 | 8 | Dashboard |

Los puntos usan Fibonacci (1, 2, 3, 5, 8, 13). La prioridad combina valor de negocio, dependencia y riesgo técnico; el detalle completo y los criterios BDD están en [01 Transformando a ágil](01%20Transformando%20a%20%C3%A1gil%20V_1_0_0.md).

## 3. Roadmap y Sprint 1

| Periodo | Entrega | Épicas |
|---|---|---|
| Sprint 1 — semanas 1–2 | Registro, validación de pedidos y configuración de flota | EP-01, EP-02 |
| Sprint 2 — semanas 3–4 | Optimización inicial y medición de rendimiento | EP-03 |
| Sprint 3 — semanas 5–6 | Mapa, seguimiento y re-enrutamiento | EP-04 |
| Sprint 4 — semanas 7–8 | Dashboard, auditoría y endurecimiento | EP-05 |
| Release v1.0.0-MVP | Integración y aceptación | EP-01 a EP-05 |

## 4. Evidencias requeridas para completar en Jira

La consigna exige recortes exclusivos del panel de Jira, sin escritorio, navegador ni espacio sobrante. Se deben insertar aquí, una vez obtenidas del proyecto Jira real, las siguientes evidencias:

1. **Evidencia 1 — Roadmap:** épicas ubicadas en la línea de tiempo.
2. **Evidencia 2 — Backlog:** orden, puntos y componentes visibles.
3. **Evidencia 3 — Sprint Planning:** Sprint 1 preparado con su Sprint Goal: MVP operativo de pedidos, flota, rutas sostenibles y seguimiento.
4. **Evidencia 4 — Tablero Scrum:** tarjetas distribuidas en To Do, In Progress, In Review / QA y Done.
5. **Evidencia 5 — Release:** `v1.0.0-MVP` y asociación de historias.

> En esta sesión no se recibió una pestaña de Jira ni capturas del proyecto ALM. Por integridad académica no se fabrican imágenes ni se afirma que la configuración haya sido ejecutada; este documento deja la parametrización lista y marca el punto exacto que debe verificarse antes de la entrega.

## 5. Checklist de configuración

- [ ] Crear proyecto Scrum `EcoLogística Huancayo`.
- [x] Crear EP-01 a EP-05 en Jira: SCRUM-5 a SCRUM-9.
- [ ] Crear HU/EN del backlog y asignar puntos Fibonacci.
- [ ] Crear versión `v1.0.0-MVP`.
- [ ] Configurar columnas del flujo indicado.
- [x] Crear Sprint 1 con duración planificada de 2 semanas y Sprint Goal.
- [ ] Asociar todas las historias al Sprint 1 y a la versión (pendiente de configuración visual de Jira).
- [ ] Capturar los cinco recortes limpios e insertarlos en este archivo.
