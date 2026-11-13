# Informe de reducción del impacto ambiental (Green IT) — EcoLogística Huancayo

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Fecha | 13/11/2026 |
| Proyecto | EcoLogística Huancayo (React + Vite + TypeScript, FastAPI, PostgreSQL/PostGIS) |
| Asignatura | Taller de Proyectos 2 — Inspección 04 (Semana 13) |
| Rama / commit de trabajo | `sprint-4/green-it-calidad` |
| Documento complementario | [02 Estándares de ingeniería de software y guía de desarrollo verde](02%20Estandares%20Ingenier%C3%ADa%20de%20software%20V_1_0_0.md) |

> **Nota de adaptación.** La consigna de la Semana 13 describe las 8 optimizaciones para el stack MERN (MongoDB, Express, React, Node). EcoLogística usa **FastAPI y PostgreSQL/PostGIS** en el servidor. Cada optimización se aplicó con su equivalente real en este stack y se explica en la sección 3 (`.lean()`/`.select()` → columnas explícitas e índices en SQL; `compression` de Express → `BrotliMiddleware` de Starlette; ETag de Express → middleware ETag propio). **Todas las cifras de este informe fueron medidas sobre este repositorio**; no se reutilizaron los valores ilustrativos de la plantilla.

---

## 1. Introducción y propósito

La eficiencia computacional es un factor directo de sostenibilidad digital: cada byte que no viaja por la red, cada ciclo de CPU que el navegador no ejecuta y cada consulta acotada reducen la energía consumida en centros de datos, redes y dispositivos finales. EcoLogística Huancayo es, además, una plataforma cuyo objetivo es reducir el CO₂ del transporte urbano; resulta coherente que su propia huella digital sea mínima.

Este informe:

1. diagnostica el estado inicial medido de la aplicación;
2. documenta las 8 optimizaciones del stack con código ANTES y DESPUÉS;
3. mide el efecto con Lighthouse 12 y el modelo **Sustainable Web Design Model v4 (SWDM v4)**;
4. declara con transparencia lo que **no** se cumplió o no se pudo medir.

## 2. Diagnóstico inicial y método de medición

### 2.1 Método

| Aspecto | Detalle |
|---|---|
| Herramienta | Lighthouse 12 (Chrome headless), categorías rendimiento, accesibilidad, buenas prácticas y SEO |
| Página auditada | Pantalla pública de acceso `/` del build de producción servido con `vite preview` |
| Perfiles | **Móvil** (predeterminado de Lighthouse: Moto G con 4G lenta simulada) y **escritorio** (`--preset=desktop`) |
| Repeticiones | Línea base: 1 corrida por perfil. Estado final: 3 corridas móvil + 3 corridas LHCI escritorio (resultados estables, variación ≤ 1 punto) |
| Evidencia | [`evidencias/resumen-lighthouse.json`](evidencias/resumen-lighthouse.json) y `lighthouse-reports/` local (no versionado por tamaño; CI publica los informes como artefacto) |

**Limitación del alcance de la auditoría.** Las vistas autenticadas (pedidos, flota, rutas, indicadores) requieren sesión con MFA y no son auditables con `lighthouse <url>` sin un guion de autenticación. La auditoría de la página pública mide el costo de **la primera carga**, que es la que paga todo usuario. El efecto de la paginación y la compresión de la API se midió por separado (sección 3, optimizaciones 2 y 8).

### 2.2 Estado ANTES (commit `2b08013`, compilación local)

| Métrica | Móvil | Escritorio |
|---|---:|---:|
| Rendimiento Lighthouse | **74** | 96 |
| First Contentful Paint (FCP) | 1,97 s | 0,45 s |
| Largest Contentful Paint (LCP) | **7,38 s** | 1,42 s |
| Total Blocking Time (TBT) | 101 ms | 0 ms |
| Cumulative Layout Shift (CLS) | 0 | 0 |
| Peso transferido | **1 211 513 B (1,16 MiB)** | 1 211 638 B |
| Solicitudes HTTP | 14 | 14 |

**Hallazgos del diagnóstico (todos verificados en el repositorio):**

