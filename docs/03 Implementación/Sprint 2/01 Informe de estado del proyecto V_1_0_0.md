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
| Versión | 1.8.0 |
| Iteración reportada | ECO Sprint 2 |
| Objetivo replanificado del sprint | "Que Planificación inicie sesión con MFA, registre y consulte pedidos, y los conserve después de reiniciar la API." |
| Fuentes | Historial Git (`main`), cambios OpenSpec `registro-pedidos` y `autenticacion-mfa`, resultados de pruebas automatizadas, [Retrospectiva del Sprint 1](../04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) |
| Documentos hermanos | [02 Registro de Impedimentos](02%20Registro%20de%20Impedimentos%20V_1_0_0.md) · [03 Revisión del Sprint](03%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) · [04 Retrospectiva del Sprint](04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) |
| Sprint anterior | [Informe de estado del Sprint 1](../01%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md) |

> **Actualización Jira al 09/10/2026, 13:30 hora de Lima:** el Sprint 2 id. 37 tiene como meta la gestión de flota y contiene ECO-12 (5 puntos) y ECO-19 (5 puntos), ambas en `Listo` (2/2; 10 puntos estimados). ECO-9 y ECO-15 conservan su asociación histórica al Sprint 1 cerrado; ECO-16 y ECO-20 están completas en el backlog, fuera del Sprint 2 activo. La métrica dinámica de Sprint 1 es 1/2 (ECO-9 lista, ECO-15 pendiente), mientras el corte original del 28/09 permanece en 0/2. La E2E de flota aprobó 5/5 criterios; la revisión del Product Owner está prevista para hoy a las 15:40 y el Sprint 2 continúa activo.

> **Regresión local más reciente (09/10/2026):** se recolectaron y aprobaron 107 pruebas de backend y 39 de frontend; la compilación de producción terminó correctamente. El lint dejó dos advertencias de `set-state-in-effect`; el build avisó que faltan los cuatro archivos Codec Pro. No hay una suite automatizada de integración para los adaptadores PostgreSQL; la persistencia tras reiniciar se comprobó manualmente en una base aislada.

> **Rebase funcional posterior (09/10/2026):** el alcance vigente conserva en Sprint 1 el incremento de MFA/roles y pedidos persistentes; asigna a Sprint 2 la gestión de flota y a Sprint 3 la generación y consulta de rutas; el propósito de Sprint 4 sigue siendo la ejecución de rutas por Conducción. Este informe conserva el corte original; las metas y tarjetas de Jira ya se actualizaron para Sprint 2, sin reescribir el historial del Sprint 1 ni el resultado al 28/09. La decisión no equivale a una aceptación formal del Product Owner.

> **Evidencia posterior de Sprint 1 y 2 (09/10/2026):** la API, la migración PostgreSQL/PostGIS y la pantalla de flota implementan alta y consulta de vehículos para Administración, además de disponibilidad por fecha y elegibilidad para Planificación. La E2E web comprobó MFA, estos flujos de flota y el ciclo de registrar, buscar y abrir el detalle de un pedido, que siguió disponible tras reiniciar la API. Las cuentas de usuario continúan en archivo local; la persistencia de rutas y la protección de secretos TOTP quedan pendientes. La prueba usó una base aislada; los datos temporales se retiraron y la base local queda sin pedidos ni vehículos de prueba. La aceptación formal de Sprint 2 sigue pendiente.

> **Regresión técnica posterior (09/10/2026):** la suite del backend recolecta y aprueba 107 pruebas; la suite existente del frontend aprueba 39 y la compilación de producción termina correctamente. El lint termina con dos advertencias de actualización de estado dentro de efectos, una en Pedidos y otra en Flota; la compilación también advierte que los cuatro archivos Codec Pro no están incluidos. La E2E manual complementa las suites, que no incluyen pruebas de componente específicas para Flota.

