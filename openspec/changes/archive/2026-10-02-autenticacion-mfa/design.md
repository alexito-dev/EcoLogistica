# Design

## Context

Ver `proposal.md` (Why) y `auditoria-especificacion.md` (hallazgos que moldearon la spec). Estado actual: API FastAPI de pedidos abierta, frontend React sin sesión, persistencia en memoria. Restricciones del Modelo C4: la API no guarda sesiones en memoria del proceso; tokens de corta duración en un mecanismo resistente a XSS; auditoría sin tokens ni contraseñas. RNF-06 exige hash robusto y cero secretos en Git; RNF-07, bloqueo tras 5 intentos en 15 minutos.

## Goals / Non-Goals

**Goals:**
- Autenticación de dos factores (contraseña + TOTP) para todos los roles, con enrolamiento guiado.
- Sesión sin estado en el proceso, revocable y con expiración por inactividad y máxima.
- Autorización por rol reutilizable como dependencia de FastAPI en cualquier router.
- Interfaz de acceso accesible, coherente con el diseño de la app.

**Non-Goals:**
- Gestión de usuarios desde la interfaz (alta, baja, cambio de rol) y restablecimiento del segundo factor o de la contraseña.
- ABAC por ámbito, distrito o propiedad (solo ABAC-01: usuario activo y sesión válida).
- Consulta o exportación de la auditoría; persistencia y cifrado en PostgreSQL (EN-005).

## Decisions

### D1. Módulo `app/auth` con la misma arquitectura por capas
`router` → `service` (`AutenticacionService`) → `domain` (`Usuario`, `Rol`, reglas de bloqueo) → `UsuariosRepository` (puerto) ← `UsuariosArchivoRepository` (adaptador JSON). Las utilidades criptográficas viven en `seguridad.py` (hash Argon2id, TOTP, tokens) y la autorización en `dependencias.py` (`usuario_actual`, `requerir_rol(*roles)`).

### D2. Token firmado en cookie `HttpOnly` con versión de sesión (auditoría P1)
Tras el MFA, se emite un JWT HS256 en la cookie `eco_sesion` (`HttpOnly`, `SameSite=Strict`, `Path=/api`, `Secure` según `COOKIE_SECURE`) con: `sub` (id), `ver` (versión de sesión), `auth` (instante del inicio), `exp` (15 min). En cada solicitud autenticada válida se reemite con nuevo `exp` (inactividad deslizante) si el inicio tiene menos de 8 h. `logout` incrementa `version_sesion` en el registro del usuario: todo token con otra `ver` se rechaza. No hay estado de sesión en el proceso.
- *Alternativa descartada:* sesiones en memoria o en un diccionario del servidor (contradice el C4 y no escala con réplicas). *Alternativa descartada:* token en `localStorage` (expuesto a XSS).

### D3. Comprobante temporal del paso MFA
Tras la contraseña se emite otro JWT (`eco_mfa`, `Path=/api/v1/auth`, 5 min) con `sub`, `proposito=mfa` y `ver`. En el enrolamiento, el secreto nuevo se guarda en el registro del usuario como `mfa_pendiente` (nunca dentro del token) y pasa a `mfa_secreto` solo al validar un código. Los códigos fallidos se cuentan en el registro del usuario (`mfa_fallidos`); al llegar a 5 se invalida el comprobante (se incrementa `version_sesion`, que también va en el comprobante).

### D4. TOTP con `pyotp` y anti-repetición (auditoría A4, E1)
`pyotp.TOTP(secreto).verify(codigo, valid_window=1)`; se calcula el paso usado y se guarda `mfa_ultimo_paso`: un paso menor o igual al último aceptado se rechaza. La URI `otpauth://` se genera con `provisioning_uri(correo, issuer_name="EcoLogística Huancayo")`; el QR lo dibuja el frontend con la librería `qrcode`, sin enviar el secreto a terceros.

### D5. Contraseñas y anti-enumeración (auditoría E2)
`argon2-cffi` (`PasswordHasher`, Argon2id con parámetros por defecto). Si el correo no existe, se verifica la contraseña contra un hash ficticio para igualar tiempos. El mensaje 401 es único.

