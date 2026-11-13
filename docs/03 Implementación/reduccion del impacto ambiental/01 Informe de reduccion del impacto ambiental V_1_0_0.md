# INFORME DE REDUCCIÓN DEL IMPACTO AMBIENTAL (GREEN IT)

| Campo | Valor |
|---|---|
| **Versión** | 1.0.0 |
| **Fecha** | 13 de noviembre de 2026 |
| **Autor** | Equipo EcoLogística Huancayo — Zorrilla Apumayta, Alex Jesus; Anco Porras, Jhean Pier Julio; Hilario Talavera, Alexander Daniel; Vera Zea, Jhoanna Hade; Isidro Casio, Jose Luis |
| **Proyecto** | EcoLogística Huancayo (React + Vite + TypeScript, FastAPI, PostgreSQL/PostGIS) |
| **Asignatura** | Taller de Proyectos 2 — Inspección 04 (Semana 13) |
| **Documento complementario** | [02 Estándares de ingeniería de software y guía de desarrollo verde](02%20Estandares%20Ingenier%C3%ADa%20de%20software%20V_1_0_0.md) |

> **Nota de adaptación.** La consigna describe las 8 optimizaciones para el stack MERN (MongoDB, Express, React, Node). EcoLogística usa **FastAPI y PostgreSQL/PostGIS** en el servidor, por lo que cada optimización se aplicó con su equivalente real: `.select()`/`.lean()` → columnas explícitas, filtros en SQL e índices; middleware `compression` de Express → `BrotliMiddleware` de Starlette; ETag de Express → middleware ETag propio. **Todas las cifras fueron medidas sobre este repositorio**; no se reutilizaron los valores ilustrativos de la plantilla.

---

## 1. Informe de Reducción del Impacto Ambiental y Optimización

### 1.1 Introducción y Propósito del Informe

El presente informe documenta el proceso de auditoría, refactorización y optimización del rendimiento realizado sobre la plataforma **EcoLogística Huancayo**. En el contexto tecnológico actual, la eficiencia computacional influye de manera directa en la sostenibilidad digital (*Green IT*): cada ciclo de CPU omitido, cada megabyte no transferido y cada consulta de base de datos acotada se traducen en una reducción del consumo energético en servidores, redes y dispositivos finales. La plataforma busca reducir el CO₂ del transporte urbano; resulta coherente que su propia huella digital sea mínima.

El propósito principal de este documento es:

1. Identificar cuellos de botella en la arquitectura full-stack original.
2. Aplicar refactorizaciones técnicas en 8 áreas estratégicas del stack.
3. Medir numéricamente el impacto mediante auditorías estandarizadas (Google Lighthouse, mediciones de la API y modelo SWDM v4).
4. Validar la reducción de la huella de carbono digital sin comprometer la experiencia de usuario ni la integridad funcional, y declarar con transparencia lo que no se cumplió.

### 1.2 Diagnóstico Inicial del Proyecto (Métricas Previas)

La auditoría inicial, realizada sobre el commit `2b08013` antes de las intervenciones, reveló ineficiencias en la transferencia de datos y en la ejecución en cliente y servidor. Se cargaba un logotipo PNG de 1 MB para mostrarlo a 32–56 px, el listado de pedidos pedía 100 registros por solicitud sin comprimir ni validadores de caché, la compilación local empaquetaba React en modo desarrollo, y la planificación diaria descargaba **todos** los pedidos para filtrarlos en Python.

**Método de medición.**

| Aspecto | Detalle |
|---|---|
| Herramienta | Lighthouse 12 (Chrome headless): rendimiento, accesibilidad, buenas prácticas y SEO |
| Página auditada | Pantalla pública de acceso `/` del build de producción servido con `vite preview` |
| Perfiles | **Móvil** (predeterminado de Lighthouse: Moto G, 4G lenta simulada) y **escritorio** (`--preset=desktop`) |
| API | `backend/scripts/medir_api_verde.py`: 100 pedidos sintéticos en memoria, mediana de 40 llamadas |
| Modelo de carbono | SWDM v4 (`scripts/calcular_swdm.py`) |
| Evidencia consolidada | [`evidencias/`](evidencias/): cuatro informes Lighthouse completos (antes y después, móvil y escritorio), `resumen-lighthouse.json` y `medicion-api.txt` |