> **E2E funcional de flota de Sprint 2 (09/10/2026):** se completaron en navegador los cinco criterios del plan: alta/edición, normalización y duplicados; rechazo de capacidades/consumo no positivos y turno invertido; motivo obligatorio al declarar no disponible; exclusión de unidades en Mantenimiento e Inactivo aun con turno registrado; y persistencia después de reiniciar la API. Resultado: **5/5 criterios aprobados**. Se usó PostGIS temporal aislado; tras el reinicio y una recarga web reaparecieron los tres vehículos y turnos, y solo el vehículo Disponible con disponibilidad activa resultó elegible. La cuenta, el contenedor y los registros se retiraron; la base local no recibió datos E2E. Jira refleja ECO-12 y ECO-19 en `Listo`. La revisión del Product Owner sigue programada para las 15:40 y no se registra antes de que ocurra.

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 02/10/2026 | Alex Zorrilla | Primera emisión con el corte al 02/10/2026. Si hay avances hasta la revisión del 09/10, se publicará la versión 1.1.0. |
| 1.1.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se actualiza la evidencia de Jira, se registra ECO-20 sin puntos, se distingue la métrica dinámica del Sprint 1 de su corte planificado y se conserva pendiente la revisión del Sprint 2. |
| 1.1.1 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se aclara que la métrica dinámica actual de Sprint 1 cuenta a ECO-9 por su estado posterior al 28/09; no se usa como velocidad histórica del corte planificado. |
| 1.1.2 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se alinea la planificación futura de GitHub Actions y ramas con el flujo `feature/*` y PR hacia `main`; se mantiene pendiente retirar `developer`. |
| 1.1.3 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se registra la métrica actual de Jira (2/2 incidencias en `Listo`) y se aclara que no sustituye la aceptación ni el cierre formal del Sprint 2. |
| 1.1.4 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se precisa el historial de estados de ECO-9 al cerrar Sprint 1 y al incorporarla a Sprint 2. |
| 1.1.5 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se limita la lectura de los 5 puntos al estado de Jira observado al corte del 02/10; no se presentan como velocidad aceptada antes de la revisión del sprint. |
| 1.1.6 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se precisa que ECO-20 no tiene persona asignada en Jira al corte previo a la revisión. |
| 1.1.7 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se explica el recorrido que ya puede completar Planificación en el sistema y se anotan sus límites de persistencia y acceso de demostración. |
| 1.1.8 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se ordenan los próximos pasos como un flujo completo de generación de rutas, con datos persistentes, flota y optimización como partes que lo habilitan. |
| 1.1.9 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se integra y comprueba persistencia PostGIS para pedidos; se actualiza el riesgo y queda pendiente ampliar EN-005 a cuentas, flota y rutas. |
| 1.2.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se incorpora ECO-16 al Sprint 2 con persistencia de pedidos y ubicaciones y se alinea la meta funcional del sprint en Jira; ECO-21 registra la ampliación pendiente de EN-005. |
| 1.2.1 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se registran las suites de regresión reejecutadas y se distingue su cobertura de la comprobación manual de PostGIS. |
| 1.3.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se agrega una nota de rebase funcional posterior, sin alterar el corte histórico del informe. |
| 1.4.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se documenta la implementación y la E2E web de flota como alcance vigente de Sprint 2, diferenciándolas de la aceptación formal pendiente. |
| 1.5.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se registra la regresión actual de backend, frontend y compilación, con las advertencias de lint y tipografía pendientes. |
| 1.6.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se registra el E2E completo de aceptación funcional de flota: 5/5 criterios aprobados, incluida persistencia tras reinicio. |
| 1.7.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se alinea el estado vigente de Jira con la rebase: ECO-12 y ECO-19 en `Listo`, 2/2; se preservan los cortes históricos previos. |
| 1.8.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se actualiza el corte Jira, se precisa la ubicación de ECO-15 y se registra la normalización del tablero a cuatro columnas. |

## Resumen ejecutivo

**Resumen del corte histórico al 02/10/2026:** el Sprint 2 corrigió el desvío del Sprint 1, priorizó HU-001 e incorporó MFA. Las cifras, el resumen y las decisiones de esta sección describen aquel corte; la línea base vigente se reordenó el 09/10 a MFA/pedidos para Sprint 1 y flota para Sprint 2, con rutas para Sprint 3.

