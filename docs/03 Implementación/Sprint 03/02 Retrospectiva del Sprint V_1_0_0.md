# Retrospectiva del sprint

[← Volver al README Principal](../../../README.md#93-fase-03-implementación)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla

**Líder del Proyecto:** Alex Jesus Zorrilla Apumayta

## Metadatos del documento

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Sprint | ECO Sprint 3 — rutas, indicadores, calidad, seguridad y accesibilidad |
| Formato | Aprendimos / Hacemos bien / Mejorar en 4 dimensiones / Acciones con responsable y fecha |
| Fuentes | Historial de Git, [Revisión del Sprint 03](01%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md), [Calidad de código](03%20Calidad%20de%20c%C3%B3digo%20V_1_0_0.md), [OWASP](04%20OWASP%20V_1_0_0.md), [WCAG](05%20WCAG%20V_1_0_0.md) |
| Base | Historial de Git y documentos del sprint |
| Retrospectiva anterior | [Retrospectiva del Sprint 2](../Sprint%2002/04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) |

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 30/10/2026 | Hilario Talavera, Alexander Daniel | Primera emisión con aprendizajes, aciertos y acciones medibles en las cuatro dimensiones. |

## ¿Qué aprendimos?

1. **Medir antes de opinar sobre calidad.** El primer análisis de SonarQube mostró 2 bugs reales (botones de formulario sin `type`) y 103 code smells que ningún linter ni prueba había señalado. Con una línea base medida se priorizó lo crítico en lugar de "limpiar todo".
2. **Las herramientas automáticas no reemplazan la revisión manual.** SonarQube marcó 3 problemas de contraste que eran falsos positivos (fondos translúcidos sobre degradados), pero no vio 2 fallos reales que sí encontró la prueba en navegador con axe-core: contraste en tema oscuro (4,05:1) y bordes de campos casi invisibles (≈ 1,2:1).
3. **El tema oscuro es otra interfaz.** Todas las vistas pasaban en claro; los fallos aparecieron solo al cambiar de tema. Cada vista nueva debe probarse en ambos.
4. **Una rama larga sin fusionar cuesta.** `feature/rutas-indicadores` quedó tres semanas sin integrar; al traerla aparecieron 4 conflictos en documentos del Sprint 2, porque `main` había reordenado el alcance (rutas pasaron al Sprint 3).
5. **Una "vista previa" no es una historia terminada.** El mapa y el cálculo se ven completos, pero sin persistencia la meta del sprint no se cumple. Separar "se ve" de "está hecho" evita sobrestimar el avance. Se resolvió guardando las rutas por fecha antes de cerrar el sprint.
6. **OWASP Top 10:2025 cambió.** Incluye *Software Supply Chain Failures* (A03) y *Mishandling of Exceptional Conditions* (A10); SSRF se integró en A01. Evaluar con la lista de 2021 habría dejado fuera la cadena de suministro, justo donde estaba la vulnerabilidad alta (Vite).

## ¿Qué estamos haciendo bien?

- **Pruebas como red de seguridad:** 137 pruebas de backend (92,6 % de cobertura de líneas) y 58 de frontend; todas las correcciones del sprint se hicieron sin romper ninguna.
- **Seguridad desde el diseño:** MFA con TOTP, Argon2id, cookies `HttpOnly` + `SameSite=Strict`, bloqueo tras 5 intentos y control de rol en cada endpoint. SonarQube no encontró vulnerabilidades ni *hotspots*.
- **Accesibilidad de base sólida:** enlace "Saltar al contenido", foco visible, `prefers-reduced-motion`, etiquetas en todos los campos, objetivos táctiles ≥ 24 px y vista móvil sin desplazamiento horizontal.
- **Especificar antes de programar:** rutas e indicadores llegaron con especificaciones OpenSpec archivadas, lo que hizo verificables los criterios de la revisión.
- **Honestidad documental:** se separa lo comprobado de lo pendiente y no se publican cifras sin medir (EN-001).
- **Cero duplicación** de código (0,0 %) en 6 988 líneas analizadas.

## ¿Qué podemos hacer mejor?

### Personas

- La generación de rutas (núcleo del producto) depende de una sola persona y el benchmark EN-001 se ejecutó recién al final de este sprint.
- Las verificaciones de accesibilidad y seguridad se concentraron al final del sprint, en lugar de hacerse con cada historia.

### Relaciones

- El trabajo de rutas se desarrolló en una rama que el resto del equipo no revisó durante tres semanas; nadie lo vio hasta integrarlo.

### Procesos

- El CI solo se ejecutaba en `main` y `developer`; en este sprint se amplió a `sprint-*` y `feature/*` (`ci.yml`).
- No existía un paso de calidad (SonarQube) ni de accesibilidad en la Definición de Hecho; se agregó en este sprint.
- Las tarjetas HU-004, EN-001 y la de indicadores no están en Jira, así que la velocidad del sprint no se puede medir.

### Herramientas

- SonarQube se ejecutó localmente y a mano; no forma parte del CI, así que la próxima medición depende de que alguien lo repita.
- `requirements.txt` usa rangos (`>=`) sin versiones fijas ni *hashes*, y las GitHub Actions se fijan por etiqueta y no por SHA (A08:2025).
- Falta una auditoría automática de accesibilidad (axe) en las pruebas de interfaz.

### Acciones a realizar

| # | Dimensión | Acción concreta | Responsable | Fecha límite | Indicador de logro |
|---:|---|---|---|---|---|
| 1 | Personas | Sesión de *pair programming* sobre `rutas/planificador.py` para que una segunda persona pueda mantener el motor. La complejidad de `planificar()` ya se redujo de 23 a ≤ 15 el 30/10/2026 (funciones `_mejor_insercion` y `_construir_ruta`). | Hilario Talavera, Alexander Daniel + Anco Porras, Jhean Pier Julio | 06/11/2026 | Regla S3776 sin incidencias en el siguiente análisis de SonarQube |
| 2 | Personas | Repetir el benchmark EN-001 con el volumen real. Con datos sintéticos, 150 pedidos y 12 vehículos en 1,13 s (objetivo ≤ 45 s). | Hilario Talavera, Alexander Daniel | 13/11/2026 | Tabla de tiempos con datos reales en el informe del Sprint 4 |
| 3 | Relaciones | Ninguna rama vive más de 5 días hábiles sin PR abierto; cada PR necesita la revisión de otra persona. | Isidro Casio, Jose Luis | Desde el 02/11/2026 | 0 ramas activas con más de 5 días sin PR |
| 4 | Relaciones | Ensayar la demostración con el guion de 10 pasos antes de cada revisión. | Zorrilla Apumayta, Alex Jesus | Cada cierre de sprint | Guion ejecutado sin fallos antes de la revisión |
| 5 | Procesos | Agregar a la Definición de Hecho: *Quality Gate* de SonarQube en verde y 0 violaciones axe A/AA en claro y oscuro. | Zorrilla Apumayta, Alex Jesus | Planning del Sprint 4 | DoD actualizada en el plan funcional |
| 6 | Procesos | Crear en Jira HU-004, EN-001 y la tarjeta de indicadores con su estimación aprobada. | Zorrilla Apumayta, Alex Jesus | Cierre del Sprint 3 | Velocidad del Sprint 3 calculable en Jira |
| 7 | Herramientas | Ejecutar el CI en `pull_request` de cualquier rama y en *push* a `sprint-*` y `feature/*` (aplicado en `ci.yml` el 30/10/2026). | Isidro Casio, Jose Luis | 06/11/2026 | Esta rama muestra el check de CI en su PR |
| 8 | Herramientas | Integrar el análisis de SonarQube (o SonarCloud) en el CI usando `sonar-project.properties`. | Isidro Casio, Jose Luis | 13/11/2026 | Análisis automático en cada PR |
| 9 | Herramientas | Fijar versiones de Python con un archivo de bloqueo y fijar las Actions por SHA. | Anco Porras, Jhean Pier Julio | 13/11/2026 | Elemento A08 pasa de "Bajo revisión" a "Limpio" |
| 10 | Herramientas | Añadir una prueba de interfaz con axe-core para las cuatro vistas principales. | Vera Zea, Jhoanna Hade | 13/11/2026 | La prueba falla si aparece una violación A/AA |
