# Auditoría de coherencia del proyecto — 09/10/2026

[← Volver al README Principal](../../README.md)

## Propósito y alcance

Esta auditoría contrasta la documentación versionada, el código y las dependencias del repositorio, las especificaciones OpenSpec y el tablero Jira `ECO`. Distingue el diseño objetivo de lo implementado y registra los desajustes que deben resolverse antes de considerar cerrada la documentación del Sprint 2.

La auditoría inicial de Jira fue de solo lectura el 09/10/2026. Después, el mismo día, se regularizaron los sprints y la historia de autenticación en Jira y se verificó el resultado. Las pruebas y la compilación local también se ejecutaron el 09/10. El Sprint 2 continúa activo (29/09–12/10); la revisión de las 15:40, hora de Lima, aún está pendiente al corte de esta actualización.

## Idioma, identidad y stack comunes

- La documentación de producto y planificación en `README.md`, `docs/`, las plantillas de GitHub y OpenSpec está redactada en español. El 09/10 también se localizaron al español los seis comandos `.claude/commands/opsx` y sus seis habilidades `.claude/skills/openspec-*`; se conservaron los identificadores de comandos, campos JSON, estados de la CLI, la categoría de metadatos `Workflow` y los encabezados estructurales que forman parte del contrato de OpenSpec. `openspec/config.yaml` exige `es`; las especificaciones mantienen `SHALL`/`MUST` y `WHEN`/`THEN` donde los requiere el formato.
- El nombre del integrante se normaliza en la documentación como **Anco Porras, Jhean Pier Julio**.
- La línea base vigente es **React + Vite + TypeScript** en el frontend y **FastAPI + Python** en la API. La propuesta de Next.js/Nest.js se revirtió el 02/10/2026 y no es una alternativa vigente.
- PostgreSQL/PostGIS, Leaflet/OpenStreetMap y el motor Python de optimización pertenecen a la arquitectura objetivo. No deben presentarse como componentes ya ejecutados.
- Las herramientas de seguimiento y entrega son Jira (`ECO`) para backlog y sprints, GitHub para el repositorio y OpenSpec para especificaciones y cambios. PostgreSQL/PostGIS, mapas, optimización, Docker Compose y CI no forman parte del stack ejecutable actual.
- El árbol del README se contrastó con el repositorio: `database/` aún no existe. `docs/04 Seguimiento y Control/` y `docs/05 Cierre/` sí existen, pero solo tienen `.gitkeep` y no contienen entregables; el README ahora distingue los directorios reservados de la documentación pendiente.
- El diagrama de módulos del README queda etiquetado como alcance objetivo y enumera por separado los módulos implementados y los pendientes al 09/10.
- `.env.example` y las instrucciones de instalación se contrastaron con `backend/src/app/config.py`, `frontend/vite.config.ts` y `frontend/package-lock.json`: se eliminaron variables de base de datos, mapas y optimización que el código actual ignora, se documentaron solo variables operativas y se actualizaron los comandos de PowerShell y el requisito real de Node para Vite 8.
- El flujo de ramas se armonizó en README, OpenSpec, RES-17 y RST-ACA-02: ramas breves `feature/*` desde `main`, PR hacia `main`, sin `develop` obligatoria. La consulta Git del 09/10 muestra `developer` 29 commits detrás de `main` y sin commits propios; `docs/semana-3-entregables` está 45 commits detrás y 1 por delante, con un commit del 04/09 que añadió versiones iniciales de ocho documentos de Inicio ahora presentes y revisados en `main`. No se integran ni eliminan ramas remotas sin confirmar su destino con el equipo. La protección de `main`, revisión obligatoria y CI siguen pendientes; `gh auth status` indica que esta sesión no está autenticada y no permitió leer la configuración de protección.
- Las referencias a `develop` en actas y retrospectivas de Sprint 1 se conservan como acuerdos históricos de esa fecha; las tareas futuras de los documentos de Sprint 2 ya apuntan al flujo actualizado. No se deben interpretar esas referencias antiguas como configuración vigente.

## Plan y resultado hasta el Sprint 2

