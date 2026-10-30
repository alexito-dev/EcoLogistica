# Proposal

## Why

Con pedidos (HU-001) y flota con turnos (HU-003, HU-009) ya implementados, el planificador todavía no puede **ver** cómo quedaría el reparto del día: la opción "Rutas" del menú estaba marcada como "Pronto". HU-004 (generar ruta sostenible) y HU-005 (consultar la operación en mapa) están planificadas para el Sprint 3, pero su núcleo depende del motor VRPTW con OR-Tools, que aún no existe. Una vista previa ligera permite validar desde ahora, con datos reales del sistema, el contrato de una ruta (vehículo, secuencia, distancia, puntualidad estimada y CO₂), la experiencia en el mapa y la restricción RES-06 (Leaflet/OpenStreetMap), y reduce el riesgo de integración del Sprint 3.

## What Changes

- Nuevo módulo **Rutas** en la API (`backend/src/app/rutas/`): `GET /api/v1/rutas/vista-previa?fecha=AAAA-MM-DD`, de solo lectura, para `PLANIFICADOR` y `ADMIN`.
- Heurística determinista sin dependencias externas: inserción más barata con capacidad (kg y m³), ventanas horarias y emisiones (Green VRP), y mejora local 2-opt. No persiste nada.
- Por cada ruta: vehículo, paradas en orden, llegada estimada, indicador de llegada dentro de la ventana, distancia, duración, carga, uso de capacidad y CO₂e.
- Pedidos no asignables con su causa (sin vehículos con turno o sin capacidad libre).
- Comparación contra un despacho sin optimizar (orden de registro) para mostrar ahorro de distancia, CO₂ y puntualidad, en línea con HU-011.
- Depósito de salida configurable (`DEPOSITO_NOMBRE`, `DEPOSITO_LAT`, `DEPOSITO_LON` en `.env.example`).
- Nueva página **Rutas** en React con **Leaflet + OpenStreetMap**: mapa con depósito, paradas numeradas y una línea de color por vehículo; indicadores de pedidos, vehículos, distancia y emisiones; tarjeta por vehículo que resalta su ruta; sección "¿Cómo se calcula?" con los supuestos.
- Datos de demostración opcionales (`DEMO_PEDIDOS=true`): además de los 6 pedidos, 3 vehículos (diésel, GNV y eléctrico) con turno para el día siguiente.

## Capabilities

### New Capabilities
- `rutas`: vista previa de rutas del día sobre el mapa, con asignación por capacidad, orden por ventanas y emisiones, pedidos no asignables y comparación contra un despacho sin optimizar.

### Modified Capabilities
<!-- Ninguna: pedidos y flota se consumen a través de sus puertos de repositorio sin cambiar sus requisitos. -->

## Impact

- **Código:** `backend/src/app/rutas/` (planificador, servicio, esquemas y router), `backend/src/app/flota/siembra.py`, `backend/src/app/main.py`, `backend/src/app/config.py`; `frontend/src/api/rutas.ts`, `frontend/src/components/MapaRutas.tsx`, `frontend/src/pages/PaginaRutas.tsx`, `frontend/src/App.tsx`, `frontend/src/components/AppShell.tsx`, `frontend/src/styles.css`.
- **Dependencias:** `leaflet@1.9.4` y `@types/leaflet` en el frontend (código abierto, sin clave de API, conforme a RES-06). Ninguna nueva en el backend.
- **Pruebas:** `backend/tests/rutas/` (reglas del planificador y API) y `frontend/tests/PaginaRutas.test.tsx`.
- **Trazabilidad:** adelanta parte de HU-004 y HU-005 (EP-03, EP-04) como vista previa; no cierra esas historias, que siguen dependiendo del motor VRPTW (EN-001) y de la planificación publicada.