1. `frontend/public/logo_ecologistica.png` pesaba **1 049 853 B** (1536 × 1024 px) y se mostraba a 32–56 px: el 87 % de la transferencia y el elemento LCP de la pantalla de acceso.
2. El `.env` local de la raíz contenía `NODE_ENV=development`. Vite lo leía y `vite build` **empaquetaba React en modo desarrollo** (`index.js` de **476–477 kB**, 140 kB gzip, con advertencias y comprobaciones de depuración). En CI no ocurría porque el archivo `.env` no se versiona; el defecto afectaba a quien compilaba localmente para la demo.
3. Las fuentes `Codec Pro` se referenciaban con `url('/fonts/*.woff2')` pero los archivos no existen (licencia comercial): 4 advertencias de compilación y 3 solicitudes por carga que el servidor resolvía con `index.html` (≈ 1 KB cada una; en un hosting con rutas estrictas serían errores 404). Tampoco existía `favicon`, lo que generaba un 404 real.
4. El listado de pedidos pedía **100 registros** por solicitud y los paginaba solo en el navegador (8 por página); el valor por defecto de la API era 20.
5. Las respuestas JSON de la API se enviaban **sin compresión** y sin validadores de caché (`ETag`).
6. La consulta SQL, el uso de dependencias y las vistas diferidas ya eran correctos (ver optimizaciones 1, 4, 5 y 6); no se inventaron defectos en esas áreas.

## 3. Las 8 optimizaciones aplicadas

### 3.1 Consultas magras a la base de datos (equivalente de `.select()`/`.lean()`/índices)

**Estado de partida.** El adaptador `PedidosPostgresRepository` ya ejecuta SQL explícito (`text(...)`) que enumera las columnas necesarias —nunca `SELECT *`— y construye directamente objetos de dominio, sin capa ORM que hidrate entidades (el beneficio que en Mongoose aportan `.lean()` y `.select()`). Los filtros frecuentes ya tienen índices desde los Sprints 1 y 2. En esta área **no se modificó código de producción**; se agregaron pruebas que impiden la regresión.

ANTES — patrón que la guía **prohíbe** (no existía en el repositorio; se muestra como contraste):

```python
# Anti-patrón: todas las columnas y entidades hidratadas
pedidos = session.query(Pedido).filter(Pedido.estado == "PENDIENTE").all()
```

DESPUÉS — código vigente verificado (`backend/src/app/pedidos/postgres_repository.py`, migraciones `20261009_01` y `20261009_02`):

```python
_SELECT_PEDIDO = """
SELECT p.id, p.codigo, p.destinatario_alias, p.demanda_kg, p.demanda_m3, ...
       ST_Y(u.punto)::double precision AS latitud, ST_X(u.punto)::double precision AS longitud
FROM pedidos AS p JOIN ubicaciones AS u ON u.id = p.ubicacion_id
"""
rows = connection.execute(
    text(_SELECT_PEDIDO + filtro + " ORDER BY p.creado_en DESC, p.id DESC LIMIT :limite OFFSET :offset"),
    {**parametros, "limite": limite, "offset": (pagina - 1) * limite},
)
```

```sql
CREATE INDEX ix_pedidos_estado_creado ON pedidos (estado, creado_en DESC);   -- filtro + orden del listado
CREATE INDEX ix_ubicaciones_punto ON ubicaciones USING GIST (punto);          -- consultas espaciales
CREATE INDEX ix_vehiculos_estado_placa ON vehiculos (estado, placa);
CREATE INDEX ix_disponibilidad_fecha_estado ON disponibilidad_vehiculos (fecha, disponible);
```

**Nuevo:** [`backend/tests/test_green_it_consultas.py`](../../../backend/tests/test_green_it_consultas.py) falla si aparece un `SELECT *`, si el listado pierde `LIMIT/OFFSET` o si desaparece un índice.

**Límite de la evidencia.** No se ejecutó `EXPLAIN ANALYZE` en este informe; la mejora por índices es una propiedad del diseño y no se cuantifica en milisegundos.

### 3.2 Paginación en backend y frontend (bloques de 12)

ANTES (`frontend/src/pages/PaginaPedidos.tsx`, `PedidosTable.tsx`, `router.py`):

```tsx
listarPedidos(1, 100)            // 100 registros en cada carga
const POR_PAGINA = 8             // paginación solo en el navegador
```
```python
limite: Annotated[int, Query(ge=1, le=100)] = 20
```

DESPUÉS:

