# Design

## Context

Ver `proposal.md` (Why). La API ya expone pedidos (`PedidosRepository`) y flota con disponibilidad por fecha (`FlotaRepository`, `Vehiculo.elegible_para_planificar`), ambos con adaptadores en memoria y PostgreSQL/PostGIS. El stack obligatorio (RES-06) fija Leaflet/OpenStreetMap para cartografía y operación ligera en 2G/3G. El motor VRPTW con OR-Tools y la metaheurística (EN-001, HU-004) no forman parte de este cambio.

## Goals / Non-Goals

**Goals:**
- Mostrar en un mapa una propuesta de rutas razonable y explicable con los datos ya registrados.
- Fijar el contrato JSON de una ruta (secuencia, llegada estimada, puntualidad, distancia, carga y CO₂e) que el motor definitivo podrá reutilizar.
- Medir el beneficio frente a un despacho sin optimizar, con supuestos visibles para el usuario.

**Non-Goals:**
- Optimización exacta o metaheurística, rendimiento de EN-001 (150 pedidos / 15 vehículos en 45 s).
- Publicar, guardar o asignar rutas; cambiar el estado de los pedidos.
- Trazado por calles reales, tráfico o restricciones de circulación por placa.
- Vista del conductor, seguimiento en tiempo real y modo sin conexión (HU-005 completa).

## Decisions

1. **Heurística propia en Python puro.** Inserción más barata seguida de 2-opt. Costo lexicográfico: primero minimizar paradas fuera de ventana; luego, kg CO₂e. Es determinista (desempates por prioridad, código y placa), por lo que es probable con pruebas. Alternativa descartada: incorporar OR-Tools ahora, porque adelanta EN-001 sin su diseño ni sus pruebas de rendimiento.
2. **Orden de inserción.** Primero prioridad alta y ventana temprana, para que, si falta capacidad, queden fuera los menos urgentes.
3. **Distancia aproximada.** Haversine × 1,3 (factor de circuito urbano) y velocidad media de 25 km/h. Evita depender de un servicio de rutas externo; los valores se devuelven en `supuestos` y se muestran en la interfaz.
4. **Emisiones.** `km / 100 × consumo_base_por_100km × factor`. Se usa el factor del vehículo si existe; si no, uno de referencia por combustible (diésel 2,68; gasolina e híbrido 2,31; GNV 1,93 kg CO₂e por unidad; eléctrico 0,21 kg CO₂e/kWh).
5. **Línea base.** Despacho sin optimizar: vehículos por placa, llenados en orden de registro y visitados en ese orden. Se reportan su distancia, CO₂e y paradas tardías; el ahorro porcentual se calcula sobre el CO₂e.
6. **Pedidos elegibles.** Estado `PENDIENTE` o `VALIDADO` con inicio de ventana en la fecha consultada (hora de Lima). Vehículos: solo los aptos para planificar en esa fecha.
7. **Frontend.** Leaflet imperativo dentro de un componente React (sin `react-leaflet`, una dependencia menos). Las teselas se oscurecen con un filtro CSS en tema oscuro. Al resaltar una ruta no se reencuadra el mapa.
8. **Permisos.** `PLANIFICADOR` y `ADMIN`, igual que la consulta de pedidos (matriz RBAC del documento 08).

## Risks / Trade-offs

- [La línea recta subestima o sobreestima tramos con ríos o vías de un solo sentido] → Se declara como supuesto; el trazado vial llegará con el motor definitivo.
- [La heurística no garantiza el óptimo] → Se presenta como "vista previa" y nunca como solución óptima, en línea con el escenario de degradación de EN-001.
- [Costo cuadrático o cúbico con muchos pedidos] → Suficiente para el volumen de demostración; el motor VRPTW reemplazará el algoritmo detrás del mismo contrato.
- [Uso de teselas públicas de OpenStreetMap] → Volumen bajo y atribución visible; para producción se configurará un proveedor propio (`VITE_MAP_TILE_PROVIDER`).
