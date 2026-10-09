# Registro de impedimentos

[← Volver al README Principal](../../../README.md)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla

**Líder del Proyecto:** Alex Jesus Zorrilla Apumayta

**Facilitador del sprint:** Alex Jesus Zorrilla Apumayta

**Iteración:** ECO Sprint 2 (inicio 29/09/2026; revisión 09/10/2026) · **Corte del registro:** 02/10/2026

## Metadatos del documento

| Campo | Valor |
|---|---|
| Versión | 1.3.0 |
| Formato de fechas | DD/MM/AAAA |
| Escala de prioridad | Alta · Media · Baja |
| Estados válidos | Abierto · En Espera · Cerrado |
| Plantilla base | *Issues Log* del curso (`Registro de Impedimentos.xlsx`) |
| Continuidad | Se arrastran IMP-006 a IMP-008 del [Registro del Sprint 1](../02%20Registro%20de%20Impedimentos%20V_1_0_0.md); IMP-003 se incorpora reabierto tras la auditoría de Jira del 09/10. Los nuevos impedimentos se numeran desde IMP-009. |
| Documentos relacionados | [01 Informe de estado](01%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md) · [03 Revisión del Sprint](03%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) · [04 Retrospectiva](04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) · [Registro de riesgos](../../02%20Planificaci%C3%B3n/03%20Registro%20de%20riesgos%20V_1_0_0.md) |

> **Rebase funcional posterior (09/10/2026):** Sprint 1 conserva MFA/roles y pedidos persistentes; Sprint 2 gestiona flota; Sprint 3 genera rutas. El propósito de Sprint 4 para Conducción se mantiene. Este registro preserva su corte histórico; el estado vigente de implementación se documenta en el [plan de sprints](../../02%20Planificaci%C3%B3n/05%20Plan%20funcional%20de%20sprints.md).

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 02/10/2026 | Alex Zorrilla | Primera emisión del Sprint 2: 3 impedimentos arrastrados y 5 nuevos, con impacto, prioridad, responsable y trazabilidad de estado. |
| 1.1.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se actualiza IMP-008: ECO-20 ya está registrada; siguen pendientes la estimación de MFA y siete tarjetas de backlog. |
| 1.1.1 | 09/10/2026 | Anco Porras, Jhean Pier Julio | IMP-010 adopta ramas breves `feature/*` desde `main` y PR hacia `main`; `developer`, la protección de rama y CI permanecen pendientes. |
| 1.2.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se incorpora IMP-003 reabierto tras comprobar la configuración actual del tablero y la ausencia de versiones de entrega en Jira. |
| 1.2.1 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se precisa que ECO-20 sigue sin estimación aprobada ni persona asignada al corte previo a la revisión. |
| 1.2.2 | 09/10/2026 | Anco Porras, Jhean Pier Julio | IMP-011 pasa a En curso: pedidos y ubicaciones ya están en PostGIS; siguen pendientes usuarios, flota, rutas y cifrado de TOTP. |
| 1.2.3 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se localiza en español la etiqueta del rol de facilitación del sprint. |
| 1.2.4 | 09/10/2026 | Anco Porras, Jhean Pier Julio | ECO-16 se cierra con persistencia de pedidos y ubicaciones en Sprint 2; ECO-21 deja trazado el trabajo restante de EN-005. |
| 1.3.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se actualiza IMP-011 con la persistencia de flota y se documenta la rebase funcional posterior. |
| 1.4.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se delimita EN-005 restante a cuentas, secretos TOTP y rutas; la E2E confirmó Flota y quedó activa la API vigente en IPv6. |

## Registro

