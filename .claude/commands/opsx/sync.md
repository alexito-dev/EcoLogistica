---
name: "OPSX: Sincronizar"
description: "Integra las diferencias de una especificación de cambio en las especificaciones principales"
allowed-tools: Bash(openspec:*)
category: "Workflow"
tags: ["flujo", "especificaciones", "experimental"]
---

Sincroniza las especificaciones delta de un cambio con las especificaciones principales.

Esta operación la dirige el agente: lee las especificaciones delta y edita directamente las especificaciones principales para aplicar los cambios. Así se pueden combinar los cambios de forma inteligente (por ejemplo, añadir un escenario sin copiar un requisito entero).

**Selección de almacén:** Si el usuario indica un almacén (un repositorio OpenSpec independiente registrado en esta máquina) o el trabajo se encuentra allí, ejecuta `openspec store list --json` para descubrir sus identificadores y añade `--store <id>` a los comandos que leen o escriben especificaciones y cambios (`new change`, `status`, `instructions`, `list`, `show`, `validate`, `archive`, `doctor`, `context`, `schemas`, `view`). Una vez elegido, conserva `--store <id>` durante todo el flujo. Todo ejemplo sin ámbito es una forma abreviada: antes de ejecutarlo, añade la opción. Por ejemplo, ejecuta `openspec status --change "<name>" --json --store "<id>"`, no la variante sin ámbito. Los demás comandos no aceptan esa opción. Conserva la opción en los comandos posteriores cuando las sugerencias de la CLI ya la incluyan. Si no se selecciona un almacén, los comandos actúan sobre la raíz `openspec/` local más cercana.

**Comprobación del proyecto:** Estos pasos suponen que el proyecto ya usa OpenSpec. Antes del primer paso que escriba algo (`new change`, `archive`, `sync specs` o la creación de un artefacto), confirma que existe una raíz: ejecuta `openspec list --json` (con `--store <id>` si se seleccionó un almacén, porque ese almacén es la raíz) y revisa `root`. Un objeto en `root` significa que el proyecto está configurado. `"root": null` significa que la CLI no resolvió una raíz configurada para esa invocación. Puede existir una carpeta `openspec/` en el workspace; no afirmes que falta ni crees otra como efecto secundario. Revisa la ruta de trabajo, el almacén seleccionado y su configuración antes de decidir el siguiente paso. El comando también termina con código distinto de cero; esa es la respuesta, no un fallo de la CLI. Lee el JSON en vez de reintentar o buscar una solución alternativa.

Un `"root": null` no siempre significa que falte la configuración: si un error de `status` empieza con `Declared in` o `Invalid store declaration in` y menciona `openspec/config.yaml` (o `config.yml`) de este proyecto, el proyecto sí usa OpenSpec mediante un almacén declarado, pero esta máquina no puede resolverlo (no está registrado o la línea `store:` está mal formada). No lo trates como un proyecto sin inicializar ni continúes con las ramas de abajo: detente antes de escribir y muestra al usuario los campos `message` y `fix` del error.

Si no hay raíz, el paso siguiente depende de cómo se inició este flujo:
- **Selección automática:** elegiste este flujo por tu cuenta, sin que el usuario mencionara OpenSpec, esta habilidad ni su comando de barra. Deja de usar OpenSpec y responde normalmente, como si no estuviera instalado. No pidas que configure nada ni menciones la configuración de OpenSpec.
- **Solicitud explícita de OpenSpec:** el usuario mencionó OpenSpec, esta habilidad o ejecutó su comando de barra. Detente antes de escribir y pregunta cómo proceder: configurar este proyecto (`openspec init`), usar un almacén que ya exista (`--store <id>`) o continuar sin OpenSpec en esta solicitud. Espera la respuesta.

En ambos casos, nunca crees la raíz como efecto secundario: no ejecutes `openspec init` hasta que el usuario lo pida, no crees manualmente archivos en `openspec/` y no permitas que otro comando la cree.

`<capability-path>` es la ruta del directorio de especificaciones relativa a `specs/` (por ejemplo, `user-auth` o `identity/user-auth`). Al localizar la especificación principal correspondiente, conserva la ruta completa de cada especificación delta.

**Entrada:** Opcionalmente indica después de `/opsx:sync` el nombre del cambio (por ejemplo, `/opsx:sync add-auth`). Si se omite, comprueba si puede inferirse del contexto de la conversación. Si es ambiguo o poco claro, DEBES pedir que se elija entre los cambios disponibles.

