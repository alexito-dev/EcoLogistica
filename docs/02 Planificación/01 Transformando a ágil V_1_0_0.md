# 01. Transformando a ágil

[← Volver al README Principal](../../README.md)

## Metadatos

| Campo | Valor |
|---|---|
| Proyecto | EcoLogística Huancayo |
| Código | PFA-TP2-ECOLOG-2026 |
| Equipo | Zorrilla Apumayta, Alex Jesus; Anco Porras, Jhean Pier Julio; Hilario Talavera, Alexander Daniel; Vera Zea, Jhoanna Hade; Isidro Casio, Jose Luis |
| Versión | 1.0.0 |
| Fecha | 11 de septiembre de 2026 |

## 1. Método de transformación

Se toma como línea base la documentación de requisitos de las semanas 2 y 3. Cada capacidad de negocio se convierte en una **Épica**; los resultados observables para un rol se expresan como **Historias de Usuario (US)**; y las condiciones de calidad, arquitectura, seguridad, datos y operación se expresan como **Enablers (EN)**. La trazabilidad evita convertir una decisión técnica en una promesa de usuario.

## 2. Mapa de épicas y backlog inicial

| Épica | Objetivo de valor | Requisitos relacionados |
|---|---|---|
| EP-01 Gestión de pedidos | Registrar, validar y ubicar entregas con ventana horaria | RF-001 a RF-004, RNF-006 |
| EP-02 Flota y conductores | Mantener capacidades, turnos y restricciones operativas | RF-005 a RF-007 |
| EP-03 Optimización sostenible | Generar rutas VRPTW/Green VRP medibles | RF-008 a RF-010, RNF-001, RNF-004 |
| EP-04 Seguimiento y re-enrutamiento | Visualizar y ajustar la operación durante la jornada | RF-011 a RF-013, RNF-003 |
| EP-05 Indicadores y auditoría | Explicar puntualidad, costo, CO₂ y trazabilidad | RF-014 a RF-016, RNF-005 |

| Orden | ID | Tipo | Épica | Puntos | Elemento |
|---:|---|---|---|---:|---|
| 1 | US-001 | Story | EP-01 | 5 | Registrar pedido con dirección y ventana horaria |
| 2 | US-002 | Story | EP-01 | 3 | Validar datos y geocodificar pedido |
| 3 | US-003 | Story | EP-02 | 5 | Configurar vehículo y conductor |
| 4 | US-004 | Story | EP-03 | 8 | Generar ruta optimizada sostenible |
| 5 | EN-001 | Enabler | EP-03 | 5 | Medir latencia y calidad del optimizador |
| 6 | US-005 | Story | EP-04 | 5 | Consultar ruta en mapa y estado de entregas |
| 7 | US-006 | Story | EP-04 | 8 | Reoptimizar ante pedido urgente o incidencia |
| 8 | EN-002 | Enabler | EP-04 | 5 | Implementar disponibilidad y recuperación |
| 9 | US-007 | Story | EP-05 | 5 | Consultar KPI de costo, puntualidad y CO₂ |
| 10 | EN-003 | Enabler | EP-05 | 3 | Proteger datos y registrar auditoría |

## 3. Historias de usuario y criterios BDD

### US-001 — Registrar pedido

**Épica:** EP-01. **Prioridad:** Alta.

Como **despachador**, quiero **registrar un pedido con dirección, carga y ventana horaria**, para **incorporarlo a la planificación diaria**.

#### Criterios de aceptación

```gherkin
Escenario: Registrar pedido válido
Dado que el despachador está autenticado
Cuando ingresa dirección, peso y ventana horaria válida
Entonces el sistema crea el pedido con estado Pendiente y muestra su identificador

Escenario: Rechazar ventana inválida
Dado que la hora final es anterior a la hora inicial
Cuando el despachador intenta guardar el pedido
Entonces el sistema rechaza la operación e indica el campo que debe corregirse
```

### US-002 — Geocodificar pedido

**Épica:** EP-01. **Prioridad:** Alta.

Como **despachador**, quiero **confirmar la ubicación geográfica de un pedido**, para **evitar rutas basadas en direcciones ambiguas**.

```gherkin
Escenario: Geocodificación con confianza suficiente
Dado un pedido con dirección válida
Cuando el servicio devuelve una coincidencia con precisión de manzana o superior
Entonces el sistema guarda latitud, longitud y nivel de confianza

Escenario: Geocodificación no concluyente
Dado un pedido cuya dirección no tiene coincidencia suficiente
Cuando finaliza la búsqueda automática
Entonces el sistema solicita un punto manual y mantiene el pedido fuera de la ruta
```

### US-003 — Configurar flota

**Épica:** EP-02. **Prioridad:** Alta.

Como **administrador de operaciones**, quiero **registrar capacidad, combustible y turno de cada vehículo**, para **generar asignaciones factibles**.

