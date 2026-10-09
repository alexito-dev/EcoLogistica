## MODIFIED Requirements

### Requirement: Visualizar las rutas en un mapa

La interfaz SHALL mostrar la vista previa en un mapa Leaflet con teselas de OpenStreetMap y su atribución, sin claves de API: el depósito, cada parada numerada según su orden con un color por vehículo, y la línea de cada recorrido. Cuando el servicio de rutas OSRM responde, la línea MUST seguir las calles; si no responde, falla o no encuentra camino, MUST mostrarse en línea recta y la página MUST seguir funcionando. Una etiqueta MUST indicar cuál de los dos trazados se ve. Las paradas fuera de ventana MUST distinguirse visualmente. La interfaz SHALL mostrar indicadores de pedidos asignados, vehículos usados, distancia y emisiones con su ahorro, una tarjeta por vehículo con carga, duración y llegadas, los pedidos no asignados con su causa y los supuestos del cálculo. Seleccionar una tarjeta MUST resaltar su ruta en el mapa. Si no hay pedidos para la fecha, MUST explicar qué registrar para obtener rutas.

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

#### Scenario: Recorrido por calles

- **WHEN** el servicio de rutas devuelve el camino de cada recorrido
- **THEN** el mapa dibuja las rutas siguiendo las calles y la etiqueta indica "Recorrido por calles · OSRM"

#### Scenario: Servicio de rutas no disponible

- **WHEN** el servicio de rutas no responde o devuelve un error
- **THEN** el mapa muestra las rutas en línea recta, indica que el servicio no está disponible y el resto de la página funciona igual
