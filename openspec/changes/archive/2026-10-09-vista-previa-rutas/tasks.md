# Tasks

## 1. Backend: planificador

- [x] 1.1 Implementar `rutas/planificador.py` con distancia haversine × 1,3, emisiones por combustible y factores de referencia; verificar con tests de distancia y de factor propio o de referencia
- [x] 1.2 Implementar la asignación por inserción más barata con capacidad en kg y m³, prioridad y causa de no asignación; verificar con tests de capacidad, prioridad y flota vacía
- [x] 1.3 Programar llegadas (velocidad media, salida ajustada a la primera ventana, espera a la apertura de ventana y tiempo de servicio) y ordenar con costo lexicográfico (paradas tardías, CO₂e) y 2-opt; verificar con tests de ventana temprana, espera y llegada tardía
- [x] 1.4 Calcular el despacho sin optimizar y el ahorro de CO₂e; verificar que la propuesta es más corta que el orden de registro en un caso en zigzag

## 2. Backend: API

- [x] 2.1 Implementar `rutas/service.py` (pedidos `PENDIENTE`/`VALIDADO` de la fecha en hora de Lima, vehículos aptos) y `rutas/schemas.py` en camelCase
- [x] 2.2 Exponer `GET /api/v1/rutas/vista-previa?fecha=` con RBAC `PLANIFICADOR`/`ADMIN` y documentación OpenAPI; verificar 200, fecha ausente o inválida (400) y rol sin permiso (403)
- [x] 2.3 Agregar `DEPOSITO_NOMBRE`, `DEPOSITO_LAT`, `DEPOSITO_LON` y `DEMO_PEDIDOS` a la configuración y a `.env.example`
- [x] 2.4 Sembrar 3 vehículos de demostración con turno del día siguiente cuando `DEMO_PEDIDOS=true`; verificar la vista previa completa con los datos de demostración
- [x] 2.5 Aislar las pruebas del `.env` local (`DATABASE_URL` vacía y `DEMO_PEDIDOS=false` en `conftest.py`)

## 3. Frontend

- [x] 3.1 Agregar `leaflet@1.9.4` y `@types/leaflet`; crear el cliente `api/rutas.ts`
- [x] 3.2 Crear `MapaRutas.tsx` (OpenStreetMap con atribución, depósito, paradas numeradas por color, paradas tardías destacadas, resaltado sin reencuadrar, tema oscuro)
- [x] 3.3 Crear `PaginaRutas.tsx` con fecha de reparto, indicadores, tarjetas por vehículo, no asignados, supuestos y estado vacío
- [x] 3.4 Habilitar "Rutas" en la navegación lateral e inferior y corregir el fondo de los botones de navegación
- [x] 3.5 Verificar con `tests/PaginaRutas.test.tsx` (mapa e indicadores, resaltado, estado vacío y cambio de fecha)

## 4. Cierre

- [x] 4.1 Ejecutar las suites completas: backend (125 pruebas) y frontend (43 pruebas) en verde; `tsc -b` sin errores
- [x] 4.2 Validar el cambio con `openspec validate vista-previa-rutas --strict` y archivarlo para incorporar la capability `rutas` a `openspec/specs/`
