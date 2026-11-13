# Evaluación de usabilidad (SUS y heurísticas de Nielsen) — protocolo e instrumentos

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Fecha | 13/11/2026 |
| Guía de laboratorio | Semana 13 — Usabilidad (Nielsen, SUS, Playwright) |
| Estado | **Instrumentos y procesamiento listos; resultados pendientes de aplicar a personas usuarias** |

> **Declaración de integridad.** Este documento no contiene puntuaciones SUS ni resultados de Nielsen porque la evaluación **todavía no se ha aplicado**. La puntuación solo puede obtenerse de respuestas reales; no se simulan ni se estiman. Los ficheros de ejemplo de la guía de laboratorio no se incorporan como si fueran datos de EcoLogística.

## 1. Participantes y muestra

Aplicar a **5 personas como mínimo** por rol relevante (Planificación y Conducción), idealmente de DistriRápido S.A.C. o con perfil equivalente. Registrar rol, experiencia con herramientas de rutas y dispositivo usado, sin datos personales identificables.

## 2. Tareas guiadas

| # | Rol | Tarea | Éxito |
|---|---|---|---|
| T1 | Planificación | Entrar con MFA y registrar un pedido con ventana horaria | Pedido visible en el listado |
| T2 | Planificación | Generar y guardar las rutas de mañana | Mensaje «Rutas guardadas» |
| T3 | Planificación | Asignar un conductor a una ruta | Conductor visible en el seguimiento |
| T4 | Conducción | Abrir su ruta y marcar una entrega | Parada en estado Entregado |
| T5 | Conducción | Reportar una incidencia | Incidencia visible para Planificación |
| T6 | Planificación | Atender la incidencia (reprogramar) | Pedido de nuevo Pendiente |

Medir por tarea: éxito (sí/no), tiempo y errores. Las tareas T1–T6 se corresponden con las pruebas E2E [`sprint4-conduccion.spec.ts`](../../../frontend/e2e/sprint4-conduccion.spec.ts), que garantizan que el recorrido es técnicamente posible.

## 3. System Usability Scale (SUS)

Aplicar los 10 enunciados estándar con escala 1 (totalmente en desacuerdo) a 5 (totalmente de acuerdo), al finalizar las tareas:

1. Creo que me gustaría usar este sistema con regularidad.
2. Encuentro que este sistema es innecesariamente complejo.
3. Considero que el sistema es fácil de usar.
4. Creo que necesitaría ayuda de una persona con experiencia para usar este sistema.
5. Creo que las diversas funciones de este sistema están bien integradas.
6. Creo que hay demasiada inconsistencia en este sistema.
7. Imagino que la mayoría de las personas aprenderían a usar este sistema muy rápidamente.
8. Encuentro que el sistema es muy complicado de usar.
9. Me sentí muy confiado al usar el sistema.
10. Necesité aprender muchas cosas antes de poder usar el sistema.

**Procesamiento:** copiar [`scripts/usabilidad/respuestas_sus.plantilla.csv`](../../../scripts/usabilidad/respuestas_sus.plantilla.csv), registrar una fila por participante (columnas `P1`–`P10`) y ejecutar:

```powershell
python scripts\usabilidad\procesar_sus.py respuestas_sus.csv
```

La puntuación estándar es: preguntas impares (valor − 1), pares (5 − valor), suma × 2,5. Interpretación de la guía: **> 68 buena**, **50–68 aceptable**, **< 50 baja**. El cálculo está verificado por [`backend/tests/test_usabilidad_sus.py`](../../../backend/tests/test_usabilidad_sus.py) (casos extremos 0 y 100, valor neutro 50, validación de entradas).

## 4. Evaluación heurística de Nielsen

Cada evaluador califica de 1 (en total desacuerdo) a 5 (totalmente de acuerdo) las 10 heurísticas aplicadas a las vistas principales, y anota hallazgos con severidad 0–4:

| # | Heurística | Dónde observar en EcoLogística |
|---|---|---|
| 1 | Visibilidad del estado del sistema | Indicadores de carga, avisos `role="status"`, avance de la ruta |
| 2 | Relación entre el sistema y el mundo real | Estados «En ruta», «Entregado», «Incidencia»; lenguaje de logística |
| 3 | Control y libertad del usuario | Cancelar, «Volver» en la incidencia, reintentar entrega |
| 4 | Consistencia y estándares | Insignias, botones y menús entre vistas |
| 5 | Prevención de errores | Transiciones válidas, descripción obligatoria de incidencia |
| 6 | Reconocer en vez de recordar | Menú por rol, mapa de navegación |
| 7 | Flexibilidad y eficiencia | Filtros, paginación de 12, teclado |
| 8 | Estética y diseño minimalista | Densidad de información por pantalla |
| 9 | Ayuda para reconocer y corregir errores | Mensajes junto al campo, texto de ayuda |
| 10 | Ayuda y documentación | Texto de apoyo en acceso y MFA |

Procesar con el script de la guía de laboratorio (`procesar-nielsen.py`) tras registrar las respuestas en CSV.

## 5. Criterio de aceptación sugerido

SUS media > 68 con al menos 5 participantes por rol; ningún hallazgo de severidad 4 sin plan de corrección; tasa de éxito ≥ 80 % en T1–T6. Los resultados se anexarán a este documento (versión 1.1.0) con fecha, participantes (anónimos) y datos crudos.
