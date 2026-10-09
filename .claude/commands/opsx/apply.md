---
name: "OPSX: Aplicar"
description: "Implementa las tareas de un cambio de OpenSpec (Experimental)"
allowed-tools: Bash(openspec:*)
category: "Workflow"
tags: ["flujo", "artefactos", "experimental"]
---

Implementa las tareas de un cambio de OpenSpec.

**Selección de almacén:** Si el usuario indica un almacén (un repositorio OpenSpec independiente registrado en esta máquina) o el trabajo se encuentra allí, ejecuta `openspec store list --json` para descubrir sus identificadores y añade `--store <id>` a los comandos que leen o escriben especificaciones y cambios (`new change`, `status`, `instructions`, `list`, `show`, `validate`, `archive`, `doctor`, `context`, `schemas`, `view`). Una vez elegido, conserva `--store <id>` durante todo el flujo. Todo ejemplo sin ámbito es una forma abreviada: antes de ejecutarlo, añade la opción. Por ejemplo, ejecuta `openspec status --change "<name>" --json --store "<id>"`, no la variante sin ámbito. Los demás comandos no aceptan esa opción. Conserva la opción en los comandos posteriores cuando las sugerencias de la CLI ya la incluyan. Si no se selecciona un almacén, los comandos actúan sobre la raíz `openspec/` local más cercana.

**Comprobación del proyecto:** Estos pasos suponen que el proyecto ya usa OpenSpec. Antes del primer paso que escriba algo (`new change`, `archive`, `sync specs` o la creación de un artefacto), confirma que existe una raíz: ejecuta `openspec list --json` (con `--store <id>` si se seleccionó un almacén, porque ese almacén es la raíz) y revisa `root`. Un objeto en `root` significa que el proyecto está configurado. `"root": null` significa que no lo está: aquí no hay un directorio `openspec/` y una escritura como `openspec new change` lo crearía como efecto secundario. El comando también termina con código distinto de cero; esa es la respuesta, no un fallo de la CLI. Lee el JSON en vez de reintentar o buscar una solución alternativa.

Un `"root": null` no siempre significa que falte la configuración: si un error de `status` empieza con `Declared in` o `Invalid store declaration in` y menciona `openspec/config.yaml` (o `config.yml`) de este proyecto, el proyecto sí usa OpenSpec mediante un almacén declarado, pero esta máquina no puede resolverlo (no está registrado o la línea `store:` está mal formada). No lo trates como un proyecto sin inicializar ni continúes con las ramas de abajo: detente antes de escribir y muestra al usuario los campos `message` y `fix` del error.

Si no hay raíz, el paso siguiente depende de cómo se inició este flujo:

- **Selección automática:** elegiste este flujo por tu cuenta, sin que el usuario mencionara OpenSpec, esta habilidad ni su comando de barra. Deja de usar OpenSpec y responde normalmente, como si no estuviera instalado. No pidas que configure nada ni menciones la configuración de OpenSpec.
- **Solicitud explícita de OpenSpec:** el usuario mencionó OpenSpec, esta habilidad o ejecutó su comando de barra. Detente antes de escribir y pregunta cómo proceder: configurar este proyecto (`openspec init`), usar un almacén que ya exista (`--store <id>`) o continuar sin OpenSpec en esta solicitud. Espera la respuesta.

En ambos casos, nunca crees la raíz como efecto secundario: no ejecutes `openspec init` hasta que el usuario lo pida, no crees manualmente archivos en `openspec/` y no permitas que otro comando la cree.

**Entrada:** Opcionalmente indica un nombre de cambio (por ejemplo, `/opsx:apply add-auth`). Si se omite, comprueba si puede inferirse del contexto de la conversación. Si es ambiguo o poco claro, DEBES pedir que se elija entre los cambios disponibles.

**Pasos**

