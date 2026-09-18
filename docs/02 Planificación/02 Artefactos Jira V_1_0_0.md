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
| Clave del proyecto en Jira | `ECO` |
| Estado | Proyecto Scrum `ECO` creado y en configuración activa; 8 épicas y 10 historias/tareas creadas, verificado en el proyecto real el 18 de septiembre de 2026 (`ECO-18` y `ECO-19` — antes duplicados de `ECO-11`/`ECO-12` — se renombraron a HU-008 y HU-009). El Sprint 1 seguía sin iniciar |

## 1. Configuración objetivo

| Elemento | Configuración |
|---|---|
| Tipo de proyecto | Scrum administrado por el equipo |
| Jerarquía | Epic → Story / Task → Sub-task; Bug para incidencias |
| Flujo | To Do → In Progress → In Review / QA → Done |
| Release | `v1.0.0-MVP` (pendiente de crear en Jira) |
| Sprint | ECO Sprint 1, 18 sep – 25 sep 2026 (**activo**, iniciado el 18 de septiembre) |
| Sprint Goal (real, tomado de Jira) | "Entregar el primer incremento funcional de EcoLogística: registrar pedidos y flota, generar rutas optimizadas y visualizar resultados, con criterios de calidad verificables." |

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
| 23 | Task | EN-005 | ECO-16 | Configurar PostgreSQL y PostGIS | 5 | ✅ |
| 24 | Task | EN-006 | ECO-17 | Configurar CI/CD, pruebas y documentación OpenAPI | 8 | ✅ |

Los puntos usan Fibonacci (1, 2, 3, 5, 8, 13); los de los ítems marcados ✅ son los reales tomados de Jira, los de los ítems ⬜ son la estimación propuesta en esta especificación, pendiente de validar por el equipo al crearlos. La prioridad combina valor de negocio, dependencia y riesgo técnico; el detalle completo y los criterios BDD están en [01 Transformando a ágil](01%20Transformando%20a%20%C3%A1gil%20V_1_0_0.md).

> ✅ **Resuelto el 18 de septiembre de 2026:** `ECO-18` y `ECO-19` habían sido creados como duplicados literales de `ECO-11` y `ECO-12` (mismo título y misma épica EP-01). Se renombraron en Jira a HU-008 "Importar pedidos por plantilla" y HU-009 "Parametrizar restricciones vehiculares" respectivamente, completando así los 8 épicas + 10 historias/tareas reales del backlog.
>
> ⚠️ **Pendiente de corrección:** `ECO-19` (HU-009, restricciones vehiculares) quedó asignado a la épica `EP-01 Gestión de pedidos`; por su contenido debería estar en `EP-02 Gestión de flota y conductores`, igual que `ECO-12`. Falta reasignar la épica en Jira.

## 3. Roadmap y Sprint 1

| Periodo | Entrega | Épicas |
|---|---|---|
| Sprint 1 — 11 sep a 25 sep 2026 | Registrar pedido y re-enrutar ante incidencia (ECO-9, ECO-15 ya cargados en el sprint) | EP-01, EP-06 |
| Sprint 2 — semanas 3–4 | Flota, geocodificación y motor de optimización | EP-02, EP-03 |
| Sprint 3 — semanas 5–6 | Visor cartográfico y disponibilidad del servicio | EP-04 |
| Sprint 4 — semanas 7–8 | Dashboard, auditoría y hardening de seguridad | EP-05 |
| Sprint 5 — semana adicional de cierre | Persistencia geoespacial, CI/CD y documentación técnica | EP-07 |
| Release v1.0.0-MVP | Integración y aceptación | EP-01 a EP-07 |

> El Sprint 1 real en Jira solo tiene 2 historias cargadas (10 puntos), aunque su Sprint Goal menciona también generar rutas y visualizar resultados; el resto del alcance del objetivo se completará al cargar HU-004 y HU-005 en un sprint posterior.

## 4. Evidencias requeridas para completar en Jira

La consigna exige recortes exclusivos del panel de Jira, sin escritorio, navegador ni espacio sobrante. Se deben insertar aquí, una vez obtenidas del proyecto Jira real, las siguientes evidencias:

