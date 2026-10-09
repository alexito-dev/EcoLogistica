# 02. Artefactos Jira

[← Volver al README Principal](../../README.md)

## Metadatos

| Campo | Valor |
|---|---|
| Proyecto | EcoLogística Huancayo |
| Herramienta | Atlassian Jira Software — Scrum |
| Versión del entregable | 1.10.0 (sin versión de entrega creada en Jira al 09/10/2026) |
| Fecha de actualización | 09 de octubre de 2026 |
| Responsable de configuración | Isidro Casio, Jose Luis |
| Clave del proyecto en Jira | `ECO` |
| Estado observado | Jira contiene 8 épicas, 9 historias y 3 tareas. `ECO board` (id. 2) tiene el Sprint 1 oficial cerrado, un sprint inicial renombrado como duplicado y el Sprint 2 activo (id. 37); no hay versión de entrega. |

## 1. Configuración observada en Jira al 09/10/2026

| Elemento | Configuración |
|---|---|
| Proyecto / tablero | `EcoLogística Huancayo` / `ECO board` (id. 2; tablero administrado por el equipo) |
| Jerarquía | Epic → Story / Task → Sub-task; Bug para incidencias |
| Columnas del tablero | 5: `Por hacer`, `En curso`, `Listo`, `In Review / QA`, `Done`. Jira mapea `Listo` al estado de categoría completada; `Done` apunta a `Finalizada`, cuya categoría figura como nueva. Persisten la mezcla de idiomas y el mapeo incoherente. |
| Versiones de entrega | Ninguna: la consulta de versiones de `ECO` devolvió 0 resultados el 09/10/2026. |
| Sprints | Sprint id. 3, cerrado y renombrado `ECO Sprint 1 (duplicado)`; Sprint 1 oficial id. 36, cerrado administrativamente el 09/10 con fechas de trabajo 14/09–28/09; Sprint 2 id. 37, activo del 29/09 al 12/10 (hora de Lima). |
| Resultado del Sprint 1 (id. 36) | El informe del sprint registra 0 de 2 al corte planificado del 28/09. Jira lo mantuvo activo hasta el 09/10 a las 07:42 (Lima). El historial de ECO-9 muestra `Listo` el 02/10, luego `Por hacer` al cerrar el Sprint 1 y otra vez `Listo` a las 07:43 al añadirse también al Sprint 2; ECO-15 sigue `Por hacer`. La métrica dinámica de Jira cuenta 1 de 2 porque ECO-9 conserva asociación con ambos sprints; no equivale a la velocidad del Sprint 1 al 28/09. |
| Sprint 2 (id. 37) | Meta: Planificación inicia sesión con MFA, registra y consulta pedidos y los conserva después de reiniciar la API. Incluye ECO-9 / HU-001 (5 puntos), ECO-16 / persistencia de pedidos y ubicaciones (3 puntos) y ECO-20 / MFA (sin estimación aprobada ni persona asignada); las tres están `Listo`. El sprint continúa activo hasta el 12/10. Ver [Informe de estado del Sprint 2](../03%20Implementaci%C3%B3n/Sprint%202/01%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md). |

La evidencia actual de sprints se consultó y regularizó en Jira el 09/10/2026. El historial de Jira se leyó para ECO-9 y ECO-15: ECO-9 cambió de estado tres veces entre el 02/10 y el 09/10; ECO-15 se reabrió al cerrar el Sprint 1 y permanece en `Por hacer`. ECO-20 se creó y marcó `Listo` el 09/10, sin persona asignada ni estimación aprobada. Después se actualizó ECO-9 para incluir la persistencia tras reiniciar, ECO-16 se acotó a pedidos y ubicaciones y se incorporó al Sprint 2 en `Listo`; ECO-21 registra el resto de EN-005, aún sin estimación ni sprint. ECO-15 sigue sin re-enrutamiento en el código. El informe dinámico actual del Sprint 1 no se usa para reconstruir la velocidad al cierre planificado.

> **Línea base funcional posterior acordada el 09/10/2026:** este documento conserva el estado de Jira consultado ese día; Jira aún refleja el alcance anterior. La distribución funcional vigente en la documentación oficial del repositorio conserva MFA/roles y pedidos persistentes en Sprint 1, asigna gestión de flota a Sprint 2 y generación/consulta de rutas a Sprint 3, y conserva el propósito de los sprints posteriores. El E2E de flota aprobó 5/5 criterios en la aplicación; no actualizó tarjetas, estimaciones, responsables ni estados de Jira. ECO-12/HU-003 y ECO-19/HU-009 siguen `Por hacer` en Jira aunque el código ya implementa el alcance de flota. ECO-21 debe ajustarse en el Planning para dejar cuentas/TOTP y rutas, sin volver a mover flota a Sprint 3.

