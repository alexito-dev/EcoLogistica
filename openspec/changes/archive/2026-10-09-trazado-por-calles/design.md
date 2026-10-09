# Design

## Context

Ver `proposal.md`. El mapa (`MapaRutas.tsx`) usa Leaflet y dibuja una `polyline` por ruta.

## Goals / Non-Goals

**Goals:** dibujar recorridos creíbles sin romper la página si el servicio externo falla.

**Non-Goals:** recalcular kilómetros, duraciones o CO₂e con la red vial (lo hará el motor del Sprint 3), ni montar un OSRM propio.

## Decisions

1. **En el frontend y solo para el dibujo.** La propuesta no depende de un servicio externo; si OSRM cae, la API y sus pruebas siguen iguales.
2. **Una solicitud por ruta** a `/route/v1/driving/{lon,lat;...}?overview=full&geometries=geojson`, en paralelo, con tiempo máximo de 8 s y cancelación al cambiar la fecha.
3. **Primero la línea recta, luego el trazado.** El mapa se dibuja de inmediato y se reemplaza cuando llegan los caminos; no se reencuadra.
4. **Configurable** con `VITE_OSRM_URL` para usar un OSRM propio (Docker con el extracto de Perú) en producción.

## Risks / Trade-offs

- [El servidor público de OSRM tiene límites de uso y puede no estar disponible] → Respaldo automático a líneas rectas y etiqueta visible; OSRM propio para producción.
- [La distancia mostrada no coincide exactamente con el trazado] → Se explica en "¿Cómo se calcula?"; se resolverá al calcular con la red vial.
