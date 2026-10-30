# 03. Registro de riesgos

[← Volver al README Principal](../../README.md)

## Metadatos

| Campo | Valor |
|---|---|
| Proyecto | EcoLogística Huancayo |
| Versión | 1.2.0 |
| Fecha | 30 de octubre de 2026 (emisión original: 11 de septiembre de 2026) |
| Escala | Probabilidad e impacto de 1 a 5; exposición = P × I |

## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.0.0 | 11/09/2026 | No consignado en la fuente original | Primera emisión del registro de riesgos del proyecto. |
| 1.1.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se incorpora el historial de cambios para mantener la trazabilidad de versiones del documento. |
| 1.2.0 | 30/10/2026 | Hilario Talavera, Alexander Daniel | Se agrega el seguimiento del Sprint 3 de RSK-02, RSK-05, RSK-06 y RSK-07 con la evidencia de SonarQube, OWASP y WCAG. |

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
| RSK-03 | Direcciones ambiguas producen coordenadas incorrectas. | Datos / Operación | 3 | 4 | **12 Media** | Confianza mínima, revisión manual y muestra de validación de 100 direcciones. | Excluir el pedido, solicitar punto de referencia y no publicar ruta insegura. | Anco Porras, Jhean Pier Julio |
| RSK-04 | Cambios de requisitos afectan alcance y fechas. | Gestión | 4 | 4 | **16 Alta** | Backlog priorizado, control de cambios y aceptación por Sprint. | Replanificar, usar reserva y diferir alcance no esencial. | Alex Zorrilla |
| RSK-05 | Baja adopción por interfaz compleja o conectividad limitada. | Usuario / Social | 3 | 4 | **12 Media** | Pruebas con despachadores y conductores, WCAG 2.1 AA y modo de bajo consumo. | Capacitación, modo offline de última ruta y soporte guiado. | Jhoanna Vera |
| RSK-06 | Exposición de datos personales o credenciales. | Seguridad / Legal | 2 | 5 | **10 Media** | Datos sintéticos, mínimo privilegio, secretos fuera de Git y revisión OWASP. | Revocar sesiones, rotar secretos, preservar auditoría y activar protocolo de incidente. | Anco Porras, Jhean Pier Julio |
| RSK-07 | Retraso por defectos detectados al integrar frontend y backend. | Calidad | 3 | 4 | **12 Media** | Contratos API, integración continua, revisión por PR y pruebas automatizadas. | Congelar cambios, priorizar defectos críticos y reducir alcance del Sprint. | Jose Luis Isidro |
| RSK-08 | Incremento de precios cloud, mapas o licencias supera el presupuesto. | Financiera | 3 | 3 | **9 Media** | Preferir OSM/Leaflet, cuotas, presupuesto mensual y alternativas open source. | Desactivar servicios no esenciales y migrar a componentes de menor costo. | Alex Zorrilla |
| RSK-09 | Regla local de movilidad o restricción vehicular cambia durante el desarrollo. | Normativa | 2 | 4 | **8 Media** | Parametrizar reglas y revisar fuentes oficiales al cierre de cada Sprint. | Marcar regla como pendiente, suspender rutas afectadas y actualizar configuración. | Alex Zorrilla |
| RSK-10 | Pérdida o corrupción de datos de planificación. | Operación / Datos | 2 | 5 | **10 Media** | Transacciones, copias diarias, migraciones versionadas y restauración probada. | Restaurar última copia íntegra, reconciliar cambios y documentar incidente. | Isidro Casio |

## 3. Seguimiento

El registro se revisará semanalmente y en cada Sprint Review. Un riesgo pasa a incidencia cuando ocurre el evento disparador; el responsable debe actualizar probabilidad, impacto, respuesta y evidencia en Jira.

### 3.1. Seguimiento en la revisión del Sprint 3 (30/10/2026)

| ID | Evidencia del sprint | Efecto en la exposición | Próximo paso |
|---|---|---|---|
| RSK-02 | La vista previa de rutas funciona, pero el benchmark EN-001 sigue sin ejecutarse; no hay medición frente a los 45 s. | Sin cambio (15 Alta): no se puede reducir sin medir. | Ejecutar EN-001 en el Sprint 4 ([Revisión del Sprint 03](../03%20Implementaci%C3%B3n/Sprint%2003/01%20Revisi%C3%B3n%20del%20Sprint%20V_1_0_0.md#pendientes)). |
| RSK-05 | Auditoría WCAG 2.2 AA: 86,7 % de criterios aplicables; 5 defectos corregidos, incluidos contrastes en tema oscuro y bordes de campos ([05 WCAG](../03%20Implementaci%C3%B3n/Sprint%2003/05%20WCAG%20V_1_0_0.md)). | Mitigación en curso; P se mantiene en 3 hasta alcanzar ≥ 90 % y probar con usuarios. | Aviso de vencimiento de sesión (2.2.1) y prueba automática con axe. |
| RSK-06 | SonarQube: 0 vulnerabilidades y 0 *hotspots*; revisión OWASP Top 10:2025 sin vulnerabilidades críticas abiertas; se añadieron cabeceras de seguridad y se actualizó Vite ([04 OWASP](../03%20Implementaci%C3%B3n/Sprint%2003/04%20OWASP%20V_1_0_0.md)). | Mitigación reforzada; se mantiene 10 Media mientras los secretos TOTP no estén cifrados. | Cifrado de secretos TOTP y cuentas en PostgreSQL (EN-005 / ECO-21). |
| RSK-07 | CI con pruebas de backend y frontend, migraciones y OpenSpec; 182 pruebas en verde; *Quality Gate* PASSED ([03 Calidad](../03%20Implementaci%C3%B3n/Sprint%2003/03%20Calidad%20de%20c%C3%B3digo%20V_1_0_0.md)). La integración tardía de `feature/rutas-indicadores` generó 4 conflictos documentales. | Mitigación parcial. | Ejecutar el CI en todas las ramas y limitar la vida de las ramas a 5 días hábiles. |