## 2. Épicas y backlog priorizado

> Las claves `ECO-#` son las reales verificadas en el proyecto Jira del equipo el 11 de septiembre de 2026. La columna "En Jira" indica si el ítem ya existe como tarjeta creada o si todavía está solo en esta especificación.

| Prioridad | Tipo | ID interno | Clave Jira | Resumen | Story Points | En Jira |
|---:|---|---|---|---|---:|:---:|
| 1 | Epic | EP-01 | ECO-1 | Gestión de pedidos y ventanas horarias | — | ✅ |
| 2 | Story | HU-001 | ECO-9 | Registrar pedido con ventana horaria | 5 | ✅ |
| 3 | Story | HU-002 | ECO-11 | Consultar pedidos geocodificados | 3 | ✅ |
| 4 | Story | HU-008 | ECO-18 | Importar pedidos por plantilla | 3 | ✅ |
| 5 | Epic | EP-02 | ECO-2 | Gestión de flota y conductores | — | ✅ |
| 6 | Story | HU-003 | ECO-12 | Registrar vehículos y capacidades | 5 | ✅ |
| 7 | Story | HU-009 | ECO-19 | Parametrizar restricciones vehiculares | 5 | ✅ |
| 8 | Epic | EP-03 | ECO-3 | Motor de optimización VRPTW y Green VRP | — | ✅ |
| 9 | Story | HU-004 | — | Generar ruta VRPTW/Green VRP | 8 | ⬜ |
| 10 | Task | EN-001 | — | Benchmark del motor ≤45 s | 5 | ⬜ |
| 11 | Epic | EP-04 | ECO-4 | Visor cartográfico de rutas | — | ✅ |
| 12 | Story | HU-005 | ECO-13 | Visualizar ruta en mapa | 3 | ✅ |
| 13 | Story | HU-010 | — | Reportar y consultar estados de entrega | 5 | ⬜ |
| 14 | Epic | EP-05 | ECO-5 | Dashboard analítico y sostenibilidad | — | ✅ |
| 15 | Story | HU-007 | ECO-14 | Consultar KPIs y reducción de CO₂ | 5 | ✅ |
| 16 | Story | HU-011 | — | Comparar ruta optimizada contra línea base manual | 5 | ⬜ |
| 17 | Task | EN-003 | — | Protección de datos y auditoría | 3 | ⬜ |
| 18 | Task | EN-004 | — | Hardening OWASP Top 10 | 8 | ⬜ |
| 19 | Epic | EP-06 | ECO-6 | Re-enrutamiento dinámico | — | ✅ |
| 20 | Story | HU-006 | ECO-15 | Reenrutar ruta ante incidencia | 5 | ✅ |
| 21 | Task | EN-002 | — | Disponibilidad y recuperación del servicio | 5 | ⬜ |
| 22 | Epic | EP-07 | ECO-8 | Plataforma técnica y calidad | — | ✅ |
| 23 | Task | EN-005 | ECO-16 | Persistir pedidos y ubicaciones en PostgreSQL/PostGIS | 3 | ✅ |
| 24 | Task | EN-005 | ECO-21 | Completar EN-005 para usuarios, flota y rutas | Sin estimar | ✅ |
| 25 | Task | EN-006 | ECO-17 | Configurar CI/CD, pruebas y documentación OpenAPI | 5 | ✅ |
| 26 | Historia técnica | RF-11.1 | ECO-20 | Autenticación MFA y autorización por rol | — | ✅ |

Jira devuelve ocho tarjetas de tipo Epic, pero `ECO-7` repite la épica de re-enrutamiento registrada como `ECO-6`. La línea base del proyecto contiene siete épicas lógicas (EP-01–EP-07); `ECO-7` no se cuenta como una épica adicional hasta que se aclare o corrija en Jira.

Los puntos de los ítems con estimación marcada corresponden a los valores consultados en Jira; EN-005 y EN-006 tienen 3 y 5 puntos. ECO-20 existe en Jira, pero no tiene estimación aprobada ni persona asignada al corte actual. Los ítems ⬜ no están creados; sus puntos son propuestas de planificación, no compromisos del equipo. La prioridad combina valor de negocio, dependencia y riesgo técnico; los criterios BDD están en [01 Transformando a ágil](01%20Transformando%20a%20%C3%A1gil%20V_1_0_0.md).

