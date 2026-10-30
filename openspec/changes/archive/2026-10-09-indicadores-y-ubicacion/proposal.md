# Proposal

## Why

Tras la vista previa de rutas, la última opción del menú ("Indicadores") seguía marcada como "Pronto" y el rol `GERENTE` solo veía un aviso de acceso no autorizado, aunque la visión del producto (documento 03) y HU-011 piden cuantificar el ahorro de distancia y CO₂. Además, registrar un pedido exigía escribir latitud y longitud a mano, lo que vuelve lento el formulario y propicia errores de ubicación fuera del ámbito (RN-001). Finalmente, la página de flota usaba clases de estilo inexistentes y el repositorio no tenía integración continua que impida regresiones.

## What Changes

- Nuevo endpoint `GET /api/v1/indicadores?fecha=` para `PLANIFICADOR`, `ADMIN` y `GERENTE`. Resume los pedidos por estado, distrito y prioridad, y la flota por combustible. Para la fecha, informa uso de capacidad, puntualidad, distancia y CO₂e con su ahorro frente al despacho sin optimizar, reutilizando la vista previa de rutas.
- Nueva página **Indicadores** con cuatro indicadores clave y gráficos de barras accesibles (cada fila se lee como texto). Se descarga solo al abrirla.
- **Menú por rol:** cada rol ve solo las vistas que puede abrir. `GERENTE` entra directo a Indicadores; `CONDUCTOR` y `AUDITOR` ven el aviso de acceso no autorizado hasta que existan sus vistas.
- **Ubicar el destino en el mapa** al registrar un pedido: un clic completa latitud y longitud; el marcador se puede arrastrar y refleja las coordenadas escritas a mano. Leaflet se descarga solo al abrir el formulario.
- Página Flota alineada al resto de la aplicación: indicadores con `StatCard`, filtro de fecha en la cabecera y botones con los estilos existentes.
- Integración continua en GitHub Actions: pruebas y cobertura del backend, migraciones sobre PostgreSQL/PostGIS (aplicar, revertir y volver a aplicar), tipos, lint, pruebas y build del frontend, y `openspec validate --specs --strict`.

## Capabilities

### New Capabilities
- `indicadores`: dashboard de operación y sostenibilidad de una fecha, con menú de vistas por rol.

### Modified Capabilities
- `pedidos`: la interfaz de registro permite ubicar el destino en un mapa.
- `autenticacion`: el aviso de acceso no autorizado se muestra cuando el rol no tiene ninguna vista, no solo cuando no puede ver pedidos.

## Impact

- **Código:** `backend/src/app/indicadores/`, `backend/src/app/main.py`; `frontend/src/api/indicadores.ts`, `frontend/src/pages/PaginaIndicadores.tsx`, `frontend/src/lib/navegacion.ts`, `frontend/src/components/SelectorUbicacion.tsx`, `frontend/src/components/PedidoForm.tsx`, `frontend/src/components/AppShell.tsx`, `frontend/src/App.tsx`, `frontend/src/pages/PaginaFlota.tsx`, `frontend/src/styles.css`; `.github/workflows/ci.yml`.
- **Dependencias:** ninguna nueva (Leaflet ya se agregó con `vista-previa-rutas`).
- **Pruebas:** `backend/tests/indicadores/`, `frontend/tests/PaginaIndicadores.test.tsx` y un caso nuevo en `frontend/tests/PedidoForm.test.tsx`.
- **Trazabilidad:** adelanta HU-011 (comparación contra línea base) con un despacho sin optimizar como referencia; la línea base manual histórica sigue pendiente.
