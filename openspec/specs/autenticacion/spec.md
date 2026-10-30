# autenticacion Specification

## Purpose
Garantiza que solo personas autenticadas con contraseña y un segundo factor TOTP usen EcoLogística, que cada acción se autorice según su rol y que la sesión sea segura, expire y pueda cerrarse (RF-11.1, RNF-05, RNF-06, RNF-07).

## Requirements

### Requirement: Inicio de sesión con contraseña
El sistema SHALL iniciar la autenticación con correo y contraseña. Cuando las credenciales son correctas y el usuario está `ACTIVO`, el sistema MUST responder que falta el segundo factor (`MFA`) o que debe enrolarlo (`ENROLAR`), sin conceder todavía acceso a ningún recurso. El correo SHALL compararse sin distinguir mayúsculas. Ante correo inexistente, contraseña incorrecta o usuario no `ACTIVO`, el sistema MUST responder 401 con el mismo mensaje genérico, sin revelar cuál de las condiciones falló.

#### Scenario: Credenciales correctas con segundo factor activo
- **WHEN** un usuario activo con segundo factor enrolado envía correo y contraseña correctos
- **THEN** el sistema responde 200 indicando el paso `MFA` y entrega un comprobante temporal de 5 minutos, sin sesión

#### Scenario: Credenciales incorrectas
- **WHEN** se envía una contraseña incorrecta o un correo que no existe
- **THEN** el sistema responde 401 con el mensaje "Correo o contraseña incorrectos" en ambos casos

#### Scenario: Usuario inactivo
- **WHEN** un usuario con estado `INACTIVO` o `BLOQUEADO` envía credenciales correctas
- **THEN** el sistema responde 401 con el mismo mensaje genérico

### Requirement: Segundo factor TOTP obligatorio
El sistema MUST exigir un código TOTP de 6 dígitos (RFC 6238, pasos de 30 segundos) generado por una app autenticadora para completar el inicio de sesión de todos los roles. SHALL aceptar el paso actual y uno de tolerancia hacia atrás o adelante por desfase de reloj. Un código ya usado MUST rechazarse aunque siga en su ventana (anti-repetición). El comprobante temporal del paso anterior MUST expirar a los 5 minutos y quedar invalidado tras 5 códigos incorrectos.

#### Scenario: Código correcto
- **WHEN** el usuario envía un código vigente dentro del plazo del comprobante temporal
- **THEN** el sistema crea la sesión, responde 200 con nombre, correo y rol, y elimina el comprobante temporal

#### Scenario: Código incorrecto
- **WHEN** el usuario envía un código incorrecto
- **THEN** el sistema responde 401 indicando el campo `codigo` y no crea sesión

#### Scenario: Código repetido
- **WHEN** el usuario reutiliza un código que ya permitió un inicio de sesión
- **THEN** el sistema responde 401 y no crea sesión

#### Scenario: Comprobante vencido o agotado
- **WHEN** el código llega después de 5 minutos o tras 5 códigos incorrectos
- **THEN** el sistema responde 401 y el usuario debe volver a ingresar su contraseña

### Requirement: Enrolamiento del segundo factor
Cuando el usuario aún no tiene segundo factor, el sistema SHALL generar un secreto TOTP nuevo y entregar la clave en Base32 y la URI `otpauth://` (emisor "EcoLogística Huancayo" y el correo como cuenta) para mostrarla como código QR. El secreto MUST activarse solo cuando el usuario valide un primer código correcto; mientras tanto, el usuario no tiene sesión.

#### Scenario: Primer inicio de sesión
- **WHEN** un usuario sin segundo factor envía credenciales correctas
- **THEN** el sistema responde con el paso `ENROLAR`, la clave y la URI `otpauth://`

#### Scenario: Confirmación del enrolamiento
- **WHEN** el usuario envía un código correcto generado con la clave entregada
- **THEN** el sistema activa el segundo factor, crea la sesión y en los siguientes ingresos pide el paso `MFA`

### Requirement: Sesión segura con expiración
La sesión SHALL mantenerse en una cookie `HttpOnly`, `SameSite=Strict`, con `Secure` configurable para HTTPS, que contiene un token firmado sin datos sensibles. La sesión MUST expirar tras 15 minutos sin actividad y a las 8 horas del inicio, aunque haya actividad. Cada solicitud autenticada SHALL renovar el plazo de inactividad. El servidor MUST NOT guardar sesiones en memoria del proceso (Modelo C4). El sistema SHALL ofrecer la consulta de la sesión actual.

#### Scenario: Consulta de sesión vigente
- **WHEN** un usuario con sesión vigente consulta su sesión
- **THEN** el sistema responde 200 con nombre, correo y rol

#### Scenario: Sesión inactiva
- **WHEN** pasan más de 15 minutos sin solicitudes
- **THEN** la siguiente solicitud recibe 401 y el usuario debe iniciar sesión de nuevo

#### Scenario: Duración máxima
- **WHEN** pasan más de 8 horas desde el inicio de sesión
- **THEN** la siguiente solicitud recibe 401 aunque haya habido actividad

#### Scenario: Token alterado
- **WHEN** se envía una cookie de sesión modificada o firmada con otra clave
- **THEN** el sistema responde 401

