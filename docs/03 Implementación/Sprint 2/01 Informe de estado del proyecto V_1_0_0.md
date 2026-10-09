# Informe de estado del proyecto

[← Volver al README Principal](../../../README.md)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla

**Líder del Proyecto:** Alex Jesus Zorrilla Apumayta

**Fecha:** 2 de octubre de 2026

**Periodo del Informe:** 29/09/2026 – 02/10/2026 (Sprint 2, corte de mitad de iteración; el sprint se revisa en la Evaluación Parcial del 09/10/2026)

## Metadatos del documento

| Campo | Valor |
|---|---|
| Código del proyecto | PFA-TP2-ECOLOG-2026 |
| Versión | 1.1.3 |
| Iteración reportada | ECO Sprint 2 |
| Objetivo replanificado del sprint | "Entregar el primer incremento demostrable: registro de pedidos (HU-001) con acceso seguro por roles y verificación en dos pasos." |
| Fuentes | Historial Git (`main`), cambios OpenSpec `registro-pedidos` y `autenticacion-mfa`, resultados de pruebas automatizadas, [Retrospectiva del Sprint 1](../04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) |
| Documentos hermanos | [02 Registro de Impedimentos](02%20Registro%20de%20Impedimentos%20V_1_0_0.md) · [03 Revisión del Sprint](03%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) · [04 Retrospectiva del Sprint](04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) |
| Sprint anterior | [Informe de estado del Sprint 1](../01%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md) |

> **Actualización al 09/10/2026, antes de la revisión:** Jira mantiene el Sprint 2 id. 37 activo (29/09–12/10). Incluye ECO-9 / HU-001 (5 puntos) y ECO-20 / autenticación MFA (sin estimación aprobada); ambas están `Listo`. La métrica dinámica actual cuenta 2/2 incidencias completadas (100 %); no representa aceptación del producto ni cierre del sprint. El informe del Sprint 1 registra 0 de 2 al corte planificado del 28/09; Jira permaneció activo hasta el 09/10 y su métrica dinámica actual cuenta ECO-9 como completada por su estado `Listo` desde el 02/10. La revisión del Sprint 2 está prevista para hoy a las 15:40, hora de Lima; sus acuerdos y aceptación todavía están pendientes.

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 02/10/2026 | Alex Zorrilla | Primera emisión con el corte al 02/10/2026. Si hay avances hasta la revisión del 09/10, se publicará la versión 1.1.0. |
| 1.1.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se actualiza la evidencia de Jira, se registra ECO-20 sin puntos, se distingue la métrica dinámica del Sprint 1 de su corte planificado y se conserva pendiente la revisión del Sprint 2. |
| 1.1.1 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se aclara que la métrica dinámica actual de Sprint 1 cuenta a ECO-9 por su estado posterior al 28/09; no se usa como velocidad histórica del corte planificado. |
| 1.1.2 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se alinea la planificación futura de GitHub Actions y ramas con el flujo `feature/*` y PR hacia `main`; se mantiene pendiente retirar `developer`. |
| 1.1.3 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se registra la métrica actual de Jira (2/2 incidencias en `Listo`) y se aclara que no sustituye la aceptación ni el cierre formal del Sprint 2. |

## Resumen ejecutivo

El Sprint 2 corrigió el desvío del Sprint 1: el proyecto pasó de **0 a 1 historia de usuario completada** y entregó su **primer incremento de software funcional y demostrable**. El equipo replanificó el sprint siguiendo las acciones de la retrospectiva anterior: se priorizó la historia arrastrada **HU-001 (registrar pedido, 5 pts)** y se incorporó la **autenticación con verificación en dos pasos (RF-11.1)**, precondición de HU-001 ("despachador autenticado") y actividad de laboratorio de la semana 6. Ambas se construyeron con el ciclo **OpenSpec** (especificar, auditar, implementar, verificar y archivar) y quedaron publicadas en `main` con **139 pruebas automatizadas en verde**.

Al inicio del sprint también se **ratificó el stack React + FastAPI** (Alternativa A, 93 % en la matriz), revirtiendo una propuesta no evaluada, y se alinearon cinco documentos de la línea base. El alcance original del roadmap para este sprint (flota, geocodificación y motor de optimización) **no se inició** y pasa al Sprint 3.

## Estado del proyecto

| Variables de control | Descripción del estado |
| --- | --- |
| **Alcance** | 🟡 **1 historia de usuario completada: HU-001 / ECO-9 (5 pts), arrastrada del Sprint 1.** La historia técnica de **autenticación y autorización (RF-11.1)** también está completada y se registró como ECO-20 el 09/10, sin estimación de puntos. Avance del PMV: 1 de 11 historias de usuario originales (9 %). Del roadmap previsto (flota y motor) no se inició ningún ítem. |
| **Cronograma** | 🟡 **Recuperando, con atraso respecto del roadmap.** Al 02/10 han transcurrido 5,6 de 15 semanas (37 % del tiempo) y el avance funcional es del 9 % de las historias. La velocidad pasó de 0 a 5 puntos. El motor de optimización (camino crítico de HU-004 y HU-006) aún no empieza; es el principal riesgo de plazo. |
| **Costos** | 🟢 **Sin sobrecosto.** Gasto en infraestructura cloud a la fecha: S/ 0 (todo se ejecuta en local). Licencias: solo Jira, dentro de lo previsto. Las nuevas dependencias son de código abierto y sin costo (FastAPI, React, Argon2, PyOTP, PyJWT, Lucide y qrcode). Contingencia sin usar: S/ 5,843.40. |
| **Calidad** | 🟢 **139 pruebas automatizadas en verde: 100 de backend (cobertura del 99 %) y 39 de frontend.** 4 defectos detectados por las pruebas y la verificación, y corregidos dentro del sprint (ver [Revisión](03%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md)). Auditoría de la especificación de seguridad con 13 hallazgos, todos resueltos o declarados fuera de alcance. Validación estricta de OpenSpec, compilación de producción y linter correctos. |

