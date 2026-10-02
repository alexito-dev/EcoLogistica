# Auditoría de la especificación — autenticación MFA y sesiones

Evidencia de la actividad de la semana 6 (Taller de Proyectos 2): se aplicó el prompt **"Auditor Senior de Arquitectura de Software"** (`Guías de Laboratorio/Prompts/Prompt Auditor Senior de Arquitectura de Software.md`) al borrador del módulo, antes de implementarlo.

- **Módulo auditado:** Autenticación con MFA y gestión segura de sesiones.
- **Borrador de partida:** requisitos tal como estaban en la línea base: RF-11.1 (documento 06), RNF-05, RNF-06 y RNF-07 (documento 07), Modelo C4 (documento 12, secciones de contenedores y seguridad) y matriz RBAC/ABAC (documento 08).
- **Fecha:** 02/10/2026 · **Responsable:** Alex Zorrilla (líder), con asistencia de IA.
- **Resultado:** 4 ambigüedades, 6 casos de borde y 3 preguntas de arquitectura; todos resueltos en `specs/autenticacion/spec.md` y `design.md` o declarados fuera de alcance.

## 1. Inconsistencias y ambigüedades

| # | Texto del borrador | Problema | Resolución en la especificación |
|---|---|---|---|
| A1 | RNF-07: "bloqueo temporal tras 5 intentos fallidos en 15 min" | No define **cuánto dura** el bloqueo, **qué se bloquea** (cuenta, IP o ambos) ni si cuentan los correos inexistentes. | Requisito *Bloqueo por intentos fallidos*: 15 minutos por correo, respuesta 429, y los correos inexistentes cuentan igual. |
| A2 | C4: "tokens de corta duración" | "Corta" no es medible. | Requisito *Sesión segura con expiración*: 15 minutos de inactividad y 8 horas de duración máxima, con escenarios de prueba para ambos. |
| A3 | RF-11.1 y HU-001: "inicia sesión" / "despachador autenticado" | No dice qué factores se exigen ni si el MFA aplica a todos los roles. | Requisito *Segundo factor TOTP obligatorio*: contraseña más TOTP para los cinco roles. |
| A4 | Actividad: "código MFA válido" | No define formato, algoritmo ni tolerancia de reloj. | RFC 6238, 6 dígitos, pasos de 30 s, tolerancia de ±1 paso. |

## 2. Casos de borde omitidos

| # | Escenario | Riesgo | Resolución |
|---|---|---|---|
| E1 | Reutilizar un código TOTP dentro de su ventana de 30–90 s | Un código observado o interceptado sirve dos veces. | Escenario *Código repetido*: anti-repetición por usuario. |
| E2 | Mensajes o tiempos distintos para correo inexistente y contraseña errónea | Enumeración de cuentas. | Mensaje único, mismo conteo de bloqueo y verificación de hash simulada para igualar tiempos. |
| E3 | Cambio de rol o desactivación con una sesión abierta | El usuario conserva permisos que ya no tiene. | El rol y el estado se leen del registro en cada solicitud; escenario *Usuario desactivado con sesión abierta*. |
| E4 | Cookie de sesión enviada desde otro sitio (CSRF) | Acciones no deseadas con la sesión de la víctima. | `SameSite=Strict` y rechazo 403 de `POST` con `Origin` distinto (escenario *Origen no permitido*). |
| E5 | Fuerza bruta sobre el código (1 entre 1 000 000) | Adivinar el segundo factor. | Comprobante temporal de 5 minutos que se invalida tras 5 códigos incorrectos. |
| E6 | Pérdida del teléfono con la app autenticadora | El usuario queda sin acceso. | **Fuera de alcance** de este cambio: el restablecimiento por un administrador queda para un cambio posterior y se registra como riesgo en `design.md`. |

## 3. Preguntas de arquitectura y decisiones

| # | Pregunta | Decisión |
|---|---|---|
| P1 | ¿Sesión guardada en el servidor o token firmado? El C4 dice que la API "no mantiene estado de sesión en memoria", pero cerrar sesión exige invalidar tokens. | Token JWT firmado en cookie `HttpOnly` (sin estado en memoria). La revocación usa una **versión de sesión** guardada en el registro del usuario: cerrar sesión la incrementa y todos los tokens anteriores dejan de valer. |
| P2 | ¿Dónde y cómo se guarda el secreto TOTP? RNF-06 pide cifrar en reposo los datos sensibles. | En el PMV, en el almacén local de usuarios (archivo ignorado por Git, fuera de la carpeta pública). El cifrado en reposo se implementará con PostgreSQL (EN-005); queda como riesgo aceptado y documentado. |
| P3 | ¿El MFA es viable para conductores con 2G/3G? | Sí: TOTP funciona sin red en el teléfono y no depende de SMS. Por eso se eligió TOTP y no códigos por SMS o correo. |

## 4. Verificación posterior

La especificación auditada se valida con `openspec validate autenticacion-mfa --strict`, y cada escenario tiene al menos una prueba automatizada en `backend/tests/auth/` o `frontend/tests/`.
