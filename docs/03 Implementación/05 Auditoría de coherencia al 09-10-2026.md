# Auditoría de coherencia del proyecto — 09/10/2026

[← Volver al README Principal](../../README.md)

## Propósito y alcance

Esta auditoría contrasta la documentación versionada, el código y las dependencias del repositorio, las especificaciones OpenSpec y el tablero Jira `ECO`. Distingue el diseño objetivo de lo implementado y registra los desajustes que deben resolverse antes de considerar cerrada la documentación del Sprint 2.

## Auditoría integral alineada con la línea base vigente

**Corte de verificación: 09/10/2026.** Se revisaron los **56 archivos Markdown presentes** en el árbol de trabajo: 55 versionados y la nueva especificación principal de flota; el desglose es README (1), Inicio (13), Planificación (5), Implementación/Sprints (9), OpenSpec y archivos archivados (12), instrucciones `.claude/` (12), plantillas `.github/` (3) y guía de fuentes (1). Se comprobaron los enlaces Markdown locales de los 56 archivos; el resultado es **0 enlaces rotos**. Las especificaciones archivadas y los informes de cortes anteriores se mantienen como evidencia histórica; las notas posteriores indican cuándo cambió el contexto.

| Tema contrastado | Evidencia vigente del repositorio | Conclusión documental |
|---|---|---|
| Interfaz y API | React + Vite + TypeScript; FastAPI + Pydantic. `frontend/package.json`, `backend/src/app/main.py` y routers de auth, pedidos y flota. | Es el stack ejecutable; React/Next, Nest, Django o Vue no son la arquitectura vigente. |
| Persistencia | Alembic `20261009_01` para pedidos/ubicaciones y `20261009_02` para vehículos/disponibilidad; repositorios PostgreSQL en `backend/src/app/pedidos/` y `backend/src/app/flota/`. | Pedidos y flota persisten en PostGIS. Las cuentas siguen en archivo local y no hay tablas ni API de rutas. |
| Ejecución local | `docker-compose.yml` define únicamente el servicio PostGIS; Vite y Uvicorn se ejecutan por separado. | Docker Compose no levanta todo el sistema ni equivale a un despliegue productivo. |
| Funciones presentes | Login MFA/roles, pedidos y flota en la aplicación. La regla de elegibilidad requiere estado Disponible y disponibilidad activa. | El E2E de flota del 09/10 pasó 5/5 criterios; no se atribuye a la aplicación generación de rutas, mapas, motor, dashboard o seguimiento de entregas. |
| Línea base del programa | Decisión del usuario aplicada: Sprint 1 MFA/roles y pedidos; Sprint 2 flota; Sprint 3 rutas; se conserva el propósito posterior. | Plan y metas Jira ya reflejan el rebase. Sprint 2 contiene ECO-12 y ECO-19 en `Listo` (2/2); el Sprint 1 está cerrado y conserva su resultado histórico y pertenencias originales. |
| Cobertura documental | Requisitos, reglas, visión, modelo de datos y diagramas mantienen la arquitectura objetivo; README, stack, C4, datos, OpenSpec de flota/config y planificación distinguen el estado vigente de lo propuesto. | Se corregían afirmaciones actuales que aún marcaban como pendientes la base o flota, movían flota a Sprint 3 o daban por configurada toda la arquitectura objetivo. |

La línea base vigente deja los pendientes de producto en **rutas** para Sprint 3 y en los propósitos posteriores conservados (ejecución/seguimiento por Conducción, analítica y cierre según el plan). El trabajo de flota no se vuelve a cargar en Sprint 3. Los documentos actuales y las metas/tarjetas disponibles de Jira se alinearon a la rebase funcional; los cortes originales se mantienen como historia. La columna Jira `Done` aún mapea a `Finalizada`, cuya categoría es `Por hacer`; esta configuración del tablero no puede editarse con la operación Jira disponible en esta sesión. No se cambió el alcance de requisitos de negocio.

