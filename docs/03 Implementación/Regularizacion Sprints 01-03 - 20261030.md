# Plan de regularización técnica y documental — Sprint 1 a Sprint 3
**Proyecto:** EcoLogística Huancayo  
**Corte de diagnóstico:** 30/10/2026  
**Estado:** acciones de regularización en ejecución; no constituye acta de aceptación ni cierre retroactivo.  
**Rama:** `audit/correcciones-sprints-1-3-20261030`.

## 1. Propósito y criterio de redacción
Como equipo de EcoLogística, corregimos la divergencia entre los entregables y la trazabilidad en Jira. Describimos nuestras actividades en primera persona del plural y diferenciamos resultados históricos, evidencia nueva, limitaciones y compromisos pendientes. No atribuimos aceptación al Product Owner sin una constancia verificable.

## 2. Línea base preservada
| Sprint | Alcance reordenado | Evidencia histórica | Reserva |
|---|---|---|---|
| 1 | Autenticación MFA/RBAC, registro y persistencia de pedidos | ECO-9, ECO-16, ECO-20 y documentación de incremento | No alteramos la velocidad histórica del Sprint 1 ni trasladamos artificialmente trabajo posterior |
| 2 | Alta/edición de flota, turnos, elegibilidad y persistencia | ECO-12 y ECO-19, pruebas funcionales 5/5 en PostGIS temporal | Sprint con cierre administrativo pendiente |
| 3 | Planificación de rutas, visualización cartográfica, indicadores y calidad | Implementación de rutas/indicadores, workflow CI, benchmark y documentación del 30/10 | Faltan trazabilidad Jira integral, comprobación independiente y varios criterios de seguridad/calidad |

## 3. Inventario de discrepancias
| Referencia | Observación comprobable al corte | Acción y verificación exigida |
|---|---|---|
| ECO-11 | Historia por hacer; la visualización de coordenadas aparece en pedidos | E2E de destino válido e inválido y validación de requisitos de geocodificación antes del cierre |
| ECO-13 | Jira por hacer; mapa Leaflet/OSM y trazado OSRM descritos en Sprint 3 | Documentar flujo conductor/repartidor, paradas sin coordenadas y evidencia del flujo completo |
| ECO-14 | Jira por hacer; indicadores calculados, pero falta comprobar el KPI basado en entregas reales y su estado vacío | Separar estimación de CO₂e de reducción observada, probar estados vacíos y puntualidad real |
| ECO-17 | Jira desactualizado (menciona ausencia de CI); existe workflow `.github/workflows/ci.yml` | Vincular run con éxito, cubrir persistencia PostGIS y E2E de navegación, confirmar OpenAPI |
| ECO-21 | Usuarios y rutas guardados en JSON local, sin cifrado de TOTP en reposo | Migración Alembic, cifrado, rotación, estrategia de recuperación, pruebas de reinicio y concurrencia |
| ECO-15 | Por hacer y ligado históricamente a Sprint 1 | Mantener resultado del Sprint 1; planificar re-enrutamiento en alcance posterior |
| ECO-18 | No hay evidencia de importador por plantilla | No marcar realizado sin implementación y pruebas |
| Jira Sprint 2 | 10/10 puntos completados; sprint abierto tras el 12/10 | Comprobar aceptación y cerrar administrativamente sin cambiar fechas históricas |

## 4. Implementaciones y controles de esta intervención
1. **Sprint 1:** Fortalecemos el adaptador local de usuarios ante errores de escritura y agregamos una prueba de regresión. Este cambio es mitigación transitoria; no resuelve ECO-21.
2. **Sprint 3:** Endurecemos el almacenamiento temporal de rutas con sincronización antes del reemplazo. Seguimos requiriendo un repositorio PostgreSQL transaccional para concurrencia y operación real.
3. **Integración:** Trabajamos por rama y solicitamos revisión mediante Pull Request. No fusionamos directamente en `main`.
4. **Validación:** Contrastamos CI de GitHub Actions, pruebas backend/frontend, migraciones Alembic y ejecución E2E. Una ejecución declarada en README no sustituye un resultado nuevo.
5. **Seguridad:** No publicamos valores de `.env`, claves de sesión, contraseñas, tokens ni secretos TOTP. Antes de habilitar producción verificamos cifrado y control de accesos.
6. **Desempeño:** No confundimos el benchmark sintético del motor con una reducción real del 15 % ni con puntualidad observada del 92 %.

## 5. Definición de Terminado para regularización
Declaramos cada historia **Lista** exclusivamente cuando: (a) sus criterios de aceptación están reproducidos en un caso de prueba; (b) la implementación queda en una rama revisada y CI aprobado; (c) existe evidencia identificable de integración/E2E cuando corresponde; (d) la documentación corresponde al mismo commit; y (e) las dependencias, riesgos y desviaciones están registradas en Jira. Si falta alguno, mantenemos En curso / En revisión / Por hacer según corresponda.

## 6. Secuencia de entrega verificable
- **A — Conciliación:** preservar actas e historiales, actualizar descripciones obsoletas, enlazar commits y tests.
- **B — Defectos y seguridad:** corregir persistencia, protección de TOTP y controles de acceso, agregar pruebas automatizadas con PostGIS.
- **C — Requisitos incompletos:** cerrar brechas de geocodificación, mapa, dashboard y calidad sin ampliar indebidamente el alcance.
- **D — Validación:** pytest, Vitest, lint, build, migraciones, CI, OWASP/WCAG y pruebas funcionales.
- **E — Cierre formal:** revisión humana, aceptación verificable, transición de tickets y cierre administrativo de sprint.

## 7. Reglas de integridad de evidencia
Conservamos los documentos originales como registros históricos. Añadimos correcciones fechadas y referencias a los archivos/commits, sin atribuir resultados a reuniones no celebradas. La revisión documental del 30/10 es nuestro punto de partida; cualquier resultado posterior debe mostrar fecha, entorno y ejecución.

## 8. Referencias
- [Backlog Jira](https://continental-team-ecologistica.atlassian.net/jira/software/projects/ECO/boards/2/backlog)
- [Repositorio](https://github.com/alexito-dev/EcoLogistica)
- [CI](https://github.com/alexito-dev/EcoLogistica/actions)
- [Sprint 1](../Sprint%2001/)
- [Sprint 2](../Sprint%2002/)
- [Sprint 3](../Sprint%2003/)
