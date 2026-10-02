# Proposal

## Why

HU-001 / ECO-9 (EP-01, 5 puntos) quedó sin implementar en el Sprint 1: no existe código en `backend/` ni `frontend/`, y sin pedidos registrados no es posible alimentar el motor de optimización VRPTW ni ninguna historia posterior (HU-002, HU-004, HU-006). El planificador necesita incorporar pedidos a la planificación diaria con dirección, carga y ventana horaria válidas, rechazando datos incoherentes antes de que lleguen al optimizador (RF-02.1, RF-02.2, RN-001).

## What Changes

- Nuevo módulo **Pedidos** en la API FastAPI (`backend/`): registrar un pedido, consultarlo por id y listar pedidos, con validación de entrada y reglas de dominio.
- Un pedido nuevo se crea con estado `PENDIENTE` (valor del dominio `estado_pedido` del modelo físico y del Gherkin de HU-001) y se devuelve con su identificador y código.
- Validaciones de RF-02.2 / RN-001: coordenadas válidas dentro del ámbito configurado, ventana con inicio anterior al fin, peso y volumen no negativos con al menos una demanda mayor que cero, tiempo de servicio positivo y prioridad entre 1 y 4. Cada rechazo indica el campo a corregir.
- Código de pedido único (idempotencia de registro): un código repetido se rechaza con conflicto.
- Persistencia detrás de un puerto de repositorio con adaptador en memoria para este cambio; el adaptador PostgreSQL/PostGIS llegará con EN-005 (ECO-16) sin modificar el dominio.
- Nueva pantalla en el frontend React + Vite (`frontend/`): formulario de registro de pedido y listado de pedidos, con mensajes de error por campo, etiquetas accesibles y consumo de la API.
- Contrato OpenAPI de los endpoints nuevos (RNF-20) y pruebas automatizadas de dominio y API (RNF-14).

Fuera de alcance (se documenta como *Non-goals* en el diseño): autenticación y RBAC (RF-11.1), edición de pedidos, importación CSV (HU-008), geocodificación y mapa (HU-002, HU-005), auditoría (RF-11.2) y persistencia PostgreSQL.

## Capabilities

### New Capabilities
- `pedidos`: registro, consulta y listado de pedidos con ventana horaria, carga, prioridad y ubicación, incluyendo sus validaciones de dominio y estado inicial.

### Modified Capabilities
<!-- Ninguna: openspec/specs/ aún no contiene capabilities. -->

## Impact

- **Código:** `backend/app/pedidos/` (módulo FastAPI: router, esquemas Pydantic, dominio, servicio, puerto de repositorio y adaptador en memoria), `backend/tests/`, `frontend/src/` (página, componentes y cliente API), `frontend/tests/`.
- **API:** `POST /api/v1/pedidos`, `GET /api/v1/pedidos`, `GET /api/v1/pedidos/{id}`; documentación OpenAPI generada por FastAPI.
- **Configuración:** variables nuevas en `.env.example` (`PORT`, límites del ámbito geográfico y `VITE_API_URL`), sin secretos en Git (RNF-06, RNF-15).
- **Dependencias:** FastAPI, Uvicorn, Pydantic y pydantic-settings, pytest y httpx en backend; React, Vite, TypeScript, Vitest y Testing Library en frontend.
- **Documentación:** el cambio se archiva en `openspec/changes/archive/` y su spec pasa a `openspec/specs/pedidos/`; la Revisión del Sprint 2 reportará HU-001.
- **Trazabilidad:** RF-02.1, RF-02.2, RN-001, RN-004 (estado inicial), RNF-03, RNF-07, RNF-10, RNF-14, RNF-20 (stack ratificado en [10. Stack tecnológico](../../../docs/01%20Inicio/10.%20Stack%20tecnol%C3%B3gico%20V_1_0_0.md), Alternativa A); HU-001 / ECO-9.