**Pendientes de gestión al corte actual:** Sprint 2 permanece activo con 2/2 historias de flota en `Listo`; falta registrar la reunión de revisión prevista para las 15:40 y hacer el cierre administrativo. La configuración de columnas del tablero sigue inconsistente. ECO-21 ahora excluye la flota ya persistida y contiene cuentas, TOTP y rutas. No existe Sprint 3 aprobado ni versión `v1.0.0-MVP` en Jira. La especificación principal de flota está en `openspec/specs/flota/spec.md` y `openspec/config.yaml` la reconoce.

La auditoría inicial de Jira fue de solo lectura el 09/10/2026. En la actualización de las 13:00, hora de Lima, se cambió la meta del Sprint 1 para conservar explícitos el compromiso original y la rebase; el Sprint 2 se alineó a flota; ECO-12 y ECO-19 se asignaron al Sprint 2 y se marcaron `Listo`; ECO-9, ECO-16 y ECO-20 salieron del sprint activo sin borrar sus historiales. Se actualizó el alcance de ECO-21 y se dejó ECO-15 pendiente en el backlog. Lectura posterior confirmó Sprint 2 activo con 2/2. La reunión de las 15:40 aún no había ocurrido al momento de ese corte.

> **Actualización posterior de implementación (09/10/2026):** después de redactar los hallazgos iniciales de esta auditoría, se integraron PostgreSQL/PostGIS, una migración Alembic y el repositorio de pedidos y ubicaciones. Una comprobación aislada confirmó que un pedido sigue disponible después de reiniciar la API. Por eso, las frases siguientes que describen PostgreSQL, Docker Compose o `database/` como pendientes corresponden al corte de la auditoría inicial; el estado vigente se detalla en el [informe del Sprint 2](Sprint%202/01%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md) y el [plan funcional](../02%20Planificaci%C3%B3n/05%20Plan%20funcional%20de%20sprints.md). En ese corte todavía faltaba persistir cuentas, flota y rutas; después se implementó y verificó la persistencia de flota. La aceptación según los criterios funcionales de Sprint 2 se informa en la actualización E2E que sigue más abajo; la reunión/decisión del Product Owner no se ha registrado.

> **Estado Jira antes del rebase funcional (corte histórico):** la meta era pedidos/MFA y el sprint activo incluía ECO-9, ECO-16 y ECO-20. Esta instantánea explica por qué esas historias ya completadas salieron del Sprint 2 cuando se alineó a flota; no describe el estado actual.

> **Verificación de regresión posterior (09/10/2026, 10:15, hora de Lima):** se volvieron a ejecutar las suites disponibles y aprobaron 100 pruebas de backend y 39 de frontend. Las pruebas existentes no cubren la integración de `PedidosPostgresRepository` con PostGIS; la permanencia del pedido tras reiniciar se respalda con la comprobación manual aislada descrita en la revisión del Sprint 2.

> **Verificación de ejecución (09/10/2026, 08:51, hora de Lima):** el frontend en http://localhost:3000/ respondió HTTP 200 con HTML en español; la API en http://localhost:8000/openapi.json respondió HTTP 200 y entregó el esquema OpenAPI.

> **Rebase funcional e implementación posterior (09/10/2026):** la línea base acordada mantiene MFA/roles y pedidos persistentes en Sprint 1, mueve flota a Sprint 2 y generación/consulta de rutas a Sprint 3; Sprint 4 conserva la ejecución de ruta por Conducción. Se añadieron API, modelo persistente, reglas, pantalla y migración de flota. La migración `20261009_02` quedó aplicada en la base local; el recorrido autenticado de alta y disponibilidad se comprobó en un PostGIS temporal aislado, incluyendo consulta tras reiniciar la API. El detalle y los criterios vigentes están en el [plan funcional](../02%20Planificaci%C3%B3n/05%20Plan%20funcional%20de%20sprints.md). Los resultados Jira y del corte histórico que siguen en esta auditoría no se reescriben.