**Resumen de Métricas de Referencia (Estado ANTES, perfil móvil):**

- **Score Global de Rendimiento (Lighthouse):** 74 / 100
- **First Contentful Paint (FCP):** 1,97 s
- **Largest Contentful Paint (LCP):** 7,38 s
- **Total Blocking Time (TBT):** 101 ms
- **Cumulative Layout Shift (CLS):** 0
- **Peso Total de la Página (Transferencia de Red):** 1 211 513 B (1,21 MB)
- **Número Total de Peticiones HTTP:** 14 solicitudes
- **Tiempo Promedio de Respuesta API (listado de pedidos):** 9,19 ms (medición en proceso, 100 registros sin comprimir)
- **Estimación de Emisiones de CO₂ por Visita:** 0,1672 g CO₂e (según modelo SWDM v4)

**Hallazgos verificados en el repositorio:**

1. `frontend/public/logo_ecologistica.png` pesaba **1 049 853 B** (1536 × 1024 px) y se mostraba a 32–56 px: 87 % de la transferencia y elemento LCP del acceso.
2. El `.env` local contenía `NODE_ENV=development`; Vite lo leía y `vite build` **empaquetaba React en modo desarrollo** (`index.js` de 477 kB en vez de 265 kB). En CI no ocurría porque `.env` no se versiona.
3. Las fuentes `Codec Pro` se referenciaban con `url('/fonts/*.woff2')` pero los archivos no existen (licencia comercial): 4 advertencias de compilación y 3 solicitudes por carga resueltas con `index.html`; tampoco había favicon (404).
4. El listado de pedidos pedía **100 registros** por solicitud y los paginaba solo en el navegador (8 por página); el valor por defecto de la API era 20.
5. Las respuestas JSON de la API no se comprimían ni llevaban `ETag`.
6. `RutasService.pedidos_del_dia` recorría **todos** los pedidos en lotes de 100 y filtraba fecha y estado en Python.

### 1.3 Detalle Técnico de las 8 Optimizaciones Implementadas

#### 1. Optimización de Consultas a la Base de Datos (equivalente de `.select()`, `.lean()` e índices)

**Diagnóstico:** `RutasService.pedidos_del_dia` descargaba todos los pedidos de la base (en lotes de 100, con un conteo adicional por lote) y descartaba en Python los que no eran de la fecha o no eran planificables, sobrecargando la red entre la API y PostgreSQL y la memoria del servidor.

**Implementación:** se movió el filtro a la base de datos con un método de repositorio `listar_por_ventana` (día en hora de Lima y estados), que usa un índice compuesto nuevo `(estado, ventana_inicio)`. La consulta enumera columnas explícitas —nunca `SELECT *`— y construye directamente objetos de dominio sin capa ORM de hidratación, el beneficio que en Mongoose aportan `.select()` y `.lean()`.

**ANTES** (`backend/src/app/rutas/service.py`):

```python
def pedidos_del_dia(self, fecha: date) -> list[Pedido]:
    encontrados: list[Pedido] = []
    pagina = 1
    while True:
        lote, total = self._pedidos.listar(None, pagina, _LOTE)   # todos los pedidos, 100 por lote
        encontrados += [
            p for p in lote
            if p.estado in ESTADOS_PLANIFICABLES and p.ventana_inicio.astimezone(LIMA).date() == fecha
        ]
        if pagina * _LOTE >= total or not lote:
            return encontrados
        pagina += 1
```

**DESPUÉS** (`rutas/service.py`, `pedidos/postgres_repository.py`, migración `20261113_02`):

