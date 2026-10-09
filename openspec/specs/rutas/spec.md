# rutas Specification

## Purpose
Permite a Planificación ver en un mapa, antes de salir a reparto, cómo se distribuirían los pedidos del día entre los vehículos con turno: secuencia, llegadas estimadas, puntualidad, distancia, carga y CO₂e, junto con el ahorro frente a un despacho sin optimizar. Es una vista previa de solo lectura que adelanta HU-004 y HU-005 hasta que exista el motor VRPTW (EN-001).

## Requirements

### Requirement: Consultar la vista previa de rutas de una fecha

El sistema SHALL permitir a una persona con rol `PLANIFICADOR` o `ADMIN` solicitar la vista previa de rutas de una fecha de reparto. La vista previa MUST considerar solo los pedidos en estado `PENDIENTE` o `VALIDADO` cuya ventana inicia en esa fecha (hora de Lima) y solo los vehículos aptos para planificar en esa fecha. La operación MUST ser de solo lectura: no guarda rutas ni cambia el estado de pedidos o vehículos. La fecha MUST ser obligatoria y con formato válido; toda solicitud MUST requerir sesión autenticada y el sistema MUST denegar los demás roles.

#### Scenario: Obtener rutas con pedidos y flota del día

- **WHEN** una persona `PLANIFICADOR` solicita la vista previa de una fecha con pedidos planificables y vehículos con turno disponible
- **THEN** el sistema responde 200 con las rutas por vehículo, el depósito de salida, un resumen y los supuestos del cálculo

#### Scenario: Fecha sin pedidos

- **WHEN** se solicita una fecha sin pedidos planificables
- **THEN** el sistema responde 200 sin rutas, sin pedidos no asignados y con ahorro igual a cero

#### Scenario: Fecha ausente o inválida

- **WHEN** se solicita la vista previa sin fecha o con una fecha que no tiene el formato AAAA-MM-DD
- **THEN** el sistema responde 400 con el formato común de error

#### Scenario: Rol sin permiso

- **WHEN** una persona con rol distinto de `PLANIFICADOR` o `ADMIN` solicita la vista previa
- **THEN** el sistema responde 403 y no expone datos

### Requirement: Asignar pedidos respetando la capacidad

El sistema MUST asignar cada pedido a lo sumo a un vehículo sin superar su capacidad en kilogramos ni en metros cúbicos. Los pedidos de mayor prioridad y ventana más temprana MUST ubicarse primero. Un pedido que no quepa en ningún vehículo MUST reportarse como no asignado con su causa: "No hay vehículos disponibles para la fecha" cuando no hay vehículos aptos, o "Supera la capacidad libre de la flota" en otro caso.

#### Scenario: Pedido que excede la capacidad libre

- **WHEN** la demanda de un pedido supera la capacidad que queda en todos los vehículos aptos
- **THEN** el pedido aparece como no asignado con la causa "Supera la capacidad libre de la flota" y ninguna ruta excede su capacidad

#### Scenario: Prioridad ante capacidad escasa

- **WHEN** dos pedidos compiten por la última capacidad disponible y uno tiene mayor prioridad
- **THEN** el de mayor prioridad se asigna y el otro queda como no asignado

#### Scenario: Sin vehículos con turno

- **WHEN** existen pedidos en la fecha pero ningún vehículo apto para planificar
- **THEN** todos los pedidos quedan no asignados con la causa "No hay vehículos disponibles para la fecha"

### Requirement: Ordenar cada ruta por ventanas horarias y emisiones

Cada ruta MUST partir del depósito configurado y volver a él. El sistema MUST elegir la asignación y el orden de visita minimizando, en este orden, la cantidad de paradas que llegan fuera de su ventana y luego las emisiones estimadas de CO₂e. Para cada parada MUST informar el orden, la llegada estimada y si llega dentro de su ventana; si el vehículo llega antes de que abra la ventana, la llegada estimada MUST ser la apertura de la ventana. El resultado MUST ser determinista para los mismos datos.

