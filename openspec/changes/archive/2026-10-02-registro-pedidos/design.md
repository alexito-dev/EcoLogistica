# Design

## Context

Ver `proposal.md` (Why). Estado actual: `backend/` y `frontend/` solo contienen `.gitkeep`; no hay código. El stack es el de la **Alternativa A** del documento `10. Stack tecnológico` (React + Vite + TypeScript; FastAPI + Python con Pydantic y SQLAlchemy/Alembic; PostgreSQL + PostGIS; Leaflet/OSM), ratificada por el líder del proyecto el 02/10/2026 por ser la de mayor puntuación de la matriz (93 %). La arquitectura ya está definida en `docs/01 Inicio`:

- **Modelo C4:** API de aplicación en FastAPI con límites internos por módulo; componente "Pedidos y geocodificación" separado de repositorios y de PostGIS.
- **Contrato de errores (C4, nivel 3):** DTO versionado, JSON y OpenAPI; 400 validación, 401/403 acceso, 409 conflicto, 422 semántica.
- **Modelo físico (documento 11):** tabla `pedidos` (`codigo` único, `demanda_kg/m3 ≥ 0` con al menos una > 0, `tiempo_servicio_min > 0` por defecto 10, `ventana_fin > ventana_inicio`, `prioridad` 1–4 por defecto 2, `estado` por defecto `PENDIENTE`, `timestamptz`) y tabla `ubicaciones` (`punto geometry(Point,4326)`, `direccion_referencial`, `distrito`, `fuente`).
- **Reglas:** RN-001 (ventana coherente, demanda > 0, ubicación en el ámbito), RN-004 (estados), parámetros del negocio no fijos en código.
- **Calidad aplicable:** RNF-03 (p95 ≤ 3 s en escrituras), RNF-07 (100 % de entradas validadas, sin trazas), RNF-10 (WCAG 2.1 AA), RNF-14 (cobertura ≥ 80 % en servicios críticos, capas desacopladas), RNF-15 (variables en `.env.example`), RNF-20 (OpenAPI).
- **Dependencia pendiente:** PostgreSQL/PostGIS se configura en EN-005 (ECO-16), aún no disponible.

## Goals / Non-Goals

**Goals:**
- Primer corte vertical funcional: formulario React → API FastAPI → repositorio, que cumpla los dos escenarios Gherkin de HU-001 y las validaciones de RF-02.2.
- Dominio independiente del transporte y de la persistencia, para sustituir el adaptador en memoria por PostgreSQL/PostGIS (SQLAlchemy) sin tocar reglas ni router.
- Reglas de negocio en un solo lugar (backend); el frontend no las duplica.

**Non-Goals:**
- Autenticación y autorización (RF-11.1) y auditoría (RF-11.2): el módulo se diseña para recibir una dependencia de seguridad después; este cambio no se despliega fuera de entornos locales.
- Edición/cancelación de pedidos, transiciones de estado posteriores a `PENDIENTE` (RN-004), importación CSV, geocodificación y mapa.
- Persistencia PostgreSQL/PostGIS, migraciones Alembic y seeds (EN-005).
- Integración con el motor de optimización.

## Decisions

### D1. Módulo FastAPI `pedidos` con capas y puerto de repositorio
`router` (rutas, códigos HTTP, OpenAPI) → `service` (casos de uso) → `domain` (entidad `Pedido` y reglas) → `PedidosRepository` (protocolo/puerto) ← `PedidosMemoryRepository` (adaptador). El servicio recibe el repositorio por inyección de dependencias de FastAPI (`Depends`), nunca importa el adaptador directamente.
- *Alternativa descartada:* SQLAlchemy/PostgreSQL desde ya. Requiere EN-005 y un entorno de base de datos que el equipo aún no tiene; retrasaría el primer incremento. El puerto mantiene abierta la ruta.