```python
def pedidos_del_dia(self, fecha: date) -> list[Pedido]:
    desde = datetime.combine(fecha, time.min, tzinfo=LIMA)
    return self._pedidos.listar_por_ventana(desde, desde + timedelta(days=1), ESTADOS_PLANIFICABLES)
```
```python
# PedidosPostgresRepository.listar_por_ventana: el filtro se resuelve en la base
text(_SELECT_PEDIDO
     + f" WHERE p.ventana_inicio >= :desde AND p.ventana_inicio < :hasta AND p.estado IN ({lista})"
     + " ORDER BY p.ventana_inicio, p.codigo")
```
```sql
CREATE INDEX ix_pedidos_estado_ventana ON pedidos (estado, ventana_inicio);   -- filtro de planificación
CREATE INDEX ix_pedidos_estado_creado  ON pedidos (estado, creado_en DESC);   -- listado paginado
CREATE INDEX ix_ubicaciones_punto      ON ubicaciones USING GIST (punto);     -- consultas espaciales
```

**Verificación:** pruebas del repositorio en memoria (borde del día en hora de Lima, estados, orden), prueba de integración contra PostGIS en CI y la guarda [`test_green_it_consultas.py`](../../../backend/tests/test_green_it_consultas.py), que falla si aparece un `SELECT *`, si el listado pierde `LIMIT/OFFSET` o si desaparece un índice. **Límite:** no se ejecutó `EXPLAIN ANALYZE`, por lo que la mejora en milisegundos de PostgreSQL no se cuantifica; el beneficio medible es que deja de transferirse la tabla completa.

#### 2. Paginación de Datos en Backend y Frontend (bloques de 12)

**Diagnóstico:** el listado pedía 100 registros por solicitud (48 647 B sin comprimir en la medición) y la tabla los paginaba solo en el navegador.

**Implementación:** paginación por `pagina` y `limite` en el servidor, con valor por defecto de **12 registros**, y filtro por estado resuelto también en el servidor. La tabla del frontend es controlada por la página y muestra «Mostrando a–b de total».

**ANTES:**

```tsx
listarPedidos(1, 100)            // 100 registros en cada carga
const POR_PAGINA = 8             // paginación solo en el navegador
```
```python
limite: Annotated[int, Query(ge=1, le=100)] = 20
```

**DESPUÉS:**

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

**Medición** ([`evidencias/medicion-api.txt`](evidencias/medicion-api.txt)):

| Escenario | Bytes |
|---|---:|
| ANTES: 100 registros, sin compresión | 48 647 |
| DESPUÉS: página de 12 con Brotli | 728 |
| Revalidación con `If-None-Match` | 0 (HTTP 304) |

Reducción de **98,5 %**; la cifra está inflada porque los pedidos sintéticos son casi idénticos y comprimen de forma excepcional. Por paginación sola la reducción esperada con datos reales es de ≈ 88 % (12 de 100 registros).

#### 3. Compresión y Optimización de Imágenes (AVIF/WebP con `<picture>`)

**Diagnóstico:** el logotipo PNG de 1536 × 1024 px (1 049 853 B) se descargaba para mostrarse a 32–56 px.

**Implementación:** variantes AVIF, WebP y PNG de 64 y 128 px (1x/2x) servidas con `<picture>` y `srcset` adaptativo.

**ANTES:**

```tsx
<img src="/logo_ecologistica.png" alt="" width="40" height="40" />   // 1 049 853 B
```

**DESPUÉS** (`frontend/src/components/Logo.tsx`):

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
| `logo-64` AVIF / WebP / PNG | 1 526 / 1 824 / 2 255 B |
| `logo-128` AVIF / WebP / PNG | 3 063 / 4 156 / 4 145 B |

El PNG original sale de `public/` (se conserva en `assets/images/`). El logotipo está visible desde el inicio, por lo que lleva `decoding="async"` y dimensiones explícitas (sin `loading="lazy"`, que retrasaría el LCP).

#### 4. Carga Diferida (Lazy Loading) y Code Splitting

