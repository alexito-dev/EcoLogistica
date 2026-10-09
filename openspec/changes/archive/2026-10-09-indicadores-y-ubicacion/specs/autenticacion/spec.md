## MODIFIED Requirements

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
