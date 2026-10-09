# Auditoría de coherencia del proyecto — 09/10/2026

[← Volver al README Principal](../../README.md)

## Propósito y alcance

Esta auditoría contrasta la documentación versionada, el código y las dependencias del repositorio, las especificaciones OpenSpec y el tablero Jira `ECO`. Distingue el diseño objetivo de lo implementado y registra los desajustes que deben resolverse antes de considerar cerrada la documentación del Sprint 2.

La consulta de Jira se realizó el 09/10/2026 en modo de solo lectura. Las pruebas y la compilación local se ejecutaron el mismo día. El Sprint 2 aún está en curso (29/09–12/10); la revisión de las 15:40, hora de Lima, todavía no se había celebrado a la hora de esta auditoría.

## Idioma, identidad y stack comunes

- Los documentos de producto en `README.md`, `docs/` y los artefactos OpenSpec están redactados en español. `openspec/config.yaml` exige `es`; mantiene en inglés únicamente los encabezados estructurales y las palabras obligatorias `SHALL`/`MUST` del formato. Los archivos `.claude/commands/opsx` y `.claude/skills/openspec-*` son instrucciones del flujo de herramienta y se conservan en el idioma original del proveedor.
- El nombre del integrante se normaliza en la documentación como **Anco Porras, Jhean Pier Julio**.
- La línea base vigente es **React + Vite + TypeScript** en el frontend y **FastAPI + Python** en la API. La propuesta de Next.js/Nest.js se revirtió el 02/10/2026 y no es una alternativa vigente.
- PostgreSQL/PostGIS, Leaflet/OpenStreetMap y el motor Python de optimización pertenecen a la arquitectura objetivo. No deben presentarse como componentes ya ejecutados.

## Plan y resultado hasta el Sprint 2

| Iteración | Plan registrado | Resultado comprobado al 09/10/2026 |
|---|---|---|
| Sprint 1 · 14/09–28/09 | ECO-9 / HU-001 y ECO-15 / HU-006; 10 puntos. | El informe de cierre registra 0 de 2 historias y 0 puntos que cumplieron la Definición de Hecho. El código de HU-001 se implementó después, durante el Sprint 2. HU-006 sigue sin implementación de re-enrutamiento. |
| Sprint 2 · 29/09–12/10 | Replanificación para entregar el primer incremento: HU-001 con autenticación y autorización MFA. | HU-001 (5 puntos) y MFA están en `main`. En la ejecución local del 09/10: 100 pruebas de backend aprobadas, 99 % de cobertura, 39 pruebas de frontend aprobadas y compilación de producción completada. El Sprint 2 aún no está cerrado. |
| Sprint 3 | El plan de trabajo de la retrospectiva contempla PostgreSQL/PostGIS, gestión de flota, prototipo y benchmark del motor, y CI. | Trabajo futuro; las historias/tareas faltantes y su capacidad aún deben confirmarse y estimarse en Jira. |
| Sprints 4–5 y cierre | El roadmap de planificación conserva dashboard, visor, seguridad, disponibilidad e integración/aceptación. | Alcance de alto nivel; no hay evidencia para asignar resultados, fechas detalladas o compromisos no aprobados. |

El backend registra **tres advertencias deprecadas** durante `pytest`. La compilación frontend concluye, pero avisa que los archivos licenciados Codec Pro `.woff2` no están disponibles. La compilación y las pruebas no prueban una revisión visual extremo a extremo ni despliegue continuo.

## Estado real de Jira `ECO`

El tablero consultado fue `ECO board` (id. 2). Jira devuelve 8 tarjetas de tipo Epic, 8 historias y 2 tareas; `ECO-7` duplica la épica de re-enrutamiento `ECO-6`, por lo que el backlog tiene 7 épicas lógicas EP-01–EP-07. La planificación publicada en el repositorio no está sincronizada con el tablero:

1. Hay dos sprints llamados `ECO Sprint 1`: id. 3 está cerrado; id. 36 sigue activo con fecha de fin 28/09/2026. No hay un Sprint 2 en Jira.
2. Jira devuelve ECO-9 y ECO-15 en el Sprint 1 activo y marca ambas `Listo`. El informe del Sprint 1 dice que ninguna cumplió la Definición de Hecho al cierre. El código confirma HU-001 después, durante el Sprint 2, pero no se encontró implementación para HU-006. El estado actual de la tarjeta no cambia el resultado histórico ni prueba una funcionalidad.
3. No existe una incidencia Jira para la autenticación MFA que se incorporó al Sprint 2 en la replanificación documental y se implementó en el repositorio.
4. El backlog no contiene HU-004, HU-010, HU-011 ni EN-001–EN-004. ECO-16 está estimada en 3 puntos y ECO-17 en 5.
5. El tablero conserva cinco columnas (`Por hacer`, `En curso`, `Listo`, `In Review / QA`, `Done`). `Listo` está mapeado a una categoría completada; `Done` está mapeado al estado `Finalizada`, que la configuración devuelve con categoría nueva.
6. La consulta de versiones del proyecto devuelve cero; `v1.0.0-MVP` no existe como versión Jira.
7. Las descripciones de ECO-16 y ECO-17 mencionaban Next.js/Nest.js. Se actualizaron el 09/10 para indicar React/Vite y FastAPI, documentar el estado real y mantener las tareas de PostgreSQL/CI como pendientes. No se cambiaron los estados de las incidencias ni el ciclo de vida de los sprints.

La imagen histórica que antes se llamaba `05-releases.png` muestra un resumen analítico del proyecto, no una versión de Jira. Se renombró a `05-resumen-analitico-historico.png`; la evidencia actual de versiones sigue pendiente.

## Documentos contrastados

- `README.md` y la guía de ejecución local.
- Los 13 documentos de Inicio, los 4 de Planificación y los 8 entregables de Sprint 1 y Sprint 2.
- `openspec/config.yaml`, los dos cambios archivados y las especificaciones vigentes de pedidos y autenticación.
- `backend/requirements.txt`, `frontend/package.json`, fuentes actuales, scripts de pruebas y estructura de `.github/`.
- Tablero, sprints, backlog, configuración de columnas, versiones y tarjetas ECO-16/ECO-17 en Jira.

La documentación histórica de cada sprint conserva su fecha de corte original. Este documento resume las comprobaciones posteriores sin reescribir los resultados de fechas anteriores.

## Acciones abiertas

- Cerrar y renombrar de forma inequívoca el Sprint 1 duplicado; registrar en Jira el Sprint 2 y la historia de MFA conforme a la replanificación aprobada.
- Revisar el estado `Listo` de ECO-15 frente a la ausencia de código de re-enrutamiento, y corregir las categorías/columnas del tablero.
- Completar las tarjetas faltantes, confirmar estimaciones y decidir cuándo crear la versión `v1.0.0-MVP`.
- Después de la revisión del Sprint 2 y de confirmar los acuerdos del equipo, actualizar su informe, revisión y retrospectiva con resultados y evidencia final.
- Mantener PostgreSQL/PostGIS, optimización, mapa, dashboard y CI como pendientes hasta implementar y verificar cada incremento.

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 09/10/2026 | Contraste de idioma, stack, implementación, sprints y Jira; evidencia local de pruebas y compilación. |