**Diagnóstico:** las vistas secundarias ya se cargaban con `React.lazy` desde el Sprint 3; el defecto era el empaquetado de producción (hallazgo 2) y las vistas nuevas debían seguir el mismo patrón.

**ANTES:**

```text
dist/assets/index-*.js   476,01 kB │ gzip: 140,31 kB   (React en modo desarrollo)
```

**DESPUÉS:**

```tsx
// frontend/src/App.tsx — Flota, Rutas, Seguimiento, Mi ruta e Indicadores bajo demanda
const PaginaFlota = lazy(() => import('./pages/PaginaFlota'))
const PaginaRutas = lazy(() => import('./pages/PaginaRutas'))
const PaginaSeguimiento = lazy(() => import('./pages/PaginaSeguimiento'))
const PaginaMiRuta = lazy(() => import('./pages/PaginaMiRuta'))
const PaginaIndicadores = lazy(() => import('./pages/PaginaIndicadores'))
// <Suspense fallback={<CargandoVista />}> ... </Suspense>
```
```js
// frontend/scripts/build.mjs — "build": "tsc -b && node scripts/build.mjs"
process.env.NODE_ENV = 'production'
const { build } = await import('vite')
await build({ mode: 'production' })
```
```text
dist/assets/index-*.js        265,42 kB │ gzip: 82,69 kB   (−44 % y −41 % gzip)
dist/assets/leaflet-*.js      148,60 kB │ gzip: 43,33 kB   (solo al abrir Rutas o Mi ruta)
dist/assets/browser-*.js (qrcode) 23,46 kB │ gzip: 8,86 kB  (solo al enrolar MFA)
```

La pantalla de acceso no descarga Leaflet ni las vistas de gestión. Forzar `NODE_ENV` desde `vite.config.ts` no funcionó (Vite lee `.env` antes), por eso se usa un lanzador que lo fija antes de importar Vite.

#### 5. Depuración y Eliminación de Dependencias Innecesarias

**Diagnóstico:** se auditaron las dependencias de ejecución (`react`, `react-dom`, `leaflet`, `lucide-react`, `qrcode`). No existen `moment`, `lodash`, `axios`, `dayjs` ni `jquery`: las fechas usan `Intl.DateTimeFormat` y las peticiones, `fetch`. `lucide-react` se importa por nombre y se *tree-shakea*; `qrcode` y `leaflet` están en fragmentos diferidos. El único hallazgo real fue que `@types/qrcode`, un paquete solo de tipos, figuraba como dependencia de ejecución.

**ANTES** (`frontend/package.json`):

```json
"dependencies": { "@types/qrcode": "^1.5.6", "leaflet": "^1.9.4", "lucide-react": "^1.50.0", "qrcode": "^1.5.4", "react": "^19.2.8", "react-dom": "^19.2.8" }
```

**DESPUÉS:**

```json
"dependencies": { "leaflet": "^1.9.4", "lucide-react": "^1.50.0", "qrcode": "^1.5.4", "react": "^19.2.8", "react-dom": "^19.2.8" },
"devDependencies": { "@types/qrcode": "^1.5.6" }
```

```ts
// Ya vigente: API nativa en lugar de moment.js (frontend/src/lib/fechas.ts)
const formato = new Intl.DateTimeFormat('es-PE', { timeZone: 'America/Lima', day: '2-digit', month: '2-digit',
  year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false })
```

La guarda [`GreenIt.test.ts`](../../../frontend/tests/GreenIt.test.ts) falla si se incorpora alguna de esas librerías. **Límite:** la mejora de esta área es pequeña; no se afirma un ahorro de peso medido.

#### 6. Reducción de Solicitudes HTTP (inlining de SVG y recursos inexistentes)

**Implementación:** las ilustraciones (`Hero.tsx`, acceso) son `<svg>` en línea y los íconos son componentes de `lucide-react` compilados en el paquete JS: 0 solicitudes por ícono. Además se eliminaron las solicitudes a fuentes inexistentes y se agregó favicon.

