# Acta consolidada de cierre y trazabilidad — Sprints 01, 02 y 03

**EcoLogística Huancayo — Corte: 30 de octubre de 2026**  
**Naturaleza:** cierre de incrementos de software y conciliación administrativa de Jira.  
**Repositorio:** [EcoLogistica](https://github.com/alexito-dev/EcoLogistica) · **Tablero:** [ECO board (id 2)](https://continental-team-ecologistica.atlassian.net/jira/software/projects/ECO/boards/2/backlog)  
**Estado:** los tres sprints oficiales están **cerrados en Jira**. El cierre **no** significa despliegue productivo ni aceptación de historias ajenas al alcance delimitado.

## 1. Declaración del equipo y criterio de integridad

Como equipo de EcoLogística, damos por entregados al corte del **30/10/2026** los tres primeros **incrementos funcionales acordados**: autenticación y pedidos; gestión de flota; y planificación de rutas con indicadores **estimados**, benchmark y CI. Conciliamos el seguimiento en Jira con el código efectivamente construido, manteniendo las pruebas y las actas históricas. No inventamos asistencia a reuniones, aprobaciones académicas, rendimiento operativo, puntos retroactivos ni cumplimiento de controles que aún faltan.

Conservamos dos cronologías separadas: **la de ejecución técnica**, documentada en las revisiones, y **la de operaciones administrativas Jira**, en particular el cierre tardío de Sprint 2 y la creación/inicio/cierre de Sprint 3 el propio 30/10. Ambas son reales, pero **no son intercambiables**.

## 2. Estado verificado de las iteraciones

| Sprint | ID Jira | Ciclo de vida Jira | Objetivo funcional entregado | Datos de seguimiento |
|---|---:|---|---|---|
| **Sprint 1** | 36 | Cerrado administrativamente el 09/10/2026 | MFA/TOTP + roles, pedidos con ventanas y ubicación PostGIS | El corte original **28/09** registró **0/2 historias** del compromiso inicial; rebase del 09/10 integró ECO-16/ECO-20 fuera de velocidad histórica. ECO-15 permaneció pendiente. |
| **Sprint 2** | 37 | Cerrado el **30/10/2026 a las 14:58:02 (Lima)** | Catálogo de vehículos, capacidades, turnos y disponibilidad por fecha | **ECO-12 y ECO-19 Listo, 2/2, 10/10 puntos**. Cinco criterios E2E documentados con PostGIS temporal; aceptación funcional reportada el 09/10. Periodo planificado original 29/09–12/10. |
| **Sprint 3** | 38 | Creado e iniciado el **30/10/2026 a las 14:59 (Lima)**; cerrado el **30/10/2026 a las 15:09:55 (Lima)** | Planificación y guardado de rutas, dashboard de previsiones, benchmark, CI y OpenAPI | **ECO-22, ECO-23, ECO-17 y ECO-25 en Listo: 4/4 elementos**. Se regularizó el incremento técnico documentado entre 09/10–30/10, sin recrear una velocidad retrospectiva. El término administrativo inicialmente previsto para 13/11 fue anticipado por solicitud del usuario. |

> El Sprint 1 duplicado (id 3) sigue preservado como evento histórico accidental y no se suma a las tres iteraciones oficiales. Su existencia no se utiliza para duplicar velocidad. En Sprint 3, solo ECO-17 tenía cinco puntos estimados; ECO-22, ECO-23 y ECO-25 se añadieron sin estimación retrospectiva. **No presentamos 5 puntos como velocidad histórica completa del Sprint 3.**

## 3. Entregables y evidencia por incremento

### Sprint 1 — acceso y pedidos

Implementamos autenticación con contraseña y TOTP, restricción por roles, registro y consulta de pedidos con ventanas horarias, validación de ubicación y persistencia de pedidos/ubicaciones con PostGIS. Conservamos los resultados documentados y ahora verificamos repositorios mediante integración automatizada en una base de pruebas aislada.

- **Jira:** [ECO-9](https://continental-team-ecologistica.atlassian.net/browse/ECO-9), [ECO-16](https://continental-team-ecologistica.atlassian.net/browse/ECO-16) y [ECO-20](https://continental-team-ecologistica.atlassian.net/browse/ECO-20) figuran `Listo`.
- **Código:** `backend/src/app/auth/`, `backend/src/app/pedidos/` y migración `20261009_01_pedidos_postgis.py`.
- **Pruebas:** `backend/tests/auth/`, `backend/tests/pedidos/` y `backend/tests/integracion/test_postgis.py`.
- **Límite:** el registro utiliza coordenadas seleccionadas manualmente, no un servicio automático universal de geocodificación. [ECO-11](https://continental-team-ecologistica.atlassian.net/browse/ECO-11) sigue en revisión; [ECO-15](https://continental-team-ecologistica.atlassian.net/browse/ECO-15) conserva la deuda de reenrutamiento del alcance histórico.

### Sprint 2 — flota

Implementamos alta/edición de vehículos con placa única y normalización, tipo, capacidad, combustible, consumo y estado; disponibilidad por fecha y horario con validación; exclusión de unidades no elegibles. Los datos se guardan en PostgreSQL con la migración `20261009_02_flota.py`.

- **Jira:** [ECO-12](https://continental-team-ecologistica.atlassian.net/browse/ECO-12) y [ECO-19](https://continental-team-ecologistica.atlassian.net/browse/ECO-19), ambas `Listo`.
- **Evidencia funcional histórica:** cinco de cinco criterios E2E en navegador con flota de prueba y PostGIS temporal el **09/10**; resultados conservados en la [Revisión del Sprint 2](Sprint%2002/03%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md).
- **Pruebas y datos:** `backend/tests/flota/`, `backend/tests/integracion/test_postgis.py` y `frontend/src/pages/PaginaFlota.tsx`.

### Sprint 3 — planificación, analítica prevista y calidad de integración

Implementamos vista previa de rutas por **fecha** para pedidos elegibles, selección de vehículos con turno y capacidad, secuencia y mapa para Planificación, advertencias de pedidos no asignados, guardado y reapertura por fecha. Añadimos indicadores **de planificación estimada** y controles de calidad en GitHub Actions.

| Elemento en Jira | Evidencia entregada | Estado |
|---|---|---|
| [ECO-22](https://continental-team-ecologistica.atlassian.net/browse/ECO-22) | `backend/src/app/rutas/`, `frontend/src/pages/PaginaRutas.tsx`, `frontend/src/components/MapaRutas.tsx`; pruebas de servicio/guardado/UI | Listo |
| [ECO-23](https://continental-team-ecologistica.atlassian.net/browse/ECO-23) | `backend/scripts/benchmark_rutas.py`, `backend/tests/rutas/test_benchmark.py`; puerta de CI que falla al exceder **45 s** | Listo |
| [ECO-17](https://continental-team-ecologistica.atlassian.net/browse/ECO-17) | `.github/workflows/ci.yml`, integración PostgreSQL/PostGIS y `backend/tests/test_openapi_contract.py` | Listo en el alcance **CI/OpenAPI**, no CD/Playwright |
| [ECO-25](https://continental-team-ecologistica.atlassian.net/browse/ECO-25) | `backend/src/app/indicadores/` y `frontend/src/pages/PaginaIndicadores.tsx`, pruebas de estado vacío/permisos y etiquetado de previsiones | Listo |

- **Demostración histórica:** diez de diez pasos manuales documentados el 30/10 con **seis pedidos y tres vehículos sintéticos** en [Pruebas E2E del Sprint 3](Sprint%2003/20261030%20Pruebas%20E2E%20V_1_0_0.md).
- **Benchmark histórico:** 150 pedidos / 12 vehículos en **1,13 s**, reportados en un ensayo **sintético** del 30/10; no equivale a rendimiento operativo.
- **Integración GitHub:** [PR #5](https://github.com/alexito-dev/EcoLogistica/pull/5) fusionado a `main`, commit **`8ac95644`**. [CI del PR anterior](https://github.com/alexito-dev/EcoLogistica/actions/runs/41120401761) aprobado; el [CI de `main` posterior a la fusión](https://github.com/alexito-dev/EcoLogistica/actions/runs/41120929684) es la ejecución que debemos consultar para constatar el estado del commit integrado.
- **Limitación funcional:** las rutas usan una heurística con distancias aproximadas, los indicadores miden escenarios previstos y la persistencia de rutas/usuarios continúa temporalmente en archivo JSON local.

## 4. Requisitos expresamente no cerrados al 30/10

| Jira | Obligación pendiente | Razón de no imputarla al Sprint 3 |
|---|---|---|
| [ECO-14](https://continental-team-ecologistica.atlassian.net/browse/ECO-14) y [ECO-26](https://continental-team-ecologistica.atlassian.net/browse/ECO-26) | Puntualidad/CO₂e basados en **entregas ejecutadas** | El dashboard de Sprint 3 es predictivo y no registra entregas reales |
| [ECO-13](https://continental-team-ecologistica.atlassian.net/browse/ECO-13) | Mapa de rutas asignadas para **Conducción** | El mapa de Sprint 3 corresponde a Planificación y Administración |
| [ECO-15](https://continental-team-ecologistica.atlassian.net/browse/ECO-15) | Reenrutamiento operativo ante incidencias | Pendiente desde el compromiso histórico del Sprint 1 |
| [ECO-21](https://continental-team-ecologistica.atlassian.net/browse/ECO-21) | Migrar cuentas/rutas a PostgreSQL y cifrar secretos TOTP | Los archivos JSON actuales son una solución provisional; el cifrado en reposo sigue pendiente |
| [ECO-24](https://continental-team-ecologistica.atlassian.net/browse/ECO-24) | Completar verificación WCAG 2.2 AA | Auditoría reportada **40/45 = 88,9 %**, inferior al objetivo interno ≥90 %; no presentamos conformidad global |
| [ECO-27](https://continental-team-ecologistica.atlassian.net/browse/ECO-27) | E2E Playwright, CD y controles de ramas | La CI ya existe, pero no sustituye un despliegue ni una suite Playwright |
| [ECO-18](https://continental-team-ecologistica.atlassian.net/browse/ECO-18) | Importación por plantilla | No existe entrega funcional verificada |

Nuestra regla es conservar esas incidencias en **backlog posterior**, con responsable y criterios, sin cerrarlas por conveniencia. También conservamos la épica duplicada ECO-7 marcada para no planificar y utilizamos ECO-6 como referencia canónica.

## 5. Control de calidad, aceptación y cierre

Comprobamos que los entregables y documentos correspondan al mismo repositorio y a sus tests. Distinguimos: **(a)** pruebas automatizadas y manuales, **(b)** aceptación del alcance funcional declarado, **(c)** transición Jira a Listo y **(d)** cierre administrativo. Un resultado sintético o un status de GitHub no sustituye la conformidad del producto ni el despliegue real. La autorización del usuario del 30/10 para completar los tres incrementos y regularizar Jira constituye el alcance de esta actuación; **no documentamos firmas, participantes o reuniones académicas que no constan**.

Para el siguiente Planning, retomamos las tareas abiertas, estimamos capacidad y puntos de manera prospectiva y mantenemos enlaces a los commits, pruebas y restricciones. No alteramos los reportes originales por efecto de esta conciliación.

**Fuentes oficiales internas:** [Revisión Sprint 1](Sprint%2001/03%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) · [Revisión Sprint 2](Sprint%2002/03%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) · [Revisión Sprint 3](Sprint%2003/01%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) · [Artefactos Jira](../02%20Planificaci%C3%B3n/02%20Artefactos%20Jira%20V_1_0_0.md) · [Plan funcional](../02%20Planificaci%C3%B3n/05%20Plan%20funcional%20de%20sprints.md).
