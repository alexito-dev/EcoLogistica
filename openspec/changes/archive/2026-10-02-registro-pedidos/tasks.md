# Tasks

## 1. Backend: base del proyecto FastAPI

- [x] 1.1 Crear el proyecto FastAPI en `backend/` (paquete `src/app/`, `requirements.txt` con FastAPI, Uvicorn, Pydantic, pydantic-settings, pytest, pytest-cov y httpx; entorno virtual `.venv` ignorado por Git) y verificar que `pip install -r requirements.txt` termina sin errores
- [x] 1.2 Configurar `src/app/main.py`: prefijo `/api/v1`, CORS por `CORS_ORIGIN`, documentación OpenAPI en `/docs`; verificar que `GET /docs` responde 200 con el servidor levantado (`uvicorn app.main:app`)
- [x] 1.3 Crear los manejadores globales de excepciones con el formato `{ status, message, errors }`: validación de Pydantic a 400 y error no controlado a 500 genérico sin traza; verificar con un test que ambos casos responden con ese formato
- [x] 1.4 Agregar a `.env.example` las variables `AMBITO_LAT_MIN`, `AMBITO_LAT_MAX`, `AMBITO_LON_MIN`, `AMBITO_LON_MAX` y `AMBITO_DISTRITOS` (el resto de variables ya existe), sin secretos, y verificar que la app arranca copiando solo `.env.example` a `.env`

## 2. Backend: dominio de pedidos

- [x] 2.1 Implementar la entidad `Pedido` y su método `crear` con las reglas de RN-001/RF-02.2 (ventana fin > inicio, al menos una demanda > 0, no negativos, tiempo de servicio > 0, prioridad 1–4, ámbito y distrito configurados, estado `PENDIENTE`, valores por defecto 10 y 2); verificar con tests unitarios que cubren cada regla y sus límites
- [x] 2.2 Implementar la configuración del ámbito con `pydantic-settings`, validada al arrancar; verificar con un test que una configuración inválida impide el arranque
- [x] 2.3 Definir el puerto `PedidosRepository` y el adaptador `PedidosMemoryRepository` (guardar, buscar por id, buscar por código normalizado, listar con filtro y paginación, correlativo); verificar con tests unitarios de unicidad, orden descendente y paginación
- [x] 2.4 Implementar el servicio de pedidos (registrar con generación de código `PED-000001` y normalización, obtener, listar) apoyado en el puerto; verificar con tests unitarios de código duplicado (409), código generado y no encontrado (404)

## 3. Backend: API REST

- [x] 3.1 Crear los esquemas Pydantic de registro (alias camelCase, `extra="forbid"`, fecha con desfase obligatorio) y de consulta de listado (`estado`, `pagina`, `limite` ≤ 100); verificar con tests que las respuestas 400 identifican cada campo inválido
- [x] 3.2 Implementar el router con `POST /pedidos`, `GET /pedidos` y `GET /pedidos/{id}` (`UUID` tipado); verificar que `/openapi.json` lista los tres endpoints
- [x] 3.3 Mapear errores de dominio a 422, conflicto a 409 y no encontrado a 404; verificar con `TestClient` los escenarios "Rechazar ventana inválida", "Sin carga", "Coordenadas fuera del ámbito", "Distrito no configurado" y "Código duplicado"
- [x] 3.4 Escribir las pruebas de API de todos los escenarios de `specs/pedidos/spec.md` (registro válido, valores por defecto, código generado, fecha sin zona horaria, magnitudes, consulta, listado, filtro, límite excesivo, error uniforme); verificar con `pytest` en verde
- [x] 3.5 Medir cobertura con `pytest --cov=app` y verificar ≥ 80 % en dominio y servicio de pedidos (RNF-14)

## 4. Frontend: base del proyecto React + Vite

- [x] 4.1 Crear el proyecto React + Vite + TypeScript en `frontend/` (scripts `dev`, `build`, `test`) y verificar que `npm run build` compila sin errores
- [x] 4.2 Configurar Vitest con Testing Library y verificar que un test de humo de `App` pasa con `npm test`
- [x] 4.3 Crear `src/api/pedidos.ts` (cliente tipado de `POST`/`GET /pedidos`, lectura de `VITE_API_URL`, traducción de `errors` por campo); verificar con tests que mapea una respuesta 422 y una 400 a errores por campo

## 5. Frontend: pantalla de pedidos

- [x] 5.1 Implementar `PedidoForm` con todos los campos, etiqueta asociada por control, `aria-invalid`/`aria-describedby`, conversión de hora de Lima (UTC−5) a ISO con `-05:00` y conservación de valores tras un rechazo; verificar con tests de formulario (error en `ventanaFin`, valores conservados, código mostrado tras éxito)
- [x] 5.2 Implementar `PedidosTable` y la vista de pedidos (listado con código, dirección, ventana en hora de Lima, prioridad y estado; refresco tras registrar); verificar con un test que el pedido registrado aparece con estado `PENDIENTE`
- [x] 5.3 Revisar accesibilidad por teclado y contraste (foco visible, orden de tabulación, resumen de errores) y verificar con una revisión manual documentada más una prueba que recorra los controles por teclado (RNF-10)

## 6. Integración, documentación y cierre

- [x] 6.1 Ejecutar la demostración extremo a extremo con backend y frontend levantados: registrar un pedido válido y uno con ventana inválida, y verificar que se ve el resultado esperado de ambos escenarios Gherkin de HU-001; guardar capturas en `assets/images/`
- [x] 6.2 Actualizar `README.md` (guía de instalación y ejecución local con `.env`, comandos de prueba y rutas de la API) y verificar que los comandos documentados funcionan en un clon limpio
- [x] 6.3 Documentar el límite de este cambio (repositorio en memoria, sin autenticación, ámbito aproximado y divergencia de nomenclatura de estados) en `docs/03 Implementación` del Sprint 2 y en el Registro de Impedimentos, y verificar que los enlaces relativos resuelven
- [x] 6.4 Ejecutar `openspec validate registro-pedidos`, `pytest` y `npm test` y el análisis estático; verificar que todo pasa y archivar con `/opsx:archive` en la rama `feature/registro-pedidos` con commits Conventional Commits
