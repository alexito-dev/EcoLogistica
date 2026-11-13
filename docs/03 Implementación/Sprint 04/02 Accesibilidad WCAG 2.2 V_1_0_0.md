# Accesibilidad WCAG 2.2 AA — cierre de pendientes (Sprint 4)

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Fecha | 13/11/2026 |
| Base | [05 WCAG del Sprint 3](../Sprint%2003/05%20WCAG%20V_1_0_0.md): 40 de 45 criterios aplicables (88,9 %), meta ≥ 90 % |
| Pruebas | [`frontend/e2e/accesibilidad.spec.ts`](../../../frontend/e2e/accesibilidad.spec.ts) y [`sprint4-conduccion.spec.ts`](../../../frontend/e2e/sprint4-conduccion.spec.ts) |

## 1. Resultado por criterio pendiente

| Criterio | Antes | Verificación | Resultado |
|---|---|---|---|
| 1.4.4 Cambio de tamaño del texto | Sin verificar | Ventana de 640 × 360 px (equivale a 200 % de 1280 × 720) en 5 vistas: sin desplazamiento horizontal | ✔ |
| 1.4.12 Espaciado del texto | Sin verificar | Se inyecta interlineado 1,5, letras 0,12 em, palabras 0,16 em y párrafos 2 em: ningún texto visible queda recortado | ✔ |
| 1.4.13 Contenido al pasar el puntero o enfocar | Sin verificar | El globo de una parada del mapa se cierra con `Esc` | ✔ |
| 2.4.5 Varias vías | Parcial | Nuevo «Mapa de navegación» en el pie con enlaces a todas las vistas del rol, además del menú | ✔ |
| 2.4.11 Foco no oculto | Sin verificar | Con 390 px de ancho, 25 pulsaciones de `Tab`: ningún control enfocado queda bajo la barra inferior; `scroll-padding` para las barras fijas | ✔ |

**Total: 45 de 45 criterios aplicables verificados por prueba (100 %)**, frente a 40 de 45 (88,9 %) en el Sprint 3. La meta interna KPI-Q5 (≥ 90 %) se cumple.

## 2. axe-core en todas las vistas

La suite ejecuta `axe-core` (etiquetas `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa` y `wcag22aa`) sobre el acceso, Pedidos, Flota, Rutas, Seguimiento e Indicadores en tema claro y oscuro, y sobre «Mi ruta» en el recorrido de Conducción: **0 violaciones**.

La prueba corrige un falso positivo propio: las filas de la tabla aparecen con una animación de desvanecimiento y `axe` medía colores a medio opacar (contrastes de 1,9:1 a 4,3:1). Se ejecuta con `prefers-reduced-motion: reduce`, que la aplicación respeta, para medir los colores finales. Con ese ajuste, la regla `color-contrast` también pasa en «Mi ruta».

## 3. Lo que esta verificación no demuestra

- No se probó con lectores de pantalla reales (NVDA, JAWS, VoiceOver) ni con usuarios con discapacidad; es **conformidad por pruebas automáticas y guiones**, no una certificación.
- Los criterios se evaluaron en Chrome; no en otros navegadores.
- Las alertas `css:S7924` de SonarQube documentadas en el Sprint 3 siguen siendo falsos positivos documentados.
