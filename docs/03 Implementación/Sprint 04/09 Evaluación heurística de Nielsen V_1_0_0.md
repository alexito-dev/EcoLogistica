# Evaluación heurística de Nielsen — inspección de la interfaz (Sprint 4)

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Fecha | 13/11/2026 |
| Método | Inspección experta con las 10 heurísticas de Nielsen sobre la aplicación en ejecución (Planificación y Conducción) |
| Quién la hizo | El desarrollador con asistencia de IA, recorriendo los flujos reales en el navegador y en las pruebas E2E |
| Documento relacionado | [04 Usabilidad SUS y Nielsen](08%20Protocolo%20SUS%20y%20Nielsen%20V_1_0_0.md) |

> **Alcance honesto.** Esta es una **evaluación heurística de expertos (una sola persona evaluadora)**, que la propia metodología reconoce como complementaria. **No es** una prueba con usuarios y **no produce una puntuación SUS**: esa escala solo existe con respuestas reales de personas, y por eso sigue pendiente de aplicarse (ver documento 04). Los hallazgos de abajo son observaciones reales de la aplicación, no resultados inventados.

## 1. Hallazgos y acciones

Severidad según Nielsen: 0 = no es un problema; 1 = cosmético; 2 = menor; 3 = mayor; 4 = catastrófico.

| # | Heurística | Hallazgo observado | Sev. | Acción |
|---|---|---|:---:|---|
| H1 | 1. Visibilidad del estado | Planificación guarda las rutas del **día siguiente**, pero «Mi ruta» y «Seguimiento» abrían en el día de **hoy** y mostraban «No hay rutas», lo que confundía (se vio al probar el flujo en el navegador). | 3 | **Corregido:** si hoy no hay rutas y mañana sí, la vista abre en mañana y lo avisa con un mensaje. Prueba en `Conduccion.test.tsx`. |
| H2 | 5. Prevención de errores | «Reprogramar» cerraba la incidencia con un solo clic y no se puede deshacer. | 3 | **Corregido:** ahora pide confirmación («¿Devolver el pedido a Pendiente? Esta incidencia quedará cerrada») con botones Confirmar y Cancelar. Cubierto por prueba unitaria y E2E. |
| H3 | 9. Reconocer y corregir errores | Los errores de importación mostraban nombres técnicos de campo. | 2 | **Corregido en el diseño:** la importación informa «fila N · columna» con el nombre de la columna de la plantilla y un mensaje legible; cada error aparece en una lista dentro de una alerta. |
| H4 | 3. Control y libertad | Un pedido marcado **Entregado** por error no se puede revertir (estado final). | 3 | **Pendiente de decisión de negocio:** requiere una regla acordada con Planificación (por ejemplo, ventana de corrección de pocos minutos con registro). No se cambia sin esa regla. |
| H5 | 7. Flexibilidad y eficiencia | Para asignar el mismo conductor a varios vehículos hay que elegirlo uno por uno. | 2 | **Pendiente:** mejora de productividad (asignación masiva); no bloquea ninguna tarea. |
| H6 | 4. Consistencia | Las vistas de Planificación y Conducción reutilizan los mismos componentes (encabezado, insignias de estado, botones, filtros de fecha) y la misma redacción. | 0 | Sin acción. |
| H7 | 6. Reconocer en lugar de recordar | El menú muestra solo las vistas del rol y el pie incluye un mapa de navegación; las acciones de cada parada dependen de su estado actual (no se ofrece «Entregado» si aún no salió). | 0 | Sin acción. |
| H8 | 8. Diseño minimalista | La vista «Mi ruta» combina mapa y lista; en pantallas pequeñas la lista queda debajo del mapa. | 1 | Aceptado; se verificó sin desplazamiento horizontal al 200 % de zoom. |
| H9 | 10. Ayuda y documentación | La importación explica el formato de fecha y el carácter de todo o nada junto al botón de carga; no hay manual de usuario general. | 2 | **Pendiente:** manual breve para personas usuarias. |
| H10 | 2. Relación con el mundo real | Estados y textos usan el vocabulario de reparto (En ruta, Entregado, Incidencia, Reprogramar); las horas se muestran en hora de Lima. | 0 | Sin acción. |

**Resumen:** de severidad 3, 2 corregidos y 1 pendiente de una regla de negocio; de severidad 2, 1 corregido y 2 pendientes de producto. Ningún hallazgo de severidad 4.

## 2. Lo que sigue pendiente de verdad

- La **puntuación SUS** se obtuvo después con 5 personas (77,5, grado B+; ver el [documento 04](04%20Usabilidad%20V_1_0_0.md)); falta aplicarla a personal de la empresa.
- Las decisiones H4, H5 y H9 quedan en el backlog para que el equipo y el Product Owner las prioricen.
