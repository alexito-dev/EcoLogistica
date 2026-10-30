# Validación de vigencia del reporte SonarQube y procedimiento de reanálisis

**Proyecto:** EcoLogística Huancayo  
**Corte documental:** 30/10/2026  
**Tipo de revisión:** contraste de informes, configuración, repositorio y GitHub Actions. **No es una nueva ejecución de SonarQube.**  
**Referencia original:** [03 Calidad de código V_1_0_0.md](03%20Calidad%20de%20c%C3%B3digo%20V_1_0_0.md)

## 1. Dictamen

Como equipo, verificamos que el repositorio **sí contiene un análisis SonarQube documentado y explicativo**, con un informe versión 1.1.0, captura del panel, distribución de hallazgos, recomendaciones y comandos de repetición. Lo consideramos **evidencia histórica válida del commit analizado** y conservamos sus cifras.

**No podemos atribuirlo al último commit de `main`**. El análisis publicado corresponde a **`9b31dd04a04443b6f7ee40c77b575b725a51ab33`** (30/10/2026), mientras que durante esta verificación la rama principal estaba en **`e7e4a00dba48a0c9140409c998ebffcd207b0ef7`**, 41 commits después del commit inspeccionado. La comparación de GitHub evidencia cambios de código, pruebas y documentación entre ambas revisiones. **Las métricas de SonarQube del commit final siguen sin medirse directamente en su instancia local.**

En el repositorio también existen [`sonar-project.properties`](../../../sonar-project.properties), la captura [`20261030-panel-sonarqube-overall.jpg`](../../../assets/images/sonarqube/20261030-panel-sonarqube-overall.jpg) y [`.github/workflows/ci.yml`](../../../.github/workflows/ci.yml). La CI ejecuta pytest, Vitest, lint, build, migraciones PostGIS y OpenSpec, **pero no ejecuta SonarScanner ni publica un Quality Gate de SonarQube**. Un workflow verde de GitHub Actions no es un reanálisis SonarQube.

## 2. Resultados del análisis histórico (no extrapolar a `main` actual)

| Indicador reportado al 30/10 | Valor histórico | Interpretación correcta |
|---|---:|---|
| Quality Gate | **PASSED / OK** | Cumplimos el criterio configurado en ese análisis: **cero incidencias nuevas**. El estado no significa que todas las incidencias del código total estén resueltas. |
| Cobertura combinada | **82,8 %** | Importada de reportes XML de pytest y LCOV de Vitest; ponderación calculada por SonarQube. No es un promedio aritmético simple. |
| Cobertura de líneas / ramas | **86,0 % / 69,3 %** | Indica qué fracción de código/decisiones mide la herramienta y ayuda a orientar pruebas faltantes. |
| Pruebas backend | **137 aprobadas**, 92,6 % de líneas | Es la ejecución reportada sobre `9b31dd0`, no una ejecución independiente de esta revisión. |
| Pruebas frontend | **58 aprobadas**, 76,0 % de líneas | Es la ejecución reportada en el documento histórico. |
| Bugs / vulnerabilidades / Security Hotspots | **0 / 0 / 0** | No detectados por el análisis ejecutado. No es garantía de ausencia absoluta de defectos o vulnerabilidades. |
| Code smells | **101** | Oportunidades de mantenibilidad, simplicidad, legibilidad y otras reglas; no son 101 fallos funcionales. |
| Duplicación | **0,0 %** | Sin duplicación detectada por el perfil y el alcance de ese análisis. |
| Fiabilidad | **C** | El análisis contabilizó 3 incidencias de impacto en fiabilidad, a pesar de que la métrica clásica de bugs marcaba 0. |
| Seguridad / revisión de seguridad | **A / A** | Calificación de las reglas de seguridad efectivamente cubiertas en la edición Community. |
| Mantenibilidad | **A** | No contradice que haya 101 code smells: la calificación depende de la deuda relativa, no de exigir cero incidencias. |
| Deuda técnica estimada | **8 h 47 min** | Tiempo estimado por SonarQube para abordar incidencias; no un plazo contractual ni esfuerzo medido. |
| Archivos / líneas de código analizadas | **83 / 7467** | Alcance histórico del proyecto en ese escaneo. |

**Limitación de seguridad:** SonarQube Community Build no sustituye análisis de vulnerabilidades de dependencias, revisiones de autorización, OWASP, pruebas dinámicas ni pentesting. Recomendamos leer también [04 OWASP](04%20OWASP%20V_1_0_0.md) y [05 WCAG](05%20WCAG%20V_1_0_0.md).

## 3. Cambios posteriores al escaneo que hacen necesario repetirlo

Entre `9b31dd0` y `e7e4a00d`, comprobamos en GitHub:

- Correcciones de durabilidad y consistencia ante errores de escritura en `backend/src/app/auth/archivo_repository.py` y `backend/src/app/rutas/guardadas.py`, con nuevas pruebas.
- Integración real de pedidos y flota en PostgreSQL/PostGIS aislado, en `backend/tests/integracion/test_postgis.py`, añadida a CI.
- Benchmark sintético con umbral de **45 segundos** que ahora falla cuando se supera y tiene pruebas de regresión.
- Pruebas adicionales de contratos OpenAPI y autorización HTTP.
- Ajustes del dashboard para distinguir **emisiones estimadas** y **puntualidad prevista** de indicadores operativos observados.
- Cambios y ampliaciones documentales posteriores, además de un análisis adicional de SonarQube del equipo sobre el commit `9b31dd0`.

