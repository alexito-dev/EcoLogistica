# Proposal

## Why

En la vista previa de rutas, cada recorrido se dibujaba como líneas rectas entre paradas, cruzando manzanas y ríos. Eso no se parece a lo que hará el vehículo y resta credibilidad a la propuesta frente a Planificación y Gerencia. OSRM es un motor de rutas de código abierto sobre los mismos datos de OpenStreetMap, por lo que respeta la restricción RES-06.

## What Changes

- El mapa de Rutas pide a OSRM el camino por calles de cada recorrido (depósito → paradas en orden → depósito) y lo dibuja en lugar de la línea recta.
- Si OSRM no responde en 8 segundos, falla o no encuentra camino, el mapa conserva las líneas rectas; nada más se ve afectado.
- Una etiqueta sobre el mapa indica el estado: trazando, recorrido por calles u otra vez líneas rectas.
- El servidor se configura con `VITE_OSRM_URL`; por defecto, el servidor público de demostración de OSRM.
- Los kilómetros, la duración y el CO₂e siguen calculándose en el backend con la aproximación en línea recta × 1,3; este cambio solo afecta al dibujo.

## Capabilities

### New Capabilities
<!-- Ninguna. -->

### Modified Capabilities
- `rutas`: el recorrido del mapa sigue las calles cuando el servicio de rutas está disponible.

## Impact

- **Código:** `frontend/src/lib/trazado.ts` (nuevo), `frontend/src/components/MapaRutas.tsx`, `frontend/src/pages/PaginaRutas.tsx`, `frontend/src/styles.css`, `.env.example`.
- **Pruebas:** `frontend/tests/trazado.test.ts` (nuevo) y casos en `frontend/tests/PaginaRutas.test.tsx`.
- **Privacidad:** se envían al servidor de rutas solo las coordenadas de depósito y paradas, sin nombres ni pesos. Con datos reales se recomienda un OSRM propio.
