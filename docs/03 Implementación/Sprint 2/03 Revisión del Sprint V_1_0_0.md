# Revisión del sprint

[← Volver al README Principal](../../../README.md)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla

**Líder del Proyecto:** Alex Jesus Zorrilla Apumayta

## Metadatos del documento

| Campo | Valor |
|---|---|
| Versión | 1.8.0 |
| Sprint | ECO Sprint 2 (inicio 29/09/2026) |
| Objetivo vigente tras el rebase | "Administración gestiona vehículos; Planificación configura su disponibilidad y turnos por fecha." |
| Reunión de revisión | Evaluación Parcial — Sprint 02, viernes 09/10/2026, 15:40–16:00 |
| Ensayo de la demostración | 02/10/2026, contra los servidores locales (resultados en la sección *Demostración*) |
| Participantes previstos | Equipo Scrum: Alex Zorrilla (líder / PM), Anco Porras, Jhean Pier Julio (backend), Alexander Daniel Hilario Talavera (optimización), Jhoanna Hade Vera Zea (frontend/UX), Jose Luis Isidro Casio (QA/DevOps). Docente asesor y *Product Owner* académico: Ing. Job Daniel Gamarra Moreno |
| Documentos hermanos | [01 Informe de estado](01%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md) · [02 Registro de Impedimentos](02%20Registro%20de%20Impedimentos%20V_1_0_0.md) · [04 Retrospectiva](04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) |
| Sprint anterior | [Revisión del Sprint 1](../03%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) |

> **Nota de rebase funcional (09/10/2026):** el incremento de MFA y pedidos persistentes corresponde a la línea base funcional de Sprint 1; flota corresponde a Sprint 2 y rutas a Sprint 3. Se actualizaron las metas de Jira y Sprint 2 quedó con ECO-12 y ECO-19 en `Listo`. El Sprint 1 cerrado conserva sus fechas y el resultado histórico de su compromiso original; ECO-16 y ECO-20 permanecen completadas en el backlog porque no se pueden añadir a un sprint cerrado.

> **Comprobación posterior del alcance reordenado (09/10/2026):** en la aplicación local se completó MFA, alta/listado de vehículos con rol de Administración, disponibilidad por fecha con Planificación, y alta, búsqueda y detalle de un pedido. Se recargaron los datos tras reiniciar la API. La evidencia es de una E2E manual en una base PostGIS aislada, con datos temporales retirados al terminar; la base local conserva la migración `20261009_02` y no contiene los registros de prueba. Esta comprobación no reemplaza la decisión de aceptación que debe registrarse en la tabla de la reunión.

> **E2E funcional de flota (09/10/2026):** se completaron en navegador, con acceso MFA de Administración y Planificación y PostGIS temporal, los cinco criterios de Sprint 2 (**5/5 aprobados**). Tras reiniciar la API se verificó la persistencia de los tres vehículos y sus turnos; Mantenimiento e Inactivo siguieron excluidos de elegibilidad. Las cuentas, el contenedor y los datos temporales se retiraron al terminar. Jira refleja ECO-12 y ECO-19 en `Listo` (2/2). El sprint sigue activo hasta el cierre administrativo previsto y la revisión del Product Owner está programada para las 15:40; no se registra esa reunión ni una decisión formal antes de que ocurran.

