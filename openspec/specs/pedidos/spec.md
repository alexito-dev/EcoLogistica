# pedidos Specification

## Purpose
Permite al planificador incorporar pedidos de última milla a la planificación diaria con dirección, carga y ventana horaria validadas, consultarlos y listarlos, garantizando que ningún pedido incoherente llegue al motor de optimización (RF-02.1, RF-02.2, RN-001, HU-001).

## Requirements

### Requirement: Registrar pedido con ventana horaria
El sistema SHALL permitir registrar un pedido con ubicación (dirección referencial, distrito y coordenadas), demanda en kilogramos y metros cúbicos, tiempo de servicio, prioridad, ventana horaria (inicio y fin) y, opcionalmente, alias del destinatario y observación operativa. El sistema MUST crear el pedido con estado `PENDIENTE`, asignarle un identificador único (`id`) y un `codigo` único, y devolver el pedido creado con sus fechas de creación y actualización. Si no se envía `codigo`, el sistema SHALL generar uno único. Si no se envía `tiempoServicioMin`, el sistema SHALL usar 10 minutos; si no se envía `prioridad`, SHALL usar 2 (normal).

#### Scenario: Registrar pedido válido
- **WHEN** el planificador envía un registro con dirección, distrito, coordenadas dentro del ámbito, peso y volumen no negativos con al menos uno mayor que cero, y una ventana cuyo fin es posterior a su inicio
- **THEN** el sistema crea el pedido con estado `PENDIENTE`, responde 201 con su `id` y su `codigo`, y el pedido queda disponible para consulta y listado

#### Scenario: Valores por defecto
- **WHEN** el planificador registra un pedido válido sin `tiempoServicioMin` ni `prioridad`
- **THEN** el sistema registra el pedido con `tiempoServicioMin` igual a 10 y `prioridad` igual a 2

#### Scenario: Código generado automáticamente
- **WHEN** el planificador registra un pedido válido sin `codigo`
- **THEN** el sistema genera un `codigo` único y lo devuelve en la respuesta

### Requirement: Coherencia de la ventana horaria
El sistema MUST rechazar un pedido cuya ventana tenga el fin igual o anterior al inicio (RN-001). Las fechas de la ventana SHALL enviarse en formato ISO 8601 con desfase horario explícito (por ejemplo `2026-10-05T08:00:00-05:00`); el sistema MUST rechazar una fecha sin desfase o con formato inválido, de modo que la ventana no dependa de la zona horaria del servidor.

#### Scenario: Rechazar ventana inválida
- **WHEN** el planificador intenta guardar un pedido cuya hora final es anterior o igual a la hora inicial
- **THEN** el sistema rechaza la operación con 422, indica que el campo `ventanaFin` debe corregirse y no crea el pedido

#### Scenario: Fecha sin zona horaria
- **WHEN** el planificador envía `ventanaInicio` sin desfase horario o con formato que no es ISO 8601
- **THEN** el sistema responde 400 indicando el campo `ventanaInicio` y no crea el pedido

### Requirement: Validación de magnitudes del pedido
El sistema MUST rechazar un pedido con peso o volumen negativos, con peso y volumen ambos iguales a cero, con tiempo de servicio no positivo o con prioridad fuera del rango 1 a 4 (1 baja, 2 normal, 3 alta, 4 urgente). El sistema MUST rechazar un cuerpo con campos obligatorios ausentes o de tipo incorrecto, indicando cada campo inválido, y SHALL conservar sin cambios los pedidos ya registrados.

#### Scenario: Peso negativo
- **WHEN** el planificador intenta guardar un pedido con `demandaKg` negativo
- **THEN** el sistema responde 400, indica el campo `demandaKg` y no crea el pedido

#### Scenario: Sin carga
- **WHEN** el planificador intenta guardar un pedido con `demandaKg` y `demandaM3` iguales a cero
- **THEN** el sistema responde 422, indica que al menos una demanda debe ser mayor que cero y no crea el pedido

#### Scenario: Prioridad fuera de rango
- **WHEN** el planificador intenta guardar un pedido con `prioridad` igual a 5
- **THEN** el sistema responde 400, indica el campo `prioridad` y no crea el pedido

#### Scenario: Campos obligatorios ausentes
- **WHEN** el planificador envía un registro sin dirección, distrito, coordenadas o ventana
- **THEN** el sistema responde 400 con la lista de campos faltantes y no crea el pedido

### Requirement: Pertenencia de la ubicación al ámbito
El sistema MUST validar que las coordenadas (latitud entre -90 y 90, longitud entre -180 y 180, en WGS 84) estén dentro del ámbito geográfico configurado y que el distrito pertenezca a los distritos configurados (Huancayo, El Tambo, Chilca, Pilcomayo y San Agustín de Cajas). El ámbito y la lista de distritos SHALL ser parámetros de configuración y no valores fijos en el código.

#### Scenario: Coordenadas fuera del ámbito
- **WHEN** el planificador intenta guardar un pedido con coordenadas fuera del ámbito configurado
- **THEN** el sistema responde 422, indica los campos `latitud` y `longitud` y no crea el pedido

#### Scenario: Coordenadas inexistentes
- **WHEN** el planificador intenta guardar un pedido con latitud 120
- **THEN** el sistema responde 400, indica el campo `latitud` y no crea el pedido

#### Scenario: Distrito no configurado
- **WHEN** el planificador intenta guardar un pedido con un distrito que no está entre los configurados
- **THEN** el sistema responde 422, indica el campo `distrito` y no crea el pedido