En el sistema, Planificación puede iniciar sesión con MFA, registrar un pedido y luego buscarlo, filtrarlo o abrir su detalle. Los pedidos y sus coordenadas ya quedan en PostgreSQL/PostGIS y siguen disponibles tras reiniciar la API. Las cuentas son de demostración local, no están conectadas al correo institucional. La revisión de Sprint 2 sigue pendiente y la métrica de Jira no equivale a aceptación formal.

Al inicio del sprint también se **ratificó el stack React + FastAPI** (Alternativa A, 93 % en la matriz), revirtiendo una propuesta no evaluada, y se alinearon cinco documentos de la línea base. En el corte histórico inicial, el alcance original del roadmap para este sprint (flota, geocodificación y motor de optimización) **no se había iniciado**. La rebase funcional posterior asigna flota a este Sprint 2 y rutas al Sprint 3; el motor se integra como parte del recorrido de rutas según la capacidad acordada.

## Estado del proyecto

| Variables de control | Descripción del estado |
| --- | --- |
| **Alcance** | **Corte histórico del backlog:** 1 de 11 historias originales (9 %). **Línea base funcional vigente:** Sprint 1 conserva MFA/roles y pedidos persistentes; Sprint 2 se dedica a flota, cuyo E2E aprobó 5/5 criterios; Sprint 3 se dedica a generar y consultar rutas. Jira ya muestra ECO-12 y ECO-19 en `Listo` en Sprint 2; el Sprint 1 cerrado conserva su historia y el resultado 0/2 del corte original. |
| **Cronograma** | 🟡 **Recuperando, con atraso respecto del roadmap.** Al 02/10 han transcurrido 5,6 de 15 semanas (37 % del tiempo) y el avance funcional es del 9 % de las historias. Jira mostraba HU-001 (5 puntos) en `Listo` al corte del 02/10; este dato es provisional y no constituye velocidad aceptada en la revisión. El motor de optimización (camino crítico de HU-004 y HU-006) aún no empieza; es el principal riesgo de plazo. |
| **Costos** | 🟢 **Sin sobrecosto.** Gasto en infraestructura cloud a la fecha: S/ 0 (todo se ejecuta en local). Licencias: solo Jira, dentro de lo previsto. Las nuevas dependencias son de código abierto y sin costo (FastAPI, React, Argon2, PyOTP, PyJWT, Lucide y qrcode). Contingencia sin usar: S/ 5,843.40. |
| **Calidad** | **Corte del 02/10:** 100 pruebas de backend y 39 de frontend. **Regresión más reciente (09/10):** 107 de backend y 39 de frontend aprobadas; build de producción correcto. El lint conserva dos advertencias y faltan los archivos Codec Pro. La suite no integra los adaptadores PostgreSQL; la persistencia se verificó manualmente en PostGIS aislado. |

Leyenda: 🟢 en control · 🟡 atención · 🔴 fuera de lo planificado.

### Indicadores del Sprint