Leyenda: 🟢 en control · 🟡 atención · 🔴 fuera de lo planificado.

### Indicadores del Sprint

| Indicador | Sprint 1 | Sprint 2 (corte 02/10) |
|---|---:|---:|
| Historias de usuario completadas | 0 | 1 (HU-001) |
| Puntos de historia completados (velocidad) | 0 | 5 |
| Historias técnicas completadas | 0 | 1 (autenticación RF-11.1) |
| Cambios OpenSpec completados y archivados | 0 | 2 |
| Pruebas automatizadas | 0 | 139 |
| Cobertura del backend | — | 99 % |
| Defectos abiertos | 0 | 0 |
| Commits en `main` desde el cierre del Sprint 1 | 0 | 8 |
| Impedimentos activos en el periodo (ver [Registro](02%20Registro%20de%20Impedimentos%20V_1_0_0.md)) | 8 | 8 (3 cerrados, 4 abiertos, 1 en espera) |

## Riesgos

| **Riesgo** | **Responsable** | **Mitigación** |
| -- | -- | -- |
| **R-S2-01 — Motor de optimización sin iniciar** (RSK-02, exposición 15, Alta). HU-004 y HU-006 dependen de él y es el núcleo del valor del producto (VRPTW/Green VRP). | Alexander Daniel Hilario Talavera | Iniciar en el Sprint 3 un prototipo con OR-Tools y el benchmark EN-001 (50/100/150 pedidos); entregar resultados parciales antes que nada. |
| **R-S2-02 — Concentración del trabajo en una persona.** Todos los commits del sprint son del líder; el conocimiento del código no está distribuido. | Alex Zorrilla | Asignar en el Sprint 3 un cambio OpenSpec por integrante (flota a backend, motor a optimización, mapa a frontend) con revisión cruzada por *pull request*. |
| **R-S2-03 — Persistencia en memoria y en archivo local.** Los pedidos se pierden al reiniciar y los secretos TOTP no están cifrados en reposo (RNF-04, RNF-06, RNF-11). | Anco Porras, Jhean Pier Julio | PostgreSQL + PostGIS con migraciones (EN-005) en el Sprint 3; los adaptadores ya están aislados detrás de puertos de repositorio. |
| **R-S2-04 — Integración sin CI.** Las pruebas solo se ejecutan en local; una regresión podría llegar a `main` (RSK-07). | Jose Luis Isidro Casio | GitHub Actions con pruebas de backend y frontend obligatorias en cada *pull request* (EN-006). |
| **R-S2-05 — Pérdida del autenticador.** Un usuario sin su teléfono no puede entrar; no existe restablecimiento del segundo factor. | Alex Zorrilla | Cambio OpenSpec posterior para restablecimiento por administrador con auditoría; mientras tanto, procedimiento manual documentado en el README. |
| **R-S2-06 — Ámbito geográfico aproximado** (rectángulo configurable sin validar con el negocio, RF-02.2). | Alex Zorrilla | Validar límites con DistriRápido y migrar a polígono PostGIS con EN-005. |

## Próximos avances

1. **Para la revisión del 09/10:** confirmar el incremento y registrar los acuerdos; ECO-20 ya está en Jira sin puntos aprobados. Los archivos licenciados de Codec Pro siguen pendientes. El Sprint 2 se cerrará en Jira al finalizar su periodo el 12/10.
2. **Sprint 3:** PostgreSQL + PostGIS con migraciones (EN-005) y adaptadores de repositorio reales para pedidos y usuarios.
3. **Sprint 3:** gestión de flota (HU-003 y HU-009) como cambio OpenSpec, asignado al responsable de backend.
4. **Sprint 3:** prototipo del motor de optimización y benchmark EN-001, prerrequisito de HU-004 y HU-006.
5. **Sprint 3:** CI en GitHub Actions (EN-006) y aplicación del flujo acordado de ramas `feature/*` con PR hacia `main`; retirar `developer` cuando el equipo confirme la migración.

## Notas

- El corte original del informe es 02/10/2026. La actualización del 09/10 añade el estado de Jira y conserva las cifras de pruebas del corte inicial; la ejecución local de backend, frontend y compilación del 09/10 se registra también en la auditoría de coherencia.
- La historia de autenticación responde a la actividad de la semana 6 del Taller (especificación auditada con el prompt "Auditor Senior de Arquitectura"); su evidencia está en `openspec/changes/archive/2026-10-02-autenticacion-mfa/`.
- Trazabilidad: [06 Requisitos funcionales](../../01%20Inicio/06.%20Requisitos%20funcionales%20V_1_0_0.md), [07 Requisitos no funcionales](../../01%20Inicio/07.%20Requisitos%20no%20funcionales%20V_1_0_0.md), [08 Usuarios](../../01%20Inicio/08.%20Usuarios%20V_1_0_0.md) y [10 Stack tecnológico](../../01%20Inicio/10.%20Stack%20tecnol%C3%B3gico%20V_1_0_0.md).
- Nomenclatura de versionado: *Semantic Versioning* `MAYOR.MENOR.PARCHE`, escrita en el nombre del archivo como `V_M_m_p`.