> **Corte Jira actualizado (09/10/2026, 12:57 hora de Lima):** Sprint 2 tiene ECO-12 y ECO-19 en `Listo` (10 puntos estimados; 100 % de sus incidencias). Sprint 1 conserva 1/2 incidencias en su métrica dinámica histórica: ECO-9 `Listo` y ECO-15 `Por hacer`. El informe del corte original (28/09) sigue mostrando 0/2. La funcionalidad MFA/pedidos/persistencia está comprobada en el producto, pero no se suma retroactivamente a la velocidad de aquel corte.

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 02/10/2026 | Alex Zorrilla | Primera emisión con el trabajo completado al 02/10 y el guion de demostración ensayado. |
| 1.1.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se incorpora ECO-20 en Jira sin estimación aprobada y se actualiza el Sprint 1 como cerrado administrativamente. La reunión de revisión del Sprint 2 sigue pendiente. |
| 1.1.1 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se alinea la acción futura de CI y ramas con el flujo de ramas breves y PR hacia `main`; la aceptación del Sprint 2 sigue pendiente de la reunión. |
| 1.2.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se añade el historial de cambios de estado de ECO-9 y se confirma que la reunión aún no ocurrió al corte de esta actualización. |
| 1.2.1 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se distingue el estado provisional de Jira de la velocidad y aceptación oficiales del Sprint 2, que siguen pendientes de la revisión y del cierre. |
| 1.2.2 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se registra que ECO-20 aparece sin persona asignada ni estimación aprobada en Jira al corte previo a la revisión. |
| 1.2.3 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se traducen las referencias narrativas a partes interesadas. |
| 1.2.4 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se corrige la concordancia de género en las referencias a las partes interesadas. |
| 1.2.5 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se aclara que `Listo` y las pruebas documentadas respaldan la implementación, mientras la aceptación del Sprint 2 sigue pendiente de su reunión. |
| 1.2.6 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se deja lista una pauta para revisar el recorrido funcional, explicar sus límites y registrar la decisión sin adelantarla. |
| 1.2.7 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se agrega una verificación API aislada de MFA, registro, consulta y rechazo de ventana inválida, separada del ensayo visual y de la aceptación pendiente. |
| 1.2.8 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se registra la comprobación aislada en PostGIS: el pedido permanece después de reiniciar la API; se ajusta la agenda de revisión y el alcance restante de EN-005. |
| 1.2.9 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se alinea la pauta con ECO-16 en Sprint 2, se deja EN-005 pendiente bajo ECO-21 y se actualizan los puntos observados en Jira. |
| 1.3.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se vuelven a ejecutar las suites de backend y frontend después de incorporar PostGIS; se aclara que no cubren automáticamente ese adaptador. |
| 1.4.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se registra la revisión visual compartida, la sesión real de Planificación y el listado vacío; se deja sin conclusión una solicitud manual que devolvió 400 y se contrasta con las 28 pruebas existentes de API. |
| 1.5.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se anota la rebase funcional posterior y se remite al plan vigente, preservando los resultados del corte original. |
| 1.6.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se añade evidencia E2E posterior de pedidos y flota, manteniendo pendiente la aceptación formal. |
| 1.7.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se ejecuta y registra el E2E de los cinco criterios de aceptación del alcance de flota; 5/5 aprobados. La reunión/decisión del Product Owner queda diferenciada del resultado E2E. |
| 1.8.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se alinea Jira con la rebase funcional: Sprint 2 contiene ECO-12 y ECO-19 en `Listo` (2/2); se actualizan la meta y el estado administrativo observado sin atribuir una reunión futura. |

## Criterios E2E de flota aprobados; registro de reunión pendiente

El ensayo histórico de la demostración descrito abajo se hizo el 02/10. Para el alcance funcional reordenado, el E2E de flota ejecutado el 09/10 aprobó los cinco criterios del plan. Jira muestra ECO-12 y ECO-19 en `Listo`; Sprint 2 sigue activo hasta el cierre administrativo. La reunión de revisión está programada para las 15:40 del 09/10 y la tabla de decisión se conserva pendiente hasta registrar lo que ocurra.

### Evidencia de aceptación E2E del alcance vigente: flota

| Criterio del plan funcional | Resultado E2E en navegador | Evidencia observada |
|---|---|---|
| Administración crea/edita vehículo, normaliza placa y rechaza duplicados. | Aprobado | Se creó `S2-E2E-A1` con placa en minúscula y se comprobó su normalización; el duplicado mostró “La placa debe ser única”; la edición confirmó “Vehículo actualizado”. |
| Capacidades/consumo no positivos y fin de turno no posterior al inicio se rechazan. | Aprobado | El formulario rechazó valores negativos y bloqueó cero como campo requerido; la combinación 17:00–08:00 mostró “La hora final debe ser posterior a la hora inicial”. |
| Planificación configura turno y exige motivo si la unidad no está disponible. | Aprobado | Se guardó un turno 08:00–17:00; al desactivar disponibilidad, el formulario exigió el motivo y la unidad dejó de ser elegible. |
| Mantenimiento o Inactivo impiden elegibilidad aunque haya turno guardado. | Aprobado | `S2-E2E-B2` con turno 08:00–17:00 pasó a Mantenimiento y `S2-E2E-C3` con el mismo turno pasó a Inactivo; la cuenta Planificación mostró ambos estados sin etiqueta “Apto para planificar”. |
| Vehículo y disponibilidad persisten tras reiniciar la API. | Aprobado | Se detuvo y volvió a iniciar la API contra la misma base PostGIS E2E; al recargar Flota reaparecieron tres vehículos, todos los turnos y un único vehículo elegible (`S2-E2E-A1`). |