1. **Evidencia 1 — Roadmap:** épicas ubicadas en la línea de tiempo.
2. **Evidencia 2 — Backlog:** orden, puntos y componentes visibles.
3. **Evidencia 3 — Sprint Planning:** Sprint 1 con su Sprint Goal real, iniciado (no solo planificado).
4. **Evidencia 4 — Tablero Scrum:** tarjetas distribuidas en To Do, In Progress, In Review / QA y Done.
5. **Evidencia 5 — Release:** `v1.0.0-MVP` y asociación de historias.

> Verificado directamente en el proyecto Jira `ECO` el 11 de septiembre de 2026: existen 8 épicas y 8 historias/tareas creadas, y el Sprint 1 está planificado pero aún no iniciado. Aún faltan las 5 capturas recortadas del panel de Jira (sin escritorio ni navegador) — no se fabrican imágenes por integridad académica; deben tomarse directamente del proyecto real una vez completada la configuración pendiente.
>
> **Reverificado el 18 de septiembre de 2026:** el Roadmap (Cronograma) ya muestra las 8 épicas correctamente ubicadas en la línea de tiempo con "ECO Sprint 1" marcado en septiembre. **El Sprint 1 ya está activo** — el tablero muestra el botón "Completar sprint" y las fechas se ajustaron a 18–25 sep, con las mismas 2 historias cargadas (ECO-9, ECO-15 = 10 puntos) visibles en la columna "Por hacer". El Backlog ya no tiene duplicados: `ECO-18`/`ECO-19` se renombraron a HU-008/HU-009 (ver sección 2). Las 5 capturas recortadas siguen sin insertarse en este documento — es lo único que falta para cerrar este archivo.
>
> ⚠️ **Nuevo hallazgo:** el Tablero Scrum tiene 5 columnas (Por hacer, En curso, **Listo**, In Review/QA, Done), pero la consigna exige exactamente 4 (To Do → In Progress → In Review/QA → Done). Sobra la columna "Listo"; conviene quitarla o fusionarla antes de tomar la Evidencia 4.

### Dónde insertar cada captura

Cuando tengas los 5 recortes, se insertan aquí mismo reemplazando cada línea de la lista de arriba por una imagen Markdown, así: `![Roadmap del proyecto ECO](../../assets/jira/01-roadmap.png)`. Guarda los archivos en `assets/jira/` en la raíz del repo con estos nombres exactos:

| Archivo | Evidencia |
|---|---|
| `assets/jira/01-roadmap.png` | Evidencia 1 — Roadmap |
| `assets/jira/02-backlog.png` | Evidencia 2 — Backlog |
| `assets/jira/03-sprint-planning.png` | Evidencia 3 — Sprint Planning |
| `assets/jira/04-tablero-scrum.png` | Evidencia 4 — Tablero Scrum |
| `assets/jira/05-release.png` | Evidencia 5 — Release |

## 5. Checklist de configuración

- [x] Crear proyecto Scrum `ECO` (EcoLogística Huancayo).
- [x] Crear EP-01 a EP-05 en Jira (ECO-1 a ECO-5).
- [x] Crear EP-06 y EP-07, no previstas en la especificación original (ECO-6 y ECO-8).
- [x] Crear HU-008 (ECO-18) y HU-009 (ECO-19) — resuelto el 18 sep renombrando los duplicados de ECO-11/ECO-12.
- [ ] Crear el resto del backlog (HU-004, EN-001, HU-010, HU-011, EN-002, EN-003, EN-004) y asignarle puntos Fibonacci.
- [ ] Reasignar la épica de `ECO-19` (HU-009) de EP-01 a EP-02, donde corresponde por contenido.
- [ ] Crear la versión `v1.0.0-MVP` y asociarla a las historias (función Releases no habilitada aún en el proyecto — activarla primero en Configuración del proyecto → Features).
- [ ] Configurar columnas del flujo indicado en el tablero.
- [x] Crear Sprint 1 (18 sep – 25 sep) con Sprint Goal real.
- [x] Iniciar el Sprint 1 — confirmado activo el 18 sep (tablero con "Completar sprint").
- [ ] Cargar HU-004 y HU-005 al Sprint 1 para que coincida con lo declarado en su Sprint Goal, o reescribir el Sprint Goal para que coincida con el alcance real (ECO-9, ECO-15).
- [ ] Quitar o fusionar la columna extra "Listo" del tablero para que queden exactamente los 4 estados exigidos.
- [ ] Capturar los cinco recortes limpios e insertarlos en este archivo (pendiente — ver sección 4).