```ts
// frontend/src/api/pedidos.ts
export const PEDIDOS_POR_PAGINA = 12
export function listarPedidos(pagina = 1, limite = PEDIDOS_POR_PAGINA, estado?: EstadoPedido) {
  const filtro = estado ? `&estado=${estado}` : ''
  return solicitar<ListadoPedidos>(`/pedidos?pagina=${pagina}&limite=${limite}${filtro}`)
}
```
```python
# backend/src/app/pedidos/router.py
limite: Annotated[int, Query(ge=1, le=100)] = 12
```

La página (`PaginaPedidos`) conserva `pagina` y el filtro de estado y los envía al servidor; la tabla muestra «Mostrando a–b de total» con botones anterior/siguiente. Las tarjetas de resumen ahora indican «En esta página» porque se calculan sobre el bloque cargado.

**Medición** (`backend/scripts/medir_api_verde.py`, 100 pedidos sintéticos en memoria):

| Escenario | Bytes |
|---|---:|
| ANTES: 100 registros, sin compresión | 48 647 |
| DESPUÉS: página de 12 con Brotli | 723 |
| Revalidación con `If-None-Match` | 0 (HTTP 304) |

La reducción medida es de **98,5 %**. Esta cifra está inflada porque los pedidos sintéticos son casi idénticos y comprimen de forma excepcional; con datos reales se espera una reducción menor, aunque de magnitud similar por la paginación (12 de 100 registros ≈ 88 %).

### 3.3 Imágenes de nueva generación con `<picture>`

ANTES (3 usos en `AppShell.tsx` y `LoginPage.tsx` y 1 fondo CSS):

```tsx
<img src="/logo_ecologistica.png" alt="" width="40" height="40" />   // 1 049 853 B para 40 × 40 px
```

DESPUÉS (`frontend/src/components/Logo.tsx`):

```tsx
<picture>
  <source type="image/avif" srcSet="/img/logo-64.avif 1x, /img/logo-128.avif 2x" />
  <source type="image/webp" srcSet="/img/logo-64.webp 1x, /img/logo-128.webp 2x" />
  <img src="/img/logo-64.png" srcSet="/img/logo-64.png 1x, /img/logo-128.png 2x"
       alt="" width={tamano} height={tamano} decoding="async" />
</picture>
```

| Variante | Peso |
|---|---:|
| Original PNG 1536 × 1024 | 1 049 853 B |
| `logo-64.avif` / `.webp` / `.png` | 1 526 B / 1 824 B / 2 255 B |
| `logo-128.avif` / `.webp` / `.png` | 3 063 B / 4 156 B / 4 145 B |

El PNG original se elimina de `frontend/public/` (se conserva en `assets/images/` como fuente). El marcador del depósito en el mapa usa `logo-64.webp`. El logotipo está siempre visible (acceso y barra), por eso no lleva `loading="lazy"`.

### 3.4 Carga diferida, división de código y build de producción correcto

ANTES: Flota, Rutas e Indicadores ya se importaban con `React.lazy` desde el Sprint 3 y el generador de QR con `import('qrcode')`; esto se **conserva**. El defecto real era el empaquetado (hallazgo 2):

```text
dist/assets/index-*.js   476,01 kB │ gzip: 140,31 kB   (React en modo desarrollo)
```

DESPUÉS:

```js
// frontend/scripts/build.mjs — package.json: "build": "tsc -b && node scripts/build.mjs"
process.env.NODE_ENV = 'production'
const { build } = await import('vite')
await build({ mode: 'production' })
```
```text
dist/assets/index-*.js        265,42 kB │ gzip: 82,69 kB     (-44 % y -41 % gzip)
dist/assets/leaflet-*.js      148,60 kB │ gzip: 43,33 kB     (solo al abrir Rutas)
dist/assets/PaginaRutas-*.js   17,42 kB │ gzip:  5,50 kB
dist/assets/PaginaFlota-*.js   17,72 kB │ gzip:  4,32 kB
dist/assets/browser-*.js (qrcode) 23,46 kB │ gzip: 8,86 kB    (solo al enrolar MFA)
```

La pantalla de acceso no descarga Leaflet ni las vistas de gestión. Se intentó forzar `NODE_ENV` desde `vite.config.ts` y no funcionó (Vite lee el `.env` antes); por eso se usa un lanzador que lo fija antes de importar Vite.

### 3.5 Depuración de dependencias