#### Scenario: Cumplir una ventana temprana

- **WHEN** un pedido lejano tiene una ventana temprana que el orden de registro no alcanzaría
- **THEN** la ruta propuesta lo visita a tiempo y todas sus paradas quedan dentro de su ventana

#### Scenario: Esperar la apertura de la ventana

- **WHEN** el vehículo llegaría a una parada antes del inicio de su ventana
- **THEN** la llegada estimada es el inicio de la ventana y la parada se marca dentro de su ventana

#### Scenario: Marcar llegada tardía

- **WHEN** ninguna secuencia permite llegar antes del fin de la ventana de una parada
- **THEN** la parada se informa como fuera de su ventana

#### Scenario: Preferir el vehículo que menos emite

- **WHEN** un pedido cabe en un vehículo diésel y en uno eléctrico con la misma puntualidad
- **THEN** el pedido se asigna al vehículo con menor emisión estimada

### Requirement: Estimar distancia y emisiones con supuestos visibles

El sistema MUST estimar la distancia entre puntos como la distancia de gran círculo multiplicada por un factor de circuito urbano de 1,3, y las emisiones como `km / 100 × consumo base por 100 km × factor de emisión`. Si el vehículo tiene factor de emisión registrado, MUST usarse; si no, el de referencia de su combustible. La respuesta MUST incluir la lista de supuestos usados para que la interfaz los muestre.

#### Scenario: Usar el factor del vehículo o el de referencia

- **WHEN** se calcula la emisión de un vehículo diésel sin factor propio y la de otro con factor propio
- **THEN** el primero usa 2,68 kg CO₂e por litro y el segundo su propio factor

### Requirement: Comparar contra un despacho sin optimizar

La respuesta MUST incluir la distancia, las emisiones y las paradas fuera de ventana de un despacho sin optimizar, que llena los vehículos en orden de placa con los pedidos en orden de registro y los visita en ese mismo orden. El resumen MUST informar el ahorro porcentual de CO₂e respecto de ese despacho, y cero cuando no hay emisiones de referencia.

#### Scenario: Mostrar el ahorro

- **WHEN** la propuesta recorre menos o emite menos que el despacho sin optimizar
- **THEN** el resumen informa ambas cifras y el porcentaje de ahorro de CO₂e

### Requirement: Visualizar las rutas en un mapa

La interfaz SHALL mostrar la vista previa en un mapa Leaflet con teselas de OpenStreetMap y su atribución, sin claves de API: el depósito, cada parada numerada según su orden con un color por vehículo, y la línea de cada recorrido. Las paradas fuera de ventana MUST distinguirse visualmente. La interfaz SHALL mostrar indicadores de pedidos asignados, vehículos usados, distancia y emisiones con su ahorro, una tarjeta por vehículo con carga, duración y llegadas, los pedidos no asignados con su causa y los supuestos del cálculo. Seleccionar una tarjeta MUST resaltar su ruta en el mapa. Si no hay pedidos para la fecha, MUST explicar qué registrar para obtener rutas.

#### Scenario: Ver rutas del día

- **WHEN** el planificador abre la página Rutas y la fecha tiene rutas propuestas
- **THEN** ve el mapa con las rutas, los indicadores con el ahorro y una tarjeta por vehículo

#### Scenario: Resaltar una ruta

- **WHEN** el planificador selecciona la tarjeta de un vehículo
- **THEN** la tarjeta queda marcada como seleccionada y su ruta se resalta en el mapa mientras las demás se atenúan

#### Scenario: Cambiar la fecha

- **WHEN** el planificador cambia la fecha de reparto
- **THEN** la interfaz solicita la vista previa de la nueva fecha

#### Scenario: Fecha sin pedidos en la interfaz

- **WHEN** la vista previa de la fecha no tiene rutas ni pedidos no asignados
- **THEN** la interfaz indica que se registren pedidos en esa fecha y se declare el turno de los vehículos en Flota
