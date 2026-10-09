## ADDED Requirements

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