| Iteración | Plan registrado | Resultado comprobado al 09/10/2026 |
|---|---|---|
| Sprint 1 · 14/09–28/09 | ECO-9 / HU-001 y ECO-15 / HU-006; 10 puntos. | El informe del Sprint 1 registra 0 de 2 al corte planificado del 28/09. Jira mantuvo el sprint id. 36 activo hasta el 09/10 a las 07:42. El historial de ECO-9 muestra `Listo` el 02/10, `Por hacer` al cerrarse el Sprint 1 y nuevamente `Listo` a las 07:43 al añadirse al Sprint 2; ECO-15 sigue `Por hacer`. La métrica dinámica actual de Jira muestra 1 de 2 y no reconstruye la velocidad al 28/09. |
| Sprint 2 · 29/09–12/10 | Replanificación para entregar el primer incremento: HU-001 con autenticación y autorización MFA. | Jira sprint id. 37 activo: ECO-9 (5 puntos) y ECO-20 (MFA, sin estimación aprobada ni persona asignada), ambas `Listo`; la métrica dinámica cuenta 2/2 incidencias (100 %), no aceptación del producto. En la ejecución local del 09/10: 100 pruebas de backend aprobadas, 99 % de cobertura, 39 pruebas de frontend aprobadas y compilación de producción completada. Al corte anterior a la reunión de las 15:40, la revisión, la velocidad oficial y el cierre formal siguen pendientes. |
| Sprint 3 | El plan de trabajo de la retrospectiva contempla PostgreSQL/PostGIS, gestión de flota, prototipo y benchmark del motor, y CI. | Trabajo futuro; las historias/tareas faltantes y su capacidad aún deben confirmarse y estimarse en Jira. |
| Sprint 4 y cierre | El horizonte aprobado contempla cuatro iteraciones y una semana de cierre; el roadmap conserva dashboard, visor, seguridad, disponibilidad e integración/aceptación. | Alcance futuro de alto nivel; prioridades, compromisos y fechas detalladas del Sprint 4 aún no están aprobados. |

El backend registra **tres advertencias deprecadas** durante `pytest`. La compilación frontend concluye, pero avisa que los archivos licenciados Codec Pro `.woff2` no están disponibles. La compilación y las pruebas no prueban una revisión visual extremo a extremo ni despliegue continuo.

## Consistencia de calendario y presupuesto

- El Acta y el README fijan 14 semanas de desarrollo más una de cierre y cuatro iteraciones. Los documentos de Sprint 1 y 2 usan periodos consecutivos de dos semanas dentro de septiembre–octubre. La palabra *iteración* del calendario presupuestario no está definida frente a los *sprints* Scrum; se conservan las fechas reales de Sprint 1 y 2 y no se asignan compromisos a Sprint 3 hasta acordar ese mapeo.
- El Acta establece un techo de autorización de S/ 500,000 y una reserva máxima de S/ 35,000; el presupuesto detallado calcula S/ 54,538.40, con una reserva estimada de S/ 5,843.40. Se documenta como techo versus estimado detallado, no como dos gastos ejecutados. El gasto real reportado al cierre de Sprint 1 es S/ 0 en infraestructura.

## Estado real de Jira `ECO`

El tablero consultado fue `ECO board` (id. 2). Jira devuelve 8 tarjetas de tipo Epic, 9 historias y 2 tareas; `ECO-7` duplica la épica de re-enrutamiento `ECO-6`, por lo que el backlog tiene 7 épicas lógicas EP-01–EP-07. La historia técnica ECO-20 se registró el 09/10 sin puntos aprobados y continúa sin persona asignada al corte de esta auditoría.

