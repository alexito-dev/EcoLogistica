# 05. Plan funcional de sprints

[← Volver al README Principal](../../README.md)

## Metadatos

| Campo | Valor |
|---|---|
| Proyecto | EcoLogística Huancayo |
| Versión | 1.13.0 |
| Fecha | 09/10/2026 |
| Enfoque | Cada sprint debe dejar una tarea real que una persona pueda completar en el sistema. |

## Para qué sirve este plan

La meta de cada sprint se escribe como una acción que alguien podrá hacer en la aplicación. La base de datos, los mapas, el motor de rutas y la automatización son parte del trabajo cuando hacen falta para completar esa acción; por sí solos no cuentan como resultado funcional del sprint.

Este plan ordena lo que ya ocurrió y propone cómo continuar. Los compromisos futuros todavía necesitan conversación, estimación y acuerdo del equipo en Jira. No se asignan puntos ni fechas que el equipo no haya aprobado.

## Línea base funcional acordada el 09/10/2026

La distribución funcional vigente queda así: Sprint 1 reúne acceso MFA y roles, pedidos y persistencia PostGIS; Sprint 2, gestión de flota; Sprint 3, generación y consulta de rutas; los sprints posteriores mantienen sus objetivos. La rebase del 09/10 se reflejó en las metas y asignaciones disponibles de Jira. El Sprint 1 ya estaba cerrado, así que su asignación y su resultado histórico al corte del 28/09 se conservan; los incrementos de MFA y persistencia se muestran como completados en el backlog, sin imputarlos retroactivamente a ese corte.

## Sprints y resultado para quien usa el sistema

| Sprint | Acción que se busca habilitar | Estado con evidencia al 09/10/2026 |
|---|---|---|
| **Sprint 1** · 14/09–28/09; cerrado 09/10 | Que Planificación entre con MFA y roles, registre pedidos, los consulte y conserve los datos tras reiniciar la API. | El incremento funcional está implementado y comprobado. El corte original del 28/09 queda en 0/2 historias: ECO-15 sigue pendiente y el trabajo incorporado por la rebase posterior no se cuenta como velocidad histórica. ECO-9 sigue mostrando su historial de asignación original; ECO-16 y ECO-20 quedaron completadas en el backlog porque Jira no permite añadirlas al sprint cerrado. |
| **Sprint 2** · 29/09–13/10, alcance reordenado | Que Administración mantenga vehículos y que Planificación configure disponibilidad y turno por fecha para determinar unidades elegibles. | **Criterios E2E de flota aprobados el 09/10/2026** en navegador con MFA, API y PostGIS temporales: alta/edición y unicidad, validaciones, disponibilidad con motivo, exclusión de mantenimiento/inactivos y persistencia tras reiniciar. Jira ya refleja ECO-12 y ECO-19 en `Listo` (2/2 historias, 10 puntos). El usuario confirmó el 09/10 la aprobación del incremento; Jira mantiene el sprint activo hasta su cierre administrativo. |
| **Sprint 3** · siguiente alcance, fechas por acordar | Que Planificación genere una ruta guardada a partir de pedidos pendientes y vehículos elegibles, y vuelva a consultar el orden de paradas, cargas y ventanas horarias. | Requiere persistir rutas y paradas, aplicar capacidades y turnos de la flota de Sprint 2 y generar una secuencia factible. El optimizador y la medición de rendimiento forman parte del recorrido; no se cuentan como entrega aparte. Alcance, estimación y fechas se acuerdan en Jira. |
| **Sprint 4** · propósito conservado | Que una persona conductora consulte su ruta, marque el avance de las entregas y reporte incidencias para que Planificación pueda actuar. | Se mantiene el propósito anterior: ejecución de ruta por Conducción y visibilidad de estados/incidencias para Planificación. Mapa y re-enrutamiento se incorporan según el alcance acordado para completar el recorrido. |

## Qué debe poder hacerse al terminar Sprint 2: gestión de flota

