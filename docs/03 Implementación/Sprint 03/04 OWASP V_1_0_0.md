# Reporte de Seguridad OWASP Top 10 (2025)

[← Volver al README Principal](../../../README.md#93-fase-03-implementación)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla  
**Herramienta de Escaneo:** SonarQube / SonarCloud — SonarQube Community Build 26.9.0.129388 (local), complementado con `npm audit`, `pip-audit` 2.x, revisión manual de código y prueba de cabeceras HTTP  

## Metadatos del documento

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Fecha | 30/10/2026 |
| Referencia | [OWASP Top 10:2025](https://owasp.org/Top10/2025/) |
| Requisitos vinculados | RNF-02 (OWASP Top 10 mitigado), OQ-06 y KPI-Q4 (0 vulnerabilidades críticas), EN-004 (Hardening OWASP Top 10), RSK-06 |
| Documentos relacionados | [01 Revisión](01%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md) · [02 Retrospectiva](02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) · [03 Calidad de código](03%20Calidad%20de%20c%C3%B3digo%20V_1_0_0.md) · [05 WCAG](05%20WCAG%20V_1_0_0.md) |

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 30/10/2026 | Hilario Talavera, Alexander Daniel | Evaluación de las 10 categorías, correcciones aplicadas y elementos bajo revisión. |

## Resultado de SonarQube y alcance

| Indicador de SonarQube | Resultado |
|---|---|
| Vulnerabilidades | **0** (calificación de seguridad **A**) |
| Security Hotspots | **0** (calificación de revisión **A**) |
| Incidencias con etiqueta OWASP | 0 |

> **Limitación declarada.** La edición Community de SonarQube no incluye el análisis de flujo de datos contaminados (*taint analysis*) que detecta inyecciones entre archivos. Un resultado de 0 no prueba por sí solo la ausencia de vulnerabilidades. Por eso cada categoría se contrastó con revisión manual del código, auditoría de dependencias (`npm audit`, `pip-audit`) y una prueba de las respuestas HTTP de la API en ejecución.

**Nota sobre la versión de OWASP.** La plantilla del curso enumera las categorías con la nomenclatura de 2021. En la edición **2025** algunas cambiaron de posición o de nombre: entraron *Software Supply Chain Failures* (A03) y *Mishandling of Exceptional Conditions* (A10), y SSRF pasó a formar parte de A01. La matriz conserva las filas de la plantilla e indica en cada una su **categoría oficial 2025**; la sección 1.1 evalúa la única categoría 2025 que no tiene fila en la plantilla.

## 1. Matriz de Cumplimiento OWASP Top 10 2025

| Categoría OWASP 2025 (plantilla) | Categoría oficial 2025 | Estado en Proyecto (Limpio / Vulnerable / Bajo Revisión) | Hallazgos de SonarQube |
|---|---|---|---|
| A01:2025-Broken Access Control | **A01:2025** Broken Access Control | **Limpio** | 0 incidencias. Revisión manual: cada router exige sesión (`401`) y rol mediante `requerir_rol(...)` (`403`), y los endpoints de rutas guardadas siguen la misma regla (prueba de roles en `tests/rutas/test_guardadas.py`); los roles sin permiso se prueban en `test_api_auth.py`, `tests/rutas` y `tests/indicadores`. El middleware `verificar_origen` rechaza cambios de estado desde orígenes ajenos (defensa CSRF adicional a `SameSite=Strict`). |
| A02:2025-Cryptographic Failures | **A04:2025** Cryptographic Failures | **Bajo Revisión** | 0 incidencias. Contraseñas con **Argon2id**; JWT HS256 con algoritmo fijado al decodificar y clave aleatoria si `JWT_SECRET` tiene menos de 32 caracteres. **Pendiente:** los secretos TOTP se guardan sin cifrar en `backend/.data/usuarios.json` (fuera de Git) hasta EN-005 / ECO-21; `COOKIE_SECURE=false` es válido solo en desarrollo local sin HTTPS. |
| A03:2025-Injection | **A05:2025** Injection | **Limpio** | 0 incidencias. Acceso a datos con SQLAlchemy parametrizado; la única consulta textual (`database_health.py`) es una cadena fija sin datos del usuario. Entradas validadas con Pydantic. En el frontend no se usa `dangerouslySetInnerHTML`; los *popups* de Leaflet escapan cada dato con `escapar()` antes de insertarlo. |
| A04:2025-Insecure Design | **A06:2025** Insecure Design | **Bajo Revisión** | 0 incidencias. A favor: límites de intentos (5 fallos → bloqueo de 15 min, también para correos inexistentes), mensajes genéricos, vista previa de rutas de solo lectura y especificaciones OpenSpec auditadas antes de programar. **Pendiente:** el trazado por calles envía las coordenadas de las paradas al servidor público de demostración de OSRM (privacidad, Ley N.° 29733) y no existe restablecimiento del segundo factor por un administrador. |
| A05:2025-Security Misconfiguration | **A02:2025** Security Misconfiguration | **Vulnerable → corregido** (queda una decisión de despliegue) | 0 incidencias. **Hallazgo manual:** la API no enviaba cabeceras de endurecimiento. **Corregido** con el middleware `cabeceras_de_seguridad` (ver Hotspot #1). CORS limitado a un único origen y a los métodos `GET`, `POST` y `PUT`. **Por decidir antes de desplegar:** `/docs` y `/openapi.json` quedan públicos. |
| A06:2025-Vulnerable and Outdated Components | **A03:2025** Software Supply Chain Failures | **Vulnerable → corregido** | SonarQube no audita dependencias. `npm audit` encontró **1 vulnerabilidad alta** en Vite 8.3.0–8.3.2 (GHSA-vfpm-58rq-9qcg) y 2 moderadas; **corregida** al actualizar a Vite 8.3.5 (ver Hotspot #2). Quedan 3 moderadas **solo en herramientas de desarrollo** (`vitest`, `@vitest/mocker`, `@vitest/coverage-v8` 4.1.11), que no se incluyen en el *bundle*. Dependencias de producción: **0**. `pip-audit` en las dependencias de la API: **0** (los 4 avisos que reporta son del propio `pip` 26.1.1 del entorno local). |
| A07:2025-Identification and Authentication Failures | **A07:2025** Authentication Failures | **Limpio** | 0 incidencias. MFA obligatorio con TOTP (RFC 6238) y códigos de un solo uso; enrolamiento con QR que solo se activa al validar un código; sesión en cookie `HttpOnly` + `SameSite=Strict` con vencimiento a los 15 min de inactividad y a las 8 h; cerrar sesión invalida los tokens emitidos. Comprobado en navegador el 30/10. |
| A08:2025-Software and Data Integrity Failures | **A08:2025** Software or Data Integrity Failures | **Bajo Revisión** | 0 incidencias. A favor: `package-lock.json` con *hashes* de integridad e instalación con `npm ci` en el CI; migraciones versionadas con Alembic. **Pendiente:** `requirements.txt` usa rangos (`>=`) sin versiones fijas ni *hashes*, y las GitHub Actions se fijan por etiqueta (`@v4`), no por SHA. |
| A09:2025-Security Logging and Monitoring Failures | **A09:2025** Security Logging & Alerting Failures | **Bajo Revisión** | 0 incidencias. Los eventos de acceso (`LOGIN_OK`, `LOGIN_FALLIDO`, `BLOQUEO`, `MFA_ENROLADO`, `MFA_FALLIDO`, `LOGOUT`, `ACCESO_DENEGADO`) se registran como una línea JSON por evento en `ecologistica.auditoria` sin contraseñas, códigos ni tokens (defecto IMP-012 corregido en el Sprint 2). **Pendiente:** el registro solo va a la consola; no se conserva ni genera alertas. |
| A10:2025-Server-Side Request Forgery (SSRF) | **A01:2025** (SSRF integrado en Broken Access Control) | **Limpio** | 0 incidencias. El backend no hace solicitudes HTTP salientes. La única llamada externa (OSRM) la hace el navegador hacia una URL fija definida al compilar (`VITE_OSRM_URL`); el usuario no puede cambiar el destino. |

### 1.1. Categoría oficial 2025 sin fila en la plantilla

| Categoría oficial 2025 | Estado | Evidencia |
|---|---|---|
| **A10:2025** Mishandling of Exceptional Conditions | **Limpio** | [`errors.py`](../../../backend/src/app/errors.py) devuelve 400, 401, 403, 404, 409, 422, 429 y 500 con un formato común y **sin trazas internas**. Si OSRM falla o no responde, el mapa vuelve a líneas rectas y la página sigue funcionando (escenario "Servicio de rutas no disponible", con prueba en `trazado.test.ts`). Una configuración inválida del ámbito detiene el arranque (falla cerrada) en lugar de continuar con valores incoherentes. |

### 1.2. Resumen

| Estado | Categorías (oficiales 2025) |
|---|---|
| Limpio | A01, A05, A07, A10 |
| Vulnerable → corregido en este sprint | A02, A03 |
| Bajo revisión (sin vulnerabilidad explotable conocida; requieren trabajo planificado) | A04, A06, A08, A09 |
| **Vulnerabilidades críticas abiertas (meta OQ-06 / KPI-Q4 = 0)** | **0** |

## 2. Detalles de Security Hotspots y Vulnerabilidades Críticas

SonarQube **no reportó Security Hotspots** (0) en este análisis. Los dos hallazgos más graves salieron de la revisión complementaria y se trataron como críticos para este sprint:

- **Hotspot #1 — Respuestas de la API sin cabeceras de seguridad** (A02:2025 Security Misconfiguration).
  - *Descripción:* al consultar `GET /api/v1/auth/sesion` con la API en ejecución, la respuesta solo traía `content-type`, `content-length`, `date`, `server` y `vary`. Sin `X-Content-Type-Options`, `X-Frame-Options` ni CSP, el navegador puede interpretar mal el tipo de contenido o mostrar la API dentro de un *iframe* ajeno (*clickjacking*).
  - *Ubicación:* [`backend/src/app/main.py`](../../../backend/src/app/main.py), función `create_app()`.
  - *Mitigación aplicada:* middleware `cabeceras_de_seguridad` que añade `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY` y `Referrer-Policy: no-referrer` a todas las respuestas, y `Content-Security-Policy: default-src 'none'; frame-ancestors 'none'` a las rutas `/api/v1`. `/docs` no recibe la CSP estricta porque Swagger UI carga recursos desde un CDN. Pruebas de regresión: [`test_cabeceras_seguridad.py`](../../../backend/tests/test_cabeceras_seguridad.py) (2 pruebas, incluida una respuesta 401).
- **Hotspot #2 — Vite con vulnerabilidad de severidad alta** (A03:2025 Software Supply Chain Failures).
  - *Descripción:* Vite 8.3.0–8.3.2 permitía leer los primeros bytes de archivos fuera de la carpeta permitida (`server.fs`) mediante `?vite-wasm-instance` (GHSA-vfpm-58rq-9qcg). Afecta al servidor de desarrollo, que el equipo ejecuta en sus equipos.
  - *Ubicación:* [`frontend/package-lock.json`](../../../frontend/package-lock.json) (Vite 8.3.0 resuelto).
  - *Mitigación aplicada:* `npm audit fix` sin cambios incompatibles → **Vite 8.3.5**. Después de actualizar pasaron las 51 pruebas de frontend, el *lint* y la compilación de producción.
- **Hallazgo #3 (bajo revisión) — Secretos TOTP en texto plano** (A04:2025 Cryptographic Failures).
  - *Ubicación:* [`archivo_repository.py`](../../../backend/src/app/auth/archivo_repository.py) → `backend/.data/usuarios.json` (ignorado por Git).
  - *Mitigación prevista:* cifrar el secreto con una clave fuera del repositorio y mover las cuentas a PostgreSQL (EN-005 / ECO-21). Responsable: Anco Porras, Jhean Pier Julio. Sprint 4.
- **Hallazgo #4 (bajo revisión) — Coordenadas enviadas a un servicio público** (A06:2025 Insecure Design).
  - *Ubicación:* [`frontend/src/lib/trazado.ts`](../../../frontend/src/lib/trazado.ts) (`VITE_OSRM_URL`, por defecto `router.project-osrm.org`).
  - *Mitigación prevista:* usar un OSRM propio o anonimizar los puntos antes de enviarlos; decisión en el Planning del Sprint 4. Con los datos sintéticos actuales no hay datos personales reales expuestos.

## 3. Verificación

| Comprobación | Resultado |
|---|---|
| `pytest` backend (incluye las 2 pruebas nuevas de cabeceras y las 7 de rutas guardadas) | 137 aprobadas |
| `vitest` frontend tras actualizar Vite | 58 aprobadas (estado final de la rama) |
| `npm run build` y `npm run lint` | Sin errores |
| SonarQube después de las correcciones | 0 vulnerabilidades · 0 *hotspots* · Quality Gate PASSED |
| `npm audit --omit=dev` | 0 vulnerabilidades |
