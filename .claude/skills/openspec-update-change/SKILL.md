---
name: openspec-update-change
description: Revisa los artefactos de planificaci?n existentes de un cambio OpenSpec y mantenlos coherentes; no edita c?digo.
allowed-tools: Bash(openspec:*)
license: MIT
compatibility: Requiere la CLI de OpenSpec.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.13.2"
---

Revisa los artefactos de planificación existentes de un cambio y mantenlos coherentes. Nunca edites código.

**Selección de almacén:** Si el usuario indica un almacén (un repositorio OpenSpec independiente registrado en esta máquina) o el trabajo se encuentra allí, ejecuta `openspec store list --json` para descubrir sus identificadores y añade `--store <id>` a los comandos que leen o escriben especificaciones y cambios (`new change`, `status`, `instructions`, `list`, `show`, `validate`, `archive`, `doctor`, `context`, `schemas`, `view`). Una vez elegido, conserva `--store <id>` durante todo el flujo. Todo ejemplo sin ámbito es una forma abreviada: antes de ejecutarlo, añade la opción. Por ejemplo, ejecuta `openspec status --change "<name>" --json --store "<id>"`, no la variante sin ámbito. Los demás comandos no aceptan esa opción. Conserva la opción en los comandos posteriores cuando las sugerencias de la CLI ya la incluyan. Si no se selecciona un almacén, los comandos actúan sobre la raíz `openspec/` local más cercana.

**Comprobación del proyecto:** Estos pasos suponen que el proyecto ya usa OpenSpec. Antes del primer paso que escriba algo (`new change`, `archive`, `sync specs` o la creación de un artefacto), confirma que existe una raíz: ejecuta `openspec list --json` (con `--store <id>` si se seleccionó un almacén, porque ese almacén es la raíz) y revisa `root`. Un objeto en `root` significa que el proyecto está configurado. `"root": null` significa que no lo está: aquí no hay un directorio `openspec/` y una escritura como `openspec new change` lo crearía como efecto secundario. El comando también termina con código distinto de cero; esa es la respuesta, no un fallo de la CLI. Lee el JSON en vez de reintentar o buscar una solución alternativa.

Un `"root": null` no siempre significa que falte la configuración: si un error de `status` empieza con `Declared in` o `Invalid store declaration in` y menciona `openspec/config.yaml` (o `config.yml`) de este proyecto, el proyecto sí usa OpenSpec mediante un almacén declarado, pero esta máquina no puede resolverlo (no está registrado o la línea `store:` está mal formada). No lo trates como un proyecto sin inicializar ni continúes con las ramas de abajo: detente antes de escribir y muestra al usuario los campos `message` y `fix` del error.

Si no hay raíz, el paso siguiente depende de cómo se inició este flujo:

- **Selección automática:** elegiste este flujo por tu cuenta, sin que el usuario mencionara OpenSpec, esta habilidad ni su comando de barra. Deja de usar OpenSpec y responde normalmente, como si no estuviera instalado. No pidas que configure nada ni menciones la configuración de OpenSpec.
- **Solicitud explícita de OpenSpec:** el usuario mencionó OpenSpec, esta habilidad o ejecutó su comando de barra. Detente antes de escribir y pregunta cómo proceder: configurar este proyecto (`openspec init`), usar un almacén que ya exista (`--store <id>`) o continuar sin OpenSpec en esta solicitud. Espera la respuesta.

En ambos casos, nunca crees la raíz como efecto secundario: no ejecutes `openspec init` hasta que el usuario lo pida, no crees manualmente archivos en `openspec/` y no permitas que otro comando la cree.

**Entrada:** Opcionalmente indica después de `/opsx:update` el nombre del cambio (por ejemplo, `/opsx:update add-auth`). Si se omite, comprueba si puede inferirse del contexto de la conversación. Si es ambiguo o poco claro, DEBES pedir al usuario que elija entre los cambios disponibles.

Este flujo revisa artefactos que ya existen; nunca crea los que falten. Si falta un artefacto, `openspec status --change "<name>" --json` indica cuál sigue y `openspec instructions "<artifact-id>" --change "<name>" --json` explica cómo escribirlo.

