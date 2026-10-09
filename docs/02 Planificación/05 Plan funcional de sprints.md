# 05. Plan funcional de sprints

[← Volver al README Principal](../../README.md)

## Metadatos

| Campo | Valor |
|---|---|
| Proyecto | EcoLogística Huancayo |
| Versión | 1.6.0 |
| Fecha | 09/10/2026 |
| Enfoque | Cada sprint debe dejar una tarea real que una persona pueda completar en el sistema. |

## Para qué sirve este plan

La meta de cada sprint se escribe como una acción que alguien podrá hacer en la aplicación. La base de datos, los mapas, el motor de rutas y la automatización son parte del trabajo cuando hacen falta para completar esa acción; por sí solos no cuentan como resultado funcional del sprint.

Este plan ordena lo que ya ocurrió y propone cómo continuar. Los compromisos futuros todavía necesitan conversación, estimación y acuerdo del equipo en Jira. No se asignan puntos ni fechas que el equipo no haya aprobado.

## Sprints y resultado para quien usa el sistema

| Sprint | Acción que se busca habilitar | Estado con evidencia al 09/10/2026 |
|---|---|---|
| **Sprint 1** · 14/09–28/09 | Que Planificación registre pedidos y atienda incidencias que cambian una ruta. | El informe del corte del 28/09 registró 0 de 2 historias terminadas. ECO-15, sobre re-enrutamiento, continúa pendiente. ECO-9 se completó después y se incorporó también al Sprint 2; ese avance posterior no cambia el resultado histórico del Sprint 1. |
| **Sprint 2** · 29/09–12/10 | Que Planificación entre con contraseña y código de verificación, registre pedidos y luego pueda encontrarlos y consultar su detalle, incluso después de reiniciar la API. | La aplicación permite iniciar sesión con MFA y rol, registrar pedidos válidos, consultarlos y encontrarlos en la lista. Pedidos y coordenadas quedan en PostgreSQL/PostGIS; el recorrido se comprobó después de reiniciar la API en un entorno temporal aislado. Jira muestra ECO-9 y ECO-20 en `Listo`. El sprint sigue activo y su revisión todavía está pendiente; la aceptación formal no se da por hecha. Las cuentas de demostración siguen en el archivo local. |
| **Sprint 3** · propuesta, sin compromiso aprobado | Que Planificación registre su flota disponible, asigne pedidos pendientes y obtenga una ruta guardada para revisar. | El guardado de pedidos ya está resuelto. Para cerrar esta tarea faltan gestionar y persistir vehículos, completar las reglas de flota y generar una primera secuencia de paradas. EN-005 todavía debe cubrir las entidades que faltan; el optimizador se integra como parte de la ruta. Estimar y acordar el alcance con el equipo antes de comprometerlo en Jira. |
| **Sprint 4** · propuesta, sin alcance detallado aprobado | Que una persona conductora consulte su ruta, marque una entrega y reporte una incidencia para que Planificación pueda revisar el cambio. | Confirmar flujo y prioridades con el equipo. El mapa, el cálculo de rutas y el re-enrutamiento se suman si son necesarios para completar esa tarea, no como entregables aislados. No hay fechas ni resultados aprobados para esta propuesta. |

## Qué tendría que poder hacerse al terminar Sprint 3

**Meta propuesta:** Planificación registra la flota disponible, elige pedidos pendientes y genera una ruta que después puede volver a abrir.

Para lograrlo, el equipo tendría que trabajar juntas las historias ya definidas para configurar vehículos y restricciones (HU-003 y HU-009), generar una ruta (HU-004) y completar EN-005 para guardar la flota y las rutas. La persistencia de pedidos ya está integrada; este siguiente paso amplía el mismo almacén a las entidades necesarias. El benchmark (EN-001) ayuda a comprobar que la ruta se calcule dentro del tiempo acordado. La base de datos, el optimizador y las migraciones son parte del recorrido porque hacen posible guardar y calcular la ruta; el resultado visible sigue siendo la ruta que Planificación puede revisar.

**Criterios para revisar la propuesta:**

1. Planificación puede registrar un vehículo disponible con su capacidad y restricciones, y volver a consultar esos datos.
2. Con pedidos pendientes y vehículos disponibles, Planificación solicita una ruta y el sistema muestra el vehículo elegido, el orden de las paradas, la carga y las ventanas horarias que tuvo en cuenta.
3. La ruta queda guardada y sigue apareciendo después de reiniciar la aplicación.
4. Si no hay una combinación posible, el sistema explica qué pedido, ventana o capacidad impide crearla; no asigna una ruta parcial como si estuviera lista.
5. La generación se mide contra el objetivo de tiempo del backlog (≤45 segundos) usando el volumen y los casos que el equipo acuerde para EN-001. No se publica un resultado de rendimiento hasta medirlo.

