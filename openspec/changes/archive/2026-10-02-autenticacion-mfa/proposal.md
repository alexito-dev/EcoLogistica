# Proposal

## Why

La API y la interfaz de pedidos están abiertas: cualquiera con acceso a la red puede registrar o leer pedidos, aunque el criterio de aceptación de HU-001 exige un "despachador autenticado" y RF-11.1 pide autenticar y autorizar cada acción por rol. La actividad de la semana 6 del Taller pide especificar e implementar **autenticación con MFA y gestión segura de sesiones**, auditando la especificación antes de programar. Es el siguiente incremento del Sprint 2 y bloquea todos los módulos con datos (RNF-05, RNF-06, RNF-07).

## What Changes

- Nueva capacidad **autenticación**: inicio de sesión con correo y contraseña más un **segundo factor TOTP** (código de 6 dígitos de una app autenticadora), obligatorio para todos los roles.
- **Enrolamiento del segundo factor** en el primer inicio de sesión: el sistema entrega la clave y un código QR y solo activa el factor tras validar un primer código.
- **Sesión segura** en cookie `HttpOnly`, `SameSite=Strict`, con token firmado de corta duración (15 min de inactividad, 8 h máximo), renovación por actividad y **cierre de sesión** que invalida los tokens emitidos.
- **Protección contra fuerza bruta**: bloqueo temporal tras 5 intentos fallidos en 15 minutos (RNF-07), mensajes que no revelan si una cuenta existe y contraseñas con hash **Argon2id** (RNF-06).
- **Autorización por rol (RBAC)** para los cinco roles del documento 08: el registro de pedidos queda para `PLANIFICADOR`; la consulta, para `PLANIFICADOR` y `ADMIN`; el resto se deniega por defecto.
- **Traza de eventos de acceso** (inicio, fallo, bloqueo, MFA, cierre, denegación) sin contraseñas, códigos ni tokens (base de RF-11.2).
- **BREAKING**: los endpoints `/api/v1/pedidos` pasan a exigir sesión (401) y rol (403).
- Interfaz web: pantalla de inicio de sesión, paso de código, enrolamiento con QR, usuario y rol visibles, y cierre de sesión.

Fuera de alcance: alta y gestión de usuarios desde la interfaz, recuperación de contraseña o del segundo factor, ABAC por ámbito o distrito, consulta y exportación de auditoría, y persistencia en PostgreSQL.

## Capabilities

### New Capabilities
- `autenticacion`: inicio de sesión con contraseña y segundo factor TOTP, enrolamiento, sesión segura, cierre de sesión, bloqueo por intentos, autorización por rol y traza de eventos de acceso.

### Modified Capabilities
<!-- `pedidos` aún no está en openspec/specs/ (su cambio no se ha archivado); la exigencia de sesión y rol sobre pedidos se especifica aquí, en la capacidad de autenticación. -->

## Impact

- **Backend:** nuevo módulo `backend/src/app/auth/` (dominio, servicio, almacén de usuarios, tokens, dependencias de seguridad, router); `pedidos/router.py` exige rol; dependencias `argon2-cffi`, `pyotp` y `PyJWT`.
- **API:** `POST /api/v1/auth/login`, `POST /api/v1/auth/mfa`, `GET /api/v1/auth/sesion`, `POST /api/v1/auth/logout`.
- **Frontend:** pantallas de acceso y MFA, guarda de sesión, `fetch` con `credentials: 'include'`, dependencia `qrcode` para el QR.
- **Configuración:** `JWT_SECRET`, `COOKIE_SECURE`, `DEMO_CLAVE` en `.env.example`, sin valores reales (RNF-06, RNF-15).
- **Datos:** usuarios de demostración (uno por rol) en un archivo local ignorado por Git hasta EN-005.
- **Trazabilidad:** RF-11.1, RF-11.2 (parcial), RNF-05, RNF-06, RNF-07, RNF-08 (parcial), RNF-10; matriz RBAC y ABAC-01 del documento 08; HU-001 (precondición "autenticado").
