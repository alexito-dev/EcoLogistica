---
name: openspec-archive-change
description: Archiva un cambio OpenSpec despu?s de que su implementaci?n est? completa.
allowed-tools: Bash(openspec:*)
license: MIT
compatibility: Requiere la CLI de OpenSpec.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.13.2"
---

Archiva un cambio completado en el flujo experimental.

**Selección de almacén:** Si el usuario indica un almacén (un repositorio OpenSpec independiente registrado en esta máquina) o el trabajo se encuentra allí, ejecuta `openspec store list --json` para descubrir sus identificadores y añade `--store <id>` a los comandos que leen o escriben especificaciones y cambios (`new change`, `status`, `instructions`, `list`, `show`, `validate`, `archive`, `doctor`, `context`, `schemas`, `view`). Una vez elegido, conserva `--store <id>` durante todo el flujo. Todo ejemplo sin ámbito es una forma abreviada: antes de ejecutarlo, añade la opción. Por ejemplo, ejecuta `openspec status --change "<name>" --json --store "<id>"`, no la variante sin ámbito. Los demás comandos no aceptan esa opción. Conserva la opción en los comandos posteriores cuando las sugerencias de la CLI ya la incluyan. Si no se selecciona un almacén, los comandos actúan sobre la raíz `openspec/` local más cercana.

**Comprobación del proyecto:** Estos pasos suponen que el proyecto ya usa OpenSpec. Antes del primer paso que escriba algo (`new change`, `archive`, `sync specs` o la creación de un artefacto), confirma que existe una raíz: ejecuta `openspec list --json` (con `--store <id>` si se seleccionó un almacén, porque ese almacén es la raíz) y revisa `root`. Un objeto en `root` significa que el proyecto está configurado. `"root": null` significa que la CLI no resolvió una raíz configurada para esa invocación. Puede existir una carpeta `openspec/` en el workspace; no afirmes que falta ni crees otra como efecto secundario. Revisa la ruta de trabajo, el almacén seleccionado y su configuración antes de decidir el siguiente paso. El comando también termina con código distinto de cero; esa es la respuesta, no un fallo de la CLI. Lee el JSON en vez de reintentar o buscar una solución alternativa.

Un `"root": null` no siempre significa que falte la configuración: si un error de `status` empieza con `Declared in` o `Invalid store declaration in` y menciona `openspec/config.yaml` (o `config.yml`) de este proyecto, el proyecto sí usa OpenSpec mediante un almacén declarado, pero esta máquina no puede resolverlo (no está registrado o la línea `store:` está mal formada). No lo trates como un proyecto sin inicializar: detente antes de escribir y muestra al usuario los campos `message` y `fix` del error.

Si no hay raíz, el paso siguiente depende de cómo se inició este flujo:
- **Selección automática:** elegiste este flujo por tu cuenta, sin que el usuario mencionara OpenSpec, esta habilidad ni su comando de barra. Deja de usar OpenSpec y responde normalmente, como si no estuviera instalado. No pidas que configure nada ni menciones la configuración de OpenSpec.
- **Solicitud explícita de OpenSpec:** el usuario mencionó OpenSpec, esta habilidad o ejecutó su comando de barra. Detente antes de escribir y pregunta cómo proceder: configurar este proyecto (`openspec init`), usar un almacén que ya exista (`--store <id>`) o continuar sin OpenSpec en esta solicitud. Espera la respuesta.

En ambos casos, nunca crees la raíz como efecto secundario: no ejecutes `openspec init` hasta que el usuario lo pida, no crees manualmente archivos en `openspec/` y no permitas que otro comando la cree.

`<capability-path>` es la ruta del directorio de especificaciones relativa a `specs/` (por ejemplo, `user-auth` o `identity/user-auth`). Al localizar la especificación principal correspondiente, conserva la ruta completa de cada especificación delta.

**Entrada:** Opcionalmente indica después de `/opsx:archive` el nombre del cambio (por ejemplo, `/opsx:archive add-auth`). Si se omite, comprueba si puede inferirse del contexto de la conversación. Si es ambiguo o poco claro, DEBES pedir que se elija entre los cambios disponibles.

**Pasos**