1. **Seleccionar el cambio**

   Si se indicó un nombre, úsalo. Si no:
   - Infiérelo del contexto si el usuario mencionó un cambio.
   - Selecciónalo automáticamente si solo hay un cambio activo.
   - Si hay ambigüedad, ejecuta `openspec list --json` para obtener los cambios disponibles y pide al usuario que elija.

   Anuncia siempre: `Cambio seleccionado: <name>` e indica cómo cambiar la selección (por ejemplo, `/opsx:apply <other>`).

2. **Consultar el estado y entender el esquema**

   ```bash
   openspec status --change "<name>" --json
   ```

   Interpreta el JSON para conocer:
   - `schemaName`: esquema de flujo utilizado (por ejemplo, `spec-driven`).
   - `planningHome`, `changeRoot` y `actionContext`: alcance de planificación y restricciones de edición.
   - Qué artefacto contiene las tareas (normalmente `tasks` en `spec-driven`; consulta el estado para otros esquemas).

3. **Obtener instrucciones de implementación**

   ```bash
   openspec instructions apply --change "<name>" --json
   ```

   La respuesta incluye:
   - `contextFiles`: identificador de artefacto → rutas concretas (varían según el esquema; por ejemplo, propuesta/especificaciones/diseño/tareas o especificación/pruebas/implementación/documentación).
   - Progreso (total, completadas, pendientes).
   - Lista de tareas y sus estados.
   - Instrucción dinámica según el estado actual.
   - `context` opcional: instrucciones vigentes del proyecto seleccionadas desde la raíz.
   - `operationGuidance` opcional: recomendaciones complementarias para aplicar el cambio.
   - `missingArtifacts`, cuando exista: identificadores requeridos sin archivo de salida.

   **Gestionar los estados:**
   - Si `state: "blocked"`, muestra el mensaje y pausa la implementación.
     - Si `missingArtifacts` no está vacío, sugiere completar los artefactos faltantes. Ejecuta `openspec status --change "<name>" --json`, selecciona el siguiente artefacto `ready` (no `skipped` ni `blocked`) y consulta `openspec instructions "<artifact-id>" --change "<name>" --json` para obtener sus reglas y plantilla. Conserva `--store <id>` en ambos comandos.
     - En caso contrario, sigue la instrucción de la CLI para crear o reparar el archivo de seguimiento configurado para el esquema a partir de los artefactos de planificación existentes. No supongas que otro artefacto está listo ni empieces a implementar mientras el cambio esté bloqueado.
   - Si `state: "all_done"`, felicita al usuario y sugiere archivar.
   - En otro caso, continúa con la implementación.

   Trata `context` como una instrucción obligatoria del prompt: léela, considérala y aplica los datos, convenciones y restricciones pertinentes del proyecto. Trata `operationGuidance` como consejo adicional opcional: lee y considera cada entrada, y sigue las que sean aplicables y compatibles con el flujo integrado.

   Mantén ambos campos separados del estado que devuelve la CLI, los artefactos faltantes, las tareas, el progreso, `contextFiles` y la instrucción integrada. No son evidencia de finalización, no sustituyen la instrucción integrada ni permiten saltarse un estado bloqueado. Si `context` entra en conflicto con la instrucción integrada, una elección explícita del usuario o un valor controlado por la CLI, informa el conflicto y conserva el valor que prevalece. Si una recomendación no es aplicable o contradice esas entradas, no la sigas y explica por qué. Estos contratos guían el comportamiento del prompt, pero no son validaciones ejecutables.

4. **Leer los archivos de contexto**

   Lee todos los archivos indicados en `contextFiles` por las instrucciones de implementación. Dependen del esquema:
   - **spec-driven:** propuesta, especificaciones, diseño y tareas.
   - Otros esquemas: sigue el `contextFiles` que devuelva la CLI.

   No copies `context` ni `operationGuidance` literalmente a archivos de implementación o artefactos de planificación, salvo que el usuario pida ese contenido por separado.

5. **Mostrar el progreso actual**

   Muestra:
   - Esquema utilizado.
   - Progreso: `N/M tareas completadas`.
   - Resumen de tareas pendientes.
   - Instrucción dinámica de la CLI.

