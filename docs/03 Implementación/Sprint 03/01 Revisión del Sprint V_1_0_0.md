# Revisión del sprint

[← Volver al README Principal](../../../README.md#93-fase-03-implementación)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla

**Líder del Proyecto:** Alex Jesus Zorrilla Apumayta

## Metadatos del documento

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Sprint | ECO Sprint 3 — alcance funcional "rutas" (plan funcional del 09/10/2026) |
| Meta del sprint | "Planificación elige pedidos pendientes y solicita una ruta que después puede volver a abrir." ([05. Plan funcional de sprints](../../02%20Planificaci%C3%B3n/05%20Plan%20funcional%20de%20sprints.md#qué-debe-poder-hacerse-al-terminar-sprint-3)) |
| Inspección | Semana 11 · Inspección 03 — Sprint 03 (SonarQube, WCAG, OWASP) |
| Rama de trabajo | `sprint-3/calidad-owasp-wcag` (desde `main`, integra `feature/rutas-indicadores`) |
| Ensayo técnico de la demostración | 30/10/2026, servidores locales (API en memoria con datos sintéticos de demostración) |
| Reunión con partes interesadas | **Por confirmar:** fecha, hora y asistentes no se registraron en el repositorio |
| Documentos del Sprint 03 | [02 Retrospectiva](02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) · [03 Calidad de código](03%20Calidad%20de%20c%C3%B3digo%20V_1_0_0.md) · [04 OWASP](04%20OWASP%20V_1_0_0.md) · [05 WCAG](05%20WCAG%20V_1_0_0.md) |
| Sprint anterior | [Revisión del Sprint 2](../Sprint%202/03%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) |

> **Criterio de registro.** Este documento solo afirma lo que se puede comprobar en el código, las pruebas o el ensayo del 30/10. El estado de las tarjetas en Jira, la fecha de la reunión, los asistentes y la decisión del *Product Owner* no constan en el repositorio y quedan marcados **por confirmar**; no se inventan.

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 30/10/2026 | Hilario Talavera, Alexander Daniel | Primera emisión: incremento de rutas e indicadores, criterios del plan funcional, ensayo de la demostración y pendientes reales. |

## Historias de Usuario completadas en este Sprint

### Definición de Hecho aplicada

Se considera **Hecho** un elemento cuando: (1) el recorrido funciona desde la interfaz con sesión MFA y el rol correcto; (2) tiene pruebas automatizadas de API y de interfaz que pasan; (3) su especificación OpenSpec está archivada; (4) compila en producción y pasa el *Quality Gate* de SonarQube; y (5) cumple la regla de persistencia que prometa la historia (si guarda algo, sobrevive al reinicio). Es la definición del [plan funcional](../../02%20Planificaci%C3%B3n/05%20Plan%20funcional%20de%20sprints.md#cuándo-damos-por-útil-un-sprint), más los controles de calidad de este sprint.

### Estado por elemento del backlog

| Elemento | Qué se entregó | DoD | Estado | Evidencia |
|---|---|:---:|---|---|
| **HU-004 — Generar la ruta del día** (8 pts propuestos) | Vista previa de rutas por fecha: agrupa pedidos `PENDIENTE`/`VALIDADO` en los vehículos aptos, respeta capacidad en kg y m³, prioriza prioridad y ventana, ordena por puntualidad y luego por CO₂e (inserción + vecino más cercano + 2-opt) y reporta pedidos no asignados con su causa. | 1·2·3·4 ✔ / 5 ✘ | **Parcial** — no guarda la ruta | [`rutas/planificador.py`](../../../backend/src/app/rutas/planificador.py), [spec rutas](../../../openspec/specs/rutas/spec.md), 16 pruebas en [`tests/rutas/`](../../../backend/tests/rutas/) |
| **HU-005 / ECO-13 — Ver la ruta en el mapa** (3 pts) | Mapa Leaflet + OpenStreetMap con depósito, paradas numeradas por color de vehículo, trazado por calles con OSRM y respaldo en línea recta; resaltado al elegir una tarjeta. | 1·2·3·4 ✔ (no requiere persistencia) | **Hecho (adelantado de Sprint 4)** | [`MapaRutas.tsx`](../../../frontend/src/components/MapaRutas.tsx), [`trazado.ts`](../../../frontend/src/lib/trazado.ts), [`PaginaRutas.test.tsx`](../../../frontend/tests/PaginaRutas.test.tsx) |
| **Indicadores de operación y sostenibilidad** | Pedidos por estado/distrito/prioridad, flota por combustible, uso de capacidad, puntualidad y CO₂e frente a un despacho sin optimizar; acceso para Planificación, Administración y Gerencia. | 1·2·3·4 ✔ | **Hecho** | [`indicadores/service.py`](../../../backend/src/app/indicadores/service.py), [spec indicadores](../../../openspec/specs/indicadores/spec.md), [`PaginaIndicadores.tsx`](../../../frontend/src/pages/PaginaIndicadores.tsx) |
| **Ubicación del pedido en mapa** | Selector de punto en el mapa al registrar un pedido. | 1·2·3·4 ✔ | **Hecho** | [`SelectorUbicacion.tsx`](../../../frontend/src/components/SelectorUbicacion.tsx) |
| **EN-006 / ECO-17 — CI** (5 pts) | GitHub Actions: pytest con cobertura, migraciones en PostGIS (subir/bajar/subir), lint + pruebas + build del frontend y validación OpenSpec. | ✔ | **Hecho** (falta activarlo en `sprint-3/*`; ver pendientes) | [`.github/workflows/ci.yml`](../../../.github/workflows/ci.yml) |
| **EN-004 — Hardening OWASP Top 10** (8 pts) | Análisis SonarQube, revisión de las 10 categorías OWASP 2025, cabeceras de seguridad HTTP y actualización de Vite. | ✔ | **Avanzado** — quedan 3 elementos "bajo revisión" | [04 OWASP](04%20OWASP%20V_1_0_0.md) |
| **Calidad y accesibilidad (RNF-02, RNF-03)** | 2 bugs y 6 code smells corregidos; 5 defectos WCAG corregidos (contraste en tema oscuro, contraste de bordes de campos, nombre accesible del marcador, título de página por vista y región principal en el acceso). | ✔ | **Hecho** | [03 Calidad](03%20Calidad%20de%20c%C3%B3digo%20V_1_0_0.md) · [05 WCAG](05%20WCAG%20V_1_0_0.md) |
| **EN-005 / ECO-21 — Persistir rutas y cuentas** | Sin cambios en este sprint. | — | **No iniciado** | — |
| **EN-001 — Benchmark del motor (≤ 45 s)** | Sin medición. | — | **No iniciado** | — |

**Estado en Jira:** por confirmar. Las tarjetas HU-004, EN-001 y la de indicadores no existían en Jira al corte del 09/10 ([plan funcional](../../02%20Planificaci%C3%B3n/05%20Plan%20funcional%20de%20sprints.md#tamaño-y-estado-actual-del-trabajo-candidato)); la velocidad oficial del Sprint 3 se calculará al cerrarlo en Jira.

### Criterios de revisión del Sprint 3 (plan funcional)

| # | Criterio | Resultado | Evidencia |
|---:|---|---|---|
| 1 | Planificación elige pedidos pendientes y el sistema considera solo vehículos y turnos elegibles. | **Cumple** | `RutasService.vista_previa` filtra `elegible_para_planificar` y estados `PENDIENTE`/`VALIDADO`; prueba "Sin vehículos con turno". |
| 2 | El sistema muestra vehículo, orden de paradas, carga y ventanas consideradas. | **Cumple** | Tarjeta por vehículo con carga, duración y llegadas; ensayo del 30/10 (abajo). |
| 3 | La ruta queda guardada y sigue apareciendo tras reiniciar. | **No cumple** | La vista previa es de solo lectura por diseño; depende de EN-005 / ECO-21. |
| 4 | Si no hay combinación posible, explica qué pedido o capacidad lo impide y no asigna una ruta parcial como lista. | **Cumple** | Causas "No hay vehículos disponibles para la fecha" y "Supera la capacidad libre de la flota"; pruebas de prioridad ante capacidad escasa. |
| 5 | Tiempo de generación medido contra ≤ 45 s (EN-001). | **Pendiente** | No se publica una cifra sin medirla con el volumen acordado. |

**Resultado:** 3 de 5 criterios cumplen. La meta del sprint ("solicitar una ruta que después puede volver a abrir") **no se alcanza completa** porque la ruta todavía no se guarda.

## Demostración del trabajo completado

Demostración a los *stakeholders* de las funcionalidades implementadas. El guion se **ensayó el 30/10/2026** contra los servidores locales (`http://localhost:3000` y `http://localhost:8000`), con la API en memoria y los datos de demostración del repositorio (`DEMO_PEDIDOS=true`: 6 pedidos y 3 vehículos sintéticos de Huancayo, **no son operaciones reales de DistriRápido**). No se registraron contraseñas ni códigos en este documento.

| # | Paso | Resultado esperado | Resultado del ensayo (30/10) |
|---:|---|---|---|
| 1 | Abrir la aplicación sin sesión | Pantalla "Iniciar sesión" | Correcto |
| 2 | Ingresar como Planificación (contraseña) | Paso de enrolamiento con QR y clave manual | Correcto |
| 3 | Escribir el código TOTP | Entrada al panel de Planificación | Correcto |
| 4 | Ver Pedidos | 6 pedidos `PENDIENTE` (DR-1001 a DR-1006), 3 de prioridad alta, 498 kg | Correcto |
| 5 | Abrir Rutas para el 31/10/2026 | Mapa con depósito, paradas numeradas y una tarjeta por vehículo | Correcto |
| 6 | Seleccionar la tarjeta de un vehículo | Su ruta se resalta y las demás se atenúan | Correcto |
| 7 | Abrir Indicadores para el 31/10/2026 | Ahorro de CO₂e **46,3 %** (6,08 vs 11,32 kg), puntualidad **100 %**, uso de capacidad **46,5 %** (498 de 1 070 kg), **6/6** pedidos asignados, 49,23 km | Correcto |
| 8 | Cambiar a tema oscuro y recorrer las vistas | Todo legible (contraste corregido en este sprint) | Correcto |
| 9 | Navegar solo con teclado (Tab) | "Saltar al contenido", foco visible y orden lógico | Correcto |
| 10 | Ver la vista en celular (375 px) | Navegación inferior, sin desplazamiento horizontal | Correcto |

> Las cifras del paso 7 provienen de datos sintéticos y de supuestos visibles en la interfaz (factor de circuito 1,3; consumo base y factores de emisión de referencia). Sirven para mostrar el cálculo, **no** como resultado de negocio ni como evidencia del objetivo de reducir 15 % la distancia.

Lo que validan las partes interesadas: que Planificación puede ver, antes de salir a reparto, cómo se repartirían los pedidos del día entre los vehículos con turno, cuánto CO₂e se evitaría y qué pedidos quedan sin asignar y por qué.

| Campo de la reunión | Registro |
|---|---|
| Fecha y hora | Por confirmar |
| Asistentes | Por confirmar (equipo Scrum y docente asesor como *Product Owner* académico) |
| Decisión sobre el incremento | Por confirmar |
| Comentarios recibidos | Por confirmar |

## Pendientes

| # | Pendiente | Tipo | Responsable | Destino |
|---:|---|---|---|---|
| 1 | Persistir rutas y paradas (EN-005 / ECO-21) para cumplir el criterio 3 y la meta del sprint | Habilitador | Anco Porras, Jhean Pier Julio | Sprint 4, primera prioridad |
| 2 | Benchmark EN-001: medir la generación con el volumen acordado (objetivo ≤ 45 s, RSK-02) | Habilitador | Hilario Talavera, Alexander Daniel | Sprint 4 |
| 3 | Reducir la complejidad cognitiva de `planificar()` (23 → ≤ 15, único hallazgo crítico de SonarQube) | Deuda técnica | Hilario Talavera, Alexander Daniel | Sprint 4 |
| 4 | Cifrar secretos TOTP en reposo y mover las cuentas a PostgreSQL (OWASP A04:2025) | Seguridad | Anco Porras, Jhean Pier Julio | Sprint 4 |
| 5 | Aviso antes de que venza la sesión, con opción de extenderla (WCAG 2.2.1) | Accesibilidad | Vera Zea, Jhoanna Hade | Sprint 4 |
| 6 | Ejecutar CI también en ramas `sprint-*` y `feature/*` y fusionar mediante PR revisado | Proceso | Isidro Casio, Jose Luis | Antes de fusionar esta rama |
| 7 | Crear en Jira HU-004, EN-001 y la tarjeta de indicadores, y registrar el estado real del sprint | Gestión | Zorrilla Apumayta, Alex Jesus | Cierre del Sprint 3 |
| 8 | Registrar fecha, asistentes y decisión de la reunión de revisión en este documento (versión 1.1.0) | Gestión | Zorrilla Apumayta, Alex Jesus | Tras la Inspección 03 |
| 9 | Decidir si se usa un servidor OSRM propio: el público recibe las coordenadas de las paradas (Ley 29733) | Diseño | Equipo | Planning del Sprint 4 |