```css
/* ANTES */  src: local('Codec Pro'), local('CodecPro-Regular'), url('/fonts/CodecPro-Regular.woff2') format('woff2');
/* DESPUÉS */ src: local('Codec Pro'), local('CodecPro-Regular');   /* sin archivo remoto inexistente */
```

| Medida | ANTES | DESPUÉS |
|---|---:|---:|
| Solicitudes en la carga de acceso | 14 | **9** (−36 %) |

#### 7. Estrategia de Caché de Recursos

**ANTES:** la API no emitía `ETag` ni `Cache-Control`.

**DESPUÉS** (`backend/src/app/cache_http.py`):

```python
class EtagMiddleware(BaseHTTPMiddleware):
    """Añade ETag débil a los GET 200 con JSON y responde 304 si el cliente ya tiene la versión."""
    async def dispatch(self, request, call_next):
        ...
        etag = calcular_etag(cuerpo)          # W/"<sha256[:32]>"
        cabeceras = {"ETag": etag, "Cache-Control": "private, no-cache", "Vary": "Cookie, Accept-Encoding"}
        if _coincide(request.headers.get("if-none-match"), etag):
            return Response(status_code=304, headers=cabeceras)
```

- `private, no-cache` (no `max-age=31536000`) porque las respuestas dependen de la cookie de sesión: no se guardan en cachés compartidas y siempre se revalidan; si no cambiaron, la respuesta es **304 sin cuerpo (0 B)**.
- Para los **estáticos**, [`frontend/deploy/nginx.conf`](../../../frontend/deploy/nginx.conf) define `Cache-Control: public, max-age=31536000, immutable` en `/assets/` (nombres con hash), 30 días en `/img/` y `no-cache` para `index.html`.
- **Caché de estado en cliente.** No se incorpora TanStack Query: el navegador ya mantiene la caché HTTP y reenvía `If-None-Match`, lo que la prueba [`e2e/verde.spec.ts`](../../../frontend/e2e/verde.spec.ts) comprueba en Chrome real (la segunda carga del listado va con validador). Añadir la librería sumaría ≈ 13 kB comprimidos a un paquete inicial de 83 kB sin un beneficio medible.
- Pruebas: [`test_cache_compresion.py`](../../../backend/tests/test_cache_compresion.py) (ETag, 304, invalidación al cambiar los datos, exclusión de `/auth` y de las escrituras).

#### 8. Optimización de la API: Compresión Brotli/Gzip

**ANTES:** respuestas JSON sin comprimir.

**DESPUÉS** (`backend/src/app/main.py`, dependencia `brotli-asgi`):

```python
app.add_middleware(EtagMiddleware)
app.add_middleware(CORSMiddleware, ..., expose_headers=["ETag"])
# Capa más externa: Brotli con respaldo Gzip para respuestas > 1 KB
app.add_middleware(BrotliMiddleware, quality=4, minimum_size=1024, gzip_fallback=True)
```

Comprobado en Chrome real: el listado llega con `content-encoding` `br` o `gzip` y `limite=12`. La compresión de los **estáticos** corresponde al hosting (Gzip activo en `deploy/nginx.conf`; Brotli requiere `ngx_brotli`). El servidor `vite preview` de las mediciones aplica Gzip **tanto en el ANTES como en el DESPUÉS**, por lo que la reducción de peso del frontend proviene de la imagen y del build, no de una diferencia de compresión.

### 1.4 Tabla Comparativa de Métricas ANTES vs. DESPUÉS

**Perfil móvil (4G lenta simulada):**

