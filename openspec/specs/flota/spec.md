# flota Specification

## Purpose

Permite a Administraci?n mantener el cat?logo de veh?culos y a Planificaci?n declarar su disponibilidad por fecha, consultar sus turnos y saber cu?les pueden considerarse para generar rutas (HU-003, HU-009, RNF-05).

## Requirements

### Requirement: Administrar el cat?logo de veh?culos

El sistema SHALL permitir a una persona con rol `ADMIN` registrar y actualizar veh?culos con placa, tipo, capacidades en kilogramos y metros c?bicos, combustible, consumo base, estado y, opcionalmente, a?o y factor de emisi?n. La placa MUST normalizarse quitando espacios externos y convirti?ndose a may?sculas; MUST ser ?nica. Una persona con rol `ADMIN` o `PLANIFICADOR` SHALL poder consultar la lista y el detalle de veh?culos. Toda operaci?n SHALL requerir sesi?n autenticada y el sistema MUST denegar los roles no autorizados.

#### Scenario: Registrar y consultar veh?culo

- **WHEN** una persona `ADMIN` registra un veh?culo con datos v?lidos
- **THEN** el sistema responde 201 con el veh?culo y permite consultarlo en la lista y su detalle

#### Scenario: Normalizar placa

- **WHEN** se registra o actualiza una placa con espacios externos o letras min?sculas
- **THEN** el sistema la guarda sin espacios externos y en may?sculas

#### Scenario: Rechazar placa duplicada

- **WHEN** se registra o actualiza un veh?culo con una placa que ya pertenece a otro veh?culo
- **THEN** el sistema rechaza la operaci?n sin crear otro veh?culo ni modificar el existente

#### Scenario: Autorizar seg?n rol

- **WHEN** una persona sin sesi?n consulta flota o una persona con un rol distinto de `ADMIN` intenta modificar el cat?logo
- **THEN** el sistema deniega la operaci?n y no expone ni modifica datos

### Requirement: Validar datos y capacidades del veh?culo

El sistema MUST rechazar capacidades en kg o m? y consumo base no positivos, tipos fuera de los l?mites admitidos, placas con formato inv?lido, a?os fuera del rango configurado, combustibles o estados desconocidos y campos adicionales no admitidos. Si se informa un factor de emisi?n, este MUST ser positivo. Los errores MUST identificar los campos inv?lidos y no alterar los datos previamente guardados.

#### Scenario: Rechazar magnitudes no positivas

- **WHEN** se registra o actualiza un veh?culo con capacidad en kg, capacidad en m? o consumo base igual a cero o negativo
- **THEN** el sistema rechaza la operaci?n y conserva el cat?logo sin cambios

#### Scenario: Rechazar datos fuera de formato

- **WHEN** se env?an una placa inv?lida, un tipo vac?o, un combustible o estado desconocido, un a?o fuera de rango o campos extra
- **THEN** el sistema rechaza el registro e informa los campos que deben corregirse

### Requirement: Registrar disponibilidad y turno por fecha

Una persona con rol `PLANIFICADOR` SHALL poder consultar o guardar para un veh?culo una disponibilidad por fecha con hora de inicio, hora de fin, indicador de disponibilidad y, opcionalmente, una restricci?n de circulaci?n. La hora final MUST ser posterior a la hora inicial. Si el veh?culo se declara no disponible, el sistema MUST exigir el motivo. El indicador no podr? ser verdadero cuando el estado del veh?culo sea `MANTENIMIENTO` o `INACTIVO`.

#### Scenario: Guardar disponibilidad v?lida

- **WHEN** Planificaci?n registra para un veh?culo `DISPONIBLE` un turno v?lido en una fecha
- **THEN** el sistema conserva el turno y devuelve el veh?culo con esa disponibilidad

#### Scenario: Rechazar turno invertido

- **WHEN** la hora final del turno es igual o anterior a la hora de inicio
- **THEN** el sistema rechaza la operaci?n e identifica el campo de hora final

#### Scenario: Exigir motivo si no est? disponible

- **WHEN** Planificaci?n declara el veh?culo no disponible sin indicar motivo
- **THEN** el sistema rechaza la operaci?n e indica que debe explicar la restricci?n

#### Scenario: No marcar disponible un veh?culo no elegible por estado

- **WHEN** Planificaci?n intenta marcar como disponible un veh?culo en `MANTENIMIENTO` o `INACTIVO`
- **THEN** el sistema rechaza esa disponibilidad

### Requirement: Determinar elegibilidad para planificar

El sistema MUST informar `elegibleParaPlanificar` como verdadero solo cuando el veh?culo tenga estado `DISPONIBLE` y una disponibilidad activa para la fecha consultada. La ausencia de disponibilidad, una disponibilidad inactiva o los estados `MANTENIMIENTO` e `INACTIVO` MUST dar como resultado no elegible. El sistema SHALL filtrar y presentar el estado de elegibilidad en las consultas de veh?culos por fecha.

#### Scenario: Veh?culo elegible

- **WHEN** se consultan veh?culos para una fecha y uno tiene estado `DISPONIBLE` con turno activo en esa fecha
- **THEN** su respuesta incluye la disponibilidad y `elegibleParaPlanificar=true`

#### Scenario: Veh?culo sin disponibilidad o no disponible

- **WHEN** se consultan veh?culos para una fecha y uno no tiene turno activo, est? marcado no disponible o su estado es `MANTENIMIENTO` o `INACTIVO`
- **THEN** su respuesta indica `elegibleParaPlanificar=false`

### Requirement: Persistir veh?culos y disponibilidades

El sistema MUST guardar el cat?logo de veh?culos y sus disponibilidades por fecha en PostgreSQL/PostGIS mediante migraciones versionadas. Una consulta posterior, incluso despu?s de reiniciar la API, SHALL devolver los datos persistidos sin duplicar ni perder el veh?culo o su turno.

#### Scenario: Conservar datos tras reiniciar la API

- **WHEN** se registra un veh?culo y se guarda su disponibilidad, luego se reinicia la API y se consulta la misma fecha
- **THEN** el veh?culo, el turno, el estado y la elegibilidad coinciden con los datos guardados

### Requirement: Gestionar flota en la interfaz web

La interfaz SHALL ofrecer a Administraci?n el flujo de alta y edici?n del cat?logo y a Planificaci?n el flujo de disponibilidad por fecha. MUST mostrar capacidad, estado, turno y elegibilidad de forma coherente con los permisos del usuario y con los datos devueltos por la API. Los campos MUST tener etiquetas y errores comprensibles, y ser operables por teclado (RNF-10).

#### Scenario: Flujos de flota por rol

- **WHEN** una persona `ADMIN` o `PLANIFICADOR` abre la gesti?n de flota
- **THEN** la interfaz muestra solo las acciones permitidas para su rol y permite consultar los veh?culos

#### Scenario: Mostrar validaci?n de la API

- **WHEN** una persona env?a datos de flota que incumplen una regla de negocio
- **THEN** la interfaz muestra el error correspondiente y no presenta como guardado el cambio rechazado