### D6. Bloqueo por intentos (auditoría A1)
Registro de intentos por correo normalizado en el almacén (`intentos`: instantes de fallos recientes y `bloqueado_hasta`), también para correos inexistentes (en un apartado del mismo archivo). 5 fallos dentro de 15 minutos fijan `bloqueado_hasta = ahora + 15 min`; mientras dure, 429. Un acceso correcto limpia el registro del correo.

### D7. Autorización por rol (auditoría E3)
`requerir_rol(Rol.PLANIFICADOR)` como dependencia del router de pedidos. `usuario_actual` valida el token, carga el usuario del repositorio en cada solicitud y comprueba `estado == ACTIVO` y `ver == version_sesion`; si falla, 401. Rol no permitido: 403. Los rechazos se registran como evento `ACCESO_DENEGADO`.

### D8. Defensa CSRF por origen (auditoría E4)
Además de `SameSite=Strict`, un middleware rechaza con 403 los métodos `POST`, `PUT`, `PATCH` y `DELETE` cuya cabecera `Origin` exista y no coincida con `CORS_ORIGIN`. CORS se configura con `allow_credentials=True` y el origen exacto.

### D9. Almacén de usuarios en archivo y usuarios de demostración (auditoría P2)
`UsuariosArchivoRepository` guarda en `backend/.data/usuarios.json` (ignorado por Git) con escritura atómica (archivo temporal y reemplazo) y un candado de proceso. Al arrancar, si no hay usuarios, se crea uno por rol (`admin@`, `planificador@`, `conductor@`, `gerente@`, `auditor@` con dominio `ecologistica.test`). La contraseña de demostración se toma de `DEMO_CLAVE`; si está vacía, se genera una aleatoria y se muestra **una sola vez en la consola del servidor**. Ninguna contraseña real se versiona.

### D10. Configuración de la clave de firma
`JWT_SECRET` de al menos 32 caracteres. Si falta o es el valor de ejemplo, en desarrollo se genera una aleatoria al arrancar (las sesiones se pierden al reiniciar) y se registra una advertencia.

### D11. Eventos de acceso (base de RF-11.2)
Logger `ecologistica.auditoria` con una línea JSON por evento: `instante` (UTC ISO 8601), `accion` (`LOGIN_OK`, `LOGIN_FALLIDO`, `BLOQUEO`, `MFA_ENROLADO`, `MFA_FALLIDO`, `LOGOUT`, `ACCESO_DENEGADO`), `correo`, `resultado`. Nunca contraseñas, códigos, secretos ni tokens.

### D12. Frontend
`AuthProvider` (contexto) consulta `GET /auth/sesion` al cargar; sin sesión muestra `LoginPage`. El flujo tiene tres pasos en la misma tarjeta: credenciales → código (o enrolamiento con QR, clave en grupos de 4 y campo de confirmación) → app. Todas las llamadas usan `credentials: 'include'`; un 401 en cualquier llamada vuelve al acceso. La barra superior muestra nombre, rol y "Cerrar sesión". Un rol sin permiso sobre pedidos ve un aviso de acceso no autorizado.

### D13. Pruebas
Backend: pytest para seguridad (hash, TOTP, tokens), servicio (bloqueo, enumeración, anti-repetición, enrolamiento, expiración con reloj inyectado), API (cada escenario de la spec) y pedidos protegidos (401/403/201). Las pruebas existentes de pedidos se autentican mediante sustitución de la dependencia `usuario_actual`. Frontend: Vitest para el flujo de acceso, enrolamiento, error de credenciales, cierre de sesión y regreso al acceso ante 401.

## Risks / Trade-offs

- [Secreto TOTP sin cifrar en el archivo local de desarrollo] → archivo ignorado por Git y fuera de la carpeta pública; cifrado en reposo con EN-005.
- [Pérdida del autenticador] → fuera de alcance; un administrador podrá restablecer el factor en un cambio posterior. Mientras tanto se borra el registro del usuario en el archivo local.
- [Clave de firma generada al arrancar si no se configura] → las sesiones se pierden al reiniciar; aceptable en desarrollo y advertido en la consola.
- [Archivo JSON con varios procesos] → un solo proceso en desarrollo; PostgreSQL en EN-005.
- [Reloj del teléfono desfasado] → tolerancia de ±1 paso (±30 s).