### Requirement: Cierre de sesión
El sistema SHALL permitir cerrar la sesión. Al cerrarla MUST borrar la cookie e invalidar todos los tokens emitidos antes para ese usuario, de modo que una copia de la cookie deje de servir.

#### Scenario: Cerrar sesión
- **WHEN** el usuario cierra la sesión
- **THEN** el sistema responde 204, borra la cookie y una solicitud posterior con el token anterior recibe 401

### Requirement: Bloqueo por intentos fallidos
El sistema MUST bloquear temporalmente un correo tras 5 intentos fallidos de contraseña dentro de 15 minutos, durante 15 minutos (RNF-07). Mientras dure el bloqueo, MUST responder 429 con un mensaje genérico, aunque la contraseña sea correcta. El conteo SHALL aplicarse igual a correos inexistentes, para no revelar qué cuentas existen. Un inicio de sesión exitoso SHALL reiniciar el contador.

#### Scenario: Quinto intento fallido
- **WHEN** se registra el quinto intento fallido para un correo en menos de 15 minutos
- **THEN** los intentos siguientes durante 15 minutos reciben 429, incluso con la contraseña correcta

#### Scenario: Correo inexistente
- **WHEN** se hacen 5 intentos fallidos con un correo que no existe
- **THEN** el sistema responde igual que con un correo existente, incluido el bloqueo

### Requirement: Autorización por rol
Cada endpoint protegido MUST exigir una sesión vigente (401 si falta) y uno de los roles permitidos (403 si el rol no lo está), denegando por defecto (ABAC-01, RNF-05). El rol SHALL leerse del registro del usuario en cada solicitud, para que un cambio de rol o de estado se aplique en la siguiente autorización. Los roles válidos son `ADMIN`, `PLANIFICADOR`, `CONDUCTOR`, `GERENTE` y `AUDITOR`. En pedidos: registrar MUST requerir `PLANIFICADOR`; consultar y listar MUST requerir `PLANIFICADOR` o `ADMIN`.

#### Scenario: Sin sesión
- **WHEN** se llama a un endpoint de pedidos sin sesión
- **THEN** el sistema responde 401 sin datos del recurso

#### Scenario: Rol no autorizado
- **WHEN** un usuario `CONDUCTOR` intenta registrar o listar pedidos
- **THEN** el sistema responde 403 sin datos del recurso

#### Scenario: Rol autorizado
- **WHEN** un `PLANIFICADOR` registra un pedido válido
- **THEN** el sistema lo registra con 201

#### Scenario: Usuario desactivado con sesión abierta
- **WHEN** un usuario con sesión vigente pasa a estado `INACTIVO`
- **THEN** su siguiente solicitud recibe 401

### Requirement: Protección de credenciales y trazas
Las contraseñas MUST guardarse solo como hash Argon2id; ningún secreto (contraseña, secreto TOTP, código, token) SHALL aparecer en respuestas de error, URL ni registros. Las solicitudes que cambian estado MUST rechazarse con 403 si traen una cabecera `Origin` distinta del origen permitido. El sistema SHALL registrar los eventos de acceso (inicio correcto, fallo, bloqueo, enrolamiento, MFA fallido, cierre de sesión y acceso denegado) con instante UTC, correo, acción y resultado (base de RF-11.2).

#### Scenario: Hash de contraseña
- **WHEN** se crea un usuario
- **THEN** su contraseña se almacena como hash Argon2id y nunca en texto plano

#### Scenario: Origen no permitido
- **WHEN** llega un `POST` con una cabecera `Origin` distinta del origen configurado
- **THEN** el sistema responde 403 sin procesar la solicitud

#### Scenario: Evento auditado sin secretos
- **WHEN** ocurre un inicio de sesión fallido
- **THEN** se registra el evento con instante, correo, acción y resultado, sin la contraseña

### Requirement: Acceso en la interfaz web
La interfaz web SHALL mostrar una pantalla de inicio de sesión cuando no hay sesión y, tras la contraseña, el paso del código o el enrolamiento con el código QR, la clave para ingreso manual y el campo de confirmación. Con sesión vigente SHALL mostrar el nombre y el rol del usuario y un botón para cerrar sesión. Si una solicitud recibe 401, la interfaz MUST volver a la pantalla de inicio de sesión; si el rol no tiene ninguna vista habilitada, MUST mostrar un aviso de acceso no autorizado. Los campos MUST tener etiqueta asociada, anunciar los errores y ser operables por teclado (RNF-10).

#### Scenario: Acceso completo
- **WHEN** un planificador ingresa correo y contraseña correctos y luego un código válido
- **THEN** la interfaz muestra la vista de pedidos con su nombre y rol

#### Scenario: Error de credenciales en la interfaz
- **WHEN** el usuario envía credenciales incorrectas
- **THEN** la interfaz muestra el mensaje genérico, conserva el correo y vacía la contraseña

#### Scenario: Cierre de sesión en la interfaz
- **WHEN** el usuario pulsa "Cerrar sesión"
- **THEN** la interfaz vuelve a la pantalla de inicio de sesión

#### Scenario: Rol sin vistas habilitadas
- **WHEN** una persona `CONDUCTOR` o `AUDITOR` inicia sesión
- **THEN** la interfaz muestra el aviso de acceso no autorizado con su nombre, su rol y el botón de cierre de sesión