> **E2E web Sprint 1 y 2 (09/10/2026, primera comprobación):** en la pestaña local `http://localhost:3000/` se completó el acceso MFA, el alta y la consulta de un vehículo, la declaración de disponibilidad, y el registro, búsqueda, detalle y recarga persistente de un pedido; se reinició la API entre lecturas. Para la prueba se usaron una API y una base PostGIS temporales aisladas, ya que el proceso preexistente en `127.0.0.1:8000` no exponía Flota. Al terminar se cerró la sesión temporal y se retiraron el contenedor, las cuentas y los datos E2E. Después se dejó activo el código actual de la API en `[::1]:8000`, usando la base y las cuentas locales existentes; `localhost` resuelve primero a `::1` en este equipo y la pestaña vuelve a la pantalla de acceso. La ruta protegida `/api/v1/vehiculos` responde `401` sin sesión, mientras el proceso antiguo de IPv4 sigue respondiendo `404` en esa ruta. La base local conserva la migración `20261009_02` y cero vehículos/pedidos de prueba. Esta primera comprobación todavía no cubría todos los criterios de flota; su resultado de aceptación se completa en la actualización siguiente.

> **Actualización de aceptación E2E de flota (09/10/2026):** se amplió la comprobación hasta cubrir los cinco criterios de aceptación del alcance vigente de Sprint 2 y los cinco aprobaron. El flujo navegador verificó normalización y duplicados, edición y validaciones, turno y motivo obligatorio, inelegibilidad de Mantenimiento/Inactivo con turnos ya registrados y persistencia después de reiniciar la API. La relectura posterior al reinicio devolvió los tres vehículos y su disponibilidad desde el PostGIS temporal aislado. Se retiraron las cuentas y los datos E2E; la base local sigue sin registros de prueba. Por tanto, el E2E **sí acepta el incremento funcional de Sprint 2** conforme a esos criterios. Esta conclusión no dice que haya ocurrido la reunión prevista ni que el Product Owner o Jira hayan registrado una aceptación/cierre formal.

> **Regresión final del código (09/10/2026):** aprobaron las 107 pruebas recolectadas del backend y las 39 pruebas existentes de frontend; `npm run build` completó. `npm run lint` terminó con dos advertencias por actualizaciones de estado dentro de efectos (`PaginaPedidos` y `PaginaFlota`); la compilación informa que los archivos de Codec Pro referenciados no están presentes. El preflight `PUT` a la API desde `http://localhost:3000` recibió `200` y devolvió CORS permitido; Alembic reporta `20261009_02 (head)`, la base local tiene cero pedidos y vehículos y `git diff --check` no detectó errores.

> **Alineación documental y Jira (09/10/2026, 13:00 hora de Lima):** Sprint 1 conserva su compromiso y corte históricos (0/2 al 28/09; la métrica dinámica actual es 1/2 por ECO-9 y ECO-15 pendiente). MFA y pedidos persistentes se mantienen como la línea base funcional vigente, con ECO-16 y ECO-20 completadas en backlog porque no pueden añadirse al sprint cerrado. Sprint 2 se alineó a flota; ECO-12 y ECO-19 quedaron `Listo`, 2/2 y 10 puntos, con Sprint 2 todavía activo hasta la revisión/cierre administrativo. ECO-21 se corrigió para dejar solo cuentas, TOTP y rutas. La configuración de las cinco columnas del tablero sigue pendiente.

- Se unifican al español las etiquetas de roles y las menciones genéricas a partes interesadas en README y artefactos afectados; se mantienen los nombres propios de herramientas, tecnologías y estándares.
- Se corrige la concordancia gramatical en ocho referencias a partes interesadas detectadas en los informes y revisiones de Sprint 1 y Sprint 2.

## Idioma, identidad y stack comunes

