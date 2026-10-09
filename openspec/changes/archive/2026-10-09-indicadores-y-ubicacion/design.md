# Design

## Context

Ver `proposal.md` (Why). La vista previa de rutas (`openspec/specs/rutas`) ya calcula por fecha la propuesta y un despacho sin optimizar. Pedidos y flota exponen puertos de repositorio paginados. La matriz RBAC del documento 08 asigna a Gerencia la consulta de indicadores y reportes.

## Goals / Non-Goals

**Goals:**
- Un dashboard útil para Planificación y Gerencia sin nuevas dependencias ni consultas costosas.
- Registrar la ubicación de un pedido con un clic, sin geocodificación externa.
- Que el menú refleje exactamente los permisos del backend.
- Evitar regresiones con una integración continua que valide todo el repositorio.

**Non-Goals:**
- Reportes PDF, series históricas y línea base manual (HU-011 completa).
- Geocodificación o búsqueda de direcciones (HU-002).
- Vistas para Conductor y Auditoría.

## Decisions

1. **Indicadores en el backend.** Un solo endpoint agrega los datos y reutiliza `RutasService`, de modo que el dashboard y la página Rutas muestran las mismas cifras de CO₂e y distancia.
2. **Gráficos con HTML y CSS.** Barras horizontales en una lista: cada fila tiene etiqueta y valor como texto y la barra es decorativa (`aria-hidden`), lo que cumple RNF-10 sin una librería de gráficos. Los estados sin pedidos se omiten para no saturar.
3. **Fecha por defecto: mañana**, como en Rutas, porque es el día que normalmente se planifica.
4. **Menú por rol en un único lugar** (`lib/navegacion.ts`): la misma tabla genera el menú lateral, la barra inferior móvil y la vista inicial. Una vista ajena al rol nunca se renderiza aunque se intente seleccionar.
5. **Selector de ubicación con Leaflet**, cargado de forma diferida con `React.lazy`. Las coordenadas se redondean a 6 decimales (≈ 0,1 m). Los campos de latitud y longitud se conservan para ingreso manual y accesible por teclado: el mapa es una ayuda, no el único medio.
6. **Carga diferida de Flota, Rutas e Indicadores** para mantener el paquete inicial por debajo de 500 kB (RES-06: redes 2G/3G).
7. **CI** con cuatro trabajos independientes; el de migraciones usa el contenedor `postgis/postgis:16-3.5` del `docker-compose.yml`.

## Risks / Trade-offs

- [El dashboard recalcula la vista previa en cada consulta] → Volumen bajo en esta etapa; se podrá almacenar la planificación publicada cuando exista.
- [Las teselas de OpenStreetMap requieren conexión] → Si el mapa no carga, los campos manuales siguen funcionando.
- [Un clic fuera del ámbito completa coordenadas que el backend rechazará] → El backend ya valida el ámbito (RN-001) y la interfaz muestra el error junto al campo.