1. **Seleccionar el cambio**

   Si se indicó un nombre, úsalo. Si no:
   - Infiérelo del contexto si el usuario mencionó un cambio.
   - Selecciónalo automáticamente si solo hay un cambio activo.
   - Si hay ambigüedad, ejecuta `openspec list --json` para obtener los cambios disponibles y pide al usuario que elija.

   Al pedir que elija, muestra solo los cambios activos (no archivados) e indica el esquema utilizado cuando esté disponible.

   Anuncia siempre: `Cambio seleccionado: <name>` e indica cómo cambiar la selección (por ejemplo, `/opsx:archive <other>`).

   **Cargar entradas actuales de archivado antes de las comprobaciones existentes:**

   Después de resolver el cambio y la raíz de planificación, ejecuta:
   ```bash
   openspec instructions archive --change "<name>" --json
   ```

   Conserva las opciones de raíz seleccionada en este comando. Esta consulta es complementaria y opcional; solo aporta contexto adicional al prompt y nunca debe impedir el archivado. Si termina con código distinto de cero o devuelve JSON no válido (por ejemplo, en una versión antigua de la CLI que no admite el comando), continúa el flujo de archivado sin contexto ni recomendaciones de operación. No informes el error ni te detengas.

   Una respuesta válida puede omitir ambos campos opcionales. Trata `context` como una entrada obligatoria del prompt: léelo, considéralo y aplica los datos, convenciones y restricciones pertinentes del proyecto. Trata `operationGuidance` como consejo adicional opcional: lee y considera cada entrada, y sigue las que sean aplicables y compatibles con el flujo de archivado integrado.

   Mantén ambos campos separados de los pasos integrados, elecciones explícitas del usuario, rutas resueltas, verificaciones de la CLI y contratos de comando. Si `context` entra en conflicto con una entrada que controla el flujo, informa el conflicto y conserva el valor que prevalece. Si una recomendación no es aplicable o entra en conflicto con una entrada que controla el flujo, no la sigas y explica por qué. No infieras rutas sustitutas, prompts omitidos ni opciones de esos campos; no copies su texto literalmente a especificaciones, artefactos de cambio ni resúmenes de archivado, salvo que el usuario lo solicite por separado. Estos contratos guían el comportamiento del prompt, pero no son validaciones ejecutables.

2. **Comprobar el estado de finalización de los artefactos**

   Ejecuta `openspec status --change "<name>" --json` para comprobar la finalización.

   Interpreta el JSON para conocer:
   - `schemaName`: esquema de flujo utilizado.
   - `planningHome`, `changeRoot`, `artifactPaths` y `actionContext`: rutas y alcance.
   - `artifacts`: artefactos y sus estados (`done`, `skipped` u otro).

   Si algún artefacto no está `done` ni `skipped` (los omitidos satisfacen el requisito porque el cambio declara `skip_specs`):
   - Muestra una advertencia con la lista de artefactos incompletos.
   - Pide al usuario que confirme si desea continuar.
   - Continúa si confirma.

3. **Comprobar el estado de finalización de las tareas**

   Ejecuta `openspec list --json` con las mismas opciones de raíz seleccionada y encuentra en `changes` la entrada cuyo `name` coincida exactamente con el cambio seleccionado. Exige exactamente una coincidencia y valores enteros no negativos para `totalTasks` y `completedTasks`, con `completedTasks <= totalTasks`. La CLI resuelve los archivos de tareas que registra el esquema, incluidos nombres de artefactos personalizados, rutas de salida y patrones glob. Las tareas pendientes son `totalTasks - completedTasks`.

   No infieras que las tareas terminaron por el estado de los artefactos ni porque falte un `tasks.md` en el nivel superior. Si la consulta falla, devuelve JSON no válido, omite o duplica el cambio seleccionado, o entrega conteos inválidos, informa el problema y detente antes de sincronizar o archivar. La CLI cuenta solo las casillas `x`/`X` como completas; otros marcadores, incluidos los desconocidos, siguen pendientes.

   Si hay tareas pendientes:
   - Muestra una advertencia con su cantidad.
   - Pide al usuario que confirme si desea continuar.
   - Continúa si confirma.

   Si `totalTasks` es cero, continúa sin advertencia sobre tareas.

