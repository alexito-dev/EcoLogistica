# Guion de exposición del Sprint 3

**Duración total:** 20 minutos (16 de exposición y 4 de preguntas). **Orden:** según la tabla. Cada quien lee solo su parte; los cambios de turno están marcados con **→ Pasa a …**.

| Turno | Integrante | Tema | Tiempo |
|:---:|---|---|:---:|
| 1 | Alex Zorrilla | Apertura y meta del sprint | 2 min |
| 2 | Jhean Anco | Rutas guardadas y servicios API (demo) | 4 min |
| 3 | Alexander Hilario | Optimización y rendimiento (benchmark) | 3 min |
| 4 | Jhoanna Vera | Interfaz y accesibilidad (WCAG) | 3 min |
| 5 | Jose Luis Isidro | Calidad y seguridad (SonarQube y OWASP) | 3 min |
| 6 | Alex Zorrilla | Cierre y Sprint 4 | 1 min |
| — | Todos | Preguntas | 4 min |

---

## Turno 1 — Alex Zorrilla: apertura y meta del sprint

> **Mostrar:** documento *03.2 Informe de estado* (tabla de 5 de 5 criterios).

Buenos días. Somos el equipo de EcoLogística Huancayo y presentamos el Sprint 3.

La meta de este sprint fue que el planificador pueda **calcular las rutas de reparto, mostrarlas en el mapa y guardarlas** para volver a abrirlas.

Resultado: **se cumplen los 5 de 5 criterios** de la meta. En la reunión del 29 de octubre eran 3 de 5, porque la ruta todavía no se guardaba. Después lo implementamos y ahora sí se guarda.

Hoy van a ver cuatro cosas: las rutas guardadas, el rendimiento, la accesibilidad y la calidad del código.

**→ Pasa a Jhean.**

---

## Turno 2 — Jhean Anco: rutas guardadas y servicios API

> **Mostrar:** (1) en la app, pantalla Rutas → «Guardar rutas» → recargar la página → «Abrir rutas guardadas»; (2) `localhost:8001/docs` con `POST /rutas/guardar` y `GET /rutas/guardada`.

Yo les cuento lo que se agregó en el servidor.

Hay dos servicios nuevos. Uno **guarda** las rutas de una fecha y otro **las vuelve a abrir**. Solo pueden usarlos el rol Planificación y el Administrador. Conductor, Gerente y Auditor reciben un error de permiso.

Si no hay rutas calculadas, el sistema avisa y no guarda nada. Si la fecha no es válida, también rechaza la petición.

Por ahora las rutas se guardan en un **archivo local**, igual que las cuentas de usuario. En el Sprint 4 pasan a **PostgreSQL con PostGIS**, junto con las cuentas, y ahí también ciframos los secretos del segundo factor.

Esto tiene **10 pruebas automáticas nuevas** y está documentado en la especificación de rutas.

**→ Pasa a Alexander.**

---

## Turno 3 — Alexander Hilario: optimización y rendimiento

> **Mostrar:** en la terminal, `python scripts/benchmark_rutas.py` (dura unos 3 segundos) y la tabla que imprime.

Mi parte es el motor que calcula las rutas.

Primero, **reducimos su complejidad**. La función principal tenía complejidad 23 y la dividimos en funciones pequeñas hasta quedar en 15 o menos. El resultado de las rutas no cambió: las 16 pruebas del planificador siguen pasando.

Segundo, medimos el **tiempo de cálculo** con un benchmark que se puede repetir. El objetivo es calcular en menos de 45 segundos.

Con datos sintéticos, estos son los resultados:

- 25 pedidos: 0,14 segundos.
- 50 pedidos: 0,35 segundos.
- 100 pedidos: 0,82 segundos.
- 150 pedidos con 12 vehículos: **1,13 segundos**.

Son datos de prueba. Con pedidos reales lo vamos a repetir en el Sprint 4.

**→ Pasa a Jhoanna.**

---

## Turno 4 — Jhoanna Vera: interfaz y accesibilidad

> **Mostrar:** el aviso de sesión con su prueba (`AvisoSesion.test.tsx`) y el documento *05 WCAG* (40 de 45 criterios).

Yo les muestro lo que ve el usuario.

En la pantalla **Rutas** hay un botón nuevo, **«Guardar rutas»**. Al guardar, aparece un aviso con **quién guardó y cuándo**. Al volver a abrir esa fecha se muestran las rutas guardadas, y un botón permite alternar entre lo guardado y el cálculo actual.

También agregamos un **aviso de sesión**. Dos minutos antes de que se cierre por inactividad aparece un mensaje con cuenta regresiva y el botón **«Seguir conectado»**. Esto responde al criterio 2.2.1 de accesibilidad.

En accesibilidad WCAG 2.2 nivel AA cumplimos **40 de 45 criterios, es decir 88,9 %**. La meta es 90 %, así que nos falta poco. Los criterios pendientes ya están en el plan del Sprint 4.

**→ Pasa a Jose Luis.**

---

## Turno 5 — Jose Luis Isidro: calidad y seguridad

> **Mostrar:** (1) panel de SonarQube o, si no abre, el documento *03 Calidad de código*; (2) terminal con `pytest` y `vitest` en verde; (3) documento *04 OWASP*; (4) pestaña Actions de GitHub.

Yo les resumo la calidad y la seguridad.

En **SonarQube** el Quality Gate quedó **aprobado (PASSED)**, con **0 vulnerabilidades**, **0 bugs** y **0,0 % de duplicación**. La cobertura es **82,8 %** (backend y frontend). Quedan 101 code smells por reducir y la fiabilidad está en C por 3 incidencias abiertas, que están en el plan del Sprint 4.

En las pruebas automáticas, el backend tiene **137 pruebas** con **92,6 % de cobertura**, y el frontend tiene **58 pruebas**. Todas pasan.

En seguridad revisamos el proyecto contra **OWASP Top 10:2025** y dejamos documentado el estado de cada categoría.

La **integración continua** en GitHub ahora corre en las ramas del sprint y en las de funcionalidades: verifica backend, migraciones, frontend y especificaciones.

**→ Pasa a Alex.**

---

## Turno 6 — Alex Zorrilla: cierre y Sprint 4

> **Mostrar:** la lista de tareas del Sprint 4 en el *Plan de trabajo*.

Para cerrar: el Sprint 3 cumplió su meta, con las rutas calculadas, mostradas, guardadas y reabiertas.

En el **Sprint 4** vamos a:

- Pasar rutas y cuentas a PostgreSQL con PostGIS.
- Repetir el benchmark con pedidos reales.
- Volver a ejecutar SonarQube.
- Subir la accesibilidad por encima del 90 %.

Gracias por su atención. Quedamos atentos a sus preguntas.

---

## Preguntas probables (quién responde)

| Pregunta | Responde |
|---|---|
| ¿Dónde se guardan las rutas ahora? | Jhean |
| ¿Por qué los tiempos son tan bajos? | Alexander |
| ¿Qué falta para llegar a 90 % en WCAG? | Jhoanna |
| ¿Se volvió a ejecutar SonarQube? | Jose Luis |
| ¿Por qué eran 3 de 5 el 29 de octubre y ahora 5 de 5? | Alex |

## Recomendaciones para leer

- Hablen despacio y mirando al público de vez en cuando.
- Respeten el tiempo de cada turno; si alguien se alarga, el siguiente recorta.
- Lean las cifras tal como están escritas y no inventen otras.
- Antes de exponer, abran en local la aplicación (http://localhost:3000) por si piden mostrar el botón «Guardar rutas».
