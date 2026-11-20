# Retrospectiva del sprint

[← Volver al README principal](../../../README.md#93-fase-03-implementación)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla

**Líder del Proyecto:** Zorrilla Apumayta, Alex Jesus

## Metadatos del documento

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Fecha | 20/11/2026 |
| Sprint | ECO Sprint 5 — CI/CD, Playwright en tres navegadores, rendimiento, disponibilidad y usabilidad SUS |
| Rama | `sprint-5/cicd-playwright-usabilidad` |
| Fuentes | Historial de Git, [Revisión del Sprint 5](01%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md), [Análisis Playwright](03%20Analisis%20PlayWrigth%20V_1_0_0.md), [Usabilidad](04%20Usabilidad%20V_1_0_0.md) |
| Retrospectiva anterior | [Retrospectiva del Sprint 3](../Sprint%2003/02%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) |

> **Cómo se redactó.** Los aprendizajes y los problemas provienen de la evidencia del repositorio y de las ejecuciones de este sprint (commits, registros de las pruebas, errores reales encontrados). Los responsables de las acciones se proponen según el rol de cada integrante en el [README](../../../README.md#4-equipo-de-trabajo-y-responsabilidades); el equipo los confirma en la sesión de retrospectiva y deja constancia en Jira.

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 20/11/2026 | Hilario Talavera, Alexander Daniel | Primera emisión con aprendizajes, aciertos y acciones medibles en las cuatro dimensiones. |

## ¿Qué aprendimos?

1. **Un selector ambiguo falla en silencio.** La primera versión de la prueba del formulario de pedidos escribía la dirección en el *buscador* de la lista y no en el formulario, porque `getByLabel('Dirección')` coincidía con ambos. La prueba no falló al escribir, sino al comprobar el resultado. Desde entonces, los campos de un diálogo se buscan dentro del propio diálogo (`getByRole('dialog')`).
2. **Las pruebas deben respetar el diseño de seguridad, no esquivarlo.** El segundo factor TOTP solo acepta cada código una vez: dos ingresos de la misma cuenta en menos de 30 s obligan a esperar la ventana siguiente. Por eso cada prueba con sesión tarda entre 18 s y 40 s. Mantuvimos esa regla en lugar de desactivar el MFA en pruebas; el costo es una suite larga, que se mitiga ejecutando los tres navegadores en paralelo en CI.
3. **Una suposición sobre la interfaz es un defecto de la prueba hasta demostrar lo contrario.** Dos pruebas de resiliencia esperaban que el botón «Continuar» siguiera habilitado tras un error de red. Era falso por diseño: la contraseña se borra tras cada rechazo y el botón se bloquea hasta escribirla de nuevo. La prueba ahora verifica ese comportamiento (correo conservado, reintento posible).
4. **Un navegador instalado no es un navegador ejecutable.** En la máquina de desarrollo, Firefox de Playwright no arranca (`spawn UNKNOWN`: falta el runtime de Visual C++, error de configuración en paralelo), mientras Chromium y WebKit sí. Las pruebas de Firefox se verificaron en GitHub Actions, no localmente; allí además apareció algo que local no se veía: Firefox se cuelga al ejecutar axe-core sobre el mapa de «Mi ruta», y WebKit tuvo una espera intermitente. La primera ejecución de CI falló por eso; se corrigió en el siguiente commit.
5. **Los flujos reutilizables de GitHub Actions comparten grupos de concurrencia.** Con `group: ci-${{ github.ref }}` el CI invocado desde `deploy-production.yml` habría cancelado al CI disparado por el mismo `push`. El grupo usa ahora `${{ github.workflow }}` (en un flujo invocado vale el nombre del flujo llamador).
6. **Un despliegue sin destino configurado debe decirlo.** `deploy-production.yml` valida el código y, si faltan los secretos del hosting, publica en el resumen «no se desplegó» en vez de terminar en verde sin haber hecho nada.

## ¿Qué estamos haciendo bien?

- **Cuatro capas de verificación automática:** `ci.yml` (estilo, análisis estático, compilación y dependencias), `tests.yml` (unitarias, integración con PostGIS y E2E en tres navegadores), `green-audit.yml` (Lighthouse) y la validación de especificaciones OpenSpec.
- **Honestidad documental sostenida:** cada documento separa lo medido de lo pendiente; no hay puntuación SUS ni URL de producción porque no existen datos reales todavía.
- **Pruebas deterministas contra servicios reales:** la API y la interfaz arrancan con datos temporales y aislados; ninguna prueba toca una base real.
- **Convenciones de equipo:** Conventional Commits, ramas `sprint-N/*` que activan el CI y documentación versionada con enlaces de ida y vuelta.
- **Seguridad por defecto:** las pruebas de disponibilidad comprueban además las cabeceras de endurecimiento y que los errores no filtren trazas internas.

## ¿Qué podemos hacer mejor?

### Personas

- Firefox no pudo ejecutarse en la máquina de desarrollo de este sprint; su verificación depende de GitHub Actions o de un equipo con el runtime de Visual C++ completo. Conviene que más de una persona pueda reproducir la suite en los tres navegadores.
- La evaluación SUS necesita participantes que no pertenecen al equipo de desarrollo; reclutarlos no tiene responsable asignado hasta ahora.

### Relaciones

- Las personas de Planificación y Conducción de DistriRápido S.A.C. son quienes pueden responder el SUS de forma representativa; el [Sprint 4](../Sprint%2004/01%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md#4-límites-y-trabajo-que-sigue-abierto) ya dejó esa medición pendiente y hace falta coordinar con ellas una sesión.
- La API no tenía una sonda de disponibilidad (`/health`) hasta este sprint, aunque el despliegue y el monitoreo la necesitan; conviene acordar entre frontend y backend los endpoints de operación antes de escribir las pruebas que dependen de ellos.

### Procesos

- Las decisiones sobre el destino del despliegue (qué hosting, qué base PostGIS administrada) siguen sin tomarse; el flujo está listo, pero sin esa decisión no hay entorno que verificar.
- La protección de `main` y la revisión por pares siguen pendientes ([README 7.1](../../../README.md#71-ramas-y-revisión)): los cambios de este sprint se integran por Pull Request desde una rama de sprint.
- Las tarjetas de Jira de este alcance no están creadas; sin ellas la velocidad del Sprint 5 no se puede medir.

### Herramientas

- La suite E2E completa en Chromium tarda varios minutos por la regla del TOTP; conviene medir el tiempo por vista en CI y valorar un modo de prueba con el mismo cifrado pero reloj controlado.
- No hay entorno de *staging*: la prueba de humo posterior al despliegue (`disponibilidad.spec.ts` con `ECO_BASE_URL`) solo se ejecutará contra producción.
- SonarQube sigue sin ejecutarse en CI porque faltan los secretos `SONAR_TOKEN` y `SONAR_HOST_URL`.

### Acciones a realizar

| # | Acción | Responsable propuesto (por rol) | Fecha límite | Métrica de seguimiento |
|---|---|---|---|---|
| 1 | Mantener los tres navegadores en verde y vigilar las pruebas intermitentes (reintento = hallazgo, no aprobación) | Isidro Casio, Jose Luis (Calidad / operaciones) | 27/11/2026 | Cero pruebas marcadas *flaky* en tres ejecuciones consecutivas de `tests.yml` |
| 2 | Decidir el hosting de producción, crear los servicios y definir `DEPLOY_HOOK_BACKEND`, `DEPLOY_HOOK_FRONTEND`, `PRODUCTION_URL` y `PRODUCTION_API_URL` | Anco Porras, Jhean Pier Julio (Arquitectura) con aprobación de Zorrilla Apumayta, Alex Jesus | 27/11/2026 | Ejecución de `deploy-production.yml` con el trabajo `Desplegar a producción` en verde y `/health` respondiendo 200 |
| 3 | Aplicar la encuesta SUS a por lo menos 5 personas con las tareas T1–T6 y registrar el resultado con `procesar_sus.py --markdown` | Vera Zea, Jhoanna Hade (Interfaz / UX) | 30/11/2026 | Documento 04 en versión 1.1.0 con n ≥ 5 y SUS promedio calculado |
| 4 | Definir las variables `SONAR_TOKEN` y `SONAR_HOST_URL` para activar la puerta de calidad de SonarQube en CI | Isidro Casio, Jose Luis | 27/11/2026 | Paso de SonarQube ejecutado y *Quality Gate* en verde |
| 5 | Activar la protección de `main` (PR obligatorio y CI en verde) | Zorrilla Apumayta, Alex Jesus | 27/11/2026 | Ningún commit directo a `main` en el historial posterior a esa fecha |
| 6 | Crear en Jira las tarjetas de este alcance y estimarlas | Zorrilla Apumayta, Alex Jesus | 25/11/2026 | Tarjetas con puntos y vinculadas a los commits del Sprint 5 |
| 7 | Resolver los hallazgos de usabilidad pendientes H4 (revertir una entrega), H5 (asignar conductor a varios vehículos) y H9 (manual breve) | Vera Zea, Jhoanna Hade y Anco Porras, Jhean Pier Julio | 04/12/2026 | Hallazgos cerrados en el [documento de evaluación heurística](../Sprint%2004/05%20Evaluaci%C3%B3n%20heur%C3%ADstica%20de%20Nielsen%20V_1_0_0.md) |
| 8 | Medir el tiempo por prueba E2E y reducir la espera del TOTP en CI sin desactivar el MFA | Isidro Casio, Jose Luis | 04/12/2026 | Duración total del trabajo E2E por navegador menor a 10 minutos |