| Impedimento # | Fecha de Registro | Descripción del Impedimento así como el Impacto en el Proyecto | Prioridad | Reportado por | Fecha tope de Resolución | Estado | Fecha de Resolución | Resolución/Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMP-003 | 18/09/2026 | **(Reabierto del Sprint 1 el 09/10) Configuración de releases y columnas de Jira sin regularizar.** El tablero mantiene cinco columnas mezcladas y no hay una versión de entrega. **Impacto:** flujo incoherente con la documentación y evidencia 5 incompleta. | Media | Jose Luis Isidro Casio | Pendiente de confirmar | Abierto | Pendiente | `getJiraBoardConfig` confirma cinco columnas y mapeos incoherentes; `getJiraProjectVersions` devuelve cero versiones (ver [Artefactos Jira](../../02%20Planificaci%C3%B3n/02%20Artefactos%20Jira%20V_1_0_0.md)). La confirmación de ajuste del 02/10 no se refleja en la configuración consultada el 09/10. |
| IMP-006 | 28/09/2026 | **(Arrastrado del Sprint 1) Dependencia técnica entre HU-006 y HU-004.** Reenrutar ante incidencia (ECO-15) requiere el motor de optimización, que aún no existe. **Impacto:** HU-006 (5 pts) no puede planificarse; el valor diferencial del producto (reoptimización) sigue bloqueado. | Alta | Alex Zorrilla | 23/10/2026 | Abierto | — | HU-006 se mantiene detrás de HU-004 y EN-001 en el backlog. El motor se inicia en el Sprint 3 (R-S2-01 del [Informe](01%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md)). |
| IMP-007 | 18/09/2026 | **(Arrastrado del Sprint 1) Sin código base ejecutable y decisión de stack inestable.** `backend/` y `frontend/` estaban vacíos. **Impacto:** impedía demostrar cualquier historia. | Alta | Anco Porras, Jhean Pier Julio | 12/10/2026 | Cerrado | 02/10/2026 | Proyecto FastAPI (`backend/src/app`) y React + Vite (`frontend/src`) creados con scripts de ejecución y prueba; HU-001 y autenticación implementadas y publicadas en `main`. |
| IMP-008 | 18/09/2026 | **(Arrastrado del Sprint 1) Backlog de Jira incompleto y estimaciones sin validar.** Faltan HU-004, HU-010, HU-011 y EN-001 a EN-004. La historia técnica de autenticación ya se registró como ECO-20, sin estimación aprobada ni persona asignada al corte. **Impacto:** la velocidad y la capacidad del Sprint 3 no pueden calcularse con certeza. | Media | Jose Luis Isidro Casio | 12/10/2026 | En Espera | — | La regularización de Sprint 2 creó ECO-20 y mantuvo su estimación vacía y su asignación pendiente, sin inventar puntos ni responsable. Falta Planning Poker para ECO-20 y las siete tarjetas no creadas; no hay evidencia de que la sesión ya haya ocurrido. |
| IMP-009 | 29/09/2026 | **Propuesta de stack aplicada sin evaluación.** El commit `3565685` (18/09) cambió en `main` la arquitectura a Next.js + Nest.js sin puntuarla en la matriz del documento de stack, que favorecía React + FastAPI (93 %). **Impacto:** cinco documentos de la línea base se contradecían con la matriz; no se podía empezar a programar sin saber el stack. | Alta | Alex Zorrilla | 02/10/2026 | Cerrado | 02/10/2026 | El líder ratificó la Alternativa A. Se revirtieron el Acta, RES-06, el Modelo C4, las Restricciones y el Stack (versión 1.1.0 con historial). Regla nueva: todo cambio de stack exige ADR y nueva matriz (sección 12 del documento 10). |
| IMP-010 | 02/10/2026 | **Flujo de ramas sin aplicar de forma uniforme.** Los cambios del sprint se integraron directamente en `main` y la rama remota `developer` quedó desactualizada desde el 18/09. **Impacto:** falta revisión por *pull request* conforme a RES-17 y aumenta el riesgo de integrar defectos. | Media | Alex Zorrilla | 16/10/2026 | Abierto | — | Retirar `developer` como rama de integración y adoptar ramas breves `feature/*` desde `main`, con PR hacia `main`; configurar protección de rama y CI. Seguimiento en la acción A6 de la [Retrospectiva](04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md). |
| IMP-011 | 02/10/2026 | **Persistencia parcial de datos (EN-005).** Pedidos, ubicaciones y flota ya cuentan con persistencia PostgreSQL/PostGIS; las cuentas siguen en archivo, los secretos TOTP no se cifran en reposo y las rutas todavía no tienen tablas de aplicación. **Impacto pendiente:** falta completar RNF-06 y persistir las rutas antes de usarlas para planificar. | Alta | Anco Porras, Jhean Pier Julio | 23/10/2026 | En curso | — | ECO-16 cubre pedidos y ubicaciones. Después del corte histórico se añadió la migración `20261009_02` y la API de vehículos/disponibilidad; se verificó alta y permanencia tras reinicio en un PostGIS aislado. ECO-21 conserva el trabajo pendiente de cuentas, secretos TOTP y rutas, sin estimación ni sprint destino. El listener API anterior en `127.0.0.1:8000` no expone esa ruta; la API vigente está activa en `[::1]:8000`, dirección que resuelve primero `localhost` en el equipo local. |
| IMP-012 | 02/10/2026 | **Eventos de auditoría invisibles en ejecución real.** Durante la verificación extremo a extremo se detectó que los eventos de acceso no aparecían en la consola: las pruebas pasaban porque capturaban el registro internamente. **Impacto:** se habría incumplido el requisito de trazabilidad de accesos (base de RF-11.2) sin que las pruebas lo detectaran. | Alta | Alex Zorrilla | 02/10/2026 | Cerrado | 02/10/2026 | Se configuró el registro de la aplicación al arrancar y se agregó una prueba que lo verifica. Comprobado en el servidor real: los eventos salen en formato JSON y sin contraseñas ni tokens. |
| IMP-013 | 02/10/2026 | **Tipografía Codec Pro sin archivos con licencia.** La guía visual exige Codec Pro, una fuente comercial que no está en el repositorio. **Impacto:** la interfaz usa la fuente del sistema; la identidad visual queda incompleta en la demostración. | Baja | Jhoanna Hade Vera Zea | 09/10/2026 | Abierto | — | Las reglas `@font-face` ya están listas; falta obtener la licencia y colocar los 4 archivos `.woff2` según `frontend/public/fonts/LEEME.md`. Alternativa: usar una fuente libre equivalente si no se consigue la licencia. |