En la demo se empieza con pedidos reales ingresados durante la revisión o con datos claramente identificados como datos de prueba; no se presentan ejemplos ficticios como operaciones de DistriRápido. Esta propuesta todavía necesita estimación, capacidad y aprobación del equipo antes de convertirse en compromiso de Jira.

### Tamaño y estado actual del trabajo candidato

La consulta de Jira del 09/10 muestra los ítems siguientes en `Por hacer`; ninguno está asignado a un sprint futuro. La búsqueda de incidencias en `futureSprints()` no devolvió resultados.

| Parte del flujo | Historia o tarea | Estado en Jira | Puntos observados | Nota |
|---|---|---|---:|---|
| Persistir vehículos y rutas; ampliar EN-005 | EN-005 / ECO-16 | Por hacer | 3 | El guardado de pedidos ya se integró; falta cubrir las entidades que se usarán para planificar rutas. |
| Registrar vehículos y su disponibilidad | HU-003 / ECO-12 | Por hacer | 5 | Existe en Jira. |
| Configurar límites y restricciones de la flota | HU-009 / ECO-19 | Por hacer | 5 | Existe en Jira. |
| Generar la ruta | HU-004 | No creada | 8 propuestos | El puntaje aparece en el backlog documental; el equipo aún no lo aprueba. |
| Medir el tiempo de generación | EN-001 | No creada | 5 propuestos | El puntaje es propuesta documental, no estimación acordada. |
| Ejecutar CI en cada cambio | EN-006 / ECO-17 | Por hacer | 5 | Ayuda a revisar el incremento, pero no es por sí misma la función de Planificación. |

La función de ruta suma **26 puntos candidatos** (13 observados en Jira y 13 todavía propuestos); si se incluye EN-006 en la misma iteración, serían 31. Estas cifras no son velocidad disponible ni compromiso de Sprint 3. Jira aún no tiene un Sprint 3 futuro, y la velocidad oficial de Sprint 2 depende de la revisión pendiente. En el Planning el equipo debe contrastar la capacidad real y acordar una meta que quepa. Si el flujo completo no cabe, hay que reordenar el alcance para que cada sprint termine con una acción útil en la aplicación; no cerrar solo la base de datos o el benchmark y llamarlo incremento funcional.

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

## Qué incluye hoy el incremento del Sprint 2

Una persona de Planificación puede abrir la aplicación, autenticarse con contraseña y TOTP, registrar un pedido con dirección, carga y ventana horaria, y después localizarlo en la lista o abrir su detalle. Administración puede consultar pedidos, pero no registrarlos. El pedido queda guardado en PostgreSQL/PostGIS y sigue disponible tras reiniciar la API.

| Paso del recorrido | Qué hace el sistema | Implementación para revisar |
|---|---|---|
| Entrar | Pide contraseña y segundo factor; limita el acceso según el rol. | [Pantalla de acceso](../../frontend/src/auth/LoginPage.tsx) · [rutas de autenticación](../../backend/src/app/auth/router.py) |
| Registrar | Valida el pedido y sus ventanas horarias, lo crea como `PENDIENTE` y muestra el código generado. | [Formulario de pedidos](../../frontend/src/components/PedidoForm.tsx) · [casos de uso](../../backend/src/app/pedidos/service.py) · [API de pedidos](../../backend/src/app/pedidos/router.py) |
| Encontrar y consultar | Permite ver la lista, buscar o filtrar pedidos y abrir el detalle. | [Lista de pedidos](../../frontend/src/components/PedidosTable.tsx) · [detalle](../../frontend/src/components/PedidoDetalle.tsx) · [API de pedidos](../../backend/src/app/pedidos/router.py) |

El [informe de revisión del Sprint 2](../03%20Implementaci%C3%B3n/Sprint%202/03%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) recoge los criterios, el ensayo manual y sus resultados. El ensayo se hizo el 02/10; no se debe presentar como una demostración nueva ni como aceptación formal de la reunión prevista para el 09/10.

La verificación local del 09/10 confirmó que la interfaz responde en `http://localhost:3000/`, que la API publica sus rutas en `http://localhost:8000/openapi.json` y que `/api/v1/auth/sesion` devuelve 401 si no hay una sesión.

La comprobación de persistencia se hizo en una base PostGIS temporal y aislada. El flujo pidió MFA, registró un pedido, lo encontró en la lista y abrió su detalle; rechazó una ventana horaria inválida (422), reinició la API y volvió a encontrar el mismo pedido. Después se detuvo y retiró el contenedor temporal junto con la cuenta de prueba. Esta comprobación cubre la API y la base; no es una prueba visual en el navegador ni reemplaza la revisión del Product Owner.

Las pruebas automatizadas y la compilación anotadas en los informes corresponden a ejecuciones anteriores; no volví a ejecutar la suite en esta verificación.

Todavía no se pueden gestionar vehículos, generar o guardar rutas, verlas en un mapa ni registrar el avance de entregas. Las cuentas de demostración siguen siendo locales y requieren contraseña y TOTP; no están conectadas al inicio de sesión institucional.

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