Se auditaron las 6 dependencias de ejecución: `react`, `react-dom`, `leaflet`, `lucide-react` (íconos importados por nombre y *tree-shaken*), `qrcode` (carga diferida) y `@types/qrcode` (solo tipos). **No hay** `moment`, `lodash`, `axios`, `dayjs` ni `jquery`: las fechas usan `Intl.DateTimeFormat` (`frontend/src/lib/fechas.ts`, zona `America/Lima`) y las peticiones `fetch`. En esta área el estado de partida ya era conforme y no se cambió código; se añadió la guarda [`frontend/tests/GreenIt.test.ts`](../../../frontend/tests/GreenIt.test.ts), que falla si se incorpora alguna de esas librerías.

```ts
// Ya vigente: API nativa en lugar de moment.js
const formato = new Intl.DateTimeFormat('es-PE', { timeZone: 'America/Lima', day: '2-digit', month: '2-digit',
  year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false })
```

### 3.6 Reducción de solicitudes HTTP: SVG en línea

Las ilustraciones (`Hero.tsx`, acceso) son `<svg>` en línea y los íconos son componentes de `lucide-react` que se compilan dentro del paquete JS: **0 solicitudes por ícono**. Además: se eliminaron las solicitudes a fuentes inexistentes, se sustituyó 1 PNG por 1 variante moderna y se agregó un favicon para evitar el 404 automático.

```css
/* ANTES */  src: local('Codec Pro'), local('CodecPro-Regular'), url('/fonts/CodecPro-Regular.woff2') format('woff2');
/* DESPUÉS */ src: local('Codec Pro'), local('CodecPro-Regular');   /* sin archivo remoto inexistente */
```

Con la licencia de Codec Pro disponible, los `.woff2` pueden restituirse con `font-display: swap` (instrucciones en `frontend/public/fonts/LEEME.md`).

| Medida | ANTES | DESPUÉS |
|---|---:|---:|
| Solicitudes en la carga de acceso | 14 | **9** (−36 %) |

### 3.7 Estrategia de caché

ANTES: la API no emitía `ETag` ni `Cache-Control`.

DESPUÉS (`backend/src/app/cache_http.py`):

```python
class EtagMiddleware(BaseHTTPMiddleware):
    """Añade ETag débil a los GET 200 con JSON y responde 304 si el cliente ya tiene la versión."""
    async def dispatch(self, request, call_next):
        respuesta = await call_next(request)
        ...
        etag = calcular_etag(cuerpo)          # W/"<sha256[:32]>"
        cabeceras = {"ETag": etag, "Cache-Control": "private, no-cache", "Vary": "Cookie, Accept-Encoding"}
        if _coincide(request.headers.get("if-none-match"), etag):
            return Response(status_code=304, headers=cabeceras)
```

- Se usa `private, no-cache` (no `max-age=31536000`) porque las respuestas dependen de la cookie de sesión: no deben guardarse en cachés compartidas y siempre se revalidan; si no cambiaron, la respuesta es **304 sin cuerpo (0 B medidos)**.
- No se cachea nada bajo `/api/v1/auth` ni los métodos que modifican estado.
- Para los **recursos estáticos**, `frontend/deploy/nginx.conf` define `Cache-Control: public, max-age=31536000, immutable` en `/assets/` (nombres con hash), 30 días en `/img/` y `no-cache` para `index.html`.
- **React Query / TanStack Query no se incorpora.** El proyecto no lo usa y agregarlo contradiría la depuración de dependencias (3.5); el caché en el cliente lo resuelve el caché HTTP del navegador con las revalidaciones `If-None-Match` anteriores.
- Pruebas: `backend/tests/test_cache_compresion.py` (ETag, 304, invalidación al cambiar los datos, exclusión de `/auth` y de las escrituras).

### 3.8 Compresión Brotli/Gzip en la API

ANTES: respuestas JSON sin comprimir.

DESPUÉS (`backend/src/app/main.py`, dependencia `brotli-asgi` en `requirements.txt`):

```python
app.add_middleware(EtagMiddleware)
app.add_middleware(CORSMiddleware, ..., expose_headers=["ETag"])
# Capa más externa: Brotli con respaldo Gzip para respuestas > 1 KB
app.add_middleware(BrotliMiddleware, quality=4, minimum_size=1024, gzip_fallback=True)
```

