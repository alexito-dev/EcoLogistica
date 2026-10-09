# Retrospectiva del sprint

[← Volver al README Principal](../../../README.md)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla

**Líder del Proyecto:** Alex Jesus Zorrilla Apumayta

## Metadatos del documento

| Campo | Valor |
|---|---|
| Versión | 1.6.0 |
| Sprint | ECO Sprint 2 (inicio 29/09/2026; revisión 09/10/2026) |
| Fecha de la retrospectiva | 02/10/2026 (corte de mitad de sprint; se confirma en la reunión del 09/10) |
| Facilitador | Alex Zorrilla |
| Participantes | Alex Zorrilla, Anco Porras, Jhean Pier Julio, Alexander Daniel Hilario Talavera, Jhoanna Hade Vera Zea, Jose Luis Isidro Casio |
| Entradas | [01 Informe de estado](01%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md) · [02 Registro de Impedimentos](02%20Registro%20de%20Impedimentos%20V_1_0_0.md) · [03 Revisión del Sprint](03%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) · [Retrospectiva del Sprint 1](../04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) |

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 02/10/2026 | Alex Zorrilla | Primera emisión: seguimiento de las acciones del Sprint 1, análisis en los cuatro ejes y plan de acción para el Sprint 3. |
| 1.1.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Seguimiento de Jira: Sprint 1 cerrado administrativamente, Sprint 2 activo y ECO-20 registrada sin puntos. Esta retrospectiva es intermedia; la revisión y retrospectiva final siguen pendientes. |
| 1.1.1 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se actualiza A6 al flujo de ramas breves desde `main` y PR hacia `main`; la retrospectiva continúa como intermedia hasta la reunión del Sprint 2. |
| 1.2.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se corrigen el seguimiento de las acciones, el estado de Jira y el balance al corte previo a la revisión; se registra IMP-003 reabierto. |
| 1.3.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se aclara el corte histórico de autoría de commits y se actualiza el dato con el historial de Git hasta el 09/10. |
| 1.4.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se actualiza el estado de ECO-20: además de no tener estimación aprobada, Jira aún no muestra una persona asignada. |
| 1.5.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se centra la acción de Sprint 3 en completar un recorrido de Planificación y se deja la tecnología como trabajo que habilita esa tarea. |
| 1.6.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se registra que pedidos y ubicaciones ya sobreviven al reinicio con PostGIS; EN-005 sigue pendiente para usuarios, flota y rutas. |

## Seguimiento de las acciones del Sprint 1

| Acción del Sprint 1 | Estado | Evidencia |
|---|---|---|
| A1 — *Definition of Ready* con dependencias | Parcial | HU-006 no se volvió a comprometer sin el motor; falta formalizar la checklist en Jira |
| A2 — *Definition of Done* con código, pruebas y demostración | Cumplida | HU-001 y la autenticación cerradas con pruebas en verde y demostración ensayada |
| A3 — Base de código de backend y frontend | Cumplida | `backend/` (FastAPI) y `frontend/` (React + Vite) con scripts de ejecución y prueba |
| A4 — Primer cambio OpenSpec completo | Cumplida | `registro-pedidos` y `autenticacion-mfa` implementados, verificados y archivados |
| A5 — CI mínimo | No cumplida | Sin GitHub Actions; las pruebas solo se ejecutan en local |
| A6 — *Planning Poker* y backlog completo en Jira | Parcial | ECO-20 se creó el 09/10 sin puntos ni persona asignada; faltan siete tarjetas de backlog y evidencia de *Planning Poker*. |
| A7 — Prototipo del motor y benchmark | No cumplida | Sin código de optimización |
| A8 — Registro de decisiones técnicas (ADR) | Parcial | La ratificación del stack quedó registrada en el historial del documento 10, no como ADR independiente |
| A9 — Releases y tablero de 4 columnas en Jira | No cumplida al 09/10 | Jira aún no tiene versiones y mantiene cinco columnas con mezcla de idiomas y mapeos inconsistentes; IMP-003 se reabrió. |
| A10 — Validar el backlog con el docente | Sin evidencia | Pendiente de la revisión programada para el 09/10 a las 15:40, hora de Lima. |

**Balance al corte previo a la revisión:** 3 de 10 acciones cumplidas, 3 parciales, 3 no cumplidas y 1 sin evidencia. Las cumplidas son justamente las que desbloquearon la entrega de software.

## ¿Qué aprendimos?

