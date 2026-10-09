# 05. Plan funcional de sprints

[← Volver al README Principal](../../README.md)

## Metadatos

| Campo | Valor |
|---|---|
| Proyecto | EcoLogística Huancayo |
| Versión | 1.0.0 |
| Fecha | 09/10/2026 |
| Enfoque | Cada sprint debe dejar una tarea real que una persona pueda completar en el sistema. |

## Para qué sirve este plan

La meta de cada sprint se escribe como una acción que alguien podrá hacer en la aplicación. La base de datos, los mapas, el motor de rutas y la automatización son parte del trabajo cuando hacen falta para completar esa acción; por sí solos no cuentan como resultado funcional del sprint.

Este plan ordena lo que ya ocurrió y propone cómo continuar. Los compromisos futuros todavía necesitan conversación, estimación y acuerdo del equipo en Jira. No se asignan puntos ni fechas que el equipo no haya aprobado.

## Sprints y resultado para quien usa el sistema

| Sprint | Acción que se busca habilitar | Estado con evidencia al 09/10/2026 |
|---|---|---|
| **Sprint 1** · 14/09–28/09 | Que Planificación registre pedidos y atienda incidencias que cambian una ruta. | El informe del corte del 28/09 registró 0 de 2 historias terminadas. ECO-15, sobre re-enrutamiento, continúa pendiente. ECO-9 se completó después y se incorporó también al Sprint 2; ese avance posterior no cambia el resultado histórico del Sprint 1. |
| **Sprint 2** · 29/09–12/10 | Que Planificación entre con contraseña y código de verificación, registre pedidos y luego pueda encontrarlos y consultar su detalle. | La aplicación ya permite iniciar sesión con MFA y rol, registrar pedidos válidos y consultar, buscar, filtrar y abrir pedidos. La API y la interfaz respondieron localmente; Jira muestra ECO-9 y ECO-20 en `Listo`. El sprint sigue activo y su revisión todavía está pendiente: no se afirma aceptación formal. Los pedidos se guardan en memoria y se pierden al reiniciar la API. |
| **Sprint 3** · propuesta, sin compromiso aprobado | Que Planificación asigne pedidos pendientes a vehículos y obtenga una ruta guardada para revisar. | Para que esa tarea funcione de principio a fin harán falta persistencia, datos de flota y una primera secuencia de paradas. Evaluar PostGIS y el optimizador como parte de esa entrega, según la solución acordada. Preparar y estimar las historias con el equipo antes de cargarlas como compromiso en Jira. |
| **Sprint 4** · propuesta, sin alcance detallado aprobado | Que una persona conductora consulte su ruta, marque una entrega y reporte una incidencia para que Planificación pueda revisar el cambio. | Confirmar flujo y prioridades con el equipo. El mapa, el cálculo de rutas y el re-enrutamiento se suman si son necesarios para completar esa tarea, no como entregables aislados. No hay fechas ni resultados aprobados para esta propuesta. |

## Qué incluye hoy el incremento del Sprint 2

Una persona puede abrir la aplicación, autenticarse, registrar un pedido con dirección, carga y ventana horaria, y después localizarlo en la lista o abrir su detalle. El acceso depende del rol: Planificación puede registrar y consultar pedidos; Administración solo puede consultarlos.

La verificación local del 09/10 confirmó que la interfaz responde en `http://localhost:3000/` y que la API responde en `http://localhost:8000/openapi.json`. Las pruebas automatizadas y la compilación anotadas en los informes corresponden a ejecuciones anteriores documentadas allí; esta actualización no las vuelve a ejecutar.

Todavía no se puede guardar pedidos entre reinicios, gestionar vehículos, generar o guardar rutas, verlas en un mapa ni registrar el avance de entregas. La autenticación usa cuentas de demostración locales y requiere configurar el acceso y el código TOTP; no es inicio de sesión institucional conectado a un proveedor de identidad.

## Cuándo damos por útil un sprint

Antes de empezar, el equipo acuerda una meta que empiece con una acción concreta, quién la necesita y cómo se comprobará. Se completa el recorrido principal desde la interfaz y la respuesta del sistema confirma lo ocurrido. Si el flujo depende de una regla o un permiso, se comprueba también ese caso. La información sobrevive lo que la historia prometa: si el objetivo necesita guardar algo, reiniciar la aplicación no debe borrarlo.

Al cerrar, se muestra el flujo en un entorno reproducible, se enlaza evidencia en Jira, se registran defectos conocidos y se separa claramente lo terminado de lo que queda pendiente. Un servidor encendido, una tabla creada, una prueba aislada o un módulo técnico por sí solo no demuestra que la tarea de la persona ya se pueda hacer.

Esta definición sirve para juzgar el incremento de un sprint. No significa que el PMV completo esté listo para operar: su aceptación todavía debe cubrir, entre otras cosas, despliegue, respaldos, seguridad, disponibilidad, integración y los resultados medibles acordados con el negocio.

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se ordenan los sprints por la tarea que la persona podrá completar y se distingue el estado comprobado de las propuestas futuras. |