1. El sprint id. 36 es el Sprint 1 oficial; se cerró administrativamente el 09/10 después de su fecha final del 28/09. El sprint id. 3 se renombró `ECO Sprint 1 (duplicado)` y su objetivo aclara que no es el sprint oficial. El historial de ECO-9 registra `Listo` el 02/10, `Por hacer` al cierre del Sprint 1 y `Listo` otra vez después de añadirse al Sprint 2. El informe dinámico actual cuenta la incidencia en Sprint 1 por el estado vigente y la asociación doble; el conector no expone el reporte histórico al 28/09.
2. Se creó el Sprint 2 id. 37 con fechas 29/09–12/10 y la meta de HU-001 con MFA. ECO-9 / HU-001 (5 puntos) y ECO-20 / autenticación MFA están en el sprint y en estado `Listo`; ECO-20 permanece sin estimación y sin persona asignada.
3. ECO-15 / HU-006 está en `Por hacer`: no se encontró implementación de re-enrutamiento en el repositorio. Su historial de Sprint conserva la asignación al Sprint 1.
4. El backlog no contiene HU-004, HU-010, HU-011 ni EN-001–EN-004. ECO-16 está estimada en 3 puntos y ECO-17 en 5.
5. El tablero conserva cinco columnas (`Por hacer`, `En curso`, `Listo`, `In Review / QA`, `Done`). `Listo` está mapeado a una categoría completada; `Done` está mapeado al estado `Finalizada`, que la configuración devuelve con categoría nueva.
6. La consulta de versiones del proyecto devuelve cero; `v1.0.0-MVP` no existe como versión Jira.
7. ECO-20 se creó el 09/10 bajo EP-07 para registrar autenticación MFA; quedó sin estimación ni persona asignada y en `Listo`, con criterios vinculados a RF-11.1.
8. Las descripciones de ECO-16 y ECO-17 mencionaban Next.js/Nest.js. Se actualizaron el 09/10 para indicar React/Vite y FastAPI, documentar el estado real y mantener PostgreSQL/CI como pendientes.
9. La verificación del 09/10 mostró que la configuración de cinco columnas y la ausencia de versiones de entrega persisten, pese a la confirmación comunicada el 02/10. Se reabrió IMP-003 y se incorporó al registro del Sprint 2.

La imagen histórica que antes se llamaba `05-releases.png` muestra un resumen analítico del proyecto, no una versión de Jira. Se renombró a `05-resumen-analitico-historico.png`; la evidencia actual de versiones sigue pendiente.

## Documentos contrastados

- `README.md` y la guía de ejecución local.
- Los 13 documentos de Inicio, los 4 de Planificación y los 8 entregables de Sprint 1 y Sprint 2.
- `openspec/config.yaml`, los dos cambios archivados y las especificaciones vigentes de pedidos y autenticación.
- Los seis comandos y seis habilidades operativas de OpenSpec en `.claude/`, incluida su estructura de metadatos.
- `backend/requirements.txt`, `frontend/package.json`, fuentes actuales, scripts de pruebas y estructura de `.github/`.
- Tablero, sprints, backlog, configuración de columnas, versiones y tarjetas ECO-16/ECO-17 en Jira.

En la revisión estática del repositorio se recorrieron 39 archivos Markdown: no se encontraron enlaces locales rotos ni caracteres de reemplazo. El control de versiones de los documentos de `docs/` tampoco encontró discrepancias entre el metadato y la última entrada de historial.

La documentación histórica de cada sprint conserva su fecha de corte original. Este documento resume las comprobaciones posteriores sin reescribir los resultados de fechas anteriores.

En la revisión documental del 09/10 se corrigió el uso de “velocidad” para el Sprint 2: antes de la reunión y del cierre, los 5 puntos de ECO-9 son estado observado en Jira (`Listo`), no velocidad aceptada. También se acotó la afirmación sobre concentración de commits al corte del 02/10 y se incorporó el historial verificado hasta el 09/10.

La comprobación del control de versiones detectó cuatro documentos cuyo campo de versión no coincidía con su última entrada de historial. Se alinearon los metadatos del stack tecnológico, los registros de impedimentos de ambos sprints y la retrospectiva del Sprint 2 con sus historiales vigentes.

## Acciones abiertas