4. **Evaluar la sincronización de las especificaciones delta**

   Usa `artifactPaths.specs.existingOutputPaths` del JSON de estado como única fuente de rutas delta. Si falta la entrada `specs` o `existingOutputPaths` está vacío, continúa sin pedir sincronización y no infieras rutas de otros artefactos.

   **Si existen deltas:**
   - Compara cada delta con su especificación principal correspondiente en `<planningHome.root>/openspec/specs/<capability-path>/spec.md`. Usa `planningHome.root` consciente del almacén, indicado en el paso 2; no codifiques la ruta del repositorio.
   - Que falte una especificación principal **no significa automáticamente** que ya esté sincronizada. Para una capacidad nueva, la especificación principal es un *resultado* de la sincronización, no una entrada:
     - Si la delta tiene requisitos `MODIFIED` o `RENAMED`, informa que una especificación nueva solo puede crearse con requisitos `ADDED` y marca esa capacidad como bloqueada para sincronizar. Nunca inventes el requisito cuya versión vigente falta.
     - En otro caso, si la delta solo tiene requisitos `REMOVED` y el `.openspec.yaml` del cambio declara `retire_capabilities: true`, la capacidad ya está retirada: cuéntala como sincronizada, advierte que no queda nada que quitar y no recrees su especificación principal. Aplica esta regla ahora y al verificar una sincronización completada.
     - En otro caso, si la delta no tiene requisitos `ADDED`, informa que no se puede sincronizar y marca la capacidad como bloqueada. Para una delta que solo contiene `REMOVED`, advierte que no hay especificación principal de la cual eliminar requisitos y deja sin cambios el árbol principal. `openspec archive` rechaza el caso sin marca con `Spec must have at least one requirement`.
     - En los demás casos, cuenta la capacidad como pendiente de sincronizar e indícala en el resumen (`<capability-path>: se creará una especificación principal nueva`). Si la delta también tiene requisitos `REMOVED`, advierte que se ignorarán porque no hay especificación principal. La sincronización crea la especificación a partir únicamente de los requisitos `ADDED`, igual que `openspec archive`.
   - Determina qué cambios se aplicarían (adiciones, modificaciones, eliminaciones y renombres).
   - Continúa evaluando las demás capacidades aunque una esté bloqueada para sincronización. Muestra un resumen combinado antes de preguntar.

   **Opciones para el usuario:**
   - Si alguna capacidad está bloqueada para sincronizar: explica el motivo y ofrece solo «Archivar sin sincronizar» o «Cancelar».
   - Si no hay bloqueos y quedan cambios por aplicar: ofrece «Sincronizar ahora (recomendado)» o «Archivar sin sincronizar».
   - Si ya está sincronizado: ofrece «Archivar ahora», «Sincronizar de nuevo» o «Cancelar».

   Sigue la respuesta:
   - «Cancelar»: detente; no archives.
   - «Archivar sin sincronizar» o «Archivar ahora»: continúa con el archivado.
   - «Sincronizar ahora» o «Sincronizar de nuevo»: sincroniza y verifica (más abajo). No empieces si alguna capacidad está bloqueada; explica el impedimento y vuelve a ofrecer las opciones disponibles.
   - Cualquier otra respuesta: vuelve a preguntar en vez de archivar.

   Antes de escribir en cualquier especificación principal, ejecuta una vez `openspec instructions specs --change "<name>" --json` con las mismas opciones de raíz seleccionada. Exige código de salida cero y JSON de instrucciones de artefacto válido. Si la consulta falla o devuelve JSON no válido, informa el error y detente antes de escribir una especificación principal o mover el cambio. Una respuesta válida que no incluya `rules` significa que no hay reglas configuradas. Aplica las `rules` solo al contenido y formato de las especificaciones principales producidas por esta combinación; no las uses como orientación para archivar, cambiar el comportamiento de la CLI ni copies su texto a archivos de salida.

   Luego ejecuta en línea el flujo `/opsx:sync` para el cambio `<name>` (combinación inteligente dirigida por el agente), proporcionando el análisis de las especificaciones delta y la copia de reglas obtenida arriba, y espera a que termine. La sincronización en línea debe reutilizar esa copia sin volver a consultar las instrucciones `specs`. No la delegues a una tarea en segundo plano: el paso 5 movería `changeRoot` mientras la sincronización aún lo lee, con lo que el cambio quedaría archivado sin actualizar las especificaciones principales. Si tu agente solo puede ejecutarla mediante delegación, delega de forma síncrona y espera el resultado.

   Después vuelve a ejecutar la comparación desde el inicio de este paso, incluido el caso de capacidad retirada explícitamente, para **todas** las capacidades con delta en `artifactPaths.specs.existingOutputPaths`, no solo las que la sincronización diga haber tocado. Una sincronización correcta no deja cambios por aplicar; cada capacidad debe aparecer sincronizada:
   - Requisitos `ADDED` presentes.
   - Requisitos `MODIFIED` con los cambios de escenario y descripción indicados, y conservando los demás escenarios.
   - Requisitos `REMOVED` ausentes; si la sincronización retiró una capacidad al eliminar su último requisito y dejar vacía `## Requirements`, también debe haber eliminado su especificación principal en vez de dejarla vacía. Una especificación que la sincronización conservó intencionalmente y explicó también cuenta como coincidencia.
   - Requisitos `RENAMED` presentes con el nombre nuevo y ausentes con el antiguo.

   Si la sincronización falla o alguna capacidad no coincide, informa qué difiere y detente: no archives. Nada se ha movido y `changeRoot` sigue intacto, así que el usuario puede corregirlo o volver a iniciar el archivado.