Administración registra y actualiza vehículos con placa única, tipo, capacidades en kg y m³, combustible, consumo y estado. Planificación declara por fecha el turno, disponibilidad y cualquier nota de restricción que haya verificado con la operación. La pantalla muestra qué unidades tienen turno declarado y cuáles son elegibles para planificar ese día. La aplicación almacena los datos en PostgreSQL.

**Criterios de revisión:**

1. Administración crea y edita un vehículo; la placa se normaliza y no se permiten duplicados.
2. Se rechazan capacidades o consumo no positivos y un turno cuya hora final no sea posterior a la inicial.
3. Planificación declara disponibilidad y horario para una fecha; una unidad no disponible requiere motivo.
4. Una unidad en mantenimiento o inactiva no aparece como elegible aunque tenga una disponibilidad ingresada.
5. Vehículos y disponibilidad siguen presentes al reiniciar la API.

La nota de circulación es información ingresada por el usuario; el sistema no inventa ni valida normativa vial. Las rutas todavía no se generan en este sprint.

**Resultado E2E del Sprint 2 (09/10/2026):** los cinco criterios anteriores se comprobaron de punta a punta en la interfaz web. Se creó `S2-E2E-A1`, se normalizó la placa y se rechazó un duplicado; se editaron sus datos y se rechazaron valores no positivos y un turno invertido; una disponibilidad desactivada exigió motivo; los vehículos `S2-E2E-B2` (Mantenimiento) y `S2-E2E-C3` (Inactivo) conservaron un turno registrado sin ser elegibles; `S2-E2E-A1` quedó elegible. Tras reiniciar la API, se recargó la flota desde la misma base temporal y se observaron los tres vehículos, turnos y estados. El contenedor, las cuentas y los datos de prueba se retiraron al acabar; la base local no recibió esos registros. Esta aprobación cubre los criterios funcionales E2E definidos aquí; no afirma que se haya celebrado una reunión o registrado la decisión formal del Product Owner.

Implementación para revisar: [pantalla de flota](../../frontend/src/pages/PaginaFlota.tsx), [cliente API](../../frontend/src/api/flota.ts), [API y reglas](../../backend/src/app/flota/router.py) y [migración de PostgreSQL](../../database/migrations/versions/20261009_02_flota.py). Especificación funcional: [OpenSpec de flota](../../openspec/specs/flota/spec.md).

## Qué debe poder hacerse al terminar Sprint 3

**Meta:** Planificación elige pedidos pendientes y solicita una ruta que después puede volver a abrir.

Para lograrlo, el equipo completa la generación de ruta (HU-004) y persistencia de rutas/paradas (EN-005), usando la flota y las disponibilidades configuradas en Sprint 2. El benchmark (EN-001) comprueba que la ruta se calcule dentro del tiempo acordado. El resultado visible es la ruta que Planificación puede revisar y volver a abrir.

**Criterios para revisar la propuesta:**

1. Planificación elige pedidos pendientes y el sistema considera únicamente vehículos y turnos elegibles.
2. Con pedidos pendientes y vehículos disponibles, Planificación solicita una ruta y el sistema muestra el vehículo elegido, el orden de las paradas, la carga y las ventanas horarias que tuvo en cuenta.
3. La ruta queda guardada y sigue apareciendo después de reiniciar la aplicación.
4. Si no hay una combinación posible, el sistema explica qué pedido, ventana o capacidad impide crearla; no asigna una ruta parcial como si estuviera lista.
5. La generación se mide contra el objetivo de tiempo del backlog (≤45 segundos) usando el volumen y los casos que el equipo acuerde para EN-001. No se publica un resultado de rendimiento hasta medirlo.

En la demo se empieza con pedidos reales ingresados durante la revisión o con datos claramente identificados como datos de prueba; no se presentan ejemplos ficticios como operaciones de DistriRápido. Esta propuesta todavía necesita estimación, capacidad y aprobación del equipo antes de convertirse en compromiso de Jira.

### Tamaño y estado actual del trabajo candidato

La consulta de Jira del 09/10 muestra los ítems siguientes en `Por hacer`; ninguno está asignado a un sprint futuro. La búsqueda de incidencias en `futureSprints()` no devolvió resultados.