- Después de la revisión prevista para el 09/10 a las 15:40, registrar sus decisiones, actualizar el estado y cerrar el Sprint 2 el 12/10.
- Confirmar con el equipo si se archivan las ramas remotas `developer` y `docs/semana-3-entregables`, teniendo en cuenta sus desfases y el único commit propio de esta última.
- Corregir la mezcla de idiomas y el mapeo de las cinco columnas del tablero Jira; mantener `Listo` como único estado de categoría completada.
- Aplicar el flujo de ramas acordado, retirar la rama `developer` desactualizada cuando el equipo confirme la migración, y configurar revisión y CI para `main`.
- Definir si las cuatro iteraciones del Acta son periodos macro o si corresponden uno a uno con sprints; luego calendarizar Sprint 3 y 4 sin alterar las fechas históricas.
- Completar las tarjetas faltantes, confirmar estimaciones y decidir cuándo crear la versión `v1.0.0-MVP`.
- Después de la revisión del Sprint 2 y de confirmar los acuerdos del equipo, actualizar su informe, revisión y retrospectiva con resultados y evidencia final.
- Mantener PostgreSQL/PostGIS, optimización, mapa, dashboard y CI como pendientes hasta implementar y verificar cada incremento.

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 09/10/2026 | Contraste inicial de idioma, stack, implementación, sprints y Jira; evidencia local de pruebas y compilación. |
| 1.1.0 | 09/10/2026 | Se actualiza con la regularización de sprints e incidencias de Jira, la distinción entre techo y estimado presupuestario, y la ambigüedad pendiente entre iteración y sprint. |
| 1.2.0 | 09/10/2026 | Se actualiza con la métrica dinámica de Sprint 1 y su diferencia respecto del corte planificado, además de la regularización de sprints e incidencias de Jira, la distinción entre techo y estimado presupuestario, y la ambigüedad pendiente entre iteración y sprint. |
| 1.3.0 | 09/10/2026 | Se alinea el README y OpenSpec con la estructura existente y el flujo de ramas acordado; se identifican como pendientes la revisión del Sprint 2, la configuración de Jira, la protección de `main` y CI. |
| 1.4.0 | 09/10/2026 | Se actualiza el conteo dinámico de Jira del Sprint 2 a 2/2 y se aclara que la métrica no sustituye la aceptación ni el cierre formal. |
| 1.5.0 | 09/10/2026 | Se alinea RST-ACA-02 y se explicita en OpenSpec el límite entre stack objetivo e implementación ejecutable. |
| 1.6.0 | 09/10/2026 | Se alinea `.env.example` y la guía de instalación con las variables y herramientas realmente consumidas por el código. |
| 1.7.0 | 09/10/2026 | Se aclara que el diagrama de módulos del README representa el alcance objetivo y se identifica el subconjunto implementado al corte. |
| 1.8.0 | 09/10/2026 | Se detalla la secuencia de estados de ECO-9 y se incorpora IMP-003 reabierto; el Sprint 2 permanece pendiente de revisión y cierre formal. |
| 1.9.0 | 09/10/2026 | Se comparan las ramas remotas con `main`; se registra el límite de autenticación de GitHub CLI para verificar protección y se deja pendiente la disposición de las ramas antiguas. |
| 1.10.0 | 09/10/2026 | Se traducen al español los comandos y habilidades OpenSpec de `.claude/`, conservando sus nombres ejecutables, campos de datos y contratos estructurales. |
| 1.11.0 | 09/10/2026 | Se corrige la presentación de los 5 puntos del Sprint 2 como velocidad, se deja la velocidad oficial pendiente de revisión y cierre, y se acota al corte correspondiente el análisis de autoría de commits. |
| 1.12.0 | 09/10/2026 | Se alinean los metadatos de versión de cuatro documentos con su historial de cambios y se registra el control de consistencia documental. |
| 1.13.0 | 09/10/2026 | Se documenta la revisión estática de los 39 archivos Markdown: cero enlaces locales rotos, cero caracteres de reemplazo y metadatos de versión alineados. |
| 1.14.0 | 09/10/2026 | Se registra que ECO-20 sigue sin persona asignada en Jira y se alinea este dato en README, planificación e informes del Sprint 2. |
| 1.15.0 | 09/10/2026 | Se extiende la trazabilidad del estado sin asignación de ECO-20 al registro de impedimentos y se renueva la verificación de Jira. |
