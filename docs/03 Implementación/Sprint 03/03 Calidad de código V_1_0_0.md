# Evaluación de Calidad de Código — SonarQube

[← Volver al README Principal](../../../README.md#93-fase-03-implementación)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla  
**Fecha de Análisis:** 2026-10-30  
**Versión del Análisis:** V_1_0_0  

## Metadatos del documento

| Campo | Valor |
|---|---|
| Versión del documento | 1.0.0 |
| Herramienta | SonarQube Community Build 26.9.0.129388 (instancia local) + SonarScanner CLI 8.3.0.16463 |
| Perfil y Quality Gate | *Sonar way* (perfiles por defecto de Python, TypeScript y CSS) |
| Configuración | [`sonar-project.properties`](../../../sonar-project.properties) en la raíz del repositorio |
| Alcance | `backend/src`, `frontend/src`, `database/migrations` (código) · `backend/tests`, `frontend/tests` (pruebas) |
| Tamaño analizado | 81 archivos · 6 988 líneas de código (Python 2 542 · TypeScript 2 556 · CSS 1 890) |
| Rama | `sprint-3/calidad-owasp-wcag` (incluye rutas e indicadores) |
| Documentos relacionados | [01 Revisión](01%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) · [02 Retrospectiva](02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) · [04 OWASP](04%20OWASP%20V_1_0_0.md) · [05 WCAG](05%20WCAG%20V_1_0_0.md) |

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 30/10/2026 | Hilario Talavera, Alexander Daniel | Análisis inicial, correcciones y análisis final; plan de remediación de la deuda restante. |

## 1. Resumen Ejecutivo de Quality Gate

- **Estado del Quality Gate:** **PASSED** (estado `OK` en el análisis inicial y en el final)
- **Porcentaje de Cobertura de Pruebas (Coverage):** **81,3 %** (líneas 84,7 % · ramas 68,3 %)
- **Duplicación de Código:** **0,0 %** (0 bloques duplicados)

| Condición del Quality Gate (código nuevo) | Umbral | Valor | Estado |
|---|---|---:|:---:|
| Cobertura en código nuevo | ≥ 80 % | 86,4 % | ✅ |
| Líneas duplicadas en código nuevo | ≤ 3 % | 0,0 % | ✅ |
| Incidencias nuevas | 0 | 0 | ✅ |

| Calificación | Inicial | Final |
|---|:---:|:---:|
| Fiabilidad (*Reliability*) | **C** (2 bugs) | **A** |
| Seguridad (*Security*) | A | A |
| Revisión de seguridad (*Security Review*) | A | A |
| Mantenibilidad (*Maintainability*) | A | A |

### Cómo se obtuvo la cobertura

| Módulo | Herramienta | Pruebas | Cobertura |
|---|---|---:|---:|
| Backend (FastAPI) | `pytest --cov=app --cov-report=xml` | 130 aprobadas | 91 % de líneas |
| Frontend (React) | `vitest run --coverage` (`@vitest/coverage-v8`, reporte `lcov`) | 52 aprobadas | 75,6 % de líneas |
| **Total ponderado por SonarQube** | — | **182** | **81,3 %** |

La cobertura más baja está en los adaptadores PostgreSQL (`flota/postgres_repository.py` 33 %, `pedidos/postgres_repository.py` 38 %) y en `database_health.py` (30 %): las pruebas usan repositorios en memoria y la base real solo se verifica en el job de migraciones del CI. El motor de rutas (`rutas/planificador.py`) tiene 100 %.

## 2. Métricas Principales

| Categoría | Cantidad Detectada | Severidad (Bloqueante / Alta / Media / Baja) |
|---|---:|---|
| **Bugs** | **0** (2 en el análisis inicial, corregidos) | 0 / 0 / 0 / 0 — inicial: 0 / 0 / 2 / 0 |
| **Vulnerabilidades** | **0** | 0 / 0 / 0 / 0 |
| **Code Smells** | **97** (103 en el análisis inicial) | 0 / 1 / 51 / 45 — inicial: 0 / 2 / 55 / 46 |
| **Security Hotspots** | **0** | — (ningún punto sensible por revisar) |

*Correspondencia de severidades de SonarQube:* Blocker → Bloqueante · Critical → Alta · Major → Media · Minor → Baja.

### Comparación inicial vs. final

| Métrica | Análisis inicial | Análisis final | Variación |
|---|---:|---:|---:|
| Bugs | 2 | 0 | −2 |
| Vulnerabilidades | 0 | 0 | = |
| Code smells | 103 | 97 | −6 |
| Incidencias de severidad alta | 2 | 1 | −1 |
| Deuda técnica | 10 h 01 min | 8 h 34 min | −1 h 27 min (−14,5 %) |
| Cobertura | 81,2 % | 81,3 % | +0,1 pp |
| Duplicación | 0,0 % | 0,0 % | = |
| Pruebas backend / frontend | 128 / 51 | 130 / 52 | +3 |

### Distribución de los 97 code smells restantes

| Regla | Cantidad | Qué pide | Dónde |
|---|---:|---|---|
| `typescript:S6759` | 22 | Marcar como `Readonly` las *props* de los componentes | Componentes y páginas React |
| `python:S9073` | 21 | Dividir aserciones compuestas en pruebas | `backend/tests/auth`, `tests/pedidos` |
| `python:S8409` | 13 | Quitar `response_model` redundante (ya está en el tipo de retorno) | Routers de FastAPI |
| `python:S5778` | 9 | Una sola llamada que pueda lanzar excepción dentro de `pytest.raises` | Pruebas de dominio y servicio |
| `typescript:S3358` | 7 | Extraer ternarios anidados | `PaginaFlota`, `PaginaRutas`, `PaginaIndicadores`, `LoginPage`, `MapaRutas` |
| `typescript:S6819` | 7 | Usar elementos nativos (`<output>`, `<section>`, `<dialog>`) en vez de `role` | Avisos de estado, `Drawer`, regiones desplazables |
| `typescript:S1874` | 5 | `FormEvent` está obsoleto en los tipos de React 19 | `LoginPage`, `PedidoForm` |
| `css:S7924` | 3 | Contraste de texto | `styles.css` — **falsos positivos**, verificados con axe (ver §3) |
| Otras (8 reglas) | 10 | `S3776` complejidad cognitiva (1, **Alta**), `S4624`, `S6582`, `S6845`, `S6754`, `S6772`, `S7755`, `S7758` | Varios |

El 31 % de los code smells (30 de 97) está en archivos de prueba y no afecta el comportamiento de la aplicación.

## 3. Plan de Remediación y Deuda Técnica

- **Deuda Técnica Estimada:** **8 h 34 min** (514 min) tras las correcciones; era **10 h 01 min** (601 min) en el análisis inicial. Índice de deuda dentro de la calificación **A** de mantenibilidad.
- **Principales hallazgos y acciones correctivas:**
  1. **Bug — botones sin `type` dentro de formularios** (`typescript:S9011`, severidad Media, 2 casos). En [`PaginaFlota.tsx`](../../../frontend/src/pages/PaginaFlota.tsx) los botones "Registrar vehículo / Guardar cambios" y "Guardar disponibilidad" dependían del tipo implícito. **Corrección aplicada:** `type="submit"` explícito. Fiabilidad de **C → A**.
  2. **Literal `/api/v1` repetido 5 veces** (`python:S1192`, Alta). **Corrección aplicada:** constante `PREFIJO_API` en [`main.py`](../../../backend/src/app/main.py) y registro de routers en un bucle.
  3. **Lambdas que capturan la variable del bucle** (`python:S1515`, Media, 2 casos) en [`planificador.py`](../../../backend/src/app/rutas/planificador.py) (`_vecino_mas_cercano` y el pulido 2-opt). Hoy no fallan porque la lambda se evalúa en la misma iteración, pero un cambio futuro podía introducir un error silencioso. **Corrección aplicada:** valor capturado como argumento por defecto (`desde=actual`, `v=vehiculo`). Las 16 pruebas de rutas siguen pasando.
  4. **Selectores CSS duplicados** (`css:S4666`, 2 casos: `.nav__item` y `.flota-vehiculo`) y **valor obsoleto** `word-break: break-word` (`css:S1874`). **Corrección aplicada:** reglas fusionadas sin cambiar el orden de la cascada; `overflow-wrap: anywhere`.
  5. **Contraste de texto en CSS** (`css:S7924`, 3 casos). Son textos sobre fondos translúcidos encima de degradados, que el análisis estático no puede resolver. **Verificación:** axe-core en navegador, en tema claro y oscuro, no reporta violaciones de contraste en esos elementos ([05 WCAG](05%20WCAG%20V_1_0_0.md)). Se marcan como falsos positivos. En cambio, la prueba en navegador encontró dos problemas reales que SonarQube no detectó; también se corrigieron.

#### Deuda pendiente priorizada

| Prioridad | Hallazgo | Esfuerzo estimado | Responsable | Destino |
|---:|---|---|---|---|
| 1 | `S3776` — complejidad cognitiva 23 de `planificar()` (límite 15): extraer la inserción por vehículo y el cálculo de costo a funciones propias | 30 min de SonarQube; 2–3 h con pruebas | Hilario Talavera, Alexander Daniel | Sprint 4 |
| 2 | `S6819` / `S6845` — usar `<output>`, `<section aria-label>` y `<dialog>` nativos (relacionado con accesibilidad) | ≈ 1 h | Vera Zea, Jhoanna Hade | Sprint 4 |
| 3 | `S3358` / `S4624` — extraer ternarios y plantillas anidadas | ≈ 1 h | Vera Zea, Jhoanna Hade | Sprint 4 |
| 4 | `S8409` — quitar `response_model` redundante en 13 endpoints (comprobar que OpenAPI no cambie) | ≈ 30 min | Anco Porras, Jhean Pier Julio | Sprint 4 |
| 5 | `S6759` / `S1874` — `Readonly<Props>` y reemplazo de `FormEvent` | ≈ 2 h | Vera Zea, Jhoanna Hade | Sprint 4 |
| 6 | `S9073` / `S5778` — refactorizar aserciones de pruebas | ≈ 3 h | Isidro Casio, Jose Luis | Sprint 5 |
| 7 | Cobertura de adaptadores PostgreSQL con pruebas de integración en el job de PostGIS del CI | 4–6 h | Isidro Casio, Jose Luis | Sprint 4 |

**Meta para el próximo análisis:** 0 incidencias de severidad Alta, menos de 60 code smells, cobertura ≥ 85 % y análisis automático en cada PR (acciones 1 y 8 de la [retrospectiva](02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md#acciones-a-realizar)).

## 4. Cómo reproducir el análisis

```powershell
# 1. Cobertura
Push-Location backend;  .\.venv\Scripts\python.exe -m pytest --cov=app --cov-report=xml:coverage.xml; Pop-Location
Push-Location frontend; npx vitest run --coverage; Pop-Location

# 2. SonarQube local (requiere Java 17+): iniciar con bin\windows-x86-64\StartSonar.bat
#    y generar un token de análisis en http://localhost:9000 (My Account → Security)
sonar-scanner -D"sonar.host.url=http://localhost:9000" -D"sonar.token=$env:SONAR_TOKEN"
```

`coverage.xml`, `frontend/coverage/` y `.scannerwork/` están en `.gitignore`.