**Resultado:** 5/5 criterios aprobados. Las pruebas se ejecutaron el 09/10/2026 en `http://localhost:3000/`, con una API y PostGIS temporales aislados. Los datos no pertenecían a operaciones reales y fueron retirados al concluir. Jira se actualizó para dejar ECO-12 y ECO-19 en `Listo`; esto refleja la evidencia funcional y no atribuye aceptación formal al Product Owner.

### HU-001 / ECO-9 — Registrar pedido con ventana horaria (5 pts) · **Implementada; aceptación pendiente**

*Como despachador, quiero registrar un pedido con dirección, carga y ventana horaria, para incorporarlo a la planificación diaria.*

| Criterio de aceptación (Gherkin del backlog) | Resultado | Evidencia |
|---|---|---|
| **Registrar pedido válido:** "Dado que el despachador está autenticado, cuando ingresa dirección, peso y ventana horaria válida, entonces el sistema crea el pedido con estado Pendiente y muestra su identificador." | Cumple | Pedido creado con estado `PENDIENTE` y código `PED-000001` mostrado en un aviso; solo con sesión de **Planificador** (la autenticación se completó en este sprint). Pruebas `test_registrar_pedido_valido` y `test_planificador_registra_con_sesion_real`. |
| **Rechazar ventana inválida:** "Dado que la hora final es anterior a la hora inicial, cuando el despachador intenta guardar el pedido, entonces el sistema rechaza la operación e indica el campo que debe corregirse." | Cumple | La API responde 422 con el campo `ventanaFin`; la interfaz muestra el mensaje junto a ese campo y conserva los demás valores. Pruebas `test_rechazar_ventana_invalida` y `muestra el error junto al campo de hora final`. |

Alcance entregado (especificado en el cambio OpenSpec `registro-pedidos`, 9 requisitos y 24 escenarios):

- **API FastAPI:** registrar, consultar por identificador y listar con filtro por estado y paginación.
- **Validaciones de RF-02.2 / RN-001:** ventana coherente con zona horaria explícita, peso y volumen no negativos con al menos uno mayor que cero, prioridad de 1 a 4, ámbito geográfico y distritos configurables, y código único.
- **Errores uniformes:** 400, 404, 409, 422 y 500, sin trazas internas.
- **Interfaz React:** indicadores con conteo animado, tabla y lista en tarjetas con búsqueda y filtro, formulario en panel lateral (o en hoja inferior en el celular), detalle del pedido, tema claro y oscuro con la paleta de marca, navegación inferior en el celular y accesibilidad por teclado.

### Historia técnica — Autenticación con verificación en dos pasos y autorización por rol (RF-11.1) · **Implementada; planificación Sprint 1 tras la rebase**