```gherkin
Escenario: Crear vehículo operativo
Dado que el administrador tiene permiso de configuración
Cuando registra placa, capacidad, tipo de combustible y turno válidos
Entonces el vehículo aparece disponible para planificación

Escenario: Evitar capacidad negativa
Dado un formulario de vehículo abierto
Cuando se ingresa una capacidad menor o igual a cero
Entonces el sistema no guarda el registro y muestra una validación explícita
```

### US-004 — Generar ruta sostenible

**Épica:** EP-03. **Prioridad:** Alta.

Como **planificador**, quiero **generar rutas considerando ventanas, capacidad, distancia y CO₂**, para **reducir costo y entregas tardías**.

```gherkin
Escenario: Generar solución factible
Dado un conjunto de pedidos geocodificados y una flota disponible
Cuando el planificador solicita optimizar
Entonces el sistema devuelve rutas asignadas, secuencia, distancia, puntualidad estimada y CO2

Escenario: Reportar pedidos no asignables
Dado un pedido incompatible con capacidad o ventana de toda la flota
Cuando finaliza la optimización
Entonces el sistema conserva el pedido como no asignado y explica la causa
```

### EN-001 — Rendimiento del optimizador

**Épica:** EP-03. **Prioridad:** Alta.

```gherkin
Escenario: Cumplir tiempo objetivo
Dado un escenario de 150 pedidos y 15 vehículos
Cuando se ejecuta la optimización en el entorno objetivo
Entonces el resultado se entrega en un máximo de 45 segundos en al menos 95 de 100 ejecuciones

Escenario: Registrar degradación
Dado que la ejecución supera el umbral de 45 segundos
Cuando el motor termina o es cancelado
Entonces se registra la métrica, se informa al usuario y no se presenta la solución como óptima
```

### US-005 — Consultar operación en mapa

**Épica:** EP-04. **Prioridad:** Alta.

```gherkin
Escenario: Ver ruta y estados
Dado que existe una planificación publicada
Cuando el operador abre el visor
Entonces observa secuencia, vehículo, ventanas y estado de cada entrega

Escenario: Conexión intermitente
Dado que el dispositivo pierde conectividad temporalmente
Cuando el operador consulta la última ruta sincronizada
Entonces el sistema muestra la marca de actualización y conserva la información disponible
```

### US-006 — Re-enrutar incidencia

**Épica:** EP-04. **Prioridad:** Media.

```gherkin
Escenario: Reoptimizar pedido urgente
Dado que una ruta publicada tiene un pedido urgente nuevo
Cuando el operador solicita reoptimización
Entonces el sistema propone una nueva secuencia sin violar capacidad ni ventanas confirmadas

Escenario: Cancelar propuesta riesgosa
Dado que la propuesta aumenta la tardanza por encima del umbral configurado
Cuando el motor evalúa la alternativa
Entonces la propuesta queda en revisión y no reemplaza la ruta publicada
```

### EN-002 — Disponibilidad

**Épica:** EP-04. **Prioridad:** Alta.

```gherkin
Escenario: Recuperar servicio
Dado que un proceso de aplicación deja de responder
Cuando el monitor detecta el fallo
Entonces el servicio se reinicia y queda disponible dentro de 30 segundos

Escenario: Mantener consistencia
Dado que ocurre un fallo durante una actualización de ruta
Cuando se recupera el servicio
Entonces la última versión confirmada permanece intacta y la operación inconclusa queda registrada
```

### US-007 — Consultar indicadores

**Épica:** EP-05. **Prioridad:** Media.

```gherkin
Escenario: Consultar indicadores diarios
Dado que existen rutas ejecutadas con datos de distancia y combustible
Cuando el usuario abre el dashboard
Entonces observa puntualidad, distancia, costo estimado y CO2 con periodo y fuente

Escenario: Sin datos del periodo
Dado que no existen rutas para el filtro seleccionado
Cuando el usuario consulta el dashboard
Entonces el sistema muestra cero de forma diferenciada de un dato no disponible
```

### EN-003 — Seguridad y auditoría

**Épica:** EP-05. **Prioridad:** Alta.

```gherkin
Escenario: Autorizar acceso por rol
Dado un usuario autenticado sin permiso administrativo
Cuando intenta modificar parámetros de flota
Entonces el sistema deniega la operación y registra el evento

Escenario: Auditar exportación
Dado un usuario con permiso de auditoría
Cuando exporta un registro
Entonces el sistema registra usuario, fecha, filtro y resultado sin exponer credenciales
```

## 4. Definition of Done global

Una US o EN está Done cuando: (1) cumple todos sus criterios BDD; (2) tiene pruebas unitarias con cobertura mínima de 80% en el alcance modificado; (3) el análisis estático no reporta vulnerabilidades críticas; (4) un par técnico aprobó el Pull Request; (5) el despliegue automatizado es ejecutable en staging; (6) OpenAPI/Swagger y la documentación afectada están actualizadas; (7) no quedan errores de consola ni migraciones pendientes; y (8) la evidencia queda enlazada en Jira.