Pruebas: respuestas mayores a 1 KB salen con `content-encoding: br` o `gzip` según `Accept-Encoding` y el cuerpo descomprimido coincide con el original. La compresión de los **estáticos** del frontend corresponde al servidor de hosting (Gzip activo en `deploy/nginx.conf`; Brotli requiere el módulo `ngx_brotli`, indicado como comentario). El servidor `vite preview` usado en las mediciones aplica Gzip **tanto en el ANTES como en el DESPUÉS**; por ello la reducción de peso medida en el frontend (−91,6 %) proviene de la imagen y del build de producción, y no de una diferencia de compresión entre ambas mediciones.

## 4. Tabla comparativa ANTES y DESPUÉS (medida)

### 4.1 Perfil móvil (4G lenta simulada)

| Métrica | ANTES | DESPUÉS | Variación | Mejora |
|---|---:|---:|---:|---:|
| Rendimiento Lighthouse | 74 | **99** | +25 pts | +33,8 % |
| FCP | 1,97 s | 1,51 s | −0,46 s | −23 % |
| LCP | 7,38 s | **1,99 s** | −5,39 s | −73 % |
| TBT | 101 ms | **13 ms** | −88 ms | −87 % |
| CLS | 0 | 0 | — | — |
| Peso transferido | 1 211 513 B | **101 425 B** | −1 110 088 B | **−91,6 %** |
| Solicitudes HTTP | 14 | 9 | −5 | −36 % |
| Accesibilidad / Buenas prácticas / SEO | 100 / 93 / 91 | 100 / 96 / 100* | | |

\* El 100 de SEO se observó en las corridas de Lighthouse CI tras agregar `robots.txt` y la descripción; las corridas manuales previas al `robots.txt` registraron 91.

### 4.2 Perfil escritorio (el que verifica el pipeline `green-audit.yml`)

| Métrica | ANTES | DESPUÉS | Umbral de la rúbrica | ¿Cumple? |
|---|---:|---:|---|:---:|
| Rendimiento | 96 | **100** | ≥ 90 | Sí |
| FCP | 0,45 s | **0,39 s** | ≤ 1,0 s | Sí |
| LCP | 1,42 s | **0,54 s** | ≤ 1,4 s | Sí |
| TBT | 0 ms | **0 ms** | ≤ 85 ms | Sí |
| CLS | 0 | **0** | ≤ 0,02 | Sí |
| Peso | 1,16 MiB | **0,10 MiB** | ≤ 1,1 MB | Sí |

### 4.3 Declaración de incumplimientos y límites

- **En móvil, FCP (1,51 s) y LCP (1,99 s) no alcanzan los umbrales 1,0 s y 1,4 s** de la rúbrica, aunque el puntaje (99) y el TBT sí. En escritorio se cumplen todos. El pipeline se configura en escritorio por esa razón y así se declara.
- **Intento adicional para móvil (13/11/2026):** se probó incrustar la hoja de estilos en el HTML y mostrar una pantalla de carga estática para adelantar el primer pintado. El resultado fue FCP 1,5 s y LCP 1,9 s (frente a 1,51 s y 1,99 s), una mejora marginal que no alcanza los umbrales; se revirtió para no añadir complejidad sin beneficio. Con el perfil de 4G lenta simulada de Lighthouse, la brecha restante depende del tamaño del JavaScript inicial (83 kB gzip) y exigiría reducir React/Leaflet en la carga inicial, trabajo que no se emprendió.
- Los valores de la plantilla de la consigna (38 → 96, 8,4 MB, 68 solicitudes, 2,15 g) **no corresponden a este proyecto** y no se usan.
- Se midió la pantalla de acceso (carga inicial pública), no las vistas autenticadas. Durante las auditorías la API no estaba en ejecución: las 2–4 solicitudes de verificación de sesión fallan por igual antes y después y no suman bytes.

### 4.4 Atribución del ahorro de peso

| Intervención | Peso móvil (B) | Efecto |
|---|---:|---:|
| Línea base (compilación local con `.env` de desarrollo) | 1 211 513 | — |
| Solo build de producción correcto | 1 148 620 | −62 893 (−5,2 %) |
| + logotipo AVIF/WebP/PNG pequeño, favicon y sin fuentes inexistentes | 101 425 | −1 047 195 adicionales (−91,2 %) |