**Pasos**

1. **Seleccionar el cambio**

   Si se indicó un nombre, úsalo. Si no:
   - Infiérelo del contexto si el usuario mencionó un cambio.
   - Selecciónalo automáticamente si solo hay un cambio activo.
   - Si hay ambigüedad, ejecuta `openspec list --json` para obtener los cambios disponibles, ordenados por fecha de modificación más reciente, y pide al usuario que elija.

   Al pedirle que elija, presenta como opciones los 3 o 4 cambios modificados más recientemente e indica:
   - Nombre del cambio.
   - Estado (por ejemplo, `0/5 tasks`, `complete` o `no tasks`).
   - Antigüedad de la modificación, según `lastModified`.

   Marca el cambio más reciente como «(Recomendado)», porque probablemente sea el que el usuario desea actualizar.

   Anuncia siempre: `Cambio seleccionado: <name>` e indica cómo cambiar la selección (por ejemplo, `/opsx:update <other>`).

2. **Obtener los artefactos del cambio**

   ```bash
   openspec status --change "<name>" --json
   ```

   Interpreta el JSON para conocer el estado actual. La respuesta incluye:
   - `schemaName`: esquema de flujo utilizado (por ejemplo, `spec-driven`).
   - `artifacts`: lista de artefactos y sus estados (`done`, `skipped`, `ready`, `blocked`).
   - `isPlanningComplete`: valor booleano que indica si todos los artefactos de planificación están completos. Las versiones antiguas de la CLI exponen el mismo valor como `isComplete`.
   - `planningHome`, `changeRoot`, `artifactPaths` y `actionContext`: contexto de rutas y alcance. Usa estos datos en vez de suponer rutas locales al repositorio.

   Los identificadores y las rutas de artefactos dependen del esquema activo: no los supongas ni uses ramificaciones basadas en nombres de artefactos codificados. Los esquemas personalizados deben funcionar sin cambios.

   Los archivos editables son los indicados en `artifactPaths.<id>.existingOutputPaths`: rutas concretas de archivos que existen en disco y que ya expanden los patrones glob (por ejemplo, `specs/**/*.md`). No escribas en `resolvedOutputPath`: para un artefacto glob sigue siendo un patrón, no un archivo real.

3. **Entender la solicitud**
   - Si el usuario pidió una revisión específica («el diseño ahora usa X»), empieza por ese cambio.
   - Si solo pidió «actualizar» o «hacer coherente», revisa la coherencia: lee los artefactos y compáralos para detectar contradicciones, vacíos y duplicaciones.

4. **Leer y conciliar**
   - Lee los artefactos que afecta la solicitud y los demás artefactos existentes del cambio.
   - Redacta en la conversación el cambio solicitado, no en los archivos. Define exactamente qué cambiará; el paso 5 es el único que autoriza escrituras. Luego compara todos los demás artefactos existentes con el borrador, en ambas direcciones: editar un artefacto posterior puede requerir revisar uno anterior. El orden de construcción sirve para leer, pero no limita qué artefactos pueden revisarse.
   - Anota todas las incoherencias, omisiones y contradicciones.
   - Propón cambios solo en archivos existentes (`existingOutputPaths`). Si un artefacto no tiene archivos de salida y está `ready` o `blocked`, indícalo y señala `openspec instructions "<artifact-id>" --change "<name>" --json` para saber cómo crearlos. Deja intactos los artefactos `skipped`: no los trates como faltantes ni los postergues al flujo de continuación.
   - Un artefacto glob (por ejemplo, `specs/**/*.md`) se considera `done` cuando coincide al menos un archivo; el flujo de continuación solo gestiona artefactos `ready`. Si al conciliar detectas un archivo faltante en un artefacto glob cuyo `existingOutputPaths` no está vacío:
     1. Ejecuta `openspec instructions "<artifact-id>" --change "<name>" --json` y usa `instruction` y `template`. Trata `context` y `rules` como restricciones; no los copies al archivo. Si las instrucciones indican `skipped: true`, no crees el archivo. Lee del disco los archivos de dependencia actuales; si falta una dependencia requerida que no esté omitida, detente y pide al usuario que la restaure primero.
     2. Elige una ruta concreta dentro de `changeRoot` que coincida con `artifactPaths.<id>.outputPath` y aún no exista. Al resolver los directorios padre que puedan ser enlaces simbólicos, verifica que siga dentro de `changeRoot`. El `resolvedOutputPath` del glob no es una ruta válida de destino.
     3. Incluye el archivo nuevo entre los cambios propuestos del paso 5 y créalo solo después de que el usuario confirme.
     4. Tras la confirmación e inmediatamente antes de crearlo, vuelve a consultar el estado y las instrucciones. Comprueba que el artefacto siga dentro del alcance, no esté omitido y esté parcialmente poblado; repite las comprobaciones de ruta concreta.
     5. Usa una operación de creación que falle si el destino ya existe. Si `instruction` delega la creación a otra habilidad o comando, úsalo solo si respeta la ruta confirmada y estas protecciones; de lo contrario, detente. Si alguna comprobación falla o el borrador confirmado ya no es válido, concilia el cambio con el usuario en vez de reemplazar contenido o elegir otra ruta.
   - Si el cambio ya es coherente, dilo y no propongas modificaciones.