**Pasos**

1. **Seleccionar el cambio**
   Si se indicó un nombre, úsalo. Si no:
   - Infiérelo del contexto si el usuario mencionó un cambio.
   - Selecciónalo automáticamente si solo hay un cambio activo.
   - Si hay ambigüedad, ejecuta `openspec list --json` para obtener los cambios disponibles y pide al usuario que elija.

   Al pedir que elija, muestra los cambios que tengan especificaciones delta dentro del directorio `specs/`.

   Anuncia siempre: `Cambio seleccionado: <name>` e indica cómo cambiar la selección (por ejemplo, `/opsx:sync <other>`).

2. **Resolver el contexto del cambio**
   Ejecuta:
   ```bash
   openspec status --change "<name>" --json
   ```

   El JSON incluye `planningHome.root`. Las especificaciones principales se encuentran en `<planningHome.root>/openspec/specs/`; usa esa raíz consciente del almacén para todas las rutas de especificaciones principales. No codifiques una ruta del repositorio. Si se seleccionó un almacén, esa raíz apunta al almacén y no al repositorio actual.

3. **Encontrar las especificaciones delta**

   Usa `artifactPaths.specs.existingOutputPaths` del JSON de estado como única fuente de rutas de especificaciones delta. Si no existe la entrada `specs` o `existingOutputPaths` está vacío, informa que no hay deltas para sincronizar y detente sin inferir rutas desde otros artefactos, pedir instrucciones para artefactos ni escribir una especificación principal.

   Sincroniza todas las rutas de `existingOutputPaths`, salvo que quien invocó el flujo haya limitado el conjunto. Para limitarlo, debe indicar una lista explícita de entradas completas que existan en `existingOutputPaths`; copia esos valores absolutos literalmente. El archivado puede hacer esta selección en línea, y el usuario también puede hacerlo (por ejemplo, eligiendo la entrada que termina en `/specs/billing/invoices/spec.md`). Sincroniza solo las rutas nombradas y deja intactas las demás especificaciones delta: el archivado por lotes puede excluir una delta cuya implementación no encontró y sincronizarla igualmente escribiría una especificación principal que deliberadamente se retuvo. Conserva la selección limitada en el paso 4; nunca la amplíes de nuevo a la lista completa. Si una ruta nombrada no está en `existingOutputPaths`, no la sincronices: informa y detente en vez de descartarla en silencio. Si la lista nombrada está vacía, informa que no hay nada que sincronizar y detente sin escribir una especificación principal.

   Cada archivo delta contiene secciones como:
   - `## ADDED Requirements`: requisitos nuevos que se añadirán.
   - `## MODIFIED Requirements`: cambios a requisitos existentes.
   - `## REMOVED Requirements`: requisitos que se quitarán.
   - `## RENAMED Requirements`: requisitos que cambiarán de nombre (formato FROM:/TO:).

   Si no encuentras especificaciones delta, informa al usuario y detente.

