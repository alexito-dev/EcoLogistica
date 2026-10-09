# 02. Artefactos Jira

[← Volver al README Principal](../../README.md)

## Metadatos

| Campo | Valor |
|---|---|
| Proyecto | EcoLogística Huancayo |
| Herramienta | Atlassian Jira Software — Scrum |
| Versión del entregable | 1.12.0 (sin versión de entrega creada en Jira al 09/10/2026) |
| Fecha de actualización | 09 de octubre de 2026, 13:35 hora de Lima |
| Responsable de configuración | Isidro Casio, Jose Luis |
| Clave del proyecto en Jira | `ECO` |
| Estado observado | Jira contiene 8 épicas, 9 historias y 3 tareas. `ECO board` (id. 2) tiene el Sprint 1 oficial cerrado, un sprint inicial renombrado como duplicado y el Sprint 2 activo (id. 37); no hay versión de entrega. Las metas se alinearon al rebase funcional; Sprint 2 contiene las dos historias de flota en `Listo`. |

## 1. Configuración observada en Jira al 09/10/2026

| Elemento | Configuración |
|---|---|
| Proyecto / tablero | `EcoLogística Huancayo` / `ECO board` (id. 2; tablero administrado por el equipo) |
| Jerarquía | Epic → Story / Task → Sub-task; Bug para incidencias |
| Columnas del tablero | 4: `Por hacer` → `Por hacer` (nueva); `En curso` → `En curso` (en curso); `En revisión / QA` → `En revisión / QA` (en curso); `Listo` → `Listo` (completada). La antigua columna `Done`/estado `Finalizada` se retiró; no había incidencias en ese estado. La lectura viva de `getJiraBoardConfig` confirma el orden y el mapeo. |
| Versiones de entrega | Ninguna: `getJiraProjectVersions` devolvió 0 versiones para `ECO` en la verificación viva del 09/10/2026. |
| Sprints | Sprint id. 3, cerrado y renombrado `ECO Sprint 1 (duplicado)`; Sprint 1 oficial id. 36, cerrado el 09/10, con fechas de trabajo 14/09–28/09; Sprint 2 id. 37, activo del 29/09 al 12/10 (hora de Lima). |
| Resultado del Sprint 1 (id. 36) | El informe histórico registra 0 de 2 al corte del 28/09. Jira conserva ese objetivo original y anota la rebase funcional del 09/10. La lectura dinámica actual del sprint cerrado muestra 1/2: ECO-9 `Listo` y ECO-15 `Por hacer`; esto no reconstruye la velocidad del corte. ECO-15 conserva su asociación histórica al sprint cerrado y queda pendiente de replanificación. ECO-16 y ECO-20 están completadas fuera del sprint, como habilitadores de la línea base funcional vigente; no se imputan al corte ni a la velocidad original. |
| Sprint 2 (id. 37) | Meta alineada el 09/10 a gestión de flota. Contiene ECO-12 / vehículos y capacidades (5 puntos) y ECO-19 / restricciones vehiculares (5 puntos), ambas `Listo`: 2/2 incidencias y 10 puntos estimados. El sprint permanece activo hasta el cierre administrativo previsto; la revisión del Product Owner está programada para el 09/10 a las 15:40. |

La evidencia actual de sprints se consultó y regularizó en Jira el 09/10/2026. Se conservaron las fechas y la pertenencia histórica del Sprint 1; su meta distingue el compromiso original de la rebase funcional acordada ese día. El Sprint 2 se reorientó a flota: ECO-12 y ECO-19 están en `Listo` y son sus dos incidencias actuales. ECO-9 y ECO-15 mantienen su asociación histórica al Sprint 1 cerrado; ECO-16 y ECO-20 están completadas en el backlog, fuera de ese sprint. La métrica dinámica actual de Sprint 1 es 1/2, sin reconstruir la velocidad del corte del 28/09. ECO-20 continúa sin estimación ni responsable asignados. ECO-21 contiene cuentas, secretos TOTP y persistencia de rutas, sin estimación ni sprint. ECO-15 no tiene re-enrutamiento implementado y queda pendiente de replanificación posterior. La verificación más reciente confirma Sprint 2 activo, 2/2 incidencias y 10 puntos estimados; la revisión del Product Owner continúa programada para las 15:40.