> **Resuelto el 18 de septiembre de 2026:** `ECO-18` y `ECO-19` habían sido creados como duplicados literales de `ECO-11` y `ECO-12` (mismo título y misma épica EP-01). Se renombraron en Jira a HU-008 "Importar pedidos por plantilla" y HU-009 "Parametrizar restricciones vehiculares" respectivamente, completando así los 8 épicas + 10 historias/tareas reales del backlog.
>
> **Resuelto el 02/10/2026:** `ECO-19` (HU-009, restricciones vehiculares) está asignado a `EP-02 Gestión de flota y conductores`, como `ECO-12`. La relación actual se confirmó en Jira el 09/10/2026.

## 3. Roadmap y alcance real de los sprints 1 y 2

| Sprint / periodo | Compromiso o replanificación | Resultado / estado |
|---|---|---|
| Sprint 1 — 14/09 a 28/09/2026 | Compromiso histórico: ECO-9 / HU-001 y ECO-15 / HU-006; 10 puntos. Alcance funcional vigente: MFA/roles y pedidos persistentes. | El informe del sprint registra 0 de 2 historias al corte del 28/09. Jira lo mantuvo activo hasta el 09/10; el historial de ECO-9 registra `Listo` el 02/10, `Por hacer` al cerrar el Sprint 1 y `Listo` otra vez tras añadirla al Sprint 2. La métrica dinámica actual la cuenta en ambos sprints y no equivale a la del corte original. ECO-15 está `Por hacer`. |
| Sprint 2 — 29/09 a 12/10/2026 | Meta conservada en Jira: MFA y pedidos persistentes. Alcance funcional vigente: gestión de flota. | Jira id. 37 está activo con ECO-9 (5 puntos), ECO-16 (3 puntos) y ECO-20 (MFA, sin estimación aprobada ni persona asignada); las tres están `Listo`. Tras el rebase funcional, la aplicación de flota pasó E2E 5/5 criterios el 09/10; el resultado no cambia esos estados externos. |
| Sprint 3 — propuesta funcional, sin compromiso aprobado | Que Planificación asigne pedidos pendientes a vehículos elegibles y obtenga una ruta factible, guardada y consultable con sus paradas. | Flota y su persistencia ya son entrada disponible desde Sprint 2. Quedan persistencia de rutas/paradas, generación, integración y medición; falta estimar y acordar las historias antes de cargarlas como compromiso en Jira. |
| Sprint 4 — propuesta, sin alcance detallado aprobado | Que Conducción consulte su ruta, marque una entrega y reporte una incidencia para revisión de Planificación. | Confirmar el flujo con el equipo. Mapa y re-enrutamiento se incorporan si hacen falta para completar la tarea. No se asignan fechas ni resultados no aprobados. |
| Cierre — semana 15 | Entrega y sustentación del PMV. | Hito planificado para la semana de cierre; sin evidencia de aceptación a la fecha de esta actualización. |
| Release `v1.0.0-MVP` | Integración y aceptación del PMV. | No existe una versión de Jira con este nombre al 09/10/2026. |

La planificación original asignaba flota y optimización a Sprint 2; una replanificación posterior priorizó HU-001 y MFA. Después se acordó una nueva línea base funcional: Sprint 1 conserva el incremento actual de MFA/roles y pedidos, Sprint 2 se dedica a flota y Sprint 3 a rutas. El rebase mueve flota fuera del alcance propuesto de Sprint 3. Jira aún refleja el objetivo anterior y debe alinearse en el Planning, sin inventar estimación ni responsable.

El orden propuesto se guía por tareas completas de usuario, no por componentes técnicos sueltos. El estado comprobado y los límites del incremento del Sprint 2, más las propuestas funcionales posteriores, están detallados en [05. Plan funcional de sprints](05%20Plan%20funcional%20de%20sprints.md).

## 4. Evidencias del proyecto Jira `ECO`

Las imágenes 01–04 son capturas históricas del 18/09/2026 y describen el estado de Jira en esa fecha. No sustituyen la consulta directa del 09/10/2026, cuyos resultados se resumen en las secciones 1 y 3.

**Evidencia 1 — Roadmap:** las 8 épicas ubicadas en la línea de tiempo, con "ECO Sprint 1" marcado en septiembre.

![Roadmap del proyecto ECO](../../assets/jira/01-roadmap.png)

**Evidencia 2 — Backlog:** ítems pendientes con Story Points y épica asignada.

![Backlog del proyecto ECO](../../assets/jira/02-backlog.png)

**Evidencia 3 — Sprint Planning:** Sprint 1 activo (14–28 sep), con su Sprint Goal real y las 2 historias cargadas (ECO-9, ECO-15 = 10 puntos).