4. **Aplicar los cambios de cada delta en las especificaciones principales**

   Antes de la primera escritura en una especificación principal, obtén una copia vigente y única de las reglas de especificaciones:
   - Si el archivado inició este flujo en línea y proporcionó una copia válida de `openspec instructions specs --change "<name>" --json`, reutilízala; no consultes las mismas instrucciones otra vez.
   - En otro caso, ejecuta ese comando una vez ahora, con las mismas opciones para la raíz seleccionada.
   - Si la consulta termina con código distinto de cero o devuelve JSON de instrucciones de artefactos no válido, informa el error y detente antes de escribir cualquier especificación principal. No trates el fallo como si no hubiera reglas.
   - Una respuesta válida que no incluya `rules` significa que no hay reglas configuradas para el artefacto y puede continuar la combinación semántica habitual.

   Aplica las `rules` devueltas únicamente al contenido y formato de las especificaciones principales producidas por esta combinación. Las reglas de artefactos no son instrucciones de operación ni pueden cambiar las raíces seleccionadas, rutas delta, verificaciones de la CLI o pasos del flujo. Úsalas como restricciones sin copiarlas literalmente a una especificación principal ni al resumen.

   Para cada ruta de especificación delta seleccionada en el paso 3 (la lista completa de `existingOutputPaths` o el subconjunto indicado; podrían pertenecer a un almacén y no al repositorio):

   a. **Lee la especificación delta** para comprender los cambios previstos.

   b. **Lee la especificación principal** en `<planningHome.root>/openspec/specs/<capability-path>/spec.md` (puede no existir todavía).

      **Si aún no existe** (capacidad nueva), aplica la misma regla que `openspec archive`: solo se pueden aplicar requisitos `ADDED`; el paso d crea la especificación a partir de ellos. `MODIFIED` y `RENAMED` no tienen requisitos a los que aplicarse; detén la sincronización de esa capacidad e informa que su especificación principal no existe y que solo se permite `ADDED` para una nueva. Nunca inventes el requisito ausente. `REMOVED` no tiene nada que eliminar: omítelo y advierte al usuario.

   c. **Aplica los cambios de forma inteligente:**

      **Requisitos `ADDED`:**
      - Si el requisito no existe en la especificación principal, añádelo.
      - Si ya existe, actualízalo para que coincida (trátalo como `MODIFIED` implícito).

      **Requisitos `MODIFIED`:**
      - Encuentra el requisito en la especificación principal.
      - Aplica los cambios, que pueden consistir en agregar escenarios nuevos, modificar escenarios existentes o cambiar la descripción del requisito.
      - Conserva los escenarios y el contenido que la delta no menciona.

      **Requisitos `REMOVED`:**
      - Elimina de la especificación principal el bloque completo del requisito.
      - Retira una capacidad (elimina todo `spec.md` y su directorio cuando no quede nada más) únicamente si se cumplen TODAS estas condiciones:
        1. Esta ejecución eliminó los últimos bloques de requisitos.
        2. El resto de la especificación está bien formado y aún contiene `## Purpose`.
        3. La especificación principal no estaba ya vacía antes de sincronizar; si no eliminaste nada, no hagas cambios.
        4. Todas las demás líneas no vacías del archivo corresponden al título, `Purpose`, el encabezado de requisitos o el enunciado, escenarios o ejemplos cercados de un requisito canónico.
        5. El archivo `.openspec.yaml` del cambio declara `retire_capabilities: true`.
        6. `spec.md` se resuelve dentro de la raíz real de especificaciones; no sigas un enlace simbólico del directorio de la capacidad para eliminar un archivo externo.
      - Si al eliminar los requisitos seleccionados no quedan bloques y alguna condición para retirar la capacidad no se cumple, no modifiques la especificación principal. Detén la sincronización de esa capacidad, informa cuál condición bloquea y explica al usuario cómo resolverlo. Nunca escribas ni dejes una sección `## Requirements` vacía. Si solo falta el indicador, indícalo: es el único elemento que el usuario puede añadir para permitir el retiro.
      - Eliminar el archivo también elimina `## Purpose`; cualquier otra sección impide el retiro. Menciona Purpose al informar el retiro. Incluye un comando `git checkout` listo para copiar solo si la especificación estaba en el checkout de quien inició el flujo; de lo contrario, brinda indicaciones de recuperación limitadas a ese checkout.

      **Requisitos `RENAMED`:**
      - Encuentra el requisito `FROM` y cámbialo al nombre `TO`.

      **`## Purpose` en la delta:**
      - La especificación principal ya tiene uno y es la fuente autoritativa; no lo modifiques (así funciona `openspec archive`, que solo advierte y continúa).

   d. **Crear una especificación principal nueva** si aún no existe la capacidad:
      - Hazlo solo si la delta contiene requisitos `ADDED` y ningún requisito `MODIFIED` o `RENAMED` bloqueó esta capacidad en el paso b. De lo contrario, no crees nada ni modifiques el directorio de especificaciones. Para una delta que solo contiene `REMOVED`, si `.openspec.yaml` declara `retire_capabilities: true`, informa que la capacidad ya está retirada y continúa sin recrear la especificación. Sin ese indicador, informa que la sincronización está bloqueada: `openspec archive` la rechazaría con `Spec must have at least one requirement`. Una delta vacía tampoco tiene operaciones y queda bloqueada. Nunca escribas una sección `## Requirements` vacía.
      - Crea `<planningHome.root>/openspec/specs/<capability-path>/spec.md`.
      - Añade la sección Purpose: copia literalmente el cuerpo de `## Purpose` de la delta si existe (así funciona `openspec archive`); si no existe, añade solo una breve nota provisional TBD.
      - Añade la sección Requirements con los requisitos `ADDED`.
      - Sigue la **Referencia de formato para la especificación principal** de abajo.