1. **Especificar antes de programar sí ahorra trabajo.** La auditoría de la especificación de seguridad encontró 13 problemas antes de escribir código: la duración del bloqueo no estaba definida, se podían reutilizar códigos y los mensajes revelaban si una cuenta existía. Corregirlos en el documento costó minutos; en producción habrían sido vulnerabilidades.
2. **Las pruebas en verde no garantizan que el sistema funcione en real.** Las 100 pruebas del backend pasaban, pero los eventos de auditoría no aparecían en la consola del servidor (IMP-012). Solo la verificación extremo a extremo contra el servidor real lo reveló. La demostración ensayada es parte de la *Definition of Done*.
3. **Una decisión de arquitectura sin evidencia se paga dos veces.** El cambio de stack del 18/09 y su reversión del 29/09 (IMP-009) obligaron a reescribir cinco documentos. Desde ahora, un cambio de stack exige ADR y matriz.
4. **Reducir el alcance al incremento mínimo demostrable funciona.** Comprometer solo HU-001 y su precondición de seguridad, en lugar de todo el roadmap, permitió pasar de 0 a una entrega completa y probada.
5. **La zona horaria debe estar en la especificación.** Tal como mostró el caso del "cobro fantasma" de la semana 6, exigir fechas con desfase explícito (-05:00) eliminó una fuente clásica de errores entre el entorno local y producción.

## ¿Qué estamos haciendo bien?

1. **Incremento real y verificable:** primera historia completada (HU-001) más la autenticación de dos factores, ambas en `main`, con 139 pruebas automatizadas y 99 % de cobertura en el backend.
2. **Desarrollo guiado por especificaciones:** dos cambios OpenSpec con propuesta, especificación, diseño y tareas, validados en modo estricto y archivados, y una auditoría documentada como evidencia académica.
3. **Seguridad desde el diseño:** Argon2id, TOTP con anti-repetición, cookies `HttpOnly` y `SameSite=Strict`, bloqueo por intentos y roles que se niegan por defecto, todo trazado a RF-11.1 y a RNF-05, RNF-06 y RNF-07.
4. **Arquitectura preparada para crecer:** dominios independientes de FastAPI y de la persistencia, con puertos de repositorio que permiten pasar a PostgreSQL sin tocar las reglas de negocio.
5. **Diseño cuidado:** la paleta de marca en tema claro y oscuro, diseño adaptado al celular con navegación inferior, animaciones que respetan "reducir movimiento" y accesibilidad por teclado.
6. **Transparencia:** los documentos reportan lo que no se hizo (motor, flota, CI) con la misma claridad que lo logrado.

## ¿Qué podemos hacer mejor?

### Personas

- **El trabajo de código se concentró en una persona.** Al corte de la primera emisión (02/10, 10:05, hora de Lima), los primeros 8 commits del Sprint 2 en `main` eran de Alex Zorrilla. El historial consultado el 09/10, antes de esta actualización, contenía 20 commits desde el 29/09: 12 de Alex Zorrilla y 8 de Anco Porras, Jhean Pier Julio; estos últimos son cambios de documentación. No se verifican commits de implementación de los demás roles, por lo que la concentración del conocimiento del código sigue siendo un riesgo.
- **La especialización de roles no se aprovechó:** el responsable de optimización tenía el trabajo más crítico (el motor) y no empezó; el de QA/DevOps no montó la CI.
- **Falta tiempo protegido para aprender el stack** (FastAPI, React, OpenSpec) por parte de quienes aún no lo usan.

### Relaciones

- **El cambio de stack del 18/09 se aplicó sin conversación de equipo** y el líder tuvo que revertirlo después. Las decisiones técnicas deben acordarse antes de tocar `main`.
- **Las revisiones de código no existen todavía:** al no haber *pull requests*, nadie más leyó el código entregado.
- **Falta un canal de seguimiento diario visible** (Daily) que muestre en qué trabaja cada integrante.

### Procesos

- **El flujo de ramas acordado no se aplicó de forma uniforme:** se trabajó directamente sobre `main` y la rama remota `developer` quedó atrás (IMP-010). El estándar queda simplificado a ramas breves `feature/*` desde `main` y PR hacia `main`; no se requiere `develop`.
- **El backlog de Jira no refleja todo el trabajo real:** al corte del 02/10 no existía la historia de autenticación; el 09/10 se creó ECO-20 sin estimación aprobada. Siguen faltando siete tarjetas y la actualización formal del roadmap (IMP-008).
- **Las verificaciones extremo a extremo fueron manuales:** se ensayaron a mano en lugar de quedar como prueba automatizada repetible.
- **El roadmap no se ajustó formalmente:** flota y motor se proponen para el Sprint 3 en los documentos, pero Jira todavía no contiene ese plan como un sprint futuro aprobado.

### Herramientas