5. **Confirmar y aplicar, un artefacto a la vez**
   - Todas las escrituras de artefactos de este flujo ocurren aquí; ningún paso anterior modifica archivos.
   - Muestra cada cambio propuesto y su motivo, incluido el borrador del paso 4. Escribe solo después de que el usuario confirme.
   - Si el usuario rechaza una revisión, no la escribas y deja intacto ese artefacto.
   - Si hace falta una reescritura sustancial, consulta primero las reglas y la plantilla del artefacto:

     ```bash
     openspec instructions "<artifact-id>" --change "<name>" --json
     ```

6. **Indicar el siguiente paso (solo orientación; NUNCA lo ejecutes)**
   - Para artefactos sin archivos existentes y estado `ready` o `blocked`, ejecuta `openspec status --change "<name>" --json` para identificar el siguiente y señala `openspec instructions "<artifact-id>" --change "<name>" --json` para saber cómo crearlo.
   - Si el cambio ya está implementado (tareas marcadas o cambios aplicados), el código quizá ya no coincida con el plan revisado; sugiere `/opsx:apply` para trasladar las diferencias al código.
   - Si todo está hecho e implementado, sugiere `/opsx:archive`.

**Salida**

Después de cada invocación, muestra:
- Qué artefactos se revisaron y qué propuestas rechazó el usuario.
- Cualquier archivo creado para un artefacto glob que ya estaba parcialmente poblado.
- Qué quedó pendiente porque aún no existe (artefactos sin archivos en estado `ready` o `blocked`; nunca artefactos `skipped`).
- En qué estado queda el cambio y cuál es el siguiente comando recomendado.

**Protecciones**
- Solo artefactos de planificación: NUNCA edites código de implementación. Si el plan revisado implica cambios de código, detente y señala `/opsx:apply`.
- Usa los identificadores y las rutas que informa `openspec status`; nunca ramifiques por nombres de artefactos codificados.
- Edita únicamente los archivos concretos de `existingOutputPaths`; nunca escribas en un `resolvedOutputPath` glob.
- No avances la frontera de construcción: si un artefacto no tiene archivos en `existingOutputPaths` y está `ready` o `blocked`, crearlos es un paso aparte, fuera de este flujo. Deja intactos los artefactos `skipped`. La única excepción para crear archivos nuevos es una ruta concreta confirmada dentro de un artefacto glob cuyo `existingOutputPaths` no esté vacío.
- Confirma con el usuario cada cambio antes de escribir.
- Si la solicitud cambia la *intención* del cambio en lugar de afinarla, pide un nombre distinto y no usado, y recomienda `openspec new change "<new-change-name>"` (criterio «Actualizar o empezar de nuevo»).
