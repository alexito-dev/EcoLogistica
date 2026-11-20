# Evaluación cuantitativa de usabilidad (SUS)

[← Volver al README principal](../../../README.md#93-fase-03-implementación)

| Campo | Valor |
|---|---|
| Versión | 1.1.0 |
| Fecha | 20/11/2026 |
| Sistema evaluado | EcoLogística Huancayo, https://ecologistica.arno.services (roles Planificación y Conducción) |
| Instrumento | System Usability Scale (SUS), 10 ítems, escala Likert 1–5 |
| Resultado | **SUS promedio 77,5 / 100 · grado B+ (Bueno) · n = 5 · supera el umbral de 68** |
| Documentos relacionados | [Protocolo SUS y Nielsen](08%20Protocolo%20SUS%20y%20Nielsen%20V_1_0_0.md) · [Evaluación heurística](09%20Evaluaci%C3%B3n%20heur%C3%ADstica%20de%20Nielsen%20V_1_0_0.md) |

> **Alcance y límites de los datos.** Las diez respuestas de cada una de las cinco personas fueron entregadas por el director del proyecto a quien redactó este informe y se procesaron sin modificarlas con el script [`procesar_sus.py`](../../../scripts/usabilidad/procesar_sus.py). No se registraron, y por eso no se informan, la tasa de finalización de tareas, los tiempos, los errores ni la fecha y modalidad exacta de cada sesión. El grupo es una **muestra por conveniencia de estudiantes y egresados de Ingeniería de Sistemas**, no personal de DistriRápido S.A.C.; el resultado orienta las mejoras, pero no representa a la población de personas usuarias finales.

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 20/11/2026 | Hilario Talavera, Alexander Daniel | Primera emisión: ficha técnica, tareas, cálculo SUS con grado A–F, análisis de cuellos de botella y plan de mejora (sin respuestas de personas usuarias). |
| 1.1.0 | 20/11/2026 | Zorrilla Apumayta, Alex Jesus | Se incorporan las respuestas de 5 personas, la matriz bruta, el cálculo paso a paso, el SUS global con grado y la interpretación. |

## 1. Ficha técnica de la evaluación

| Aspecto | Definición |
|---|---|
| Instrumento | SUS (Brooke, 1996): 10 enunciados que alternan tono positivo (impares) y negativo (pares). Redacción en español en el [protocolo](08%20Protocolo%20SUS%20y%20Nielsen%20V_1_0_0.md#3-system-usability-scale-sus) |
| Escala de valoración | Likert de 1 (totalmente en desacuerdo) a 5 (totalmente de acuerdo) |
| Tamaño de la muestra (*n*) | **5 personas** |
| Perfil de la muestra | Estudiantes y egresados de Ingeniería de Sistemas e Informática, de la condición académica declarada por el equipo (tabla siguiente); no se verificó su experiencia previa con sistemas logísticos |
| Modalidad | Prueba guiada: la persona usa el sistema en el entorno desplegado y responde el SUS al terminar; el facilitador gestiona el acceso con el código de la aplicación autenticadora |
| Entorno | Producción en https://ecologistica.arno.services con datos sintéticos de Huancayo |
| Fecha | Respuestas entregadas el 20/11/2026; fecha y modalidad de cada sesión, no registradas |

| Código | Condición académica declarada |
|---|---|
| P01 | X ciclo |
| P02 | Egresada |
| P03 | VIII ciclo |
| P04 | IX ciclo |
| P05 | Egresado |

Se usan códigos y no nombres para proteger la identidad de las personas evaluadoras.

### 1.1. Tareas que ejecutan los evaluadores antes de responder

| # | Rol | Tarea | Criterio de finalización |
|---|---|---|---|
| T1 | Planificación | Registrar un pedido | El pedido aparece guardado |
| T2 | Planificación | Guardar las rutas del día siguiente | Las rutas quedan registradas |
| T3 | Planificación | Asignar un conductor a una ruta | La ruta muestra el conductor asignado |
| T4 | Conducción | Marcar una entrega como entregada | El estado de la entrega se actualiza |
| T5 | Conducción | Reportar una incidencia | La incidencia queda registrada |
| T6 | Planificación | Reprogramar esa incidencia | La nueva programación es visible |

Las seis tareas corresponden al recorrido que garantizan las pruebas E2E [`sprint4-conduccion.spec.ts`](../../../frontend/e2e/sprint4-conduccion.spec.ts) y [`criticos.spec.ts`](../../../frontend/e2e/criticos.spec.ts) en Chromium, Firefox y WebKit; así, un resultado bajo se atribuye al diseño y no a un defecto funcional. **El resultado por tarea no se registró** en estas sesiones.

## 2. Resultados cuantitativos

### 2.1. Respuestas brutas (escala 1–5)

| Participante | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | P10 |
|---|---|---|---|---|---|---|---|---|---|---|
| P01 | 4 | 2 | 4 | 2 | 4 | 2 | 4 | 2 | 4 | 1 |
| P02 | 5 | 2 | 4 | 1 | 5 | 2 | 4 | 1 | 4 | 2 |
| P03 | 4 | 3 | 4 | 2 | 4 | 3 | 4 | 2 | 3 | 2 |
| P04 | 4 | 2 | 5 | 2 | 4 | 1 | 5 | 2 | 4 | 2 |
| P05 | 4 | 2 | 4 | 3 | 5 | 2 | 4 | 2 | 4 | 2 |

### 2.2. Fórmula de conversión

| Tipo de ítem | Ítems | Contribución (0–4) |
|---|---|---|
| Positivos (impares) | 1, 3, 5, 7, 9 | valor − 1 |
| Negativos (pares) | 2, 4, 6, 8, 10 | 5 − valor |

`SUS individual = (suma de las 10 contribuciones) × 2,5` (rango 0–100). `SUS global = promedio de los SUS individuales`.

### 2.3. Cálculo paso a paso

| Participante | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | Suma | SUS = suma × 2,5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P01 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 4 | 31 | 31 × 2,5 = 77,5 |
| P02 | 4 | 3 | 3 | 4 | 4 | 3 | 3 | 4 | 3 | 3 | 34 | 34 × 2,5 = 85,0 |
| P03 | 3 | 2 | 3 | 3 | 3 | 2 | 3 | 3 | 2 | 3 | 27 | 27 × 2,5 = 67,5 |
| P04 | 3 | 3 | 4 | 3 | 3 | 4 | 4 | 3 | 3 | 3 | 33 | 33 × 2,5 = 82,5 |
| P05 | 3 | 3 | 3 | 2 | 4 | 3 | 3 | 3 | 3 | 3 | 30 | 30 × 2,5 = 75,0 |

Ejemplo detallado, P01: ítems impares (4, 4, 4, 4, 4) → 3 + 3 + 3 + 3 + 3 = 15; ítems pares (2, 2, 2, 2, 1) → 3 + 3 + 3 + 3 + 4 = 16; suma = 31; SUS = 31 × 2,5 = **77,5**.

### 2.4. Resultado global

| Indicador | Valor |
|---|---|
| Participantes (*n*) | 5 |
| **SUS promedio** | **77,5** = (77,5 + 85,0 + 67,5 + 82,5 + 75,0) / 5 |
| Desviación estándar | 6,85 |
| Mínimo / máximo | 67,5 / 85,0 |
| Grado (Sauro y Lewis, 2016) | **B+ — Bueno** |
| Umbral de aceptación ≥ 68 | **Sí** (cuatro de cinco personas lo superan; P03 queda 0,5 puntos por debajo) |

### 2.5. Contribución media por ítem

| Ítem | Enunciado resumido | Media (0–4) |
|---|---|---:|
| 1 | Usaría el sistema con regularidad | 3,2 |
| 2 | Es innecesariamente complejo | 2,8 |
| 3 | Es fácil de usar | 3,2 |
| 4 | Necesitaría ayuda de una persona experta | 3,0 |
| 5 | Las funciones están bien integradas | 3,4 |
| 6 | Hay demasiada inconsistencia | 3,0 |
| 7 | La mayoría aprendería rápido | 3,2 |
| 8 | Es muy complicado de usar | 3,2 |
| 9 | Me sentí confiado al usarlo | 2,8 |
| 10 | Necesité aprender muchas cosas antes | 3,2 |

## 3. Análisis e interpretación

### 3.1. Ubicación respecto de la referencia

| Referencia | Resultado |
|---|---|
| Umbral de aceptación de la industria (SUS ≥ 68) | 77,5: **supera el umbral** por 9,5 puntos |
| Interpretación de la guía de laboratorio (> 68 buena · 50–68 aceptable · < 50 baja) | **Buena** |
| Grado y adjetivo (curva de Sauro y Lewis) | **B+ — Bueno** |

Clasificación por grados que aplica el script:

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

### 3.2. Lectura crítica

- **Con *n* = 5, el promedio tiene un margen de error amplio.** Con una desviación estándar de 6,85, el resultado se interpreta como una señal favorable y no como una medida precisa; el grado B+ queda a 0,3 puntos del límite inferior (77,2) y podría cambiar a B con una sola respuesta distinta.
- **La muestra no son las personas usuarias reales** (personal de Planificación y Conducción de DistriRápido S.A.C.); son estudiantes y egresados de la misma carrera, con más soltura técnica que el promedio. El puntaje podría ser menor con personal de reparto.
- **No se midió el desempeño** (finalización, tiempo, errores): el SUS mide usabilidad *percibida* y no demuestra por sí solo que las tareas se completaran.
- Las respuestas fueron recogidas por el equipo del proyecto, lo que puede inclinar las respuestas hacia lo favorable (sesgo de cortesía).

### 3.3. Cuellos de botella de interfaz

**Lo que muestran los datos.** Las contribuciones más bajas son los ítems **2** («innecesariamente complejo», 2,8) y **9** («me sentí confiado», 2,8), seguidos de los ítems **4** («necesitaría ayuda de una persona experta») y **6** («demasiada inconsistencia»), ambos con 3,0. La persona con el puntaje más bajo (P03, 67,5) respondió 3 en los ítems 2, 6 y 9. Es decir: el sistema se percibe fácil de integrar (ítem 5, la mejor media, 3,4), pero con **algo de complejidad inicial y menos confianza al operarlo**.

**Hipótesis que explicarían esas respuestas** (provienen de la [evaluación heurística de Nielsen](09%20Evaluaci%C3%B3n%20heur%C3%ADstica%20de%20Nielsen%20V_1_0_0.md), hecha por una persona evaluadora; no se observaron directamente en las sesiones):

| Origen | Hallazgo | Ítems SUS relacionados |
|---|---|---|
| Heurística H4 (sev. 3) | Una entrega marcada por error no se puede revertir: resta confianza | 9 |
| Heurística H9 (sev. 2) | No hay manual breve para personas usuarias | 4, 10 |
| Heurística H5 (sev. 2) | Asignar el mismo conductor a varios vehículos obliga a elegirlo uno por uno | 2, 8 |
| Pruebas E2E | El segundo factor TOTP acepta cada código una sola vez, lo que obliga a esperar la ventana siguiente al reingresar con la misma cuenta; es una decisión de seguridad, pero puede percibirse como espera o complejidad | 2, 9 |

### 3.4. Mejoras aplicadas y propuestas

| Estado | Mejora |
|---|---|
| Aplicada antes de esta medición | H1: «Mi ruta» y «Seguimiento» abren en el día siguiente cuando hoy no hay rutas y lo avisan |
| Aplicada antes de esta medición | H2: confirmación explícita al reprogramar una incidencia |
| Aplicada antes de esta medición | H3: errores de importación por fila y columna, en lenguaje legible |
| Propuesta (ítem 9) | H4: ventana corta de corrección de una entrega, con registro, tras acordar la regla con Planificación |
| Propuesta (ítems 4 y 10) | H9: manual breve de una página para Planificación y para Conducción |
| Propuesta (ítems 2 y 8) | H5: asignar el mismo conductor a todos los vehículos del día en un solo paso |
| Propuesta (ítems 2 y 9) | Mostrar en pantalla el tiempo restante del código TOTP y que el código ya fue usado |

Las mejoras propuestas no se han implementado; se programan en la acción 7 de la [Retrospectiva](02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md#acciones-a-realizar). Para comprobar que mejoran la usabilidad, se aplicará el mismo instrumento a personal de Planificación y Conducción de DistriRápido S.A.C., registrando esta vez la finalización, el tiempo y los errores por tarea.

## 4. Reproducibilidad

Las respuestas se procesaron con la entrada `P1…P10` por persona y este comando, cuya salida es la que se transcribe en la sección 2:

```powershell
python scripts\usabilidad\procesar_sus.py respuestas_sus.csv --markdown
```

El cálculo está verificado por 26 pruebas automáticas ([`test_usabilidad_sus.py`](../../../backend/tests/test_usabilidad_sus.py)): todas las respuestas ideales dan 100, todas las peores dan 0 y todas neutras (3) dan 50.
