# Evaluación cuantitativa de usabilidad (SUS)

[← Volver al README principal](../../../README.md#93-fase-03-implementación)

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Fecha | 20/11/2026 |
| Sistema evaluado | EcoLogística Huancayo (interfaz web, roles Planificación y Conducción) |
| Instrumento | System Usability Scale (SUS), 10 ítems, escala Likert 1–5 |
| Estado de la medición | **Instrumento, tareas y cálculo listos y probados; respuestas de personas usuarias aún no registradas** |
| Documentos relacionados | [Protocolo del Sprint 4](../Sprint%2004/08%20Protocolo%20SUS%20y%20Nielsen%20V_1_0_0.md) · [Evaluación heurística](../Sprint%2004/09%20Evaluaci%C3%B3n%20heur%C3%ADstica%20de%20Nielsen%20V_1_0_0.md) |

> **Declaración de integridad.** Este documento **no contiene puntuaciones SUS de personas reales** porque la encuesta todavía no se ha aplicado. Una puntuación SUS solo existe con respuestas auténticas; inventarlas o estimarlas invalidaría el informe. Lo que sí está terminado y verificado es todo lo necesario para obtenerla en una sesión de unos 30 minutos: la ficha técnica, las tareas, la hoja de respuestas, el cálculo automatizado con grado A–F y su [prueba automática](../../../backend/tests/test_usabilidad_sus.py). La sección 3.3 muestra el cálculo con un **ejemplo ilustrativo señalado como tal**, que no representa datos del proyecto.

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 20/11/2026 | Hilario Talavera, Alexander Daniel | Primera emisión: ficha técnica, tareas, cálculo SUS con grado A–F, análisis de cuellos de botella y plan de mejora. |

## 1. Ficha técnica de la evaluación

| Aspecto | Definición |
|---|---|
| Instrumento | SUS (Brooke, 1996): 10 enunciados alternando tono positivo (impares) y negativo (pares). Equivalente en español aprobado en la [guía de laboratorio](../Sprint%2004/08%20Protocolo%20SUS%20y%20Nielsen%20V_1_0_0.md#3-system-usability-scale-sus) |
| Escala de valoración | Likert de 1 (totalmente en desacuerdo) a 5 (totalmente de acuerdo) |
| Perfil de la muestra | Personas de Planificación y de Conducción de DistriRápido S.A.C. o con perfil equivalente (quien programa rutas; quien las ejecuta en reparto). Se registran rol, experiencia previa con herramientas de rutas y dispositivo, sin datos personales |
| Tamaño de la muestra (*n*) | Mínimo **5 personas** (rúbrica y práctica habitual para una primera medición); idealmente 5 por rol |
| Modalidad | Prueba moderada: la persona ejecuta las tareas sin ayuda y responde el SUS inmediatamente después |
| Entorno | Demostración local reproducible con `scripts\iniciar-demo.ps1` (datos sintéticos de Huancayo y cuentas de demostración con contraseña y TOTP) |
| Fecha de aplicación | No aplicada al 20/11/2026 |

### 1.1. Tareas que ejecutan los evaluadores antes de responder

Las seis tareas coinciden con el recorrido que la prueba E2E [`sprint4-conduccion.spec.ts`](../../../frontend/e2e/sprint4-conduccion.spec.ts) y los flujos críticos [`criticos.spec.ts`](../../../frontend/e2e/criticos.spec.ts) garantizan que es técnicamente posible en Chromium, Firefox y WebKit; así, un resultado SUS bajo se atribuye al diseño y no a un defecto funcional.

| # | Rol | Tarea | Éxito |
|---|---|---|---|
| T1 | Planificación | Entrar con contraseña y TOTP y registrar un pedido con ventana horaria | Pedido visible en la lista |
| T2 | Planificación | Generar y guardar las rutas de mañana | Mensaje «Rutas guardadas» |
| T3 | Planificación | Asignar un conductor a una ruta | Conductor visible en Seguimiento |
| T4 | Conducción | Abrir su ruta y marcar una entrega | Parada en estado Entregado |
| T5 | Conducción | Reportar una incidencia con su descripción | Incidencia visible para Planificación |
| T6 | Planificación | Atender la incidencia (reprogramar) | Pedido de nuevo Pendiente |

Por tarea se registra: éxito (sí/no), tiempo y errores. Criterio de aceptación propuesto: tasa de éxito ≥ 80 % en T1–T6.

## 2. Registro de las respuestas

Las respuestas se guardan en un CSV a partir de la [plantilla](../../../scripts/usabilidad/respuestas_sus.plantilla.csv): una fila por participante, columnas `P1` a `P10` con valores del 1 al 5.

```powershell
Copy-Item scripts\usabilidad\respuestas_sus.plantilla.csv respuestas_sus.csv
# registrar una fila por participante y luego:
python scripts\usabilidad\procesar_sus.py respuestas_sus.csv --markdown
```

La salida (tabla de respuestas brutas, cálculo paso a paso por participante y resultado global con grado) se pega en la sección 3 de este documento y se publica como versión 1.1.0.

## 3. Resultados cuantitativos

### 3.1. Estado

Al 20/11/2026 el archivo de respuestas no existe: **n = 0**. No se reportan promedios.

### 3.2. Fórmula de conversión

| Tipo de ítem | Ítems | Contribución (0–4) |
|---|---|---|
| Positivos (impares) | 1, 3, 5, 7, 9 | valor − 1 |
| Negativos (pares) | 2, 4, 6, 8, 10 | 5 − valor |

`SUS individual = (suma de las 10 contribuciones) × 2,5` → rango 0–100. `SUS global = promedio de los SUS individuales`.

### 3.3. Ejemplo ilustrativo del cálculo (no son datos del proyecto)

Respuestas de una persona hipotética `[4, 2, 5, 1, 4, 2, 5, 2, 4, 1]`, las mismas que usa la prueba automática para verificar el algoritmo:

| Ítem | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Respuesta | 4 | 2 | 5 | 1 | 4 | 2 | 5 | 2 | 4 | 1 |
| Regla | 4 − 1 | 5 − 2 | 5 − 1 | 5 − 1 | 4 − 1 | 5 − 2 | 5 − 1 | 5 − 2 | 4 − 1 | 5 − 1 |
| Contribución | 3 | 3 | 4 | 4 | 3 | 3 | 4 | 3 | 3 | 4 |

Suma = 3+3+4+4+3+3+4+3+3+4 = **34** → SUS = 34 × 2,5 = **85,0**. Valores de referencia comprobados por prueba automática: todas las respuestas ideales = 100, todas las peores = 0, todas neutras (3) = 50.

## 4. Análisis e interpretación

### 4.1. Cómo se ubicará el puntaje

| Referencia | Criterio |
|---|---|
| Umbral de aceptación de la industria | **SUS ≥ 68** (promedio de miles de estudios) |
| Interpretación de la guía de laboratorio | > 68 buena · 50–68 aceptable · < 50 baja |

Clasificación por grados (curva de Sauro y Lewis, 2016) que calcula el script:

| SUS | Grado | Adjetivo |
|---|---|---|
| ≥ 84,1 | A+ | Excelente |
| 80,8 – 84,0 | A | Excelente |
| 78,9 – 80,7 | A− | Excelente |
| 77,2 – 78,8 | B+ | Bueno |
| 74,1 – 77,1 | B | Bueno |
| 72,6 – 74,0 | B− | Bueno |
| 71,1 – 72,5 | C+ | Aceptable |
| 65,0 – 71,0 | C | Aceptable |
| 62,7 – 64,9 | C− | Aceptable |
| 51,7 – 62,6 | D | Pobre |
| < 51,7 | F | Inaceptable |

Con n pequeño (5–10), el promedio tiene un margen de error amplio: el informe 1.1.0 debe publicar también la desviación estándar, el mínimo y el máximo, y no solo el promedio.

### 4.2. Cuellos de botella de interfaz identificados hasta ahora

Provienen de la [evaluación heurística de Nielsen](../Sprint%2004/09%20Evaluaci%C3%B3n%20heur%C3%ADstica%20de%20Nielsen%20V_1_0_0.md) (una persona evaluadora, no sustituye al SUS) y de la ejecución de las pruebas de este sprint.

| Origen | Hallazgo | Ítems SUS que probablemente lo reflejen |
|---|---|---|
| Heurística H1 (sev. 3) | «Mi ruta» y «Seguimiento» abrían en el día de hoy y mostraban «No hay rutas» cuando Planificación había guardado las de mañana | 2, 3 |
| Heurística H2 (sev. 3) | «Reprogramar» cerraba la incidencia con un clic irreversible | 9 |
| Heurística H3 (sev. 2) | Los errores de importación usaban nombres técnicos de campo | 4, 10 |
| Heurística H4 (sev. 3) | Una entrega marcada por error no se puede revertir | 9 |
| Heurística H5 (sev. 2) | Asignar el mismo conductor a varios vehículos obliga a elegirlo uno por uno | 8 |
| Heurística H9 (sev. 2) | No hay manual breve para personas usuarias | 4, 10 |
| Pruebas E2E del Sprint 4 | El segundo factor TOTP solo acepta cada código una vez: reingresar con la misma cuenta antes de 30 s obliga a esperar la ventana siguiente. Es una decisión de seguridad (RF-11.1), pero puede percibirse como espera en sesiones de prueba y en cambios rápidos de turno | 1, 8 |

### 4.3. Mejoras aplicadas y propuestas

| Estado | Mejora |
|---|---|
| Aplicada (Sprint 4) | H1: la vista abre en el día siguiente cuando hoy no hay rutas y lo avisa |
| Aplicada (Sprint 4) | H2: confirmación explícita al reprogramar una incidencia |
| Aplicada (Sprint 4) | H3: errores de importación por fila y columna con lenguaje legible |
| Propuesta | H4: ventana de corrección de pocos minutos con registro, tras acordar la regla con Planificación |
| Propuesta | H5: asignación del mismo conductor a todos los vehículos del día |
| Propuesta | H9: manual breve para Planificación y Conducción |
| Propuesta | Informar en pantalla el tiempo restante del código TOTP y que el código ya fue usado, para reducir la confusión |

Cada mejora aplicada tras la medición se volverá a evaluar con el mismo instrumento para comparar el SUS antes y después.

## 5. Criterio de cierre de este informe

Este documento pasa a la versión 1.1.0 cuando tenga: n ≥ 5 (con rol y dispositivo por participante), la matriz de respuestas brutas, el cálculo paso a paso generado por `procesar_sus.py --markdown`, el SUS global con su grado, la tasa de éxito por tarea y la decisión sobre los hallazgos de severidad 3. Responsable propuesto: Vera Zea, Jhoanna Hade (Interfaz / experiencia de usuario), según la acción 3 de la [Retrospectiva](02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md#acciones-a-realizar).