> **Rebase funcional acordado el 09/10/2026 y reflejado en Jira:** la línea base vigente conserva MFA/roles y pedidos persistentes en Sprint 1, asigna la gestión de flota a Sprint 2 y la generación/consulta de rutas a Sprint 3; los sprints posteriores mantienen su propósito. El E2E web de flota aprobó 5/5 criterios. ECO-12/HU-003 y ECO-19/HU-009 están ahora en `Listo` dentro del Sprint 2 (10 puntos combinados). Como el Sprint 1 ya estaba cerrado, ECO-16 y ECO-20 quedan completadas en el backlog, no añadidas retroactivamente a su velocidad histórica. ECO-21 conserva cuentas/TOTP/rutas pendientes; ECO-15 sigue pendiente de implementación.

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
| 24 | Task | EN-005 | ECO-21 | Completar EN-005 para usuarios y rutas | Sin estimar | ✅ |
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
| Sprint 2 — 29/09 a 12/10/2026 | Meta actualizada en Jira el 09/10: administración de vehículos y disponibilidad diaria para Planificación. | Jira id. 37 permanece activo con ECO-12 y ECO-19 en `Listo` (2/2 incidencias, 10 puntos). Los cinco criterios de flota aprobaron el E2E del 09/10. El cierre administrativo del sprint está pendiente de su fecha de revisión/cierre. |
| Sprint 3 — propuesta funcional, sin compromiso aprobado | Que Planificación asigne pedidos pendientes a vehículos elegibles y obtenga una ruta factible, guardada y consultable con sus paradas. | Flota y su persistencia ya son entrada disponible desde Sprint 2. Quedan persistencia de rutas/paradas, generación, integración y medición; falta estimar y acordar las historias antes de cargarlas como compromiso en Jira. |
| Sprint 4 — propuesta, sin alcance detallado aprobado | Que Conducción consulte su ruta, marque una entrega y reporte una incidencia para revisión de Planificación. | Confirmar el flujo con el equipo. Mapa y re-enrutamiento se incorporan si hacen falta para completar la tarea. No se asignan fechas ni resultados no aprobados. |
| Cierre — semana 15 | Entrega y sustentación del PMV. | Hito planificado para la semana de cierre; sin evidencia de aceptación a la fecha de esta actualización. |
| Release `v1.0.0-MVP` | Integración y aceptación del PMV. | No existe una versión de Jira con este nombre al 09/10/2026. |

La planificación original asignaba flota y optimización a Sprint 2; una replanificación posterior priorizó HU-001 y MFA. El 09/10 se acordó la línea base vigente: Sprint 1 MFA/pedidos, Sprint 2 flota y Sprint 3 rutas. Las metas de Jira y las historias de flota se actualizaron para coincidir. El Sprint 1 conserva su corte y pertenencia histórica; los habilitadores de pedidos y MFA ya completados no se añaden a una iteración cerrada. El Sprint 3 sigue sujeto a Planning, sin inventar estimación, responsables ni compromiso.

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

**Normalización verificada en Jira el 09/10/2026:** el flujo compartido para Historia, Tarea, Error, Subtask y Epic quedó con cuatro estados: `Por hacer`, `En curso`, `En revisión / QA` y `Listo`. Se retiró el estado duplicado `Finalizada`, que no tenía incidencias asociadas, y se eliminó la columna `Done`. `getJiraBoardConfig` confirma cuatro columnas en español, con categorías nueva, en curso, en curso y completada, respectivamente. La consulta JQL no encuentra incidencias en `Finalizada`. `getJiraProjectVersions` devuelve 0; IMP-003 permanece abierto solo por la ausencia de versión de entrega.

## 5. Checklist de configuración

- [x] Proyecto ECO, ocho épicas, nueve historias y dos tareas consultadas el 09/10/2026.
- [ ] Aclarar o corregir `ECO-7`, que duplica la tarjeta de épica `ECO-6`; conservar siete épicas lógicas EP-01–EP-07.
- [x] HU-009 / ECO-19 asociada a EP-02 y HU-003 / ECO-12 asociada a EP-02.
- [x] Resolver la duplicidad de sprints: cerrar el Sprint 1 id. 36 el 09/10 y renombrar el sprint id. 3 como duplicado.
- [x] Crear y cargar el Sprint 2 id. 37; registrar la historia técnica ECO-20 para MFA, sin inventar una estimación.
- [x] Revisar ECO-15: devolverla a `Por hacer` por falta de implementación de re-enrutamiento demostrable.
- [ ] Completar las historias y tareas ausentes: HU-004, HU-010, HU-011 y EN-001 a EN-004; confirmar prioridades y puntos con el equipo.
- [x] Corregir las categorías de `En revisión / QA` y `Finalizada`; validar los cinco estados con `getJiraBoardConfig` (09/10/2026).
- [x] Reducir y normalizar el tablero a cuatro columnas en español, retirar el estado duplicado `Finalizada` y verificar categorías y mapeos con `getJiraBoardConfig` (09/10/2026).
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
| 1.11.0 | 09/10/2026 | Se actualiza el estado vivo del tablero: categorías de `En revisión / QA` y `Finalizada` corregidas y mapeos verificados; permanecen cinco columnas mixtas y cero versiones de entrega. |
| 1.12.0 | 09/10/2026 | Se verifica el tablero normalizado a cuatro columnas en español y el retiro de `Finalizada`; Sprint 1 dinámico 1/2, Sprint 2 activo 2/2 y cero versiones de entrega. |