| Parte del flujo | Historia o tarea | Estado en Jira | Puntos observados | Nota |
|---|---|---|---:|---|
| Completar EN-005 para cuentas y rutas | EN-005 / [ECO-21](https://continental-team-ecologistica.atlassian.net/browse/ECO-21) | Por hacer | Sin estimación | ECO-16 ya cubre pedidos y ubicaciones; `20261009_02` añade persistencia de flota. ECO-21 sigue pendiente para cuentas, TOTP y rutas, sin estimar ni asignar a un sprint. |
| Generar la ruta | HU-004 | No creada | 8 propuestos | El puntaje aparece en el backlog documental; el equipo aún no lo aprueba. |
| Medir el tiempo de generación | EN-001 | No creada | 5 propuestos | El puntaje es propuesta documental, no estimación acordada. |
| Ejecutar CI en cada cambio | EN-006 / ECO-17 | Por hacer | 5 | Ayuda a revisar el incremento, pero no es por sí misma la función de Planificación. |

HU-003 / ECO-12 y HU-009 / ECO-19 están ahora asignadas al Sprint 2 y en `Listo`; sus 10 puntos corresponden al trabajo registrado en Jira, no a una estimación nueva. La implementación de vehículos, capacidades, restricciones y disponibilidad aprobó los cinco criterios E2E. La cifra anterior de 23 puntos describía un candidato que agrupaba flota y rutas antes del reordenamiento y no debe usarse como estimación de Sprint 3. El Sprint 3 sigue requiriendo Planning para acordar capacidad, meta, puntos y fechas.

## Qué tendría que poder hacerse al terminar Sprint 4

**Meta propuesta:** Conducción abre su ruta asignada, marca el avance de cada entrega y reporta una incidencia; Planificación puede ver el cambio y actuar.

El flujo reúne la consulta de la ruta en el mapa (HU-005), el registro de estados de entrega (HU-010) y, si el equipo confirma su alcance, el re-enrutamiento ante una incidencia (HU-006). Son propuestas basadas en el backlog existente, no historias ya aceptadas para el Sprint 4.

**Criterios para revisar la propuesta:**

1. La persona conductora solo ve la ruta que tiene asignada y puede consultar sus paradas en orden.
2. Puede marcar el estado permitido para cada entrega —`En ruta`, `Entregado`, `Incidencia` o `Cancelado`, según la HU-010— y el cambio se conserva.
3. Al reportar una incidencia en una ruta activa, Planificación ve cuál fue el problema. Si se habilita el re-enrutamiento, el sistema presenta la nueva secuencia y conserva el historial de lo ya entregado.
4. Un pedido o una ruta que no se pueden reasignar se muestran con una explicación; el sistema no oculta la incidencia ni cambia silenciosamente el plan.
5. Los indicadores de puntualidad, distancia o emisiones solo se muestran como resultados cuando se calculan con datos y reglas acordados; no se rellenan con cifras inventadas.

La decisión de incluir mapa, re-enrutamiento y comparación de rutas debe tomarse en el Planning después de estimar HU-005, HU-006, HU-010 y HU-011 y revisar las dependencias con lo entregado en Sprint 3.

### Tamaño y estado actual del trabajo candidato

La consulta de Jira del 09/10 tampoco encontró trabajo en un sprint futuro para este flujo. El backlog actual queda así:

| Parte del recorrido | Historia | Estado en Jira | Puntos observados | Nota |
|---|---|---|---:|---|
| Ver la ruta y sus paradas en el mapa | HU-005 / ECO-13 | Por hacer | 3 | Existe en Jira; depende de que Sprint 3 entregue una ruta. |
| Registrar y consultar estados de entrega | HU-010 | No creada | 5 propuestos | Puntaje del backlog documental; requiere aprobación y tarjeta Jira. |
| Recalcular la ruta ante una incidencia | HU-006 / ECO-15 | Por hacer | 5 | Existe en Jira; depende del motor y de una ruta activa. |
| Comparar ruta optimizada con línea base manual | HU-011 | No creada | 5 propuestos | Puntaje del backlog documental; requiere confirmar datos y medición. |

El recorrido central de mapa, avance y re-enrutamiento suma **13 puntos candidatos**, de los cuales 5 corresponden a una historia sin tarjeta ni estimación aprobada. Comparar resultados (HU-011) añadiría otros 5 puntos propuestos. Son cifras para revisar, no compromiso ni capacidad confirmada. El Planning debe acordar qué parte completa el recorrido de Conducción y qué puede esperar; los indicadores se mostrarán solo cuando existan datos y reglas de cálculo acordados.

## Qué incluye hoy el incremento vigente de Sprint 1

Una persona de Planificación puede abrir la aplicación, autenticarse con contraseña y TOTP, registrar un pedido con dirección, carga y ventana horaria, y después localizarlo en la lista o abrir su detalle. Administración puede consultar pedidos, pero no registrarlos. El pedido queda guardado en PostgreSQL/PostGIS y sigue disponible tras reiniciar la API.

| Paso del recorrido | Qué hace el sistema | Implementación para revisar |
|---|---|---|
| Entrar | Pide contraseña y segundo factor; limita el acceso según el rol. | [Pantalla de acceso](../../frontend/src/auth/LoginPage.tsx) · [rutas de autenticación](../../backend/src/app/auth/router.py) |
| Registrar | Valida el pedido y sus ventanas horarias, lo crea como `PENDIENTE` y muestra el código generado. | [Formulario de pedidos](../../frontend/src/components/PedidoForm.tsx) · [casos de uso](../../backend/src/app/pedidos/service.py) · [API de pedidos](../../backend/src/app/pedidos/router.py) |
| Encontrar y consultar | Permite ver la lista, buscar o filtrar pedidos y abrir el detalle. | [Lista de pedidos](../../frontend/src/components/PedidosTable.tsx) · [detalle](../../frontend/src/components/PedidoDetalle.tsx) · [API de pedidos](../../backend/src/app/pedidos/router.py) |

La comprobación de pedidos tras reiniciar API se hizo en una base PostGIS temporal y aislada. Los documentos de seguimiento de Sprint 1 y 2 conservan sus cortes históricos; el cambio de alcance acordado se aplica a esta línea base funcional y a la ejecución actual del proyecto.

El [informe de revisión del Sprint 2](../03%20Implementaci%C3%B3n/Sprint%202/03%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) recoge el ensayo histórico del 02/10 y el E2E actual de los cinco criterios de flota ejecutado el 09/10. Los criterios funcionales de Sprint 2 están aprobados por ese E2E; no se afirma que el ensayo antiguo sea nuevo ni que se haya registrado una decisión de Product Owner en reunión.

La comprobación local del 09/10 confirmó que la interfaz responde en `http://localhost:3000/` y la API en `http://localhost:8000/openapi.json`. La captura compartida durante esta comprobación muestra la sesión de Planificación en la pantalla de Pedidos, con la lista vacía. Al autenticar por API con contraseña y TOTP, la lista respondió 200 con 0 pedidos; la ruta de sesión sin cookie sigue respondiendo 401, como debe.

La comprobación de persistencia se hizo en una base PostGIS temporal y aislada. El flujo pidió MFA, registró un pedido, lo encontró en la lista y abrió su detalle; rechazó una ventana horaria inválida (422), reinició la API y volvió a encontrar el mismo pedido. Después se detuvo y retiró el contenedor temporal junto con la cuenta de prueba. En la comprobación actual no se agregó ningún pedido: la base local sigue con 0 registros.

Una solicitud manual de ventana invertida enviada desde PowerShell devolvió 400 y no guardó nada. No se conservó el cuerpo del error, así que ese intento no permite confirmar un defecto del endpoint. Las 28 pruebas existentes de la API pasaron e incluyen el rechazo 422 para una ventana que termina antes de empezar. Si se vuelve a probar ese caso en vivo, hay que guardar el cuerpo de la respuesta para identificar con certeza el origen del 400.

En la actualización del 09/10 pasaron la suite completa de backend, las 39 pruebas de frontend y la compilación de producción. El linter terminó con dos avisos de `set-state-in-effect`, uno ya presente en la página de pedidos y otro en la carga de flota. La comprobación visual extremo a extremo de flota se hizo con MFA y roles en una base aislada; tras reiniciar la API, el vehículo y su disponibilidad continuaron visibles.

La gestión de vehículos y turnos está implementada y sus cinco criterios funcionales de aceptación aprobaron el E2E del 09/10. La prueba usó cuentas temporales y un PostGIS aislado, retirados al terminar; no quedaron vehículos E2E en la base local del proyecto. La persistencia de rutas, su generación, el mapa y el avance de entregas siguen pendientes para Sprint 3 y posteriores. Las cuentas de demostración siguen siendo locales y requieren contraseña y TOTP; no están conectadas al inicio de sesión institucional.

## Cuándo damos por útil un sprint

Antes de empezar, el equipo acuerda una meta que empiece con una acción concreta, quién la necesita y cómo se comprobará. Se completa el recorrido principal desde la interfaz y la respuesta del sistema confirma lo ocurrido. Si el flujo depende de una regla o un permiso, se comprueba también ese caso. La información sobrevive lo que la historia prometa: si el objetivo necesita guardar algo, reiniciar la aplicación no debe borrarlo.

Al cerrar, se muestra el flujo en un entorno reproducible, se enlaza evidencia en Jira, se registran defectos conocidos y se separa claramente lo terminado de lo que queda pendiente. Un servidor encendido, una tabla creada, una prueba aislada o un módulo técnico por sí solo no demuestra que la tarea de la persona ya se pueda hacer.

Esta definición sirve para juzgar el incremento de un sprint. No significa que el PMV completo esté listo para operar: su aceptación todavía debe cubrir, entre otras cosas, despliegue, respaldos, seguridad, disponibilidad, integración y los resultados medibles acordados con el negocio.

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se ordenan los sprints por la tarea que la persona podrá completar y se distingue el estado comprobado de las propuestas futuras. |
| 1.1.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se detallan los flujos propuestos para Sprint 3 y 4 con criterios de revisión ligados a las historias del backlog, sin inventar fechas ni estimaciones. |
| 1.2.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se contrasta el backlog candidato de Sprint 3 con Jira y se documenta su capacidad pendiente de revisión. |
| 1.3.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se añade el estado y tamaño observado del backlog candidato de Sprint 4, sin presentarlo como un sprint aprobado. |
| 1.4.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se vincula cada paso que ya ofrece Sprint 2 con sus archivos de implementación y con la evidencia histórica de revisión. |
| 1.5.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se incorpora una comprobación API actual y aislada del flujo MFA, registro y consulta de pedidos, distinguiéndola de la demo visual y de la aceptación del sprint. |
| 1.6.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se integra PostgreSQL/PostGIS para pedidos, se comprueba que sobreviven al reinicio y se actualiza la propuesta de Sprint 3 para completar la persistencia de flota y rutas. |
| 1.7.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se alinea el Sprint 2 con ECO-16 y la persistencia verificada; ECO-21 registra el trabajo que queda para cuentas, flota y rutas. |
| 1.8.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se registra la pantalla autenticada y la consulta real de la lista vacía; también se aclara el resultado inconcluso de una solicitud manual inválida y la cobertura de las pruebas existentes. |
| 1.9.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se acuerda Sprint 1 MFA/pedidos, Sprint 2 flota, Sprint 3 rutas y se conserva Sprint 4 para ejecución de rutas; los cortes históricos de Jira y seguimiento no se reescriben. |
| 1.10.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se retira HU-003 y HU-009 del candidato de Sprint 3 y se aclara su estado en Jira frente a la implementación ya comprobada de Sprint 2. |
| 1.11.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se completa E2E navegador y se aprueban los cinco criterios funcionales de flota de Sprint 2. |
| 1.11.1 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se registra el E2E navegador de los cinco criterios de aceptación de flota y la persistencia después de reiniciar la API. |
| 1.12.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se enlaza la especificación principal OpenSpec de flota desde el resultado y alcance de Sprint 2. |
| 1.13.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se registra la aprobación confirmada del incremento y se mantiene Sprint 2 activo hasta el cierre administrativo. |