6. **Implementar las tareas (repetir hasta terminar o quedar bloqueado)**

   Para cada tarea pendiente:
   - Indica en qué tarea estás trabajando.
   - Realiza los cambios de código requeridos.
   - Mantén los cambios pequeños y enfocados.
   - Marca la tarea como completada en el archivo de tareas: `- [ ]` → `- [x]`.
   - Continúa con la siguiente tarea.

   **Pausa si:**
   - La tarea no está clara: pide una aclaración.
   - La implementación revela un problema de diseño: sugiere actualizar los artefactos.
   - La tarea requiere trabajo no descrito en la especificación y las tareas, o existe la tentación de quitar, reducir, postergar o aceptar excepciones para ajustarla: expón el alcance adicional y pregunta; no lo incorpores en silencio.
   - Aparece un error o bloqueo: infórmalo y espera instrucciones.
   - El usuario interrumpe.

7. **Al terminar o pausar, mostrar el estado**

   Muestra:
   - Tareas completadas en esta sesión.
   - Progreso total: `N/M tareas completadas`.
   - Si todo está hecho, sugiere archivar.
   - Si se pausó, explica el motivo y espera instrucciones.

**Formato de salida durante la implementación**

```
## Implementando: <nombre-del-cambio> (esquema: <nombre-del-esquema>)

Trabajando en la tarea 3/7: <descripción de la tarea>
[...implementación en curso...]
✓ Tarea completada

Trabajando en la tarea 4/7: <descripción de la tarea>
[...implementación en curso...]
✓ Tarea completada
```

**Formato de salida al completar**

```
## Implementación completada

**Cambio:** <nombre-del-cambio>
**Esquema:** <nombre-del-esquema>
**Progreso:** 7/7 tareas completadas ✓

### Completado en esta sesión
- [x] Tarea 1
- [x] Tarea 2
...

Todas las tareas están completas. Puedes archivar este cambio con `/opsx:archive`.
```

**Formato de salida al pausar (problema encontrado)**

```
## Implementación pausada

**Cambio:** <nombre-del-cambio>
**Esquema:** <nombre-del-esquema>
**Progreso:** 4/7 tareas completadas

### Problema encontrado
<descripción del problema>

**Opciones:**
1. <opción 1>
2. <opción 2>
3. Otro enfoque

¿Cómo deseas continuar?
```

**Protecciones**
- Continúa con las tareas hasta terminar o quedar bloqueado.
- Antes de empezar, lee los archivos de contexto de las instrucciones de implementación.
- Si una tarea es ambigua, pausa y pregunta antes de implementarla.
- Si la implementación revela problemas, pausa y sugiere actualizar los artefactos.
- Mantén los cambios de código pequeños y limitados a cada tarea.
- Actualiza la casilla de la tarea inmediatamente después de completarla.
- Ante errores, bloqueos o requisitos poco claros, pausa; no adivines.
- Si una tarea requiere trabajo no descrito, expón el alcance adicional y pausa; nunca reduzcas, postergues ni simplifiques en silencio el comportamiento especificado.
- Marca `- [x]` solo cuando el comportamiento especificado esté completamente implementado, no si es parcial o quedó postergado.
- Usa `contextFiles` de la salida de la CLI; no supongas nombres de archivo.
- No uses `context` ni `operationGuidance` como prueba de que una tarea terminó.
- Aplica el contexto pertinente del proyecto e informa los conflictos con las entradas que controlan el flujo.
- Considera todas las recomendaciones y explica las que no sean aplicables o entren en conflicto.
- No copies el contexto de ejecución ni las recomendaciones a archivos de implementación o planificación.
- Conserva los estados y criterios de finalización controlados por la CLI: `blocked`, `ready` y `all_done`.

**Integración con un flujo flexible**

Este flujo sigue el modelo de «acciones sobre un cambio»:
- Puede iniciarse en cualquier momento: antes de completar todos los artefactos (si ya hay tareas), después de una implementación parcial o intercalado con otras acciones.
- Permite actualizar artefactos: si la implementación revela problemas de diseño, sugiere actualizarlos; no impongas una secuencia rígida de fases.