- La documentación de producto y planificación en `README.md`, `docs/`, las plantillas de GitHub y OpenSpec está redactada en español. El 09/10 también se localizaron al español los seis comandos `.claude/commands/opsx` y sus seis habilidades `.claude/skills/openspec-*`; se conservaron los identificadores de comandos, campos JSON, estados de la CLI, la categoría de metadatos `Workflow` y los encabezados estructurales que forman parte del contrato de OpenSpec. `openspec/config.yaml` exige `es`; las especificaciones mantienen `SHALL`/`MUST` y `WHEN`/`THEN` donde los requiere el formato.
- El nombre del integrante se normaliza en la documentación como **Anco Porras, Jhean Pier Julio**.
- Las cuentas `@ecologistica.test` descritas para el acceso son solo de demostración local; no representan conexión con el correo institucional. El inicio de sesión aclara ahora que se usa una cuenta de acceso del sistema.
- La línea base vigente es **React + Vite + TypeScript** en el frontend y **FastAPI + Python** en la API. La propuesta de Next.js/Nest.js se revirtió el 02/10/2026 y no es una alternativa vigente.
- En el corte inicial de esta auditoría, PostgreSQL/PostGIS, Docker Compose, Leaflet/OpenStreetMap y el motor Python de optimización figuraban como pendientes. Las actualizaciones posteriores incorporaron persistencia PostGIS para pedidos y ubicaciones, además de vehículos y disponibilidades mediante `20261009_02`; mapas y optimización continúan pendientes.
- Jira (ECO), GitHub y OpenSpec cubren seguimiento, repositorio y especificaciones. Docker Compose provisiona solo la base PostGIS local; los adaptadores actuales persisten pedidos y flota, mientras rutas, mapas, optimización y CI continúan pendientes.
- En el corte inicial, `database/` aún no existía. Después se añadieron `20261009_01` para pedidos/ubicaciones y `20261009_02` para flota. `docs/04 Seguimiento y Control/` y `docs/05 Cierre/` siguen reservados y sin entregables; el README distingue esas carpetas de la documentación pendiente.
- El diagrama de módulos del README queda etiquetado como alcance objetivo y enumera por separado los módulos implementados y los pendientes al 09/10.
- `.env.example` y las instrucciones de instalación se contrastaron con `backend/src/app/config.py`, `frontend/vite.config.ts` y `frontend/package-lock.json`: se eliminaron variables de base de datos, mapas y optimización que el código actual ignora, se documentaron solo variables operativas y se actualizaron los comandos de PowerShell y el requisito real de Node para Vite 8.
- El flujo de ramas se armonizó en README, OpenSpec, RES-17 y RST-ACA-02: ramas breves `feature/*` desde `main`, PR hacia `main`, sin `develop` obligatoria. La consulta Git del 09/10 muestra `developer` 29 commits detrás de `main` y sin commits propios; `docs/semana-3-entregables` está 45 commits detrás y 1 por delante, con un commit del 04/09 que añadió versiones iniciales de ocho documentos de Inicio ahora presentes y revisados en `main`. No se integran ni eliminan ramas remotas sin confirmar su destino con el equipo. La protección de `main`, revisión obligatoria y CI siguen pendientes; `gh auth status` indica que esta sesión no está autenticada y no permitió leer la configuración de protección.
- Las referencias a `develop` en informe de estado, la revisión y la retrospectiva del Sprint 1 se conservan como acuerdos históricos de esa fecha; las tareas futuras de los documentos de Sprint 2 ya apuntan al flujo actualizado. No se deben interpretar esas referencias antiguas como configuración vigente.

## Plan y resultado hasta el Sprint 2

