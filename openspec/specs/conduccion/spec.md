# conduccion Specification

## Purpose
Permite a quien conduce consultar la ruta que Planificación le asignó, marcar el avance de cada entrega (En ruta, Entregado, Incidencia, Cancelado) y reportar incidencias, y permite a Planificación asignar conductores, ver el avance y las incidencias, reprogramar paradas y reordenar las paradas pendientes (HU-005, HU-010 y HU-006). Cada avance se conserva como un evento inmutable con su historial.

## Requirements

### Requirement: Consultar la ruta asignada

El sistema SHALL permitir a una persona con rol `CONDUCTOR` consultar, para una fecha, únicamente las rutas guardadas cuyo vehículo le fue asignado, con sus paradas en orden, ventana, carga, llegada estimada y estado actual. El sistema MUST responder 404 cuando no existan rutas guardadas para la fecha, MUST exigir sesión y MUST denegar los demás roles.

#### Scenario: Ver la ruta asignada

- **WHEN** una persona `CONDUCTOR` con un vehículo asignado consulta la fecha de rutas guardadas
- **THEN** el sistema responde 200 solo con la ruta de su vehículo, con las paradas en orden y todas en estado `PENDIENTE`

#### Scenario: Fecha sin rutas guardadas

- **WHEN** la persona conductora consulta una fecha sin rutas guardadas
- **THEN** el sistema responde 404

#### Scenario: Rol sin permiso

- **WHEN** una persona con rol distinto de `CONDUCTOR` consulta la ruta asignada
- **THEN** el sistema responde 403

### Requirement: Registrar el avance de una entrega

El sistema MUST permitir a la persona conductora cambiar el estado de una parada de su propia ruta solo mediante las transiciones válidas: `PENDIENTE` a `EN_RUTA` o `CANCELADO`; `EN_RUTA` a `ENTREGADO`, `INCIDENCIA` o `CANCELADO`; `INCIDENCIA` a `EN_RUTA` o `CANCELADO`. `ENTREGADO`, `CANCELADO` y `REPROGRAMADO` MUST ser estados finales y `REPROGRAMADO` MUST NOT ser elegible por quien conduce. Cada cambio MUST guardarse como un evento inmutable y MUST actualizar el estado del pedido (`EN_RUTA`, `ENTREGADO`, `FALLIDO` para una incidencia o `CANCELADO`). El avance MUST conservarse tras reiniciar la API.

#### Scenario: Entregar un pedido

- **WHEN** la persona conductora marca `EN_RUTA` y luego `ENTREGADO` en una parada de su ruta
- **THEN** el sistema responde 200 con la parada `ENTREGADO`, el pedido queda `ENTREGADO` y la ruta cuenta una entrega más

#### Scenario: Transición no permitida

- **WHEN** se intenta pasar de `PENDIENTE` a `ENTREGADO`, o modificar una parada final, o elegir `REPROGRAMADO`
- **THEN** el sistema responde 422 indicando los estados permitidos y no registra ningún evento

#### Scenario: Parada de otra ruta

- **WHEN** la persona conductora intenta cambiar el estado de una parada de un vehículo que no le fue asignado
- **THEN** el sistema responde 404 y no registra ningún evento

### Requirement: Reportar una incidencia

El sistema MUST exigir una descripción de al menos 5 caracteres para registrar una incidencia. La incidencia MUST quedar visible para Planificación con su descripción, vehículo, conductor y hora, y MUST NOT ocultarse ni alterar silenciosamente el plan.

#### Scenario: Incidencia sin descripción

- **WHEN** la persona conductora reporta una incidencia sin descripción suficiente
- **THEN** el sistema responde 422 con el error en el campo `nota`

#### Scenario: Incidencia visible para Planificación

- **WHEN** la persona conductora reporta una incidencia con descripción
- **THEN** el seguimiento de Planificación la lista como incidencia abierta con su descripción

### Requirement: Asignar conductores y seguir el avance

El sistema SHALL permitir a `PLANIFICADOR` y `ADMIN` asignar a un vehículo con ruta guardada una persona con rol `CONDUCTOR` activa, y consultar el seguimiento de la fecha con el avance por ruta, las incidencias abiertas y los conductores disponibles. El sistema MUST rechazar con 422 la asignación a un usuario sin rol `CONDUCTOR` o a un vehículo sin ruta guardada en la fecha.

#### Scenario: Asignar un conductor

- **WHEN** Planificación asigna un conductor activo a un vehículo con ruta guardada
- **THEN** el sistema responde 204 y el conductor ve esa ruta en su vista

#### Scenario: Asignación inválida

- **WHEN** se asigna un usuario que no es conductor o un vehículo sin ruta guardada
- **THEN** el sistema responde 422 con el campo a corregir

### Requirement: Reprogramar y reoptimizar tras una incidencia

El sistema MUST permitir a Planificación reprogramar solo una parada con incidencia: la parada pasa a `REPROGRAMADO`, el pedido vuelve a `PENDIENTE` para planificarlo de nuevo y el historial conserva `INCIDENCIA` y `REPROGRAMADO`. El sistema SHALL permitir reordenar las paradas aún no atendidas de cada ruta desde la última entrega (o el depósito) sin mover las paradas entregadas, canceladas, reprogramadas ni con incidencia, recalculando sus llegadas estimadas. La operación MUST ser idempotente: si el orden ya es el más corto, no cambia nada.

#### Scenario: Reprogramar una incidencia

- **WHEN** Planificación reprograma una parada con incidencia
- **THEN** el sistema responde 204, el pedido queda `PENDIENTE` y el historial muestra `EN_RUTA`, `INCIDENCIA` y `REPROGRAMADO`

#### Scenario: Reprogramar sin incidencia

- **WHEN** Planificación intenta reprogramar una parada que no tiene incidencia
- **THEN** el sistema responde 422

#### Scenario: Reoptimizar conservando lo ejecutado

- **WHEN** Planificación reoptimiza una fecha con paradas ya entregadas
- **THEN** las paradas entregadas conservan su lugar y estado, el orden de las pendientes se recalcula y repetir la operación no produce cambios