5. **Realizar el archivado**

   Crea el directorio `archive` dentro de `planningHome.changesDir` si aún no existe:
   ```bash
   mkdir -p "<planningHome.changesDir>/archive"
   ```

   Genera el nombre de destino: conserva el nombre del cambio si ya empieza con el prefijo `YYYY-MM-DD-`; si no, antepón la fecha actual con el formato `YYYY-MM-DD-<change-name>`. Nunca agregues una segunda fecha (misma regla que `openspec archive`).

   **Comprueba si ya existe el destino:**
   - Si existe, informa el error y sugiere renombrar el archivo existente o usar otra fecha.
   - Si no existe, mueve `changeRoot` al directorio de archivo.

   ```bash
   mv "<changeRoot>" "<planningHome.changesDir>/archive/<target-name>"
   ```

6. **Mostrar el resumen**

   Muestra un resumen de finalización con:
   - Nombre del cambio.
   - Esquema utilizado.
   - Ubicación del archivo.
   - Estado de sincronización (sincronizado, omitido o sin especificaciones delta).
   - Advertencias sobre artefactos o tareas incompletos.

**Salida cuando termina correctamente**

```markdown
## Archivado completado

**Cambio:** <nombre-del-cambio>
**Esquema:** <nombre-del-esquema>
**Archivado en:** ruta de archivo derivada de `planningHome.changesDir`/<target-name>/
**Especificaciones:** ✓ Sincronizadas con las especificaciones principales

Todos los artefactos y tareas están completos.
```

**Salida correcta sin especificaciones delta**

```markdown
## Archivado completado

**Cambio:** <nombre-del-cambio>
**Esquema:** <nombre-del-esquema>
**Archivado en:** ruta de archivo derivada de `planningHome.changesDir`/<target-name>/
**Especificaciones:** No hay especificaciones delta

Todos los artefactos y tareas están completos.
```

**Salida correcta con advertencias**

```markdown
## Archivado completado (con advertencias)

**Cambio:** <nombre-del-cambio>
**Esquema:** <nombre-del-esquema>
**Archivado en:** ruta de archivo derivada de `planningHome.changesDir`/<target-name>/
**Especificaciones:** Sincronización omitida (el usuario eligió omitirla)

**Advertencias:**
- Se archivó con 2 artefactos incompletos.
- Se archivó con 3 tareas incompletas.
- Se omitió la sincronización de especificaciones delta (el usuario lo eligió).

Revisa el archivo si esto no era intencional.
```

**Salida cuando el destino ya existe**

```markdown
## Error al archivar

**Cambio:** <nombre-del-cambio>
**Destino:** ruta de archivo derivada de `planningHome.changesDir`/<target-name>/

El directorio de destino ya existe.

**Opciones:**
1. Renombrar el archivo existente.
2. Eliminarlo si es un duplicado.
3. Esperar a otra fecha para archivar.
```

**Protecciones**
- Anuncia el cambio seleccionado y pide que lo elijan si es ambiguo.
- Usa el grafo de artefactos (`openspec status --json`) para comprobar la finalización.
- No bloquees el archivado por advertencias: informa y pide confirmación.
- Conserva `.openspec.yaml` al mover el cambio (se mueve junto con el directorio).
- Muestra un resumen claro de lo ocurrido.
- Si se solicitó sincronizar, ejecuta `/opsx:sync` en línea (dirigido por el agente).
- Nunca archives mientras una sincronización sigue en curso: ejecútala en línea y verifica las especificaciones principales antes de mover `changeRoot`.
- Si hay especificaciones delta, evalúa siempre la sincronización y muestra el resumen combinado antes de preguntar.
- Aplica el contexto de ejecución pertinente e informa conflictos; las recomendaciones de operación son orientativas.
- Considera todas las recomendaciones y explica las que no sean aplicables o entren en conflicto.
- No cambies las verificaciones existentes de la CLI, rutas resueltas, preguntas ni contratos de comandos.
- Las reglas de artefactos restringen solo las especificaciones que se escriben y nunca son instrucciones de operación.
- Nunca copies literalmente el contexto de ejecución, las recomendaciones de operación ni reglas de artefactos a archivos de salida.