### Requirement: Unicidad del código de pedido
El sistema MUST garantizar que el `codigo` de un pedido sea único, comparando sin distinguir mayúsculas y sin espacios al inicio o al final, y MUST rechazar un registro cuyo código ya exista sin modificar el pedido existente.

#### Scenario: Código duplicado
- **WHEN** el planificador registra un pedido con un `codigo` que ya pertenece a otro pedido
- **THEN** el sistema responde 409, no crea un segundo pedido y deja intacto el existente

### Requirement: Consultar pedido por identificador
El sistema SHALL permitir consultar un pedido por su `id` y MUST devolver todos sus campos, su estado y sus fechas. El sistema MUST responder 404 si el pedido no existe y 400 si el identificador no tiene formato UUID, sin revelar información interna.

#### Scenario: Consulta exitosa
- **WHEN** se consulta un `id` de pedido existente
- **THEN** el sistema responde 200 con los datos completos del pedido

#### Scenario: Pedido inexistente
- **WHEN** se consulta un `id` válido que no corresponde a ningún pedido
- **THEN** el sistema responde 404 con un mensaje de error

#### Scenario: Identificador mal formado
- **WHEN** se consulta un `id` que no es un UUID
- **THEN** el sistema responde 400 indicando el campo `id`

### Requirement: Listar pedidos
El sistema SHALL permitir listar pedidos ordenados por fecha de creación descendente, con paginación (límite por defecto de 20 y máximo de 100 por página) y filtro opcional por `estado`. La respuesta MUST incluir el total de pedidos que cumplen el filtro.

#### Scenario: Listado por defecto
- **WHEN** se solicita el listado sin parámetros
- **THEN** el sistema responde 200 con hasta 20 pedidos, el total y los datos de paginación

#### Scenario: Filtro por estado
- **WHEN** se solicita el listado con `estado=PENDIENTE`
- **THEN** el sistema responde 200 únicamente con pedidos en estado `PENDIENTE`

#### Scenario: Límite excesivo
- **WHEN** se solicita el listado con un límite mayor que 100
- **THEN** el sistema responde 400 indicando el campo `limite`

### Requirement: Errores uniformes y seguros
El sistema MUST responder los errores con un formato común que incluya un mensaje y, cuando corresponda, el detalle por campo. El sistema MUST NOT exponer trazas, rutas internas ni detalles de implementación en las respuestas de error (RNF-07). Los códigos HTTP SHALL ser 400 para validación de formato o tipo, 422 para reglas semánticas, 404 para recurso inexistente, 409 para conflicto y 500 para fallos internos.

#### Scenario: Error de validación con detalle por campo
- **WHEN** una solicitud incumple más de una validación
- **THEN** la respuesta incluye un mensaje y el detalle de cada campo incorrecto, sin trazas internas

#### Scenario: Fallo interno
- **WHEN** ocurre un error no previsto en el servidor
- **THEN** el sistema responde 500 con un mensaje genérico y no incluye información interna

### Requirement: Registro y listado de pedidos en la interfaz web
La interfaz web SHALL ofrecer un formulario para registrar un pedido con todos sus campos y un listado de pedidos registrados. El formulario MUST mostrar el error de cada campo junto al campo, MUST conservar los valores ingresados cuando el servidor rechaza el registro, y MUST mostrar el `codigo` del pedido creado tras un registro exitoso. Las horas de la ventana SHALL ingresarse y mostrarse en hora de Lima (UTC-5) y enviarse con desfase explícito. Los controles SHALL tener etiqueta asociada y ser operables por teclado (RNF-10).

#### Scenario: Registro exitoso desde la interfaz
- **WHEN** el planificador completa el formulario con datos válidos y lo envía
- **THEN** la interfaz confirma el registro mostrando el `codigo` del pedido y el pedido aparece en el listado con estado `PENDIENTE`

#### Scenario: Error de ventana en el formulario
- **WHEN** el planificador envía el formulario con la hora final anterior a la inicial
- **THEN** la interfaz muestra el mensaje junto al campo de hora final, conserva los demás valores y no agrega el pedido al listado

#### Scenario: Navegación por teclado
- **WHEN** el planificador recorre el formulario solo con teclado
- **THEN** cada campo recibe foco con indicador visible, tiene etiqueta asociada y el formulario puede enviarse sin usar el ratón

### Requirement: Ubicar el destino en un mapa

El formulario de registro SHALL incluir un mapa Leaflet con teselas de OpenStreetMap centrado en Huancayo. Un clic en el mapa MUST completar la latitud y la longitud del pedido (redondeadas a 6 decimales) y quitar los errores previos de esos campos; el marcador MUST poder arrastrarse para ajustar la ubicación. Si las coordenadas se escriben a mano, el marcador MUST reflejarlas. Los campos de latitud y longitud MUST seguir disponibles para ingreso manual y por teclado.

#### Scenario: Completar coordenadas con un clic

- **WHEN** el planificador hace clic en el mapa del formulario
- **THEN** la latitud y la longitud se completan con el punto elegido y aparece el marcador

#### Scenario: Reflejar coordenadas escritas

- **WHEN** el planificador escribe una latitud y una longitud válidas
- **THEN** el marcador se ubica en esas coordenadas

#### Scenario: Ingreso sin mapa

- **WHEN** el mapa no está disponible o el planificador usa solo el teclado
- **THEN** puede registrar el pedido escribiendo latitud y longitud en sus campos
