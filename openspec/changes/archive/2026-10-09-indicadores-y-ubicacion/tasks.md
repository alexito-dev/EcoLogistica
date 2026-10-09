# Tasks

## 1. Backend: indicadores

- [x] 1.1 Implementar `indicadores/service.py` (pedidos paginados, flota de la fecha y vista previa de rutas) y `indicadores/schemas.py` en camelCase, con porcentajes en cero cuando no hay datos
- [x] 1.2 Exponer `GET /api/v1/indicadores?fecha=` con RBAC `PLANIFICADOR`/`ADMIN`/`GERENTE` y documentación OpenAPI
- [x] 1.3 Verificar con `tests/indicadores/test_api.py`: conteos con datos de demostración, día sin operación en cero, permisos (403) y fecha obligatoria (400)

## 2. Frontend: dashboard y menú por rol

- [x] 2.1 Crear `api/indicadores.ts` y `pages/PaginaIndicadores.tsx` (indicadores clave, barras accesibles, estado sin pedidos)
- [x] 2.2 Centralizar el menú por rol en `lib/navegacion.ts` y usarlo en el menú lateral, la barra inferior y la vista inicial; `GERENTE` abre Indicadores
- [x] 2.3 Cargar Flota, Rutas e Indicadores con `React.lazy`; verificar que el paquete inicial queda por debajo de 500 kB con `npm run build`
- [x] 2.4 Verificar con `tests/PaginaIndicadores.test.tsx` (dashboard, fecha sin pedidos y vistas por rol)

## 3. Frontend: ubicación en el mapa y Flota

- [x] 3.1 Crear `SelectorUbicacion.tsx` (clic para completar coordenadas, marcador arrastrable, reflejo de coordenadas escritas) e integrarlo con carga diferida en `PedidoForm.tsx`; verificar con un caso en `tests/PedidoForm.test.tsx`
- [x] 3.2 Alinear la página Flota: `StatCard`, fecha en la cabecera y clases de botón existentes (`boton--primario`, `boton--secundario`, `formulario__acciones`)
- [x] 3.3 Dejar `npm run lint` sin advertencias (estado actualizado al resolver promesas, constantes fuera de los componentes)

## 4. Integración continua y cierre

- [x] 4.1 Crear `.github/workflows/ci.yml` con los trabajos de backend, migraciones PostGIS, frontend y OpenSpec
- [x] 4.2 Ejecutar las suites locales: backend (128 pruebas) y frontend (47 pruebas) en verde, `tsc -b` y `oxlint` sin hallazgos
- [x] 4.3 Validar con `openspec validate indicadores-y-ubicacion --strict` y archivar el cambio
