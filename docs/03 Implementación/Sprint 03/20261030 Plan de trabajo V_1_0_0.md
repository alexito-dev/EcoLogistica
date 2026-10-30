# Plan de trabajo

[← Volver al README Principal](../../../README.md#93-fase-03-implementación)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla

**Líder del Proyecto:** Alex Jesus Zorrilla Apumayta

## Metadatos del documento

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Fecha | 30/10/2026 |
| Alcance | Cierre del Sprint 3 y trabajo propuesto para el Sprint 4 |
| Base | [Plan funcional de sprints](../../02%20Planificaci%C3%B3n/05%20Plan%20funcional%20de%20sprints.md), [01 Revisión](01%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) (pendientes) y [02 Retrospectiva](02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) (acciones) |
| Documentos relacionados | [03.2 Informe de estado](20261030%2003.2%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md) · [03.3 Impedimentos](20261030%2003.3%20Registro%20de%20Impedimentos%20V_1_0_0.md) · [Flujo de trabajo GitFlow](20261030%20Flujo%20de%20trabajo%20GitFlow%20V_1_0_0.md) |

> **Estado de los compromisos.** Las fechas salen de la Retrospectiva. Los puntos y la capacidad del Sprint 4 se definen en el *Planning* y en Jira.

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 30/10/2026 | Hilario Talavera, Alexander Daniel | Primera emisión. |

## 1. Cierre del Sprint 3

| # | Tarea | Responsable | Fecha límite | Estado |
|---:|---|---|---|---|
| 1 | Abrir el PR de `sprint-3/calidad-owasp-wcag` hacia `main` con revisión de otra persona | Isidro Casio, Jose Luis | 02/11/2026 | Pendiente |
| 2 | Emitir la Revisión del Sprint 1.1.0 con las observaciones de la Inspección 03 | Zorrilla Apumayta, Alex Jesus | Tras la Inspección 03 | Pendiente |
| 3 | Crear en Jira HU-004, EN-001 y la tarjeta de indicadores; registrar el estado real | Zorrilla Apumayta, Alex Jesus | Cierre del Sprint 3 | Pendiente |
| 4 | Actualizar los documentos previos afectados (Artefactos Jira, informes del Sprint 2) con nota del Sprint 3 | Equipo | Cierre del Sprint 3 | Pendiente |

## 2. Trabajo propuesto para el Sprint 4

| Prioridad | Trabajo | Origen | Responsable | Fecha límite |
|---:|---|---|---|---|
| 1 | Pasar las rutas guardadas y las cuentas a PostgreSQL (EN-005 / ECO-21) | Hoy están en archivos locales | Anco Porras, Jhean Pier Julio | Sprint 4 |
| 2 | Repetir el benchmark del motor con el volumen real (EN-001) | Hoy se midió con datos sintéticos | Hilario Talavera, Alexander Daniel | 13/11/2026 |
| 3 | Volver a ejecutar SonarQube tras la refactorización de `planificar()` | Calidad, S3776 | Hilario Talavera, Alexander Daniel | 06/11/2026 |
| 4 | Comprobar en GitHub el CI ampliado a `sprint-*` y `feature/*` | Retrospectiva, acción 7 | Isidro Casio, Jose Luis | 06/11/2026 |
| 5 | SonarQube en el CI | Retrospectiva, acción 8 | Isidro Casio, Jose Luis | 13/11/2026 |
| 6 | Versiones de Python bloqueadas y Actions fijadas por SHA | OWASP A08 | Anco Porras, Jhean Pier Julio | 13/11/2026 |
| 7 | Prueba de interfaz con axe-core en las 4 vistas | WCAG, regresión | Vera Zea, Jhoanna Hade | 13/11/2026 |
| 8 | Cifrar secretos TOTP y mover cuentas a PostgreSQL | OWASP A04 | Anco Porras, Jhean Pier Julio | Sprint 4 |
| 9 | Decidir OSRM propio o anonimización | OWASP A06 | Equipo | Planning del Sprint 4 |

## 3. Hitos

| Hito | Fecha |
|---|---|
| Reunión de revisión del Sprint 3 | 29/10/2026, 22:30 |
| Inspección 03 | Semana 11 del curso |
| Primer bloque de mejoras de proceso (tareas 3 y 4) | 06/11/2026 |
| Benchmark, SonarQube en CI y axe-core | 13/11/2026 |

## 4. Dependencias y riesgos

- HU-006 (reenrutar) depende de pasar las rutas a PostgreSQL.
- El Sprint 4 supone la ejecución por Conducción; ese alcance no se compromete hasta cerrar el punto 1.
- Riesgos en el [Registro de riesgos](../../02%20Planificaci%C3%B3n/03%20Registro%20de%20riesgos%20V_1_0_0.md).
