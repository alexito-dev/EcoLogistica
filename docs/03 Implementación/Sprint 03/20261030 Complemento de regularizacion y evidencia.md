# Sprint 03 — Complemento de regularización y evidencia

**Fecha:** 30/10/2026  
**Naturaleza:** adenda técnica; no reemplaza ni altera el acta histórica.

## Alcance implementado y diferencias en Jira
Como equipo, reconocemos el incremento documentado de planificación de rutas, mapa Leaflet/OpenStreetMap + OSRM, indicadores y GitHub Actions. Conservamos el benchmark sintético del 30/10 separado de resultados reales de negocio. ECO-13, ECO-14 y ECO-17 siguen abiertos porque faltan criterios E2E específicos y evidencias de integración que sus descripciones exigen.

## Corrección técnica efectuada
En nuestra rama de regularización añadimos durabilidad de archivo al almacén provisional de rutas guardadas. Esta modificación no sustituye la persistencia transaccional y concurrente en PostgreSQL, pendiente en ECO-21.

## Calidad y seguridad
Verificaremos en el PR las suites pytest/Vitest, Alembic, lint, compilación, OpenSpec y evidencias OWASP/WCAG. El 88,9 % de criterios WCAG aplicables reportados está por debajo de la meta de 90 %. No presentaremos indicadores de CO₂e simulado como reducciones operativas reales. Antes de marcar Listo, ECO-13 requiere comprobar el escenario del repartidor y ruta sin coordenadas; ECO-14 necesita comprobar indicadores basados en entregas y estado vacío; ECO-17 exige integración PostGIS y Playwright.

## Registro
La validación técnica y la aceptación de producto se registrarán con enlaces a commit, ejecución CI, casos de prueba y decisión formal. No cerramos administrativamente este sprint por emitir el presente complemento.

## Referencias
[Plan transversal](../Regularizacion%20Sprints%2001-03%20-%2020261030.md) · [Jira](https://continental-team-ecologistica.atlassian.net/jira/software/projects/ECO/boards/2/backlog) · [PR de revisión](https://github.com/alexito-dev/EcoLogistica/pull/3)
