# 04. Presupuesto del proyecto

[← Volver al README Principal](../../README.md)

## Metadatos

| Campo | Valor |
|---|---|
| Proyecto | EcoLogística Huancayo |
| Horizonte | 14 semanas de desarrollo + 1 semana de cierre |
| Moneda | Soles peruanos (S/) |
| Versión | 1.2.0 |
| Fecha | 09 de octubre de 2026 |

> Presupuesto académico referencial para el PMV. Las horas y tarifas son supuestos de planificación, no pagos ejecutados. La reserva se calcula sobre el subtotal y se libera solo mediante control de cambios.

> **Relación con el Acta:** el Acta de constitución fija un techo de autorización de S/ 500,000 y una reserva máxima de S/ 35,000. Este documento calcula un presupuesto detallado estimado de S/ 54,538.40, con una reserva estimada de S/ 5,843.40. El estimado detallado se mantiene dentro del techo; no representa gasto ejecutado ni modifica la autorización máxima.

> **Nota sobre moneda:** el presupuesto se expresa en soles peruanos (S/) porque DistriRápido S.A.C., la empresa patrocinadora, opera y factura en Huancayo, Perú. La plantilla de la consigna en USD es referencial; se mantiene la moneda local para que las tarifas y subtotales sean auditables frente al contexto real del proyecto.

## 1. Recursos humanos (CAPEX)

| Rol | Horas | Tarifa S/ hora | Subtotal |
|---|---:|---:|---:|
| Director del proyecto | 168 | 45 | 7,560 |
| Arquitecto / servicios API | 240 | 50 | 12,000 |
| Desarrollador / Optimización | 224 | 45 | 10,080 |
| Interfaz / experiencia de usuario | 224 | 40 | 8,960 |
| Calidad / operaciones de desarrollo | 168 | 40 | 6,720 |
| **Total CAPEX** | **1,024** | — | **45,320** |

Fórmula aplicada: **costo = horas asignadas × tarifa hora**.

## 2. Licenciamiento y herramientas

| Concepto | Base de cálculo | Subtotal |
|---|---|---:|
| Jira Software / gestión ALM | 5 usuarios × 3 meses × S/ 35 | 525 |
| Diseño y prototipado | Plan colaborativo referencial | 450 |
| Calidad y análisis estático | Herramientas open source + configuración | 0 |
| Dominios y certificados | Certificado gratuito; dominio referencial | 180 |
| **Total licencias** | — | **1,155** |

## 3. Infraestructura y servicios (OPEX)

| Concepto | Base de cálculo | Subtotal |
|---|---|---:|
| Compute / contenedores | 4 meses × S/ 220 | 880 |
| PostgreSQL administrado / backups | 4 meses × S/ 180 | 720 |
| Mapas y geocodificación | OSM/Leaflet; cuota de pruebas | 0 |
| CI/CD y almacenamiento | 4 meses × S/ 80 | 320 |
| Observabilidad y tráfico | 4 meses × S/ 75 | 300 |
| **Total OPEX** | — | **2,220** |

## 4. Consolidación financiera

| Categoría | Subtotal | Porcentaje del subtotal |
|---|---:|---:|
| Recursos humanos (CAPEX) | S/ 45,320 | 93.08% |
| Licenciamiento de software | S/ 1,155 | 2.37% |
| Infraestructura cloud (OPEX) | S/ 2,220 | 4.56% |
| **Subtotal del proyecto** | **S/ 48,695** | **100.00%** |
| Reserva de contingencia (12%) | S/ 5,843.40 | N/A |
| **Presupuesto total estimado** | **S/ 54,538.40** | **100.00%** |

La reserva cubre principalmente RSK-02, RSK-04, RSK-06 y RSK-08. Todo uso requiere justificar el evento, aprobar el cambio y actualizar el pronóstico restante.

## 5. Control presupuestario

Se revisará el consumo al cierre de cada Sprint. Una desviación mayor al 10% del pronóstico de la categoría exige análisis de causa y decisión del Director del Proyecto; una desviación mayor al 12% del total exige activar la reserva o reducir alcance.


## Historial de cambios

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| 1.2.0 | 09/10/2026 | Anco Porras, Jhean Pier Julio | Se unifican al español los nombres de roles con los del README. |
