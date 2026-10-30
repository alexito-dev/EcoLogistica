## ADDED Requirements

### Requirement: Consultar indicadores de operación y sostenibilidad

El sistema SHALL permitir a una persona con rol `PLANIFICADOR`, `ADMIN` o `GERENTE` consultar los indicadores de una fecha de reparto. La respuesta MUST incluir: el total de pedidos registrados y su peso; su distribución por estado, por distrito (con peso) y por prioridad; la flota total, la cantidad apta para la fecha, su capacidad en kg y su distribución por combustible. La fecha MUST ser obligatoria y válida; los demás roles MUST recibir 403.

#### Scenario: Gerencia consulta los indicadores

- **WHEN** una persona `GERENTE` consulta los indicadores de una fecha con pedidos y vehículos con turno
- **THEN** el sistema responde 200 con los conteos de pedidos y de flota de esa fecha

#### Scenario: Roles sin permiso

- **WHEN** una persona `CONDUCTOR` o `AUDITOR` consulta los indicadores
- **THEN** el sistema responde 403 y no expone datos

#### Scenario: Fecha obligatoria

- **WHEN** se consultan los indicadores sin fecha
- **THEN** el sistema responde 400 con el formato común de error

### Requirement: Indicadores de la planificación del día

Para la fecha consultada, la respuesta MUST incluir, según la vista previa de rutas: pedidos planificables y asignados, demanda en kg, uso de la capacidad apta, distancia y CO₂e de la propuesta y del despacho sin optimizar, ahorro porcentual de CO₂e y porcentaje de paradas dentro de su ventana. Cuando no hay pedidos o capacidad, los porcentajes MUST ser cero.

#### Scenario: Día con operación

- **WHEN** la fecha tiene pedidos que caben en la flota apta
- **THEN** todos se informan como asignados, el uso de capacidad está entre 0 y 100 %, el CO₂e propuesto es menor que el sin optimizar y la puntualidad es la de la propuesta

#### Scenario: Día sin operación

- **WHEN** la fecha no tiene pedidos planificables
- **THEN** todos los indicadores del día se informan en cero

### Requirement: Dashboard de indicadores en la interfaz

La interfaz SHALL ofrecer una página Indicadores con selector de fecha, cuatro indicadores clave (ahorro de CO₂e, puntualidad, uso de capacidad y pedidos asignados) y gráficos de barras de emisiones (propuesta frente a sin optimizar), pedidos por estado, por distrito y por prioridad, y flota por combustible. Cada barra MUST presentar su etiqueta y valor como texto. Los estados sin pedidos no MUST ocupar filas. Si la fecha no tiene pedidos, MUST indicarlo.

#### Scenario: Ver el dashboard

- **WHEN** una persona autorizada abre Indicadores
- **THEN** ve los cuatro indicadores clave y los gráficos con sus valores en texto

#### Scenario: Fecha sin pedidos en el dashboard

- **WHEN** la fecha elegida no tiene pedidos planificables
- **THEN** la página indica que no hay pedidos planificables en esa fecha

### Requirement: Menú de vistas por rol

La interfaz MUST mostrar a cada rol solo las vistas que puede abrir: `PLANIFICADOR` y `ADMIN` ven Pedidos, Flota, Rutas e Indicadores; `GERENTE` ve solo Indicadores. Al iniciar sesión, la interfaz MUST abrir la primera vista permitida del rol y nunca MUST renderizar una vista ajena a él.

#### Scenario: Gerencia entra al dashboard

- **WHEN** una persona `GERENTE` inicia sesión
- **THEN** la interfaz abre Indicadores y el menú no ofrece Pedidos, Flota ni Rutas
