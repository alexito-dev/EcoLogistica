# Registro de impedimentos

[← Volver al README Principal](../../README.md)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla

**Líder del Proyecto:** Alex Jesus Zorrilla Apumayta

**Scrum Master / Facilitación del sprint:** Alex Jesus Zorrilla Apumayta

**Iteración:** ECO Sprint 1 (14/09/2026 – 28/09/2026) · **Corte del registro:** 02/10/2026

## Metadatos del documento

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Formato de fechas | DD/MM/AAAA |
| Escala de prioridad | Alta · Media · Baja |
| Estados válidos | Abierto · En Espera · Cerrado |
| Plantilla base | *Issues Log* del curso (`Registro de Impedimentos.xlsx`) |
| Documentos relacionados | [01 Informe de estado](01%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md) · [03 Revisión del Sprint](03%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) · [04 Retrospectiva](04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) · [Registro de riesgos](../02%20Planificaci%C3%B3n/03%20Registro%20de%20riesgos%20V_1_0_0.md) |

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 02/10/2026 | Alex Zorrilla | Primera emisión: 8 impedimentos del Sprint 1 con impacto, prioridad, responsable y trazabilidad de estado. |

## Registro

| Impedimento # | Fecha de Registro | Descripción del Impedimento así como el Impacto en el Proyecto | Prioridad | Reportado por | Fecha tope de Resolución | Estado | Fecha de Resolución | Resolución/Comentarios |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMP-001 | 11/09/2026 | **Historias duplicadas en Jira.** `ECO-18` y `ECO-19` se crearon como copias literales de `ECO-11` y `ECO-12`. **Impacto:** backlog con 2 ítems redundantes, puntos de historia inflados y riesgo de planificar trabajo duplicado en el Sprint Planning. | Media | Jose Luis Isidro Casio | 18/09/2026 | Cerrado | 18/09/2026 | Se renombraron a HU-008 "Importar pedidos por plantilla" y HU-009 "Parametrizar restricciones vehiculares". Backlog sincronizado en [02 Artefactos Jira](../02%20Planificaci%C3%B3n/02%20Artefactos%20Jira%20V_1_0_0.md). |
| IMP-002 | 18/09/2026 | **`ECO-19` (HU-009) asignada a la épica equivocada.** Quedó bajo EP-01 Gestión de pedidos en lugar de EP-02 Gestión de flota y conductores. **Impacto:** el roadmap y el avance por épica mostraban datos incorrectos y distorsionaban la planificación del Sprint 2. | Baja | Alex Zorrilla | 28/09/2026 | Cerrado | 02/10/2026 | Reasignación corregida en Jira por el equipo y confirmada por el líder el 02/10/2026; la épica de HU-009 es EP-02. |
| IMP-003 | 18/09/2026 | **Falta de permisos de administrador en Jira.** No se podía habilitar "Releases" (`v1.0.0-MVP`) ni quitar la columna extra "Listo" del tablero (5 columnas en vez de las 4 acordadas: To Do → In Progress → In Review/QA → Done). **Impacto:** flujo de trabajo distinto al definido en el proceso, evidencia 5 del entregable Jira sin completar y riesgo de métricas de tablero erróneas. | Media | Jose Luis Isidro Casio | 28/09/2026 | Cerrado | 02/10/2026 | Configuración ajustada en Jira por el equipo y confirmada por el líder el 02/10/2026. Acción de seguimiento: capturar la evidencia 5 (`assets/jira/05-release.png`) y reflejarla en el documento de Jira. |
| IMP-004 | 14/09/2026 | **Sprint 1 sin iniciar y con Sprint Goal desalineado del alcance.** Al verificar el proyecto el 18/09, el sprint seguía en estado "no iniciado" y su objetivo no coincidía con las historias cargadas (ECO-9, ECO-15). **Impacto:** 4 días de la iteración (≈ 29 %) sin ceremonias de Sprint Planning ni seguimiento de tablero; duración efectiva de ejecución menor a la planificada. | Alta | Alex Zorrilla | 18/09/2026 | Cerrado | 18/09/2026 | Sprint recreado con fechas 14/09–28/09 y Sprint Goal real ("Registrar pedidos con ventana horaria y permitir reenrutar una ruta ante incidencia"); iniciado el 18/09. Acción preventiva: iniciar el sprint el día de su Planning. |
| IMP-005 | 02/10/2026 | **Carpeta de entregables desalineada con la consigna.** El repositorio tenía `docs/03 Ejecución`, pero la consigna del Taller exige `docs/03 Implementación`. **Impacto:** entregables fuera de ruta penalizados en el criterio de ubicación y enlaces del README. | Media | Alex Zorrilla | 02/10/2026 | Cerrado | 02/10/2026 | Carpeta renombrada con `git mv` (se conserva historial) y README actualizado con los enlaces relativos a los 4 documentos del sprint. |
| IMP-006 | 28/09/2026 | **Dependencia técnica mal secuenciada entre HU-006 y HU-004.** Reenrutar ante incidencia (ECO-15 / HU-006, 5 pts) requiere el motor de optimización VRPTW (HU-004, 8 pts) y su benchmark (EN-001), planificados para el Sprint 2. **Impacto:** HU-006 era inalcanzable en el Sprint 1; 5 de 10 puntos (50 %) del compromiso nunca podían cumplirse y el Sprint Goal fue sobredimensionado. | Alta | Alex Zorrilla | 12/10/2026 | Abierto | — | HU-006 se reprograma detrás de HU-004 y EN-001 en el backlog. Se agrega al Sprint Planning una revisión obligatoria de dependencias técnicas y *Definition of Ready* con campo "depende de". Seguimiento en la [Retrospectiva](04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md). |
| IMP-007 | 18/09/2026 | **Sin código base ejecutable y cambio tardío de stack.** `backend/` y `frontend/` solo contienen `.gitkeep`; el 18/09, a mitad del sprint, se modificaron los documentos de arquitectura hacia Next.js + Nest.js sin evaluarlo en la matriz de stack; el 02/10 el líder ratificó React + Vite + FastAPI (Alternativa A, 93 %) y se revirtieron los documentos. **Impacto:** HU-001 (ECO-9, 5 pts) no pudo implementarse ni demostrarse; la decisión de stack no estuvo estable durante el sprint; riesgo de integración tardía (RSK-07). | Alta | Jhean Pier Julio Anco Porras | 12/10/2026 | Abierto | — | Plan: (1) *scaffold* de FastAPI y React + Vite con scripts `dev`/`test`, (2) cambio OpenSpec `registro-pedidos` con `propose → apply → verify → archive`, (3) CI mínimo (EN-006). Responsables: Anco Porras (backend), Vera Zea (frontend), Isidro Casio (CI). El stack se congela hasta el Sprint 3. |
| IMP-008 | 18/09/2026 | **Backlog de Jira incompleto y estimaciones sin validar.** Faltan crear HU-004, HU-010, HU-011, EN-001, EN-002, EN-003 y EN-004; sus puntos (Fibonacci) son propuestos y no validados por el equipo. **Impacto:** el Sprint Planning del Sprint 2 no puede cerrar capacidad ni dependencias con certeza; riesgo de repetir el desajuste de IMP-006. | Media | Jose Luis Isidro Casio | 05/10/2026 | En Espera | — | A la espera de una sesión de estimación (*Planning Poker*) con los cinco integrantes antes del Planning del Sprint 2. Una vez creadas las tarjetas, se actualiza [02 Artefactos Jira](../02%20Planificaci%C3%B3n/02%20Artefactos%20Jira%20V_1_0_0.md). |