| Iteración | Plan registrado | Resultado comprobado al 09/10/2026 |
|---|---|---|
| Sprint 1 · 14/09–28/09 | ECO-9 / HU-001 y ECO-15 / HU-006; 10 puntos. | El informe del Sprint 1 registra 0 de 2 al corte planificado del 28/09. Jira mantuvo el sprint id. 36 activo hasta el 09/10 a las 07:42. El historial de ECO-9 muestra `Listo` el 02/10, `Por hacer` al cerrarse el Sprint 1 y nuevamente `Listo` a las 07:43 al añadirse al Sprint 2; ECO-15 sigue `Por hacer`. La métrica dinámica actual de Jira muestra 1 de 2 y no reconstruye la velocidad al 28/09. |
| Sprint 2 · 29/09–12/10 | Meta vigente tras la rebase: Administración gestiona vehículos; Planificación configura disponibilidad. | Jira sprint id. 37 activo con ECO-12 y ECO-19 en `Listo` (2/2; 10 puntos estimados). El E2E funcional aprobó 5/5 criterios. La revisión está programada para las 15:40 y el sprint sigue activo hasta el cierre administrativo. |
| Sprint 3 | Línea base funcional vigente: Planificación asigna pedidos pendientes a vehículos elegibles y genera/consulta una ruta guardada. | Flota y su persistencia se completaron en Sprint 2; quedan persistencia de rutas/paradas, generación factible, integración y medición. El contenido y la fecha del Sprint 3 siguen sin aprobación en Jira. |
| Sprint 4 y cierre | El horizonte aprobado contempla cuatro iteraciones y una semana de cierre; el roadmap conserva dashboard, visor, seguridad, disponibilidad e integración/aceptación. | Alcance futuro de alto nivel; prioridades, compromisos y fechas detalladas del Sprint 4 aún no están aprobados. |

Para mantener el trabajo futuro centrado en lo que alguien podrá hacer en la aplicación, se añadió el [Plan funcional de sprints](../02%20Planificaci%C3%B3n/05%20Plan%20funcional%20de%20sprints.md). Allí se distingue el Sprint 1 histórico, el recorrido que ya ofrece Sprint 2 y las propuestas de Sprint 3 y 4, que todavía deben acordarse. La definición de cierre de sprint ya no exige desplegar cada historia a staging; la salida operativa del PMV mantiene sus propios requisitos.

El plan funcional ahora incluye criterios de revisión ligados a HU-003, HU-004, HU-005, HU-006, HU-009, HU-010 y EN-001/EN-005. Flota y disponibilidad ya se aceptaron funcionalmente en Sprint 2; el recorrido de rutas requiere persistencia de rutas/paradas, generación, integración y medición, sin tratar componentes técnicos aislados como entregas de valor. La capacidad y las fechas de Sprint 3 y 4 siguen por estimar y aprobar.

El [informe del Sprint 2](Sprint%202/01%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md) sitúa en Sprint 3 el recorrido de generar y consultar rutas. La persistencia de rutas/paradas, el optimizador y la integración quedan como trabajo de ese recorrido; la flota proviene del Sprint 2 reorientado a ese objetivo.

La [revisión del Sprint 2](Sprint%202/03%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) conserva la pauta de revisión del incremento de pedidos y registra el E2E posterior de flota: sus cinco criterios funcionales aprobaron. La reunión, la decisión formal del Product Owner y el cierre administrativo de Jira siguen pendientes; no se confunden con el resultado técnico de aceptación.

El 09/10 se verificó el recorrido API de Sprint 2 en una instancia temporal separada: MFA, registro, consulta y rechazo de una ventana inválida. La cuenta y el pedido de prueba se eliminaron con el almacenamiento aislado. El resultado no se presenta como validación visual del frontend ni como aceptación formal.

La consulta de Jira del 09/10 no encontró incidencias asignadas a un sprint futuro. El plan funcional registra el tamaño observado y el aún propuesto del flujo de rutas, y advierte que el conjunto podría exceder la capacidad: el equipo debe revisar esa cifra en el Planning antes de fijar Sprint 3.

El plan también deja enlazados el acceso MFA, el formulario de pedidos, su API, la lista y el detalle con los archivos donde viven. El ensayo de pedidos del 02/10 se conserva como histórico; la aceptación funcional del alcance actual de flota quedó acreditada después con el E2E 5/5. La reunión y el registro formal siguen pendientes.

El backend registra **tres advertencias deprecadas** durante `pytest`. La compilación frontend concluye, pero avisa que los archivos licenciados Codec Pro `.woff2` no están disponibles. La compilación y las pruebas no prueban una revisión visual extremo a extremo ni despliegue continuo.

## Consistencia de calendario y presupuesto