## Resumen

| Estado | Cantidad | Impedimentos |
|---|---:|---|
| Cerrado | 3 | IMP-007, IMP-009, IMP-012 |
| Abierto | 4 | IMP-003, IMP-006, IMP-010, IMP-013 |
| En curso | 1 | IMP-011 |
| En Espera | 1 | IMP-008 |
| **Total** | **9** | |

| Prioridad | Cantidad |
|---|---:|
| Alta | 5 (IMP-006, IMP-007, IMP-009, IMP-011, IMP-012) |
| Media | 3 (IMP-003, IMP-008, IMP-010) |
| Baja | 1 (IMP-013) |

## Vínculo con el registro de riesgos

| Impedimento | Riesgo materializado | Ajuste |
|---|---|---|
| IMP-003 | RSK-04 (configuración y métricas de Jira) | Mantener abierto hasta corregir las columnas y verificar la versión de entrega |
| IMP-006 | RSK-02 (rendimiento del motor) y RSK-04 (alcance y fechas) | RSK-02 se mantiene en exposición 15 (Alta) hasta tener el benchmark EN-001 |
| IMP-009 | RSK-04 (cambios de requisitos) | Se agrega control: ADR obligatorio para cambios de arquitectura |
| IMP-010 | RSK-07 (defectos de integración) | Se adelanta EN-006 (CI) al Sprint 3 |
| IMP-011 | RSK-10 (pérdida de datos) y RSK-06 (exposición de datos) | Se cerró la pérdida de pedidos al reiniciar y ya se persiste la flota; completar EN-005 para cuentas, secretos TOTP y rutas en el Sprint 3. |

## Reglas de gestión

1. Todo impedimento se registra el mismo día en que se detecta, con impacto concreto en alcance, cronograma, costo o calidad.
2. Los impedimentos de prioridad **Alta** se revisan en cada Daily y, si superan su fecha tope, se escalan al docente asesor.
3. Un impedimento pasa a **Cerrado** solo con evidencia verificable (commit, prueba, captura de Jira o documento actualizado).
4. Los impedimentos abiertos al cierre del sprint se arrastran al registro del sprint siguiente conservando su número.
