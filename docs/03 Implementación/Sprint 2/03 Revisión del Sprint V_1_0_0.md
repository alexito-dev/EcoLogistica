# Revisión del sprint

[← Volver al README Principal](../../../README.md)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla

**Líder del Proyecto:** Alex Jesus Zorrilla Apumayta

## Metadatos del documento

| Campo | Valor |
|---|---|
| Versión | 1.2.6 |
| Sprint | ECO Sprint 2 (inicio 29/09/2026) |
| Objetivo replanificado | "Entregar el primer incremento demostrable: registro de pedidos (HU-001) con acceso seguro por roles y verificación en dos pasos." |
| Reunión de revisión | Evaluación Parcial — Sprint 02, viernes 09/10/2026, 15:40–16:00 |
| Ensayo de la demostración | 02/10/2026, contra los servidores locales (resultados en la sección *Demostración*) |
| Participantes previstos | Equipo Scrum: Alex Zorrilla (líder / PM), Anco Porras, Jhean Pier Julio (backend), Alexander Daniel Hilario Talavera (optimización), Jhoanna Hade Vera Zea (frontend/UX), Jose Luis Isidro Casio (QA/DevOps). Docente asesor y *Product Owner* académico: Ing. Job Daniel Gamarra Moreno |
| Documentos hermanos | [01 Informe de estado](01%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md) · [02 Registro de Impedimentos](02%20Registro%20de%20Impedimentos%20V_1_0_0.md) · [04 Retrospectiva](04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) |
| Sprint anterior | [Revisión del Sprint 1](../03%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) |

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

## Funciones implementadas; aceptación del Sprint 2 pendiente

El ensayo de la demostración descrito abajo se hizo el 02/10. Jira muestra ECO-9 y ECO-20 en `Listo`, pero la reunión prevista para el 09/10 a las 15:40 aún no ocurre a este corte. Aquí, "cumple" describe la evidencia de implementación y pruebas; no significa que el Product Owner ya haya aceptado el sprint.

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

### Historia técnica — Autenticación con verificación en dos pasos y autorización por rol (RF-11.1) · **Implementada; aceptación pendiente**

Incorporada al sprint como precondición de HU-001 y como actividad de la semana 6. Registrada el 09/10 en Jira como [ECO-20 — Autenticación MFA y autorización por rol](https://continental-team-ecologistica.atlassian.net/browse/ECO-20), vinculada a EP-07. Al corte previo a la revisión no tiene puntos ni persona asignada: no se encontró una estimación aprobada por el equipo ni una asignación en Jira ([IMP-008](02%20Registro%20de%20Impedimentos%20V_1_0_0.md)).

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

### Habilitadores completados

| Habilitador | Evidencia |
|---|---|
| Base de código del backend (FastAPI por capas) y del frontend (React + Vite + TypeScript), con scripts de ejecución y prueba | `backend/`, `frontend/`, README sección 8 |
| Ratificación del stack React + FastAPI y alineación de 5 documentos de la línea base (versión 1.1.0) | [10 Stack tecnológico](../../01%20Inicio/10.%20Stack%20tecnol%C3%B3gico%20V_1_0_0.md) |
| Flujo OpenSpec completo: 2 cambios con propuesta, especificación, diseño y tareas, ambos archivados; sus especificaciones viven en `openspec/specs/pedidos` y `openspec/specs/autenticacion` | `openspec/` |
| 139 pruebas automatizadas (100 de backend con 99 % de cobertura y 39 de frontend) | `backend/tests/`, `frontend/tests/` |

### Defectos detectados y corregidos en el sprint

| # | Defecto | Cómo se detectó | Corrección |
|---:|---|---|---|
| 1 | El listado mostraba pedidos en orden incorrecto cuando se registraban en el mismo instante (resolución del reloj de Windows). | Prueba de servicio | Orden por inserción, estable e independiente del reloj. |
| 2 | Un registro rechazado consumía un número del correlativo de códigos (`PED-000001` se saltaba). | Ensayo contra el servidor | El código se genera solo después de pasar todas las validaciones; prueba de regresión. |
| 3 | La columna "Estado" quedaba cortada en pantallas medianas. | Revisión visual | Vista en tarjetas para pantallas de menos de 1100 px. |
| 4 | Los eventos de auditoría no aparecían en la consola real ([IMP-012](02%20Registro%20de%20Impedimentos%20V_1_0_0.md)). | Verificación extremo a extremo | Registro configurado al arrancar y prueba que lo verifica. |

## Demostración del trabajo completado

Demostración a las *partes interesadas* de las funcionalidades implementadas. Guion para la revisión del 09/10, **ensayado el 02/10** contra los servidores locales (backend `http://localhost:8000`, frontend `http://localhost:3000`):

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
| Explicar que, por ahora, los pedidos se pierden al reiniciar la API. | Pendiente | Acordar si este límite se acepta para el incremento de demostración o requiere trabajo antes de darlo por aceptado. |

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
| 2 | PostgreSQL + PostGIS con migraciones y adaptadores reales (EN-005 / ECO-16) | Habilitador | [IMP-011](02%20Registro%20de%20Impedimentos%20V_1_0_0.md) | Anco Porras, Jhean Pier Julio | Sprint 3 |
| 3 | Gestión de flota y restricciones vehiculares (HU-003, HU-009) | Historia | Roadmap del Sprint 2, no iniciado | Anco Porras, Jhean Pier Julio | Sprint 3 |
| 4 | Prototipo del motor VRPTW y benchmark EN-001 (desbloquea HU-004 y HU-006) | Historia / habilitador | Roadmap; [IMP-006](02%20Registro%20de%20Impedimentos%20V_1_0_0.md) | Alexander Daniel Hilario Talavera | Sprint 3 |
| 5 | CI en GitHub Actions y ramas breves `feature/*` con *pull requests* hacia `main` (EN-006); retirar `developer` tras confirmar la migración | Habilitador | [IMP-010](02%20Registro%20de%20Impedimentos%20V_1_0_0.md) | Jose Luis Isidro Casio | Sprint 3 |
| 6 | Restablecimiento del segundo factor por un administrador | Historia técnica | Auditoría, caso E6 | Alex Zorrilla | Sprint 4 |
| 7 | Archivos de la tipografía Codec Pro | Diseño | [IMP-013](02%20Registro%20de%20Impedimentos%20V_1_0_0.md) | Jhoanna Hade Vera Zea | Antes del 09/10 |

### Estado provisional de Jira y proyección

| Métrica | Sprint 1 al corte planificado | Sprint 2 al 09/10, antes de la revisión |
|---|---:|---:|
| Puntos de historias que alcanzaron la Definición de Hecho / están en `Listo` en Jira | 0 | 5 (estado de Jira; revisión pendiente) |
| Historias técnicas en `Listo` en Jira | 0 | 1 (ECO-20; sin estimación aprobada) |
| Velocidad oficial del Sprint 2 | 0 | Pendiente de revisión y cierre |

El Sprint 2 continúa activo y su revisión está programada para el 09/10 a las 15:40, hora de Lima; por ello, el dato de 5 puntos en `Listo` todavía no es velocidad oficial ni aceptación del producto. No se calcula una velocidad promedio con un sprint pendiente de cierre y ECO-20 sin estimación aprobada. La proyección se actualizará en el Planning del Sprint 3 con el backlog estimado y la capacidad confirmada del equipo (ver [Retrospectiva](04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md)).