- El Acta y el README fijan 14 semanas de desarrollo más una de cierre y cuatro iteraciones. Los documentos de Sprint 1 y 2 usan periodos consecutivos de dos semanas dentro de septiembre–octubre. La palabra *iteración* del calendario presupuestario no está definida frente a los *sprints* Scrum; se conservan las fechas reales de Sprint 1 y 2 y no se asignan compromisos a Sprint 3 hasta acordar ese mapeo.
- El Acta establece un techo de autorización de S/ 500,000 y una reserva máxima de S/ 35,000; el presupuesto detallado calcula S/ 54,538.40, con una reserva estimada de S/ 5,843.40. Se documenta como techo versus estimado detallado, no como dos gastos ejecutados. El gasto real reportado al cierre de Sprint 1 es S/ 0 en infraestructura.

## Estado real de Jira `ECO`

El tablero consultado fue `ECO board` (id. 2). En el corte inicial Jira devolvía 8 tarjetas de tipo Epic, 9 historias y 2 tareas; `ECO-7` duplica la épica de re-enrutamiento `ECO-6`, por lo que el backlog tiene 7 épicas lógicas EP-01–EP-07. Después se creó ECO-21, que eleva a 3 las tareas. ECO-20 continúa sin puntos aprobados ni persona asignada.

**Estado actual después de la rebase (09/10/2026, 13:00 hora de Lima):** Sprint 1 (id. 36) sigue cerrado y conserva sus incidencias históricas; la métrica dinámica muestra 1/2 (ECO-9 `Listo`, ECO-15 `Por hacer`), mientras el informe del corte del 28/09 registra 0/2. Los habilitadores completados de pedidos y MFA (ECO-16 y ECO-20) permanecen en el backlog porque Jira no permite añadirlos al sprint cerrado; ECO-20 lleva la etiqueta `sprint1`. Sprint 2 (id. 37) tiene meta de flota y ECO-12/ECO-19 en `Listo` (2/2, 10 puntos), con estado activo hasta su cierre administrativo. ECO-21 queda limitado a cuentas, TOTP y rutas; ECO-15 sigue pendiente en el backlog para iteraciones posteriores.

Los puntos numerados siguientes describen el estado anterior a la rebase, consultado al inicio del 09/10, y se conservan para explicar las transiciones; no representan la configuración vigente.

1. El sprint id. 36 es el Sprint 1 oficial; se cerró administrativamente el 09/10 después de su fecha final del 28/09. El sprint id. 3 se renombró `ECO Sprint 1 (duplicado)` y su objetivo aclara que no es el sprint oficial. El historial de ECO-9 registra `Listo` el 02/10, `Por hacer` al cierre del Sprint 1 y `Listo` otra vez después de añadirse al Sprint 2. El informe dinámico actual cuenta la incidencia en Sprint 1 por el estado vigente y la asociación doble; el conector no expone el reporte histórico al 28/09.
2. En la consulta previa a la rebase, Sprint 2 id. 37 tenía ECO-9, ECO-16 y ECO-20 para pedidos/MFA. La rebase retiró esas incidencias del sprint activo y lo orientó a flota; el detalle vigente se resume arriba.
3. ECO-15 / HU-006 está en `Por hacer`: no se encontró implementación de re-enrutamiento en el repositorio. Su historial de Sprint conserva la asignación al Sprint 1.
4. El backlog no contiene HU-004, HU-010, HU-011 ni EN-001–EN-004. ECO-17 está estimada en 5 puntos. ECO-21 se creó originalmente sin estimación para cuentas, TOTP, flota y rutas; después de persistir la flota, su alcance vigente excluye ese componente y conserva cuentas, TOTP y rutas.
5. El tablero conserva cinco columnas (`Por hacer`, `En curso`, `Listo`, `In Review / QA`, `Done`). `Listo` está mapeado a una categoría completada; `Done` está mapeado al estado `Finalizada`, que la configuración devuelve con categoría nueva.
6. La consulta de versiones del proyecto devuelve cero; `v1.0.0-MVP` no existe como versión Jira.
7. ECO-20 se creó el 09/10 bajo EP-07 para registrar autenticación MFA; quedó sin estimación ni persona asignada y en `Listo`, con criterios vinculados a RF-11.1.
8. Las descripciones de ECO-16 y ECO-17 mencionaban Next.js/Nest.js. Se actualizaron el 09/10 para indicar React/Vite y FastAPI, documentar el estado real y mantener PostgreSQL/CI como pendientes.
9. La verificación del 09/10 mostró que la configuración de cinco columnas y la ausencia de versiones de entrega persisten, pese a la confirmación comunicada el 02/10. Se reabrió IMP-003 y se incorporó al registro del Sprint 2.
10. En la actualización posterior del 09/10, ECO-16 se reespecificó y agregó al Sprint 2 como persistencia funcional de pedidos y ubicaciones; ECO-21 separa el trabajo restante de EN-005. La meta de Sprint 2 ya pide comprobar los datos después de reiniciar la API.