No asignamos nuevos porcentajes de cobertura, número de incidencias, calificaciones o Quality Gate al commit `e7e4a00d` sin ejecutar **SonarScanner sobre ese commit**. Los cambios posteriores pueden modificar las métricas en cualquier dirección.

## 4. Calidad que debemos mejorar o volver a comprobar

| Hallazgo histórico | Qué revisamos en el siguiente análisis | Criterio de verificación |
|---|---|---|
| Fiabilidad **C** (3 incidencias: `S6772`, `S6845`, `S7758`) | Si permanecen; validar comportamiento de teclado y accesibilidad antes de aceptar falsas alarmas | Registrar regla, componente, decisión y estado del hallazgo |
| Complejidad `S3776` en `PaginaRutas.tsx` | Si está vigente tras los cambios y refactorizar cuando corresponda | Evitar regresión funcional; prueba UI/estática |
| **101 code smells** | Distribución nueva por regla; priorizar severidad alta y fiabilidad | Comparar **misma base/alcance** antes de atribuir mejora |
| Cobertura **82,8 %** | Cobertura total y de módulos PostgreSQL, API y frontend | Importar XML/LCOV de la misma revisión, no mezclar commits |
| Deuda **8 h 47 min** | Deuda medida en la nueva revisión y su impacto relativo | No sumar ni restar tiempos sin resultado SonarQube |
| Calidad de seguridad | Complementar SonarQube con `npm audit`, `pip-audit`, revisión OWASP y pruebas de autorización | No convertir «0 vulnerabilidades detectadas» en una garantía absoluta |

La **meta previamente propuesta** en la retrospectiva es cero incidencias de severidad alta, fiabilidad A, menos de 60 code smells y cobertura igual o superior al 85 %. **Es una meta**, no el resultado ya obtenido.

## 5. Ejecutar un reanálisis auténtico sobre el último `main`

La instancia usada en el informe anterior está configurada en **`http://localhost:9000`**, es decir, en un equipo local. No está disponible desde la conexión GitHub ni desde los runners públicos de GitHub Actions; necesitamos ejecutar SonarScanner en el equipo con esa instancia encendida o configurar un servidor accesible.

1. En el equipo donde funciona SonarQube, actualizamos la copia de trabajo hasta el commit que queremos medir, sin cambios locales pendientes: `git checkout main` y `git pull --ff-only`.
2. Verificamos Node.js, Python 3.10, SonarScanner CLI y el entorno virtual `backend/.venv` con `backend/requirements.txt` instalado.
3. Configuramos la variable de entorno **`SONAR_TOKEN` solo en el equipo local**; no la añadimos a `.env.example`, documentos, chats, capturas, argumentos de línea ni commits.
4. Desde la raíz del repositorio, ejecutamos `./scripts/analizar-sonarqube.ps1` en PowerShell. Por defecto usa `http://localhost:9000`; aceptamos `-SonarUrl` para un servidor autorizado diferente.
5. El script ejecuta pytest con XML de cobertura, `npm ci`, Vitest con LCOV, SonarScanner, y espera el Quality Gate antes de recuperar métricas de la API. Si falla una etapa, **no publica un resultado inventado**.
6. Tras un análisis aprobado, genera localmente `docs/03 Implementación/Sprint 03/SONARQUBE-ULTIMO-ANALISIS.md`, con **commit, fecha y valores reales**. Lo revisamos, añadimos evidencia del panel e incidencias y lo incorporamos al repositorio mediante Pull Request.
7. Si el Quality Gate falla, inspeccionamos la causa en SonarQube, registramos hallazgos y corregimos antes de repetir. No reemplazamos el informe histórico con métricas nuevas fallidas o parciales.

**Importante:** la medición de cobertura requiere los reportes `backend/coverage.xml` y `frontend/coverage/lcov.info` generados **antes** del scanner. SonarQube los importa, no ejecuta automáticamente las pruebas. Las pruebas PostGIS que viven en otro job de CI no se incluyen por arte de magia en la cobertura local; si queremos medirlas, debemos ejecutarlas contra una base de pruebas y unir sus resultados en el mismo reporte de cobertura, sin contaminar datos productivos.

### Procedimiento mínimo en Windows

```powershell
git checkout main
git pull --ff-only
# En la terminal local ya debe existir SONAR_TOKEN.
# El servidor SonarQube y el entorno backend/.venv deben estar disponibles.
./scripts/analizar-sonarqube.ps1
```

**Referencias oficiales:** [SonarScanner CLI](https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/sonarscanner) · [Importación de cobertura](https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/test-coverage/test-coverage-parameters) · [Quality Gate en análisis](https://docs.sonarsource.com/sonarqube-server/2025.6/analyzing-source-code/analysis-parameters/parameters-not-settable-in-ui).

## 6. Conclusión y estado de la evidencia

**Validado:** el informe del Sprint 3 contiene resultados concretos, explicación y captura; su versión 1.1.0 puede usarse como **resultado histórico del commit `9b31dd0`**.

**Pendiente:** un reanálisis efectivo del commit `e7e4a00d` —o del último `main` vigente cuando se ejecute el script— en una instancia SonarQube accesible. No se ha realizado este reanálisis en la presente verificación y **no podemos declarar un Quality Gate SonarQube nuevo**.

Este documento es una **validación documental de vigencia**, no una sustitución del informe medido ni evidencia de ejecución remota.