### D2. Validación en dos niveles
1. **Esquemas Pydantic**: presencia, tipos, rangos y formato ISO 8601 con desfase (`AwareDatetime`) → respuesta **400** con detalle por campo. FastAPI responde 422 por defecto ante un `RequestValidationError`; un manejador global lo convierte a 400 para respetar el contrato de la spec.
2. **Dominio (`Pedido.crear`)**: reglas semánticas (ventana fin > inicio, al menos una demanda > 0, coordenadas dentro del ámbito, distrito permitido) → **422** con el campo afectado.
Ambos responden con el mismo formato: `{ "status", "message", "errors": { "<campo>": "<motivo>" } }`. Un manejador global convierte cualquier excepción no controlada en un 500 genérico sin traza (RNF-07). Los esquemas usan `extra="forbid"` para rechazar campos desconocidos.
- *Alternativa descartada:* validar todo en Pydantic. Mezcla reglas de negocio con transporte y no es reutilizable por la importación CSV de HU-008.

### D3. Estado inicial `PENDIENTE`
Se adopta el dominio `estado_pedido` del DDL (`PENDIENTE`, `VALIDADO`, `ASIGNADO`, `EN_RUTA`, `ENTREGADO`, `FALLIDO`, `CANCELADO`) y el texto de HU-001 ("estado Pendiente"). RN-004 y los documentos de requisitos nombran el flujo en minúsculas (`registrado → validado → planificado → …`), por lo que existe una divergencia de nomenclatura entre los documentos 06/09 y el documento 11; este cambio sigue el DDL por ser el contrato de persistencia. La conciliación documental queda como tarea de seguimiento, sin impacto en el comportamiento especificado.

### D4. Modelo de datos de la API y mapeo a persistencia
Campos de entrada (camelCase en español, alineados al diccionario de datos): `codigo?`, `direccion`, `distrito`, `latitud`, `longitud`, `destinatarioAlias?`, `demandaKg`, `demandaM3`, `tiempoServicioMin?`, `ventanaInicio`, `ventanaFin`, `prioridad?`, `observacionOperativa?`. Los esquemas Pydantic exponen estos nombres mediante alias. La ubicación es un objeto de valor (`direccionReferencial`, `distrito`, `latitud`, `longitud`, `fuente = 'MANUAL'`) equivalente a una fila de `ubicaciones` con `punto = POINT(longitud latitud)` (X = longitud, SRID 4326), de modo que el adaptador futuro solo traduzca.

### D5. Fechas y zona horaria
Las ventanas se reciben como ISO 8601 con desfase obligatorio y se almacenan y devuelven en UTC (`timestamptz`). Esto evita el defecto de especificación del caso "cobro fantasma en producción" (zona horaria no definida) analizado en la actividad de la semana 6. El frontend convierte hora de Lima (UTC−5, sin horario de verano) a ISO con `-05:00` al enviar y la presenta de nuevo en hora de Lima.

### D6. Ámbito geográfico configurable
Variables de entorno (documentadas en `.env.example`), leídas con `pydantic-settings` y validadas al arrancar: `AMBITO_LAT_MIN`, `AMBITO_LAT_MAX`, `AMBITO_LON_MIN`, `AMBITO_LON_MAX` y `AMBITO_DISTRITOS` (lista separada por comas). Valores por defecto de desarrollo: latitud −12.20 a −11.95, longitud −75.35 a −75.10 y los cinco distritos del ámbito (RES-10). Es un rectángulo envolvente de aproximación que **debe validarse con el negocio** (RF-02.2 habla de "ámbito configurado" y permite excepciones autorizadas cerca del límite; la excepción no entra en este cambio).
- *Alternativa descartada:* polígono PostGIS (`ST_Contains`). Requiere EN-005; se sustituirá cuando exista la base geoespacial.

### D7. Código de pedido
Si no se envía, se genera `PED-` más un correlativo de 6 dígitos (`PED-000001`). Se normaliza a mayúsculas y sin espacios laterales antes de comparar y almacenar; la unicidad se verifica en el repositorio (en memoria, mediante un índice por código normalizado; en PostgreSQL, por la restricción `UNIQUE` existente). Un código repetido produce `409`.

