# 03. Registro de riesgos

[← Volver al README Principal](../../README.md)

## Metadatos

| Campo | Valor |
|---|---|
| Proyecto | EcoLogística Huancayo |
| Versión | 1.0.0 |
| Fecha | 11 de septiembre de 2026 |
| Escala | Probabilidad e impacto de 1 a 5; exposición = P × I |

## 1. Criterios

| Exposición | Nivel |
|---:|---|
| 1–6 | Baja |
| 8–12 | Media |
| 15–25 | Alta |

## 2. Matriz de evaluación y respuesta

| ID | Descripción del riesgo | Categoría | P | I | Severidad | Plan de mitigación (preventivo) | Plan de contingencia (reactivo) | Responsable |
|---|---|---|---:|---:|---:|---|---|---|
| RSK-01 | Cuotas o indisponibilidad del proveedor cloud impiden desplegar el PMV. | Técnica / Infraestructura | 2 | 4 | **8 Media** | Alertas al 70%, límites por entorno y configuración reproducible. | Reducir entorno a staging, restaurar desde imagen y usar proveedor alterno. | Isidro Casio |
| RSK-02 | El motor no entrega solución dentro de 45 s con 150 pedidos. | Técnica / Rendimiento | 3 | 5 | **15 Alta** | Pruebas de carga desde la iteración 1, límites de tiempo y benchmark por tamaño. | Entregar mejor solución parcial, permitir ejecución asíncrona y escalar recursos. | Hilario Talavera |
| RSK-03 | Direcciones ambiguas producen coordenadas incorrectas. | Datos / Operación | 3 | 4 | **12 Media** | Confianza mínima, revisión manual y muestra de validación de 100 direcciones. | Excluir el pedido, solicitar punto de referencia y no publicar ruta insegura. | Anco Porras |
| RSK-04 | Cambios de requisitos afectan alcance y fechas. | Gestión | 4 | 4 | **16 Alta** | Backlog priorizado, control de cambios y aceptación por Sprint. | Replanificar, usar reserva y diferir alcance no esencial. | Alex Zorrilla |
| RSK-05 | Baja adopción por interfaz compleja o conectividad limitada. | Usuario / Social | 3 | 4 | **12 Media** | Pruebas con despachadores y conductores, WCAG 2.1 AA y modo de bajo consumo. | Capacitación, modo offline de última ruta y soporte guiado. | Jhoanna Vera |
| RSK-06 | Exposición de datos personales o credenciales. | Seguridad / Legal | 2 | 5 | **10 Media** | Datos sintéticos, mínimo privilegio, secretos fuera de Git y revisión OWASP. | Revocar sesiones, rotar secretos, preservar auditoría y activar protocolo de incidente. | Anco Porras |
| RSK-07 | Retraso por defectos detectados al integrar frontend y backend. | Calidad | 3 | 4 | **12 Media** | Contratos API, integración continua, revisión por PR y pruebas automatizadas. | Congelar cambios, priorizar defectos críticos y reducir alcance del Sprint. | Jose Luis Isidro |
| RSK-08 | Incremento de precios cloud, mapas o licencias supera el presupuesto. | Financiera | 3 | 3 | **9 Media** | Preferir OSM/Leaflet, cuotas, presupuesto mensual y alternativas open source. | Desactivar servicios no esenciales y migrar a componentes de menor costo. | Alex Zorrilla |
| RSK-09 | Regla local de movilidad o restricción vehicular cambia durante el desarrollo. | Normativa | 2 | 4 | **8 Media** | Parametrizar reglas y revisar fuentes oficiales al cierre de cada Sprint. | Marcar regla como pendiente, suspender rutas afectadas y actualizar configuración. | Alex Zorrilla |
| RSK-10 | Pérdida o corrupción de datos de planificación. | Operación / Datos | 2 | 5 | **10 Media** | Transacciones, copias diarias, migraciones versionadas y restauración probada. | Restaurar última copia íntegra, reconciliar cambios y documentar incidente. | Isidro Casio |

## 3. Seguimiento

El registro se revisará semanalmente y en cada Sprint Review. Un riesgo pasa a incidencia cuando ocurre el evento disparador; el responsable debe actualizar probabilidad, impacto, respuesta y evidencia en Jira.
