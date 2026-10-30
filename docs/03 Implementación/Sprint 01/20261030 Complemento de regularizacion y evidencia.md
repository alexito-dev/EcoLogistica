# Sprint 01 — Complemento de regularización y evidencia

**Fecha:** 30/10/2026  
**Naturaleza:** adenda técnica; no reemplaza ni altera el acta histórica.

## Alcance y trazabilidad
Como equipo, mantenemos el alcance funcional vigente de Sprint 1: autenticación por contraseña y TOTP, RBAC y registro/consulta persistente de pedidos (ECO-9, ECO-16, ECO-20). Distinguimos el compromiso histórico del corte original y las implementaciones regularizadas posteriormente. No reescribimos la velocidad histórica ni atribuimos al Sprint 1 funcionalidades implementadas después.

## Corrección adicional
En la rama de regularización reforzamos la durabilidad de la escritura atómica de usuarios JSON ante fallos de I/O y añadimos una prueba regresiva. El almacén local permanece temporal; las cuentas y secretos siguen pendientes de su migración/cifrado de acuerdo con ECO-21. No damos por resuelta esa obligación.

## Validación de cierre
Corroboraremos MFA enrolamiento y rechazo de reutilización TOTP, 401/403 por rol, bloqueo de intentos, persistencia de pedidos PostGIS tras reiniciar, pruebas de API/UI y evidencia del CI del PR. Registraremos los resultados nuevos por fecha y SHA, sin sustituir registros previos.

## Referencias
[Plan transversal](../Regularizacion%20Sprints%2001-03%20-%2020261030.md) · [Jira](https://continental-team-ecologistica.atlassian.net/jira/software/projects/ECO/boards/2/backlog) · [PR de revisión](https://github.com/alexito-dev/EcoLogistica/pull/3)

## Conciliación actual del tablero (30/10/2026)

Como equipo, mantenemos **cerrado** el Sprint 1 oficial (id 36). Etiquetamos ECO-9 y ECO-15 como históricos; los habilitadores ECO-16 (PostGIS) y ECO-20 (MFA) siguen en Listo dentro de la línea base reordenada, sin incorporarlos retroactivamente al sprint. ECO-11 se encuentra en revisión QA porque la consulta de coordenadas existe, pero no hemos acreditado la geocodificación automática ni el recorrido de corrección de ubicación. Esta nota no altera el 0/2 registrado en el corte original del 28/09.

[Artefactos Jira actualizados](../../02%20Planificaci%C3%B3n/02%20Artefactos%20Jira%20V_1_0_0.md#actualización-de-gestión-verificada--30102026).