En rendimiento, el build correcto por sí solo subió de 74 a 76; el grueso de la mejora (76 → 99; LCP 7,08 s → 1,99 s) proviene de reemplazar el logotipo de 1 MB.

## 5. Análisis de impacto ambiental y eficiencia energética (SWDM v4)

### 5.1 Modelo

Constantes del SWDM v4 (consultadas el 13/11/2026 en <https://sustainablewebdesign.org/estimating-digital-emissions/>): energía total **0,300 kWh/GB** (operacional 0,194 + incorporada 0,106; centros de datos 0,067, redes 0,072 y dispositivos 0,161) e intensidad eléctrica global **494 g CO₂e/kWh**.

```text
Energía (kWh)   = bytes / 1 024³ × 0,300
Emisiones (g)   = Energía × 494
```

Se calcula la **primera visita** (sin caché ni hosting verde acreditado; supuestos conservadores). No se aplicó la intensidad eléctrica peruana porque no se verificó una cifra citable; el resultado se puede recalcular cambiando `INTENSIDAD_G_KWH` en [`scripts/calcular_swdm.py`](../../../scripts/calcular_swdm.py). Las fórmulas del modelo v4 fueron verificadas contra la fuente. Las constantes de la plantilla de la consigna (0,815 kWh/GB; 442 g/kWh) son de una versión anterior y **no** se utilizaron.

### 5.2 Resultado

| Escenario | Peso | Energía por visita | CO₂e por visita |
|---|---:|---:|---:|
| ANTES | 1 211 513 B | 0,0003385 kWh | **0,1672 g** |
| DESPUÉS | 101 425 B | 0,0000283 kWh | **0,0140 g** |
| Variación | −1 110 088 B | −0,0003102 kWh | **−0,1532 g (−91,6 %)** |

### 5.3 Proyección anual

Se usa como **escenario de referencia** el volumen de 500 000 visitas/año de la consigna; no es un dato de DistriRápido S.A.C., que aún no mide su tráfico (ECO-26 está pendiente).

| | CO₂e anual |
|---|---:|
| ANTES | 83,6 kg |
| DESPUÉS | 7,0 kg |
| **Ahorro** | **76,6 kg CO₂e/año** |

Este ahorro corresponde únicamente a la carga de la pantalla de acceso. Es una cifra pequeña en términos absolutos —la mayor parte de la huella digital de la plataforma está en el uso autenticado, no medido aquí— pero demuestra el método y deja el pipeline listo para vigilarla.

## 6. Evidencia de validación

- Pruebas automáticas al cierre: **166 de backend aprobadas y 4 omitidas** (las de PostGIS requieren la base de pruebas) y **115 de frontend aprobadas**; `tsc -b` y el linter sin errores; compilación de producción sin advertencias.
- `lhci autorun` ejecutado localmente: 3 corridas, todas las aserciones de `lighthouserc.json` aprobadas.
- Pipeline [`.github/workflows/green-audit.yml`](../../../.github/workflows/green-audit.yml): compila el frontend, ejecuta LHCI con umbrales (rendimiento ≥ 90, LCP ≤ 1,4 s, TBT ≤ 85 ms, CLS ≤ 0,02, peso ≤ 1,1 MB), calcula CO₂e por visita con SWDM v4 y publica los informes como artefacto.
- **GitHub Actions:** el workflow `green-audit.yml` se ejecutó el 13/11/2026 sobre el commit `1d57b0d` y concluyó con éxito ([ejecución 43453357841](https://github.com/alexito-dev/EcoLogistica/actions/runs/43453357841)).

## 7. Conclusiones

1. El mayor impacto provino de **dos defectos reales**, no de técnicas sofisticadas: un logotipo de 1 MB y un build local mal configurado.
2. La carga inicial de acceso bajó **91,6 %** en peso y **0,1532 g CO₂e** por visita; en escritorio todos los umbrales de la rúbrica se cumplen; en móvil lento, FCP y LCP siguen por encima.
3. La API ahora pagina en bloques de 12, comprime y revalida; falta medirla con datos reales de operación.
4. Trabajo futuro: auditar las vistas autenticadas con un guion de sesión, evaluar `EXPLAIN ANALYZE` sobre PostGIS, medir tráfico real y reducir el JS inicial para mejorar el FCP móvil.

---
*Mediciones del 13/11/2026 en equipo de desarrollo; los valores de Lighthouse varían con la carga de la máquina.*