## Resumen

| Estado | Cantidad | Impedimentos |
|---|---:|---|
| Cerrado | 5 | IMP-001, IMP-002, IMP-003, IMP-004, IMP-005 |
| Abierto | 2 | IMP-006, IMP-007 |
| En Espera | 1 | IMP-008 |
| **Total** | **8** | |

| Prioridad | Cantidad |
|---|---:|
| Alta | 3 (IMP-004, IMP-006, IMP-007) |
| Media | 4 (IMP-001, IMP-003, IMP-005, IMP-008) |
| Baja | 1 (IMP-002) |

## Reglas de gestión

1. Todo impedimento se registra el mismo día en que se detecta, con impacto concreto en alcance, cronograma, costo o calidad.
2. Los impedimentos de prioridad **Alta** se revisan en cada Daily y, si superan su fecha tope, se escalan al docente asesor en la siguiente sesión.
3. Un impedimento pasa a **Cerrado** solo con evidencia verificable (commit, captura de Jira o documento actualizado).
4. Un impedimento que materializa un riesgo del [Registro de riesgos](../02%20Planificaci%C3%B3n/03%20Registro%20de%20riesgos%20V_1_0_0.md) se vincula a su ID `RSK-xx` y se actualiza su probabilidad e impacto: IMP-006 → RSK-04; IMP-007 → RSK-07; IMP-003 → RSK-04.
