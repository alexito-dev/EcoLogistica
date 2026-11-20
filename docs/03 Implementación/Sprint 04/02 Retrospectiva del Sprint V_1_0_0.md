# Retrospectiva del sprint

[← Volver al README principal](../../../README.md#93-fase-03-implementación)

**Nombre del Proyecto:** EcoLogística Huancayo — Plataforma de Optimización de Rutas Sostenibles de Última Milla

**Líder del Proyecto:** Zorrilla Apumayta, Alex Jesus

## ¿Qué aprendimos?

1. **Un selector ambiguo falla en silencio.** La primera prueba del formulario de pedidos escribía la dirección en el buscador de la lista y no en el formulario, porque `getByLabel('Dirección')` coincidía con ambos. Desde entonces los campos de un diálogo se buscan dentro del propio diálogo (`getByRole('dialog')`).
2. **Las pruebas deben respetar el diseño de seguridad, no esquivarlo.** El segundo factor TOTP acepta cada código una sola vez: dos ingresos de la misma cuenta en menos de 30 s obligan a esperar la ventana siguiente. Mantuvimos esa regla en lugar de desactivar el MFA; el costo es una suite larga, que se mitiga ejecutando los tres navegadores en paralelo en CI.
3. **Una suposición sobre la interfaz es un defecto de la prueba hasta demostrar lo contrario.** Dos pruebas de resiliencia esperaban el botón «Continuar» habilitado tras un error de red; por diseño la contraseña se borra tras cada rechazo y el botón se bloquea. La prueba ahora verifica ese comportamiento.
4. **Un navegador instalado no es un navegador ejecutable.** En la máquina de desarrollo Firefox de Playwright no arranca (falta el runtime de Visual C++); se verificó en GitHub Actions, donde además aparecieron fallos que localmente no se veían (axe-core sobre el mapa en Firefox y una espera intermitente en WebKit). Se corrigieron en `5f750bf`.
5. **Los flujos reutilizables de GitHub Actions comparten grupos de concurrencia.** Dentro de un flujo llamado, `github.workflow` vale el nombre del flujo que lo invoca; con `group: ${{ github.workflow }}-${{ github.ref }}`, `ci.yml` y `tests.yml` llamados desde `deploy-production.yml` quedaban en el mismo grupo y se cancelaban entre sí (y cancelaban el despliegue: ejecuciones #1 a #3). El grupo es ahora `${{ github.workflow }}-ci-${{ github.ref }}` y `${{ github.workflow }}-tests-${{ github.ref }}`, distinto para cada flujo y para cada invocador.
6. **Un despliegue sin destino configurado debe decirlo.** `deploy-production.yml` valida el código y, si faltan los secretos del alojamiento, publica «no se desplegó» en el resumen en vez de terminar en verde sin haber hecho nada.
7. **Una prueba de base de datos real encuentra lo que la memoria no.** La prueba de ventana por día de Lima usaba desplazamientos erróneos; solo falló contra PostgreSQL en CI y se corrigió en `8728dad`.
8. **Medir antes de optimizar.** El cambio a Preact, el CSS en línea y la compresión redujeron la carga de 1 211 513 B a 41 872 B (−96,5 %) porque se partió de mediciones con Lighthouse, no de suposiciones.

## ¿Qué estamos haciendo bien?

- **Cuatro capas de verificación automática:** `ci.yml` (estilo, análisis estático, compilación y dependencias), `tests.yml` (unitarias, integración con PostGIS y E2E en tres navegadores), `green-audit.yml` (Lighthouse) y la validación de especificaciones OpenSpec.
- **Honestidad documental:** cada documento separa lo medido de lo pendiente; el SUS se informa con su muestra (n = 5, estudiantes y egresados) y sus límites, y las métricas que no se registraron (finalización y tiempo por tarea) se declaran como tales.
- **Pruebas deterministas contra servicios reales:** la API y la interfaz arrancan con datos temporales y aislados; ninguna prueba toca una base real.
- **Convenciones de equipo:** Conventional Commits, ramas `sprint-N/*` que activan el CI, especificaciones OpenSpec por capacidad y documentación versionada con enlaces de ida y vuelta.
- **Seguridad por defecto:** TOTP cifrado en reposo, cookies `HttpOnly` y `SameSite=Strict`, y pruebas que verifican cabeceras de endurecimiento y que los errores no filtren trazas.

## ¿Qué podemos hacer mejor?

### Personas

- Firefox solo pudo ejecutarse en CI; conviene que más de una persona pueda reproducir la suite en los tres navegadores.
- El SUS se aplicó a 5 estudiantes y egresados, pero en las sesiones no se registró quién completó cada tarea ni cuánto tardó; en la próxima medición hay que llevar una hoja de observación por persona.

### Relaciones

- Las personas de Planificación y Conducción de DistriRápido S.A.C. son quienes pueden responder el SUS de forma representativa; no hubo una sesión de demostración con ellas en este sprint y debe coordinarse.
- Frontend y backend deben acordar los endpoints de operación (como `/health`) antes de escribir las pruebas que dependen de ellos: la API no tenía sonda de disponibilidad hasta este sprint.
- La documentación de Hilario Talavera y la del resto del equipo se redactaron en paralelo y hubo que reconciliarlas; conviene acordar una sola estructura de carpetas antes de empezar.

### Procesos

- La decisión sobre el destino del despliegue (qué alojamiento y qué base PostGIS administrada) sigue sin tomarse; el flujo está listo, pero sin esa decisión no hay entorno que verificar.
- La protección de `main` y la revisión por pares siguen pendientes ([README 7.1](../../../README.md#71-ramas-y-revisión)).
- Las tarjetas de Jira de parte del alcance no están creadas; sin ellas no se mide la velocidad del sprint.
- Las estimaciones de las tareas de integración (E2E con TOTP, despliegue) fueron optimistas; conviene hacer pruebas de concepto antes de comprometerlas.

### Herramientas

- La suite E2E completa en Chromium tarda varios minutos por la regla del TOTP; conviene medir el tiempo por vista y valorar un modo de prueba con el mismo cifrado pero reloj controlado.
- No hay entorno de *staging*: la prueba de humo posterior al despliegue (`disponibilidad.spec.ts` con `ECO_BASE_URL`) solo puede ejecutarse contra producción.
- SonarQube sigue sin ejecutarse en CI porque faltan los secretos `SONAR_TOKEN` y `SONAR_HOST_URL`.

### Acciones a realizar

| # | Acción | Responsable | Fecha límite | Métrica de seguimiento |
|---|---|---|---|---|
| 1 | Mantener los tres navegadores en verde y tratar cada reintento como hallazgo, no como aprobación | Isidro Casio | 27/11/2026 | Cero pruebas marcadas *flaky* en tres ejecuciones consecutivas de `tests.yml` |
| 2 | Cargar en GitHub el secreto `DEPLOY_SSH_KEY` y la variable `PRODUCTION_URL` para que `deploy-production.yml` publique en el VPS sin intervención manual | Anco Porras, con aprobación de Zorrilla Apumayta, Alex Jesus | 27/11/2026 | `deploy-production.yml` con el trabajo «Desplegar a producción» en verde y `/health` respondiendo 200 |
| 3 | Repetir el SUS con al menos 5 personas de Planificación y Conducción de DistriRápido S.A.C., registrando finalización, tiempo y errores por tarea (T1–T6) | Vera Zea | 30/11/2026 | Documento 04 en versión 1.2.0 con SUS ≥ 68 y finalización ≥ 80 % |
| 4 | Definir `SONAR_TOKEN` y `SONAR_HOST_URL` para activar la puerta de calidad de SonarQube en CI | Isidro Casio | 27/11/2026 | Paso de SonarQube ejecutado y *Quality Gate* en verde |
| 5 | Activar la protección de `main` (PR obligatorio y CI en verde) | Zorrilla Apumayta, Alex Jesus | 27/11/2026 | Ningún commit directo a `main` posterior a esa fecha |
| 6 | Crear en Jira las tarjetas de este alcance y estimarlas | Zorrilla Apumayta, Alex Jesus | 25/11/2026 | Tarjetas con puntos y vinculadas a los commits del Sprint 4 |
| 7 | Resolver los hallazgos de usabilidad H4 (revertir una entrega), H5 (asignar conductor a varios vehículos) y H9 (manual breve) | Vera Zea y Hilario Talavera | 04/12/2026 | Hallazgos cerrados en la [evaluación heurística](09%20Evaluaci%C3%B3n%20heur%C3%ADstica%20de%20Nielsen%20V_1_0_0.md) |
| 8 | Medir el tiempo por prueba E2E y reducir la espera del TOTP en CI sin desactivar el MFA | Isidro Casio, Hilario Talavera | 04/12/2026 | Duración del trabajo E2E por navegador menor a 10 minutos |
