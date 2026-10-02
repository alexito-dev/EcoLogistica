# Tasks

## 1. Backend: seguridad base

- [x] 1.1 Agregar `argon2-cffi`, `pyotp` y `PyJWT` a `backend/requirements.txt` e instalarlas; verificar que `pip install -r requirements.txt` termina sin errores
- [x] 1.2 Extender la configuración con `JWT_SECRET` (≥ 32 caracteres o generada en desarrollo con advertencia), `COOKIE_SECURE` y `DEMO_CLAVE`, y documentarlas en `.env.example` sin valores reales; verificar con tests de configuración
- [x] 1.3 Implementar `seguridad.py` (hash y verificación Argon2id, generación y verificación TOTP con anti-repetición, emisión y validación de tokens de sesión y de MFA); verificar con tests unitarios de hash, código correcto/incorrecto/repetido/desfasado y token alterado o vencido

## 2. Backend: dominio, almacén y servicio

- [x] 2.1 Implementar el dominio (`Rol`, `EstadoUsuario`, `Usuario`) y el puerto `UsuariosRepository` con el adaptador `UsuariosArchivoRepository` (escritura atómica en `backend/.data/usuarios.json`, ignorado por Git); verificar con tests de guardado, lectura y correo sin distinguir mayúsculas
- [x] 2.2 Implementar la siembra de usuarios de demostración (uno por rol) con `DEMO_CLAVE` o clave aleatoria mostrada una sola vez en consola; verificar con un test que crea los cinco roles y no sobrescribe usuarios existentes
- [x] 2.3 Implementar `AutenticacionService`: inicio de sesión (paso `MFA` o `ENROLAR`, mensaje único, hash ficticio), bloqueo por intentos (5 en 15 min, 15 min, también para correos inexistentes), verificación MFA (anti-repetición, 5 fallos invalidan el comprobante), enrolamiento, sesión vigente y cierre de sesión por versión; verificar con tests de servicio con reloj inyectado
- [x] 2.4 Implementar el registro de eventos de acceso en el logger `ecologistica.auditoria` (JSON por línea, sin secretos); verificar con un test que captura los eventos y comprueba que no contienen la contraseña ni el código

## 3. Backend: API y autorización

- [x] 3.1 Implementar el router `/api/v1/auth` (`login`, `mfa`, `sesion`, `logout`) con cookies `HttpOnly`, `SameSite=Strict`, renovación deslizante y límites de 15 min y 8 h; verificar con tests de API de cada escenario de la spec
- [x] 3.2 Implementar las dependencias `usuario_actual` y `requerir_rol`, aplicarlas al router de pedidos (registrar: `PLANIFICADOR`; consultar y listar: `PLANIFICADOR` o `ADMIN`) y adaptar las pruebas existentes de pedidos; verificar 401, 403 y 201 con pruebas
- [x] 3.3 Implementar el middleware de origen (403 ante `Origin` no permitido en métodos que cambian estado) y CORS con credenciales; verificar con tests
- [x] 3.4 Ejecutar `pytest --cov=app` y verificar todas las pruebas en verde y cobertura ≥ 80 % en el módulo de autenticación (RNF-14)

## 4. Frontend: acceso

- [x] 4.1 Agregar la librería `qrcode`, el cliente `src/api/auth.ts` y `credentials: 'include'` en todas las llamadas, con aviso global ante 401; verificar con tests del cliente
- [x] 4.2 Implementar `AuthProvider` y la pantalla de acceso (credenciales, código, enrolamiento con QR y clave), accesible y con el diseño de la app; verificar con tests del flujo completo, error de credenciales y enrolamiento
- [x] 4.3 Integrar la sesión en el *shell* (nombre, rol, "Cerrar sesión"), el regreso al acceso ante 401 y el aviso de acceso no autorizado para roles sin permiso; verificar con tests

## 5. Integración, documentación y cierre

- [x] 5.1 Demostración extremo a extremo con backend y frontend levantados: enrolamiento con una app autenticadora (o código generado con la clave), acceso, registro de un pedido, cierre de sesión y rechazo de rol no autorizado; verificar el resultado de cada paso
- [x] 5.2 Actualizar `README.md` (cómo obtener la clave de demostración, enrolar el segundo factor, roles y endpoints de autenticación) y verificar que los enlaces resuelven
- [x] 5.3 Ejecutar `openspec validate autenticacion-mfa --strict`, `pytest`, `npm test`, `npm run build` y el lint; verificar todo en verde
