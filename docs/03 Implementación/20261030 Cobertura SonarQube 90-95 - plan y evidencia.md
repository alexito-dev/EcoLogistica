# Plan y medición de cobertura verificable — SonarQube 90–95 %

**Proyecto:** EcoLogística Huancayo  
**Fecha de inicio:** 30/10/2026  
**Jira:** [ECO-28](https://continental-team-ecologistica.atlassian.net/browse/ECO-28) · [ECO-29](https://continental-team-ecologistica.atlassian.net/browse/ECO-29) · [ECO-30](https://continental-team-ecologistica.atlassian.net/browse/ECO-30)  
**Naturaleza:** objetivo de calidad **posterior** al cierre del Sprint 3. No se modifican resultados ni velocidad históricos de los tres primeros sprints.

## Meta y criterio de aceptación

Como equipo, establecemos **90 % de cobertura combinada mínima obligatoria**, con **95 % como objetivo exigente**. Ambas cifras deben obtenerse de pruebas reales, sin excluir archivos funcionales o manipular denominadores. La cobertura oficial de SonarQube se confirmará mediante SonarScanner en el mismo commit; el indicador de CI que agregamos es un **proxy calculado directamente desde Cobertura XML + LCOV**:

\[
C_{CI}=100\,\frac{L_{cubiertas}+R_{cubiertas}}{L_{totales}+R_{totales}}
\]

Este indicador explicita tanto la cobertura de líneas como la de ramas. Puede diferir del cálculo oficial de SonarQube según cómo se instrumenten y clasifiquen condiciones, por lo que no sustituimos uno por el otro.


## Segunda medición verificable: después de ampliar pruebas Python y Vitest

En la [ejecución de CI #41124453799](https://github.com/alexito-dev/EcoLogistica/actions/runs/41124453799), correspondiente a la rama `quality/coverage-90-sonarqube-20261030` en el commit `a11c0af9` (el contexto de prueba de PR identificó `722ad649`), **los cinco jobs terminaron correctamente**. Los datos medidos desde los XML y LCOV fueron:

| Área | Líneas cubiertas | Líneas | Ramas cubiertas | Ramas | Cobertura combinada |
|---|---:|---:|---:|---:|---:|
| Backend Python | 1652/1719 | **96,10 %** | 206/240 | **85,83 %** | **94,84 %** |
| Frontend TypeScript | 654/700 | **93,43 %** | 525/610 | **86,07 %** | **90,00 %** |
| **Global ponderado** | **2306/2419** | **95,33 %** | **731/850** | **86,00 %** | **92,90 %** |

**Avance medido:** de la primera línea base de CI **84,74 %** a **92,90 %**, aumento de **8,16 puntos porcentuales**. Mejoramos la cobertura de ramas en 13,76 puntos, de **72,24 % a 86,00 %**. No se añadieron exclusiones de código de producción. La diferencia respecto del 95 % combinado deseado sigue siendo de **2,10 puntos porcentuales**, y necesitamos validar el cálculo oficial de SonarQube.

La puerta de calidad posterior se ha activado con `python scripts/reporte_cobertura.py --min 90`. El resultado del run anterior aún no incluía el parámetro obligatorio, por lo que **debemos comprobar una nueva ejecución en verde antes de fusionar**.

El backend añadió pruebas de reglas y casos negativos de flota, consistencia de turnos, placas duplicadas y fallo de validación PostgreSQL/PostGIS. El frontend incorporó suites nuevas para flota, clientes HTTP/autenticación/rutas/indicadores y preferencias de movimiento reducido, además de ampliar casos de errores y estados vacíos. Esto explica una mayor proporción de decisiones realmente ejecutadas, sin modificar artificialmente el código medido.

### Pendiente para declarar la meta oficial SonarQube

El servidor SonarQube del proyecto sigue documentado como instancia local en `http://localhost:9000`, inaccesible desde este flujo. La medición **92,90 % es la cifra auditable de CI, no el Quality Gate de un nuevo análisis SonarQube**. ECO-28 seguirá en curso hasta ejecutar el Scanner sobre el mismo SHA y comprobar que la cobertura **oficial de SonarQube** alcanza al menos 90 %. El 95 % permanece como objetivo de mejora, no como resultado ya alcanzado.

---

## Situación real de partida

El escaneo histórico de SonarQube del commit `9b31dd0` (30/10) reportó **82,8 % global**, **86,0 % líneas** y **69,3 % ramas**. No corresponde al `main` actual.

El primer job de cobertura ampliado del [PR #8](https://github.com/alexito-dev/EcoLogistica/pull/8), ejecutado sobre **`96a2cd3`** con PostgreSQL/PostGIS aislado, produjo los siguientes datos desde cobertura auténtica de las suites, sin que implique un escaneo nuevo de SonarQube:

| Área | Líneas cubiertas | Líneas % | Ramas cubiertas | Ramas % | Combinada |
|---|---:|---:|---:|---:|---:|
| Backend Python | 1624/1719 | **94,47 %** | 190/240 | **79,17 %** | **92,60 %** |
| Frontend TypeScript | 532/700 | **76,00 %** | 424/610 | **69,51 %** | **72,98 %** |
| Global ponderado | 2156/2419 | **89,13 %** | 614/850 | **72,24 %** | **84,74 %** |

[Ver ejecución y archivos de cobertura (artefacto XML + LCOV)](https://github.com/alexito-dev/EcoLogistica/actions/runs/41123515247).

La principal brecha medible se encuentra en **frontend** y en las **ramas condicionales** de ambos lenguajes. El porcentaje 84,74 % es la nueva línea base de CI, no reemplaza el histórico 82,8 % de SonarQube ni prueba la meta de 90 %.

## Implementación del control

1. Configuramos `pytest --cov=app --cov-branch` para medir también ramas y ejecutar la suite completa contra PostgreSQL/PostGIS con datos aislados y migraciones Alembic previas.
2. Ejecutamos Vitest con V8 y reporte LCOV de todo `frontend/src`, incluyendo vistas y APIs. No excluimos módulos para subir métricas.
3. El script [`scripts/reporte_cobertura.py`](../../../scripts/reporte_cobertura.py) consolida numeradores y denominadores de líneas/ramas y genera el resumen de GitHub Actions.
4. Conservamos `backend/coverage.xml` y `frontend/coverage/lcov.info` en un artefacto de GitHub Actions por ejecución durante 30 días.
5. Añadimos pruebas orientadas a flujos reales de API, autenticación, flota, rutas, reintentos, permisos, persistencia y estados vacíos.
6. Una vez alcanzado el 90 % en CI sobre el mismo commit, exigiremos `--min 90` como puerta de calidad, sin cambiar artificialmente la fórmula.
7. Reanalizaremos el mismo commit en SonarQube local o servidor autorizado y compararemos cobertura global, líneas y ramas con los resultados de CI. Si SonarQube queda debajo del mínimo, ECO-28 seguirá abierto.

## Diagnóstico y medidas por módulo

| Área | Brecha de calidad | Acciones verificables |
|---|---|---|
| `frontend/src/pages/PaginaFlota.tsx` | Formularios, turnos, estados y errores de interfaz sin suite dedicada | Nuevas pruebas de registro, edición, permisos, turnos, reintentos, validación |
| `frontend/src/api/*` | Flujos de sesión, rutas y vehículos insuficientemente cubiertos | Tests de HTTP 200/204/401/403/404, errores de red, codificación de fechas, contratos |
| `frontend/src/pages/PaginaRutas.tsx` | Guardado, recálculo, fallo y condiciones límite | Tests de error/reintento y persistencia, selección de fecha y estados |
| `frontend/src/pages/PaginaIndicadores.tsx` | Estados sin datos, errores, cambios de filtros y caminos condicionales | Tests de manejo de API y distinción entre estimación y resultado observado |
| Adaptadores `PostgreSQL/PostGIS` | Cobertura antes insuficiente o ausente en el mismo reporte | Integración real en el job unificado; pruebas de recuperación por repositorios independientes |
| Seguridad/condiciones excepcionales | Faltan casos negativos y recuperación para permisos/autenticación | Pruebas de 401/403, control de sesión, cabeceras, errores y contratos OpenAPI |

## Definición de Terminado (DoD)

ECO-28 solo pasará a **Listo** cuando: (a) las suites completas pasen; (b) las medidas objetivas de CI confirmen **≥90 %** sin excluir código relevante; (c) SonarQube analice el mismo commit, publique su cobertura ≥90 % y Quality Gate conforme a la regla aprobada; (d) existan enlaces a ejecución, reporte, commit y responsable en Jira; (e) se registren explícitamente las diferencias entre mediciones y las acciones para llegar a 95 %. No inventamos métricas ni damos por satisfecha la DoD por aprobar una suite aislada.

**Estado actual:** intervención en desarrollo y verificación. Hasta una nueva ejecución completa, la referencia confirmada por CI es **84,74 %** en el commit `96a2cd3`; cualquier resultado posterior se añadirá en una nueva sección fechada y con SHA.