| Métrica / Indicador | Estado Inicial (ANTES) | Estado Optimizado (DESPUÉS) | Variación Absoluta | Mejora (%) |
|---|---:|---:|---:|---:|
| Performance Score (Lighthouse) | 74 / 100 | **99 / 100** | +25 pts | +33,8 % |
| First Contentful Paint (FCP) | 1,97 s | 1,51 s | −0,46 s | −23,4 % |
| Largest Contentful Paint (LCP) | 7,38 s | **1,99 s** | −5,39 s | −73,0 % |
| Total Blocking Time (TBT) | 101 ms | **13 ms** | −88 ms | −87,1 % |
| Cumulative Layout Shift (CLS) | 0 | 0 | 0 | — |
| Peso Total de Transferencia | 1 211 513 B (1,21 MB) | **101 425 B (0,10 MB)** | −1 110 088 B | −91,6 % |
| Número Total de Solicitudes HTTP | 14 | 9 | −5 | −35,7 % |
| Tiempo de respuesta API (listado, mediana) | 9,19 ms | 7,80 ms | −1,39 ms | −15,1 % |
| Huella de Carbono (g CO₂e / visita) | 0,1672 g | **0,0140 g** | −0,1532 g | −91,6 % |

El tiempo de respuesta de la API se midió en proceso con 100 pedidos sintéticos y osciló entre −15 % y −27 % en tres corridas; es una mejora modesta porque el costo dominante en esa medición no es la red.

**Perfil escritorio (el que verifica el pipeline `green-audit.yml`):**

| Métrica | ANTES | DESPUÉS | Umbral de la rúbrica | ¿Cumple? |
|---|---:|---:|---|:---:|
| Rendimiento | 96 | **100** | ≥ 90 | Sí |
| FCP | 0,45 s | **0,39 s** | ≤ 1,0 s | Sí |
| LCP | 1,42 s | **0,54 s** | ≤ 1,4 s | Sí |
| TBT | 0 ms | **0 ms** | ≤ 85 ms | Sí |
| CLS | 0 | **0** | ≤ 0,02 | Sí |
| Peso | 1,21 MB | **0,10 MB** | ≤ 1,1 MB | Sí |

**Declaración de incumplimientos.**

- **En móvil con 4G lenta simulada, FCP (1,51 s) y LCP (1,99 s) no alcanzan 1,0 s y 1,4 s**, aunque el puntaje (99), el TBT, el CLS y el peso sí cumplen. Se probaron dos mejoras adicionales (hoja de estilos en línea, y pantalla de carga estática con estilos no bloqueantes): la segunda dio FCP entre 0,9 s y 1,5 s según la corrida, es decir, no fue estable, y el LCP quedó en 2,0 s; se revirtieron por añadir complejidad sin beneficio reproducible. La brecha depende del JavaScript inicial (83 kB comprimidos).
- Los valores de la plantilla (38 → 96, 8,4 MB, 68 solicitudes, 2,15 g) no corresponden a este proyecto.
- Se midió la pantalla de acceso (carga inicial pública); las vistas autenticadas requieren sesión con MFA. Durante las auditorías la API no estaba en ejecución: las 2–4 solicitudes de verificación de sesión fallan igual antes y después.

**Atribución del ahorro de peso (móvil):**

| Intervención | Peso (B) | Efecto |
|---|---:|---:|
| Línea base (compilación local con `.env` de desarrollo) | 1 211 513 | — |
| Solo build de producción correcto | 1 148 620 | −62 893 (−5,2 %) |
| + logotipo AVIF/WebP/PNG pequeño, favicon y sin fuentes inexistentes | 101 425 | −1 047 195 adicionales (−91,2 %) |

### 1.5 Análisis de Impacto Ambiental y Eficiencia Energética

**Metodología de Cálculo (Sustainable Web Design Model v4 — SWDM v4).** Constantes consultadas el 13/11/2026 en <https://sustainablewebdesign.org/estimating-digital-emissions/>: energía total **0,300 kWh/GB** (operacional 0,194 + incorporada 0,106; centros de datos 0,067, redes 0,072 y dispositivos 0,161) e intensidad eléctrica global **494 g CO₂e/kWh**.

```text
Energía (kWh) = bytes / 1 024³ × 0,300
Emisiones (g) = Energía × 494
```