![Sprint Planning del Sprint 1](../../assets/jira/03-sprint-planning.png)

**Evidencia 4 — Tablero Scrum:** tarjetas del Sprint 1 en la columna "Por hacer".

![Tablero Scrum del Sprint 1](../../assets/jira/04-tablero-scrum.png)

**Evidencia 5 — Versiones:** no hay versión configurada en Jira al 09/10/2026 (`getJiraProjectVersions` devolvió cero resultados). La imagen que originalmente se guardó como `05-releases.png` contiene un resumen analítico del proyecto, no la pantalla de Versiones; por ello no se presenta como evidencia de un release.

![Resumen analítico histórico del proyecto ECO](../../assets/jira/05-resumen-analitico-historico.png)

La configuración actual todavía muestra cinco columnas con idiomas mezclados y un mapeo inconsistente: `Listo` está asociado a categoría completada, mientras `Done` está asociado a `Finalizada`, cuya categoría Jira informa como nueva. Este pendiente se mantiene separado de la regularización de sprints.

## 5. Checklist de configuración

- [x] Proyecto ECO, ocho épicas, nueve historias y dos tareas consultadas el 09/10/2026.
- [ ] Aclarar o corregir `ECO-7`, que duplica la tarjeta de épica `ECO-6`; conservar siete épicas lógicas EP-01–EP-07.
- [x] HU-009 / ECO-19 asociada a EP-02 y HU-003 / ECO-12 asociada a EP-02.
- [x] Resolver la duplicidad de sprints: cerrar el Sprint 1 id. 36 el 09/10 y renombrar el sprint id. 3 como duplicado.
- [x] Crear y cargar el Sprint 2 id. 37; registrar la historia técnica ECO-20 para MFA, sin inventar una estimación.
- [x] Revisar ECO-15: devolverla a `Por hacer` por falta de implementación de re-enrutamiento demostrable.
- [ ] Completar las historias y tareas ausentes: HU-004, HU-010, HU-011 y EN-001 a EN-004; confirmar prioridades y puntos con el equipo.
- [ ] Corregir el flujo de cinco columnas y validar las categorías de los estados `Listo` y `Done`.
- [ ] Crear y documentar la versión `v1.0.0-MVP` cuando el alcance de aceptación esté acordado.
- [ ] Sustituir las capturas históricas por evidencias actuales del roadmap, backlog, sprints, tablero y versión.

## 6. Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 11/09/2026 | Primera emisión del backlog y configuración de Jira. |
| 1.0.1 | 18/09/2026 | Verificación en el proyecto real, resolución de duplicados `ECO-18`/`ECO-19`, recreación del Sprint 1 y evidencias 1–4. |
| 1.1.0 | 02/10/2026 | Se documenta el cierre planificado del Sprint 1 al 28/09 y las correcciones comunicadas ese día para `ECO-19`; Jira continuaba activo al momento de esta versión. |
| 1.2.0 | 09/10/2026 | Auditoría inicial de solo lectura del tablero, sprints, estados, puntos, versiones y descripciones. |
| 1.3.0 | 09/10/2026 | Cierre administrativo del Sprint 1, identificación del duplicado, creación del Sprint 2 y ECO-20, corrección de ECO-15 y lectura posterior para verificar el estado final. |
| 1.4.0 | 09/10/2026 | Se distingue el resultado del Sprint 1 al 28/09 de la métrica dinámica actual de Jira, que cuenta ECO-9 como completada después de ese corte. |
| 1.5.0 | 09/10/2026 | Se incorpora el historial de cambios de estado de ECO-9 y la reapertura de IMP-003 tras comprobar columnas y versiones en la configuración actual de Jira. |
| 1.6.0 | 09/10/2026 | Se registra que ECO-20 sigue sin persona asignada ni estimación aprobada en Jira al corte actual. |
| 1.7.0 | 09/10/2026 | Se alinea el estado de ECO-20 sin asignación ni estimación en la planificación y el historial de impedimentos del Sprint 2. |
| 1.8.0 | 09/10/2026 | Se describe el trabajo futuro como tareas completas del sistema y se enlaza el plan funcional; Sprint 3 y 4 siguen sujetos a acuerdo del equipo. |
| 1.9.0 | 09/10/2026 | Se refleja en Jira y en este inventario la meta funcional actualizada, ECO-16 completada para pedidos y ECO-21 creada para el resto de EN-005. |
| 1.10.0 | 09/10/2026 | Se alinea la línea base documental a Sprint 1 MFA/pedidos, Sprint 2 flota y Sprint 3 rutas; se deja claro que Jira conserva sus asignaciones anteriores. |