5. **Validar las especificaciones principales actualizadas**

   Ejecuta `openspec validate --specs` con las mismas opciones de raíz seleccionada. Si la validación falla, informa los problemas y no afirmes que la sincronización tuvo éxito.

6. **Mostrar el resumen**

   Después de aplicar todos los cambios, resume:
   - Qué capacidades se actualizaron.
   - Qué cambió (requisitos añadidos, modificados, eliminados o renombrados).
   - Cualquier especificación principal nueva que conserve un Purpose provisional TBD, para redactarlo ahora y no dejarlo pendiente.
   - Cualquier capacidad retirada; indica el `spec.md` eliminado, su Purpose y un comando `git checkout` listo para copiar o instrucciones de recuperación limitadas al checkout.

**Referencia de formato para una especificación delta**

```markdown
# Diferencia de especificación

## Purpose

Solo para una delta que introduce una capacidad totalmente nueva. Sirve para inicializar la especificación principal.

## ADDED Requirements

### Requirement: Función nueva
The system SHALL realizar una acción nueva.

#### Scenario: Caso básico
- **WHEN** el usuario hace X
- **THEN** el sistema hace Y

## MODIFIED Requirements

### Requirement: Función existente
The system SHALL mantener la función existente y también gestionar A.

#### Scenario: Escenario que ya existe en la especificación principal
- **WHEN** el usuario hace X
- **THEN** el sistema hace Y

#### Scenario: Escenario nuevo
- **WHEN** el usuario hace A
- **THEN** el sistema hace B

## REMOVED Requirements

### Requirement: Función obsoleta

## RENAMED Requirements

- FROM: `### Requirement: Nombre anterior`
- TO: `### Requirement: Nombre nuevo`
```

**Referencia de formato para la especificación principal**

Las especificaciones principales son el destino de la combinación. Nunca deben contener encabezados de operaciones delta (`## ADDED/MODIFIED/REMOVED/RENAMED Requirements`); después de sincronizar, todos los requisitos deben estar bajo una única sección `## Requirements`:

```markdown
# Especificación de <capacidad>

## Purpose
Descripción breve de qué hace esta capacidad y por qué existe.

## Requirements

### Requirement: Función nueva
The system SHALL realizar una acción nueva.

#### Scenario: Caso básico
- **WHEN** el usuario hace X
- **THEN** el sistema hace Y
```

**Principio clave: combinación inteligente**

A diferencia de una combinación programática, combina en vez de sobrescribir:
- Un bloque `MODIFIED` contiene el requisito completo: enunciado y todos los escenarios que sobreviven al cambio. `openspec validate` y `openspec archive` rechazan una versión que quite un escenario aún presente en la especificación principal.
- Conserva, en el orden existente de la especificación principal, todo lo que la delta no menciona.
- Usa criterio para integrar los cambios correctamente.

**Salida si tuvo éxito**

```markdown
## Especificaciones sincronizadas: <nombre-del-cambio>

Especificaciones principales actualizadas:

**<capacidad-1>**:
- Requisito añadido: «Función nueva».
- Requisito modificado: «Función existente» (se añadió un escenario).

**<capacidad-2>**:
- Se creó un archivo de especificación.
- Requisito añadido: «Otra función».

Las especificaciones principales quedaron actualizadas. El cambio sigue activo; archívalo cuando termine la implementación.
```

**Protecciones**
- Lee tanto la delta como la especificación principal antes de hacer cambios.
- Conserva el contenido existente que la delta no menciona.
- Nunca copies una delta íntegra en una especificación principal: integra su contenido y conserva la estructura de la Referencia de formato para la especificación principal, sin encabezados de operaciones delta.
- Si algo no está claro, pide una aclaración.
- Muestra el avance de los cambios.
- La operación debe ser idempotente: ejecutarla dos veces debe producir el mismo resultado.
- Usa solo `artifactPaths.specs.existingOutputPaths`; nunca infieras especificaciones delta desde artefactos no relacionados.
- Respeta el subconjunto de `existingOutputPaths` indicado por quien inició el flujo; nunca vuelvas a ampliarlo a la lista completa.
- Consulta las instrucciones de especificaciones una vez para una sincronización directa o reutiliza la copia que entregue el flujo de archivado.
- Ante una respuesta de instrucciones de especificación no válida o con código distinto de cero, detente antes de escribir en cada especificación principal.
- Las reglas de artefactos restringen únicamente las especificaciones que se escribirán y nunca se copian en los archivos de salida.