Se incorporó originalmente al incremento de pedidos como precondición de HU-001 y como actividad de la semana 6. Está registrada en [ECO-20 — Autenticación MFA y autorización por rol](https://continental-team-ecologistica.atlassian.net/browse/ECO-20), vinculada a EP-07. Tras la rebase del 09/10 está completada en el backlog, porque el Sprint 1 ya se había cerrado y Jira no admite añadirle trabajo. Sigue sin puntos aprobados ni persona asignada; esos datos no se inventan ([IMP-008](02%20Registro%20de%20Impedimentos%20V_1_0_0.md)).

| Escenario clave de la especificación `autenticacion` | Resultado |
|---|---|
| Contraseña correcta → paso de código; contraseña incorrecta o correo inexistente → mismo mensaje genérico | Cumple |
| Primer ingreso → enrolamiento con código QR y clave manual; el factor solo se activa al validar un código | Cumple |
| Código correcto → sesión; incorrecto o repetido → rechazo; 5 códigos fallidos → vuelve a la contraseña | Cumple |
| Sesión en cookie `HttpOnly` y `SameSite=Strict`: vence a los 15 min de inactividad y a las 8 h; cerrar sesión invalida copias de la cookie | Cumple |
| Bloqueo de 15 min tras 5 intentos fallidos, también para correos inexistentes (429) | Cumple |
| Pedidos sin sesión → 401; rol no autorizado → 403; Planificador registra; Administrador solo consulta | Cumple |
| Eventos de acceso registrados sin contraseñas, códigos ni tokens | Cumple (tras corregir el defecto IMP-012) |

La especificación se **auditó antes de programar** con el prompt "Auditor Senior de Arquitectura de Software": 4 ambigüedades, 6 casos de borde y 3 preguntas de arquitectura, todos resueltos ([auditoría](../../../openspec/changes/archive/2026-10-02-autenticacion-mfa/auditoria-especificacion.md)). El cambio está **archivado** en OpenSpec y su especificación vive en `openspec/specs/autenticacion/`.

### Habilitador técnico — Persistir pedidos y ubicaciones (ECO-16, 3 pts) · **Implementado; backlog completado tras la rebase**

ECO-16 se incorporó originalmente al Sprint 2 para que el pedido de HU-001 siga disponible después de reiniciar la API. Docker Compose provisiona PostgreSQL/PostGIS, Alembic crea las tablas `pedidos` y `ubicaciones`, y el adaptador de pedidos crea, lista, filtra y consulta los registros. Una comprobación funcional aislada verificó registro, listado, detalle, rechazo de ventana inválida y disponibilidad del mismo pedido después del reinicio. La comprobación fue manual; no hay una suite automatizada de integración para esta capa. Tras la rebase, esta función se considera parte de la línea base funcional de Sprint 1 y permanece en el backlog completado, sin reasignarse a un Sprint 1 ya cerrado.

### Habilitadores completados

| Habilitador | Evidencia |
|---|---|
| Base de código del backend (FastAPI por capas) y del frontend (React + Vite + TypeScript), con scripts de ejecución y prueba | `backend/`, `frontend/`, README sección 8 |
| PostGIS para pedidos y ubicaciones, migración Alembic y comprobación después de reiniciar la API | [ECO-16](https://continental-team-ecologistica.atlassian.net/browse/ECO-16), `docker-compose.yml`, `database/migrations/`, [adaptador PostgreSQL](../../../backend/src/app/pedidos/postgres_repository.py) |
| Ratificación del stack React + FastAPI y alineación de 5 documentos de la línea base (versión 1.1.0) | [10 Stack tecnológico](../../01%20Inicio/10.%20Stack%20tecnol%C3%B3gico%20V_1_0_0.md) |
| Flujo OpenSpec completo: 2 cambios con propuesta, especificación, diseño y tareas, ambos archivados; sus especificaciones viven en `openspec/specs/pedidos` y `openspec/specs/autenticacion` | `openspec/` |
| Suites de regresión existentes reejecutadas el 09/10 después del cambio PostGIS (100 pruebas de backend y 39 de frontend aprobadas) | `backend/tests/`, `frontend/tests/`; estas suites no incluyen integración automatizada con PostgreSQL |

### Defectos detectados y corregidos en el sprint

| # | Defecto | Cómo se detectó | Corrección |
|---:|---|---|---|
| 1 | El listado mostraba pedidos en orden incorrecto cuando se registraban en el mismo instante (resolución del reloj de Windows). | Prueba de servicio | Orden por inserción, estable e independiente del reloj. |
| 2 | Un registro rechazado consumía un número del correlativo de códigos (`PED-000001` se saltaba). | Ensayo contra el servidor | El código se genera solo después de pasar todas las validaciones; prueba de regresión. |
| 3 | La columna "Estado" quedaba cortada en pantallas medianas. | Revisión visual | Vista en tarjetas para pantallas de menos de 1100 px. |
| 4 | Los eventos de auditoría no aparecían en la consola real ([IMP-012](02%20Registro%20de%20Impedimentos%20V_1_0_0.md)). | Verificación extremo a extremo | Registro configurado al arrancar y prueba que lo verifica. |

## Demostración del trabajo completado

Demostración a las *partes interesadas* de las funcionalidades implementadas. Guion para la revisión del 09/10, **ensayado el 02/10** contra los servidores locales (backend `http://localhost:8000`, frontend `http://localhost:3000`):

**Comprobación API del 09/10, 09:34 (hora de Lima):** en una instancia temporal aparte, sin alterar el servidor local ni sus cuentas, se completó el ingreso con MFA, el registro de un pedido válido (201), su listado por estado y consulta por identificador (200), y el rechazo de una ventana inválida (422). La cuenta y el pedido eran datos de prueba aislados; el archivo temporal se eliminó al terminar. Esto verifica el recorrido de la API, no la interfaz React en un navegador ni la aceptación del Product Owner.

**Comprobación de persistencia del 09/10:** en una segunda base PostGIS temporal, sin volumen y separada de los datos locales, se inició sesión con MFA, se registró y consultó un pedido, se rechazó una ventana inválida y se reinició FastAPI. Después del reinicio, el mismo pedido volvió a aparecer en el listado y en su detalle. El contenedor y la cuenta temporal se retiraron al terminar. Esta comprobación cubre API y base de datos, no la vista del navegador ni la aceptación del Product Owner.

**Comprobación local en navegador y API del 09/10, antes de la revisión:** la captura compartida muestra a Planificación dentro de la pantalla de Pedidos; los indicadores y la lista muestran cero pedidos. En la misma sesión de comprobación, el ingreso por API aceptó contraseña y TOTP para el rol `PLANIFICADOR`, y `GET /api/v1/pedidos` respondió 200 con `total=0`. La consulta se hizo en modo lectura y no se crearon registros. Una solicitud manual de ventana invertida enviada desde PowerShell devolvió 400, pero no se guardó su cuerpo y no se puede determinar si el rechazo se debió al formato de esa solicitud. Las 28 pruebas existentes de `tests/pedidos/test_api.py` pasaron; entre ellas, las ventanas que terminan antes de empezar se rechazan con 422. Esta evidencia no reemplaza la revisión del Product Owner.

| # | Paso de la demostración | Resultado esperado | Resultado del ensayo |
|---:|---|---|---|
| 1 | Abrir la app sin sesión | Pantalla "Iniciar sesión" | Correcto |
| 2 | Pedir la lista de pedidos a la API sin sesión | 401 | Correcto |
| 3 | Ingresar con contraseña incorrecta | Mensaje genérico "Correo o contraseña incorrectos" | Correcto |
| 4 | Primer ingreso del Planificador | Código QR y clave manual para la app autenticadora | Correcto |
| 5 | Enviar un código incorrecto y luego el correcto | Rechazo indicando el campo; después, entrada a la app | Correcto |
| 6 | Registrar un pedido con hora final anterior a la inicial | Error junto a "Ventana: fin"; valores conservados (Gherkin 2 de HU-001) | Correcto |
| 7 | Corregir y guardar | Aviso con el código `PED-000001` y estado Pendiente (Gherkin 1 de HU-001) | Correcto |
| 8 | Cerrar sesión y reutilizar la cookie anterior | 401: la sesión copiada ya no sirve | Correcto |
| 9 | Ingresar como Conductor | "Acceso no autorizado"; la API responde 403 | Correcto |
| 10 | Ingresar como Administrador | Ve los pedidos en modo consulta, sin botón de registro | Correcto |
| 11 | Cinco contraseñas incorrectas seguidas | Bloqueo de 15 minutos (429), aun con la contraseña correcta | Correcto |
| 12 | Enviar una solicitud desde un origen ajeno | 403 | Correcto |

Lo que validan las partes interesadas: que el despachador registra pedidos válidos y que el sistema rechaza los incoherentes antes de que lleguen al optimizador; y que solo entran personas autorizadas, con dos factores y según su rol.

## Registro para la reunión de revisión (pendiente)

La reunión está prevista para el 09/10 a las 15:40, hora de Lima. Este registro se completa durante la sesión; el ensayo del 02/10 y el estado `Listo` de Jira no reemplazan lo que decida el Product Owner.

Antes de mostrar el flujo, confirmar que el equipo tiene a mano una cuenta de Planificación y su app autenticadora. No anotar contraseñas, códigos TOTP ni secretos en este documento. Si se usa un pedido de prueba, identificarlo como tal y no presentarlo como una operación real de DistriRápido.

| Qué revisar en la reunión | Estado de la revisión | Comentarios que se registrarán |
|---|---|---|
| Entrar con MFA y comprobar que los permisos corresponden al rol. | Pendiente | — |
| Registrar un pedido válido y ver el código de confirmación. | Pendiente | — |
| Mostrar cómo se rechaza una ventana horaria inválida. | Pendiente | — |
| Encontrar el pedido en la lista, buscarlo o filtrarlo y abrir su detalle. | Pendiente | — |
| Reiniciar la API y confirmar que el pedido conserva código, estado y detalle. | Pendiente | El flujo ya se comprobó en una base temporal aislada; repetirlo durante la revisión y registrar comentarios del Product Owner. |

| Decisión del Product Owner sobre el incremento | Pendiente de registrar |
|---|---|
| Aceptado / aceptado con pendientes / no aceptado | — |
| Cambios o incidencias que se crearán en Jira | — |
| Responsable y fecha acordada para cada acción | — |
| Comentarios de las personas que participaron | — |

Hasta que se complete esta tabla con lo que ocurra en la reunión, la aceptación formal y la retroalimentación siguen pendientes; no se atribuyen acuerdos al docente ni al equipo.

## Pendientes

| # | Pendiente | Tipo | Origen | Responsable | Destino |
|---:|---|---|---|---|---|
| 1 | La historia técnica se registró como ECO-20, sin puntos aprobados; faltan Planning Poker y crear las 7 tarjetas HU-004, HU-010, HU-011 y EN-001 a EN-004 | Gestión | [IMP-008](02%20Registro%20de%20Impedimentos%20V_1_0_0.md) | Jose Luis Isidro Casio · equipo | Antes del Planning del Sprint 3 |
| 2 | Completar EN-005 / [ECO-21](https://continental-team-ecologistica.atlassian.net/browse/ECO-21) para persistir cuentas, proteger secretos TOTP y persistir rutas | Habilitador | [IMP-011](02%20Registro%20de%20Impedimentos%20V_1_0_0.md) | Anco Porras, Jhean Pier Julio | Planning del Sprint 3; sin estimación ni compromiso |
| 3 | Prototipo del motor VRPTW y benchmark EN-001 (desbloquea HU-004 y HU-006) | Historia / habilitador | Roadmap; [IMP-006](02%20Registro%20de%20Impedimentos%20V_1_0_0.md) | Alexander Daniel Hilario Talavera | Sprint 3 |
| 4 | CI en GitHub Actions y ramas breves `feature/*` con *pull requests* hacia `main` (EN-006); retirar `developer` tras confirmar la migración | Habilitador | [IMP-010](02%20Registro%20de%20Impedimentos%20V_1_0_0.md) | Jose Luis Isidro Casio | Sprint 3 |
| 5 | Restablecimiento del segundo factor por un administrador | Historia técnica | Auditoría, caso E6 | Alex Zorrilla | Sprint 4 |
| 6 | Archivos de la tipografía Codec Pro | Diseño | [IMP-013](02%20Registro%20de%20Impedimentos%20V_1_0_0.md) | Jhoanna Hade Vera Zea | Antes del 09/10 |

### Métricas históricas previas al rebase funcional

| Métrica | Sprint 1 al corte planificado | Sprint 2 al 09/10, antes de la revisión |
|---|---:|---:|
| Puntos de historias que alcanzaron la Definición de Hecho / están en `Listo` en Jira | 0 | 5 (ECO-9; estado de Jira, revisión pendiente) |
| Tareas técnicas en `Listo` en Jira | 0 | 2 (ECO-16: 3 pts; ECO-20: sin estimación aprobada) |
| Puntos estimados en `Listo` en Jira | 0 | 8 (5 de ECO-9 + 3 de ECO-16; no es velocidad oficial) |
| Velocidad oficial del Sprint 2 | 0 | Pendiente de revisión y cierre |

Los valores de la tabla anterior son la instantánea previa al rebase y no describen el contenido actual de Sprint 2. En la consulta Jira del 09/10 a las 12:57, ECO-12 y ECO-19 están `Listo` en Sprint 2 (2/2 incidencias; 10 puntos). Sprint 1 muestra 1/2 incidencias por ECO-15 pendiente; el resultado original al corte del 28/09 sigue siendo 0/2. La velocidad oficial de Sprint 2 se determinará al cerrar el sprint y no se atribuye una decisión del Product Owner antes de su revisión programada.