Se calcula la **primera visita** (sin caché ni hosting verde acreditado). No se aplicó la intensidad peruana porque no se verificó una cifra citable; el resultado se recalcula cambiando `INTENSIDAD_G_KWH` en [`scripts/calcular_swdm.py`](../../../scripts/calcular_swdm.py). Las constantes de la plantilla de la consigna (0,815 kWh/GB; 442 g/kWh) corresponden a una versión anterior y no se utilizaron.

- **Escenario Inicial (ANTES):** transferencia 1,21 MB (0,001128 GB) → consumo 0,0003385 kWh → emisiones **0,1672 g CO₂e / visita**.
- **Escenario Optimizado (DESPUÉS):** transferencia 0,10 MB (0,0000945 GB) → consumo 0,0000283 kWh → emisiones **0,0140 g CO₂e / visita** (−91,6 %).

**Proyección Anual** (escenario de referencia de la consigna: 500 000 visitas/año; no es dato de DistriRápido S.A.C., que aún no mide su tráfico):

| | CO₂e anual |
|---|---:|
| Emisiones previas | 83,6 kg |
| Emisiones optimizadas | 7,0 kg |
| **Ahorro neto anual** | **76,6 kg CO₂e** |

El ahorro corresponde únicamente a la carga de la pantalla de acceso; la mayor parte de la huella de la plataforma está en el uso autenticado, no medido aquí. El método y el pipeline quedan listos para vigilarla.

### 1.6 Evidencias Visuales de Validación (Auditoría Lighthouse)

Reportes consolidados en [`evidencias/`](evidencias/) (JSON completos de Lighthouse 12, abribles en el visor de Lighthouse) y ejecuciones de [GitHub Actions](https://github.com/alexito-dev/EcoLogistica/actions/runs/43453357841).

```text
================================================================================
AUDITORÍA LIGHTHOUSE - ESTADO INICIAL (ANTES) - móvil
================================================================================
[!] Performance:  ███████████████░░░░░  74/100
- FCP: 1,97 s   - LCP: 7,38 s (ROJO)   - TBT: 101 ms   - CLS: 0
- Transferencia: 1,21 MB en 14 solicitudes
================================================================================
AUDITORÍA LIGHTHOUSE - ESTADO OPTIMIZADO (DESPUÉS) - móvil
================================================================================
[*] Performance:  ████████████████████  99/100
- FCP: 1,51 s (ámbar)   - LCP: 1,99 s (ámbar)   - TBT: 13 ms   - CLS: 0
- Transferencia: 0,10 MB en 9 solicitudes
Accesibilidad 100 | Buenas prácticas 96 | SEO 100 (corridas de Lighthouse CI)
================================================================================
ESCRITORIO (verificado por green-audit.yml en GitHub Actions)
================================================================================
[*] Performance:  ████████████████████  100/100
- FCP: 0,39 s   - LCP: 0,54 s   - TBT: 0 ms   - CLS: 0   - 0,10 MB
```

**Validación adicional.** Pruebas al cierre: 191 de backend aprobadas y 9 omitidas (PostgreSQL, que corren en CI), 127 de frontend y 10 E2E con Playwright; `tsc -b` y linter sin errores; `lhci autorun` aprobado localmente y en GitHub Actions.

### 1.7 Conclusiones

1. El mayor impacto provino de **dos defectos reales** —un logotipo de 1 MB y un build local mal configurado—, no de técnicas sofisticadas.
2. La carga inicial de acceso bajó **91,6 %** en peso y **0,1532 g CO₂e** por visita; en escritorio todos los umbrales de la rúbrica se cumplen; en móvil lento, FCP y LCP siguen por encima.
3. La API ahora pagina en bloques de 12, comprime, revalida y filtra la planificación en la base; falta medirla con datos reales de operación.
4. Trabajo futuro: auditar las vistas autenticadas con un guion de sesión, ejecutar `EXPLAIN ANALYZE` sobre PostGIS, medir tráfico real y reducir el JavaScript inicial para mejorar el FCP y el LCP móviles.

---
*Mediciones del 13/11/2026 en equipo de desarrollo; los valores de Lighthouse varían con la carga de la máquina.*
