# Pruebas de sistema

[← Volver al README Principal](../../../README.md#93-fase-03-implementación)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla

**Líder del Proyecto:** Alex Jesus Zorrilla Apumayta

## Metadatos del documento

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Fecha de ejecución | 30/10/2026 |
| Rama | `sprint-3/calidad-owasp-wcag` |
| Entorno | Windows 11, backend en `backend/.venv` (Python 3.10, pytest) y frontend con Vitest |
| Documentos relacionados | [03 Calidad de código](03%20Calidad%20de%20c%C3%B3digo%20V_1_0_0.md) · [Pruebas E2E](20261030%20Pruebas%20E2E%20V_1_0_0.md) · [03.2 Informe de estado](20261030%2003.2%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md) |

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 30/10/2026 | Hilario Talavera, Alexander Daniel | Primera emisión con la ejecución de las suites automáticas y la verificación del CI. |

## 1. Alcance

Pruebas del sistema ya integrado (API, reglas de negocio, persistencia y interfaz) mediante suites automáticas. Las pruebas de punta a punta en navegador están en [Pruebas E2E](20261030%20Pruebas%20E2E%20V_1_0_0.md).

## 2. Resultados de la ejecución

| Suite | Comando | Resultado |
|---|---|---|
| Backend | `python -m pytest` en `backend/` | **137 aprobadas**, 3 advertencias, 0 fallos |
| Frontend | `npx vitest run` en `frontend/` | **58 aprobadas** en 9 archivos, 0 fallos |

Cobertura de líneas del backend con `--cov=app`: **92,6 %** (el análisis de SonarQube del documento [03 Calidad](03%20Calidad%20de%20c%C3%B3digo%20V_1_0_0.md) midió 91 % antes de sumar las pruebas de rutas guardadas). `npm run lint` y `npm run build` terminan sin errores.

## 3. Cobertura funcional por módulo

| Módulo | Pruebas en | Qué comprueba |
|---|---|---|
| Acceso y MFA | `backend/tests/auth`, `frontend/tests/Acceso.test.tsx` | Inicio de sesión, TOTP, bloqueo tras 5 intentos, roles, título de página |
| Pedidos | `backend/tests/pedidos`, `PaginaPedidos.test.tsx`, `PedidoForm.test.tsx` | Registro, validación, filtros, ubicación |
| Flota | `backend/tests/flota`, `test_flota_cors.py` | Vehículos, disponibilidad, elegibilidad, CORS |
| Rutas | `backend/tests/rutas` (23), `PaginaRutas.test.tsx`, `trazado.test.ts` | Capacidad, prioridad, ventanas, no asignados, respaldo sin OSRM, guardar y reabrir rutas, reinicio, roles |
| Indicadores | `backend/tests/indicadores`, `PaginaIndicadores.test.tsx` | CO₂e, puntualidad, uso de capacidad |
| Sesión | `AvisoSesion.test.tsx` | Aviso antes del vencimiento, botón "Seguir conectado", sin aviso sin sesión |
| Seguridad | `test_cabeceras_seguridad.py`, `test_config.py` | Cabeceras HTTP y configuración que falla cerrada |

## 4. Verificaciones del CI

[`ci.yml`](../../../.github/workflows/ci.yml) define 4 trabajos: backend (pytest con cobertura), migraciones (aplicar, revertir y volver a aplicar en PostgreSQL + PostGIS), frontend (tipos, lint, pruebas y *build*) y validación de OpenSpec. Se ejecuta en *push* a `main`, `sprint-*/**` y `feature/**` y en cada PR. Las migraciones solo se verifican ahí; las pruebas locales usan repositorios en memoria.

## 5. Pruebas de sistema no cubiertas

| Aspecto | Estado |
|---|---|
| Tiempo de generación de rutas ≤ 45 s (EN-001) | Medido con datos sintéticos (sección 6); falta repetirlo con datos reales |
| Rendimiento y carga | No ejecutadas |
| Adaptadores PostgreSQL | Cobertura baja (33 % y 38 %) |
| Persistencia de rutas en PostgreSQL | Pendiente (EN-005): hoy se guardan en un archivo local, con prueba de reinicio |

## 6. Conclusión

Las suites automáticas pasan en el estado actual de la rama. El sistema queda verificado a nivel funcional con datos en memoria; faltan rendimiento y persistencia de rutas.

## 6. Benchmark del motor de rutas (EN-001)

Comando, desde `backend/`: `python scripts/benchmark_rutas.py`. Usa pedidos sintéticos reproducibles (semilla fija) en el ámbito de Huancayo y una flota de camionetas de 500 kg (un vehículo por cada 12 pedidos, mínimo 3). Equipo local con Windows 11.

| Pedidos | Vehículos | Asignados | Tiempo (s) | Objetivo ≤ 45 s |
|---:|---:|---:|---:|:---:|
| 25 | 3 | 25 | 0,14 | Cumple |
| 50 | 4 | 50 | 0,35 | Cumple |
| 100 | 8 | 100 | 0,82 | Cumple |
| 150 | 12 | 150 | 1,13 | Cumple |

El volumen de 150 pedidos es el de RSK-02. Los datos son sintéticos: el resultado con pedidos reales de DistriRápido se medirá en el Sprint 4.