| Indicador | Sprint 1 | Sprint 2 (corte 02/10) |
|---|---:|---:|
| Historias de usuario completadas | 0 | 1 (HU-001) |
| Puntos de historia en `Listo` en Jira al corte indicado | 0 | 5 (02/10; provisional, revisión pendiente) |
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
| **R-S2-01 — Motor de optimización sin iniciar** (RSK-02, exposición 15, Alta). HU-004 y HU-006 dependen de él y es el núcleo del valor del producto (VRPTW/Green VRP). | Alexander Daniel Hilario Talavera | Incluir el motor y su benchmark EN-001 en la función de generar y guardar una ruta para Planificación; una optimización aislada no cuenta como flujo entregado. |
| **R-S2-02 — Concentración del trabajo de implementación en una persona.** Al corte inicial del 02/10, los primeros 8 commits del Sprint 2 en `main` eran de Alex Zorrilla. El historial consultado el 09/10 contenía 20 commits desde el 29/09: 12 de Alex y 8 de Anco Porras, Jhean Pier Julio, estos últimos de documentación; no se verificaron commits de implementación de los demás roles. | Alex Zorrilla | Repartir en el Sprint 3 la persistencia de rutas, la generación de secuencias, la optimización y la interfaz; usar la flota ya implementada, integrar el flujo en una demo y revisarlo entre integrantes. |
| **R-S2-03 — Persistencia parcial y secretos locales.** Pedidos, ubicaciones, vehículos y disponibilidades se guardan en PostgreSQL/PostGIS. Las cuentas siguen en archivo y los secretos TOTP no están cifrados en reposo (RNF-06); las rutas todavía no tienen tablas de aplicación. | Anco Porras, Jhean Pier Julio | ECO-16 cubre pedidos y ubicaciones; la migración `20261009_02` implementa flota. ECO-21 conserva trabajo pendiente para cuentas, secretos TOTP y rutas; se ajusta en Jira y se estima en Planning. |
| **R-S2-04 — Integración sin CI.** Las pruebas solo se ejecutan en local; una regresión podría llegar a `main` (RSK-07). | Jose Luis Isidro Casio | GitHub Actions con pruebas de backend y frontend obligatorias en cada *pull request* (EN-006). |
| **R-S2-05 — Pérdida del autenticador.** Un usuario sin su teléfono no puede entrar; no existe restablecimiento del segundo factor. | Alex Zorrilla | Cambio OpenSpec posterior para restablecimiento por administrador con auditoría; mientras tanto, procedimiento manual documentado en el README. |
| **R-S2-06 — Ámbito geográfico aproximado** (rectángulo configurable sin validar con el negocio, RF-02.2). | Alex Zorrilla | Validar límites con DistriRápido y migrar a polígono PostGIS con EN-005. |

## Próximos avances

1. **Para la revisión del 09/10:** mostrar el incremento de flota y registrar los acuerdos del Product Owner. El Sprint 2 tiene sus dos incidencias de flota en `Listo` y permanece activo hasta el cierre administrativo. ECO-20 sigue sin puntos aprobados ni persona asignada; los archivos licenciados de Codec Pro también siguen pendientes.
2. **Propuesta para Sprint 3, aún sin aprobar:** que Planificación elija pedidos pendientes, los asigne a vehículos con disponibilidad ya persistida en Sprint 2, y genere una ruta guardada que pueda volver a consultar. El alcance de rutas requiere persistencia de rutas y paradas (EN-005), generación de una secuencia factible (HU-004) y su medición (EN-001), además de integrar el flujo completo. HU-003 y HU-009 de gestión de flota quedan en Sprint 2 y ya cuentan con implementación. La capacidad, los puntos y la división final se confirman en el Planning; no se cuentan piezas técnicas aisladas como incremento terminado.
3. **Trabajo de calidad que acompaña ese flujo:** acordar cómo aplicar CI (EN-006), revisión cruzada y ramas breves en los PR; confirmar con el equipo la disposición de la rama `developer` antes de retirarla.
4. El alcance propuesto para Sprint 4 y sus historias se revisa después de estimar Sprint 3; ver el [Plan funcional de sprints](../../02%20Planificaci%C3%B3n/05%20Plan%20funcional%20de%20sprints.md).

## Notas

- El corte original del informe es 02/10/2026. La actualización del 09/10 añade el estado de Jira y conserva las cifras de pruebas del corte inicial; la ejecución local de backend, frontend y compilación del 09/10 se registra también en la auditoría de coherencia.
- La historia de autenticación responde a la actividad de la semana 6 del Taller (especificación auditada con el prompt "Auditor Senior de Arquitectura"); su evidencia está en `openspec/changes/archive/2026-10-02-autenticacion-mfa/`.
- Trazabilidad: [06 Requisitos funcionales](../../01%20Inicio/06.%20Requisitos%20funcionales%20V_1_0_0.md), [07 Requisitos no funcionales](../../01%20Inicio/07.%20Requisitos%20no%20funcionales%20V_1_0_0.md), [08 Usuarios](../../01%20Inicio/08.%20Usuarios%20V_1_0_0.md) y [10 Stack tecnológico](../../01%20Inicio/10.%20Stack%20tecnol%C3%B3gico%20V_1_0_0.md).
- Nomenclatura de versionado: *Semantic Versioning* `MAYOR.MENOR.PARCHE`, escrita en el nombre del archivo como `V_M_m_p`.