- **Sin integración continua:** las 139 pruebas solo corren en la máquina de quien las ejecuta.
- **La persistencia quedó a medias al cierre de esta actualización:** pedidos y ubicaciones ya se guardan en PostGIS, pero las cuentas siguen en archivo local y la flota/rutas aún no tienen tablas de aplicación (IMP-011).
- **Las herramientas de desarrollo no están documentadas para todos:** el servidor de Vite conservó una versión vacía de los estilos y hubo que reiniciarlo. Hace falta una guía de solución de problemas en el README.
- **Recursos de diseño incompletos:** falta la tipografía Codec Pro con licencia (IMP-013).

### Acciones a realizar

| # | Acción concreta | Eje | Responsable | Fecha límite | Indicador de éxito |
|---:|---|---|---|---|---|
| A1 | Organizar el Sprint 3 alrededor del flujo propuesto: Planificación asigna pedidos pendientes a vehículos y revisa una ruta guardada. En el Planning, acordar las historias de interfaz, persistencia, flota y primera secuencia de paradas; repartirlas por rol y comprobarlas juntas como un recorrido. | Personas | Alex Zorrilla | 09/10/2026 (Planning del Sprint 3) | La meta y sus historias están acordadas y estimadas en Jira; el incremento permite completar el flujo y el aporte de cada integrante queda visible en el trabajo integrado. |
| A2 | Sesión de nivelación de 1 hora sobre el stack y el flujo OpenSpec, dictada con el código real del proyecto | Personas | Alex Zorrilla | 12/10/2026 | Los 5 integrantes ejecutan el backend, el frontend y las pruebas en su máquina |
| A3 | Toda decisión técnica que cambie la arquitectura se discute en la reunión del equipo y se registra como ADR en `docs/otros` antes de tocar `main` | Relaciones | Anco Porras, Jhean Pier Julio | Permanente desde el 09/10/2026 | 0 cambios de arquitectura sin ADR |
| A4 | Revisión cruzada obligatoria: cada *pull request* la aprueba un integrante distinto del autor | Relaciones | Jose Luis Isidro Casio | 16/10/2026 | 100 % de PR con al menos una aprobación |
| A5 | Daily asincrónico de 15 minutos en el canal del equipo: qué hice, qué haré y qué me bloquea | Relaciones | Alex Zorrilla | 09/10/2026 | Al menos 4 registros por integrante en la semana |
| A6 | Retirar `developer` como rama de integración; crear ramas breves `feature/*` desde `main`, integrar mediante PR y configurar protección de `main` y CI | Procesos | Jose Luis Isidro Casio | 16/10/2026 | PR revisados hacia `main`; reglas de protección y CI verificadas; ningún cambio funcional entra sin revisión |
| A7 | Registrar en Jira la historia de autenticación y estimar las 7 tarjetas faltantes con *Planning Poker*; actualizar el roadmap | Procesos | Jose Luis Isidro Casio | 09/10/2026 | Backlog completo y estimado; roadmap del Sprint 3 publicado |
| A8 | Convertir el guion de demostración en pruebas extremo a extremo automatizadas (Playwright, previsto en el documento de stack) | Procesos | Jose Luis Isidro Casio | 23/10/2026 | Guion de 12 pasos ejecutándose en CI |
| A9 | Configurar GitHub Actions con las pruebas de backend y frontend, el lint y la compilación en cada PR (EN-006) | Herramientas | Jose Luis Isidro Casio | 16/10/2026 | Pipeline en verde obligatorio para fusionar |
| A10 | Completar EN-005 con PostgreSQL + PostGIS, `docker compose` y migraciones Alembic; ampliar los adaptadores de pedidos a usuarios, flota y rutas | Herramientas | Anco Porras, Jhean Pier Julio | 23/10/2026 | Pedidos y ubicaciones ya sobreviven al reinicio; verificar usuarios, flota y rutas y agregar comprobaciones de integración para esos flujos |
| A11 | Agregar al README una sección de solución de problemas (caché de Vite, contraseña de demostración, puertos) | Herramientas | Jhoanna Hade Vera Zea | 12/10/2026 | Un integrante nuevo levanta la app sin ayuda |
| A12 | Prototipo del motor con OR-Tools y benchmark EN-001 con 50, 100 y 150 pedidos | Procesos | Alexander Daniel Hilario Talavera | 23/10/2026 | Informe de tiempos y factibilidad publicado en `docs/` |

**Seguimiento al 09/10, antes de la revisión:** A7 sigue parcial; ECO-20 está creada, pero no estimada, faltan siete tarjetas y no hay evidencia de *Planning Poker* ni de una actualización del roadmap futuro en Jira. Los acuerdos de validación con el docente quedan pendientes de la reunión.

### Seguimiento de acuerdos

El avance de estas acciones se revisa en el Daily y se reporta en el Informe de estado del Sprint 3. Las acciones vinculadas a impedimentos se cierran también en el registro: A6 → IMP-010; A7 → IMP-008; A10 → IMP-011; A12 → IMP-006.