La imagen histórica que antes se llamaba `05-releases.png` muestra un resumen analítico del proyecto, no una versión de Jira. Se renombró a `05-resumen-analitico-historico.png`; la evidencia actual de versiones sigue pendiente.

## Documentos contrastados

- `README.md` y la guía de ejecución local.
- Los 13 documentos de Inicio, los 5 de Planificación y los 8 entregables de Sprint 1 y Sprint 2.
- `openspec/config.yaml`, los dos cambios archivados y las especificaciones vigentes de pedidos y autenticación.
- El nuevo plan funcional de sprints y su enlace desde README y documentos de planificación.
- Los seis comandos y seis habilidades operativas de OpenSpec en `.claude/`, incluida su estructura de metadatos.
- `backend/requirements.txt`, `frontend/package.json`, fuentes actuales, scripts de pruebas y estructura de `.github/`.
- Tablero, sprints, backlog, configuración de columnas, versiones y tarjetas ECO-16/ECO-17 en Jira.

En la revisión estática se recorrieron los 54 archivos Markdown versionados: no se encontraron enlaces locales rotos ni caracteres de reemplazo. La primera comprobación detectó que tres documentos versionados de Inicio y Planificación no tenían historial de cambios; se incorporó la trazabilidad sin atribuir autoría a sus primeras emisiones. Después de esa regularización, todos los documentos de `docs/` con número de versión tienen una entrada de historial coincidente con sus metadatos.