### D8. API y contrato
Prefijo `/api/v1`. Endpoints: `POST /pedidos` (201), `GET /pedidos?estado&pagina&limite` (200, límite por defecto 20, máximo 100, orden `creadoEn` descendente), `GET /pedidos/{id}` (identificador tipado `UUID`; 400 si no es UUID, 404 si no existe). Respuesta de listado: `{ items, total, pagina, limite }`. La documentación OpenAPI la genera FastAPI en `/docs` y `/openapi.json` (RNF-20). CORS limitado al origen del frontend mediante `CORS_ORIGIN`.

### D9. Frontend React + Vite
Aplicación React + TypeScript con un *shell* (barra lateral de navegación y barra superior con selector de tema claro/oscuro) y la vista **Pedidos** del planificador: indicadores resumen (total, pendientes, prioridad alta, carga total), tabla con búsqueda, filtro por estado y paginación, y dos paneles laterales modales: **Registrar pedido** (`PedidoForm`, secciones Destino, Carga y servicio, Ventana horaria e Identificación; un `<label>` asociado por campo, `aria-describedby` y `aria-invalid` en errores, resumen de errores con foco) y **Detalle del pedido**. La confirmación de registro se muestra en un aviso temporal (`role="status"`) con el código creado. Los paneles atrapan el foco, se cierran con Escape y devuelven el foco al botón que los abrió. `src/api/pedidos.ts` encapsula `fetch` y traduce `errors` del backend al campo correspondiente. El frontend solo omite campos vacíos para que el backend aplique sus valores por defecto; todas las reglas de negocio las decide el backend. La URL de la API viene de `VITE_API_URL`. El estilo es CSS propio ligero con la paleta de marca (#025B29, #33A905, #032D2F), tema claro/oscuro, tipografía Codec Pro e iconos Lucide (MIT); el stack no incluye Tailwind. Los elementos de navegación de módulos futuros (Flota, Rutas y mapa, Indicadores) se muestran deshabilitados con la etiqueta "Pronto".

### D10. Pruebas
Backend: pytest unitario para `Pedido.crear` (cada regla y límite) y para el servicio; pruebas de API con `TestClient`/httpx para los escenarios de la spec (201, 400, 422, 404, 409, paginación). Frontend: Vitest + Testing Library para el formulario (error por campo, conservación de valores, confirmación con código). Objetivo: cobertura ≥ 80 % en dominio y servicio (RNF-14), medida con `pytest-cov`.

## Risks / Trade-offs

- [Datos en memoria: se pierden al reiniciar y no cumplen RNF-04/RNF-11] → Mitigación: puerto de repositorio + tarea explícita de migrar a PostgreSQL/PostGIS en EN-005; el cambio se declara PMV local, no desplegable.
- [Sin autenticación, los endpoints quedan abiertos (RNF-05)] → Mitigación: no se despliega fuera de local; el router queda listo para una dependencia de RF-11.1; se registra como impedimento/riesgo en la próxima revisión de sprint.
- [Límites del ámbito aproximados con un rectángulo] → Mitigación: parámetros configurables y validación posterior con el negocio; sustituir por polígono PostGIS en EN-005.
- [Divergencia de nomenclatura de estados entre documentos 06/09 y 11] → Mitigación: se sigue el DDL; tarea de conciliación documental posterior.
- [FastAPI responde 422 por defecto en validación] → Mitigación: manejador global a 400 y pruebas que lo verifican.
- [Doble validación (frontend/backend) que diverja] → Mitigación: el frontend no replica reglas; muestra los errores que devuelve el backend.
- [Correlativo en memoria no es seguro con varios procesos] → Mitigación: aceptable para un único proceso local; en PostgreSQL se usará una secuencia.
