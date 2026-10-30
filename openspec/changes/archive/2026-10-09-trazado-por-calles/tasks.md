# Tasks

## 1. Implementación

- [x] 1.1 Crear `lib/trazado.ts` con la consulta a OSRM, conversión de coordenadas, tiempo máximo y respaldo `null`
- [x] 1.2 Usar el trazado en `MapaRutas.tsx` con respaldo a línea recta y etiqueta de estado sobre el mapa
- [x] 1.3 Documentar `VITE_OSRM_URL` en `.env.example` y explicar el trazado en "¿Cómo se calcula?"

## 2. Verificación

- [x] 2.1 Pruebas de `trazarPorCalles` (orden de coordenadas, fallo de red, sin ruta, 429 y menos de dos puntos)
- [x] 2.2 Pruebas de la página para la etiqueta con y sin trazado por calles; suite del frontend en verde (51 pruebas), `tsc` y `oxlint` sin hallazgos
- [x] 2.3 Comprobación visual con datos de demostración: los recorridos siguen las calles y aparece "Recorrido por calles · OSRM"