Esta actualización añade un documento de Planificación y deja el total en 55 archivos Markdown versionados. El plan nuevo y sus enlaces desde README y los documentos relacionados se comprobaron junto con esta actualización.

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
- Completar la persistencia de cuentas y rutas; implementar y verificar los recorridos de mapas, optimización, dashboard y CI según el plan funcional. La persistencia de flota ya quedó implementada y comprobada.

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
| 1.16.0 | 09/10/2026 | Se identifican como históricos los planes de rama develop y estructura database/ del Sprint 1, manteniendo la descripción vigente del proyecto y del repositorio. |
| 1.17.0 | 09/10/2026 | Se completa la auditoría de los 55 Markdown versionados, se actualiza el estado de persistencia de flota y se alinea la documentación a Sprint 1 pedidos, Sprint 2 flota y Sprint 3 rutas. |
| 1.17.1 | 09/10/2026 | Se añade evidencia HTTP del frontend y la API levantados en local a las 08:51, hora de Lima. |
| 1.18.0 | 09/10/2026 | Se unifican al español las etiquetas de roles y las menciones genéricas a partes interesadas, preservando nombres propios y términos técnicos. |
| 1.19.0 | 09/10/2026 | Se corrigen ocho referencias con concordancia gramatical incorrecta a las partes interesadas en los informes y revisiones de Sprint 1 y Sprint 2. |
| 1.20.0 | 09/10/2026 | Se completa el historial de cambios de tres documentos de Inicio y Planificación y se actualiza la verificación de los 54 archivos Markdown versionados. |
| 1.21.0 | 09/10/2026 | Se alinea la planificación futura a recorridos de usuario, se documentan los límites funcionales del Sprint 2 y se registra el plan funcional de sprints; la revisión del Sprint 2 sigue pendiente. |
| 1.22.0 | 09/10/2026 | Se alinea la acción de planificación del Sprint 3 y su fila de auditoría al flujo completo propuesto para Planificación. |
| 1.23.0 | 09/10/2026 | Se amplían los criterios funcionales de las propuestas de Sprint 3 y 4 y se los enlaza con las historias existentes del backlog. |
| 1.24.0 | 09/10/2026 | Se diferencia la evidencia de implementación de HU-001 y MFA de la aceptación formal del Sprint 2, todavía pendiente de la reunión prevista. |
| 1.25.0 | 09/10/2026 | Se ajusta el informe de Sprint 2 para plantear el trabajo futuro como un flujo completo de generación de rutas y no como una lista de componentes técnicos. |
| 1.26.0 | 09/10/2026 | Se prepara el registro de revisión de Sprint 2 con criterios funcionales y espacios vacíos para la decisión y los acuerdos reales. |
| 1.27.0 | 09/10/2026 | Se contrasta el backlog candidato de Sprint 3 con Jira y se deja explícito que su estimación total aún no es un compromiso de equipo. |
| 1.28.0 | 09/10/2026 | Se actualiza el plan funcional con el estado y el tamaño observado del backlog candidato de Sprint 4, manteniendo pendiente su Planning. |
| 1.29.0 | 09/10/2026 | Se añade trazabilidad desde el flujo funcional de Sprint 2 hacia su código y la evidencia del ensayo histórico. |
| 1.30.0 | 09/10/2026 | Se documenta la comprobación API aislada de Sprint 2 y se distingue del ensayo visual histórico y de la aceptación formal pendiente. |
| 1.31.0 | 09/10/2026 | Se actualiza el corte de implementación: pedidos y ubicaciones ya se persisten en PostgreSQL/PostGIS; se corrigen referencias que aún lo marcaban pendiente. |
| 1.32.0 | 09/10/2026 | Se actualizan Jira y los documentos de Sprint 2: ECO-16 entra en el sprint para persistencia de pedidos, y ECO-21 registra el alcance pendiente de EN-005. |
| 1.33.0 | 09/10/2026 | Se registra la rebase funcional acordada y la comprobación posterior del incremento de flota en PostgreSQL aislado. |
| 1.33.1 | 09/10/2026 | Se registra la regresión aprobada después del cambio PostGIS y se aclara qué cobertura automatizada sigue pendiente. |
| 1.34.0 | 09/10/2026 | Se registra la E2E web de Sprint 1 y 2 en entornos aislados y el límite del proceso API preexistente en IPv4. |
| 1.35.0 | 09/10/2026 | Se actualiza el estado de ejecución: API vigente activa en IPv6 y proceso anterior de IPv4 identificado como obsoleto para Flota. |
| 1.36.0 | 09/10/2026 | Se actualizan la verificación completa, el CORS, la migración activa y los documentos de Sprint 2 para reflejar la E2E de flota. |
| 1.37.0 | 09/10/2026 | Se registran los resultados actuales de suites, compilación, lint, CORS y estado limpio de datos locales. |
| 1.38.0 | 09/10/2026 | Se corrigen dos contradicciones sobre persistencia de flota y ECO-21, se diferencia la aceptación funcional E2E de la formal y se completan las comprobaciones de enlaces y versiones. |
| 1.39.0 | 09/10/2026 | Se incorpora la especificación principal OpenSpec de flota, basada en los contratos y reglas implementados, y se enlaza desde el plan funcional. |
| 1.40.0 | 09/10/2026 | Se corrige una versión duplicada del historial del plan funcional, se alinea su metadato y se verifica de nuevo la unicidad de versiones.
| 1.41.0 | 09/10/2026 | Se amplía el conteo y la comprobación de enlaces a los 56 Markdown presentes, incluida la especificación principal nueva de flota.
