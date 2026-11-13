# ESTÁNDARES DE INGENIERÍA DE SOFTWARE Y GUÍA DE DESARROLLO VERDE (GREEN IT)

| Campo | Valor |
|---|---|
| **Versión** | 1.0.0 |
| **Fecha** | 13 de noviembre de 2026 |
| **Autor** | Equipo EcoLogística Huancayo — Zorrilla Apumayta, Alex Jesus; Anco Porras, Jhean Pier Julio; Hilario Talavera, Alexander Daniel; Vera Zea, Jhoanna Hade; Isidro Casio, Jose Luis |
| Proyecto | EcoLogística Huancayo (React + Vite + TypeScript, FastAPI, PostgreSQL/PostGIS) |
| Asignatura | Taller de Proyectos 2 — Inspección 04 (Semana 13) |
| Documento complementario | [01 Informe de reducción del impacto ambiental](01%20Informe%20de%20reduccion%20del%20impacto%20ambiental%20V_1_0_0.md) |

Este documento fundamenta las 8 optimizaciones del informe en tres referencias internacionales y define las reglas arquitectónicas que el equipo adopta para que no se pierdan. La numeración de las pautas W3C sigue la asignación de la consigna de la Semana 13.

---

## 2. Estándares de Ingeniería de Software y Guía de Desarrollo Verde

### 2.1 Relación de Estándares Internacionales Aplicados

#### ISO/IEC 25010 (Calidad del Producto de Software)

| Característica | Subcaracterística | Cómo se justifica en EcoLogística |
|---|---|---|
| Eficiencia de desempeño | Comportamiento temporal | LCP móvil de 7,38 s a 1,99 s y TBT de 101 ms a 13 ms; el listado paginado y revalidable evita transferir y procesar datos repetidos. |
| Eficiencia de desempeño | Utilización de recursos | Transferencia de 1 211 513 B a 101 425 B (−91,6 %); respuestas de la API acotadas a 12 registros y comprimidas; bundle inicial de 477 kB a 265 kB. |
| Eficiencia de desempeño | Capacidad | `LIMIT/OFFSET` con índices compuestos mantiene acotado el costo por solicitud al crecer la tabla de pedidos. |
| Mantenibilidad | Modularidad | División de código por vista (`React.lazy`) y middleware independientes (`cache_http.py`, compresión) fáciles de reemplazar. |
| Mantenibilidad | Analizabilidad | Pocas dependencias (6 de ejecución), reglas verificables por pruebas (`GreenIt.test.ts`, `test_green_it_consultas.py`). |
| Mantenibilidad | Capacidad de ser probado | Cada optimización tiene una prueba automática que impide su regresión. |

#### Principios Green Software Foundation (GSF)

Se adoptan los cuatro principios que la consigna enumera:

| Principio | Aplicación en el proyecto |
|---|---|
| Eficiencia de energía | Minimizar el trabajo por unidad de resultado: no enviar 100 registros cuando se muestran 12; no descargar Leaflet para ver el acceso. |
| Eficiencia de carbono | Reducir bytes transferidos, que son la principal palanca de emisión en web (modelo SWDM v4: 0,300 kWh/GB × 494 g/kWh). |
| Eficiencia de hardware | Menos JavaScript y menos CLS/TBT en el dispositivo del usuario, útil con equipos modestos o redes 2G/3G del valle del Mantaro (RES-06). |
| Medición de la intensidad de carbono | Medir con Lighthouse y SWDM v4 en cada cambio (`green-audit.yml`) en lugar de suponer; el indicador SCI formal queda como trabajo futuro. |

#### W3C Web Sustainability Guidelines (WSG 1.0)

| Pauta (según la consigna) | Aplicación |
|---|---|
| 1.2 — Recursos e interfaz (imágenes) | Logotipo en AVIF/WebP/PNG con `<picture>`; tamaños 64/128 px. |
| 2.4 — Arquitectura y caché | ETag y `Cache-Control: private, no-cache` en la API; `immutable` para estáticos con hash; carga diferida por vista. |
| 3.1 — Red y transferencia | Compresión Brotli/Gzip, paginación de 12 y respuestas 304 sin cuerpo. |

---

### 2.2 Buenas Prácticas y Guía de Desarrollo Verde

#### Reglas arquitectónicas de código limpio (Clean Code, SOLID, DRY, YAGNI)

| Principio | Regla para el backend (FastAPI) | Regla para el frontend (React) |
|---|---|---|
| **Clean Code** | Funciones de una sola responsabilidad; nombres de dominio en español; errores con tipos propios (`errors.py`). | Componentes pequeños y con nombre de dominio; efectos y estado documentados; comentarios que explican el porqué. |
| **SOLID** | *Repositorio* por puerto (`repository.py`) con adaptadores PostgreSQL y memoria intercambiables (Inversión de dependencias); servicios sin conocer HTTP. | Un componente = una responsabilidad (`Logo`, `Hero`, `PedidosTable` controlada por props); contexto de autenticación aislado. |
| **DRY** | Un solo middleware para ETag y uno para compresión, no lógica repetida por router; constantes compartidas (`PREFIJO_API`). | Un cliente HTTP único (`api/http.ts`), una constante `PEDIDOS_POR_PAGINA`, un componente `Logo` para todos los usos. |
| **YAGNI** | No añadir cachés de aplicación, colas ni CDN hasta medir la necesidad; no cachear respuestas con sesión en cachés compartidas. | No añadir TanStack Query, Redux o librerías de fechas mientras `fetch` e `Intl` basten. |

#### Normas Backend (FastAPI / PostgreSQL)

1. **Prohibido** `SELECT *` y entidades completas en listados; enumerar columnas (verificado por prueba).
2. **Los filtros de fecha y estado se resuelven en SQL**, nunca descargando la tabla para filtrar en Python (`listar_por_ventana`).
2. **Obligatorio** acotar todo listado con `LIMIT/OFFSET` y un máximo (`le=100`, valor por defecto 12).
3. Todo filtro o criterio de orden frecuente debe tener índice, documentado en la migración correspondiente.
4. Las respuestas JSON mayores a 1 KB se comprimen (Brotli o Gzip) mediante middleware.
5. Las lecturas autenticadas devuelven `ETag` y `Cache-Control: private, no-cache`; **no** se emite `max-age` en datos por usuario.
6. Dependencia nueva solo con justificación del impacto en instalación e imagen de despliegue.

#### Normas Frontend (React)

1. **Prohibido** subir imágenes PNG/JPG de más de 200 KB sin convertirlas a AVIF/WebP y servirlas con `<picture>`.
2. Las imágenes bajo el pliegue usan `loading="lazy"`; las visibles al inicio, `decoding="async"` y `width/height` para evitar CLS.
3. Las vistas secundarias y las librerías pesadas (mapas, QR) se cargan con `React.lazy()` o `import()` dinámico.
4. Antes de añadir una librería, comprobar su peso en Bundlephobia y si existe una API nativa; está prohibido `moment`, `lodash`, `axios`, `dayjs` y `jquery` (verificado por prueba).
5. Los listados piden bloques de `PEDIDOS_POR_PAGINA` (12) registros y filtran en el servidor.
6. Los íconos y las ilustraciones decorativas se incluyen como SVG en línea o componentes, no como archivos separados.
7. La compilación de producción se ejecuta siempre con `npm run build` (fija `NODE_ENV=production`); no se compila con `vite build` directo.

#### Integración en CI/CD Verde (GitHub Actions Workflow)

El flujo [`.github/workflows/green-audit.yml`](../../../.github/workflows/green-audit.yml) se ejecuta en cada `push` a `main`, `sprint-*/**` y `feature/**`, y en cada `pull_request`:

```yaml
name: Green IT & Performance Audit
on:
  push:
    branches: [main, "sprint-*/**", "feature/**"]
  pull_request:
jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm, cache-dependency-path: frontend/package-lock.json }
      - run: npm ci
        working-directory: frontend
      - run: npm run build
        working-directory: frontend
      - run: npx --yes @lhci/cli@0.14.0 autorun --config=./lighthouserc.json
```

A diferencia de la plantilla de la consigna, **el paso de Lighthouse no usa `|| true`**: si la interfaz supera los umbrales (rendimiento < 90, LCP > 1,4 s, TBT > 85 ms, CLS > 0,02 o peso > 1,1 MB), el flujo falla. Los umbrales se versionan en [`lighthouserc.json`](../../../lighthouserc.json) y se ejecutan en el perfil de escritorio, que es el que cumple la rúbrica. El flujo calcula además los gramos de CO₂e por visita con [`scripts/calcular_swdm.py`](../../../scripts/calcular_swdm.py) y publica los informes como artefacto.

#### Lista de verificación para cada Pull Request

- [ ] ¿Hay listados nuevos? Tienen paginación, índice y columnas explícitas.
- [ ] ¿Hay imágenes nuevas? Están en AVIF/WebP y con dimensiones.
- [ ] ¿Hay dependencias nuevas? Se justificó el peso y no existe alternativa nativa.
- [ ] ¿`green-audit.yml` pasa en verde?
- [ ] ¿Se actualizó la medición SWDM si cambió el peso de la carga inicial?

---

### 2.3 Matriz de Mapeo Directo: Estándares vs. Optimizaciones

| # | Optimización aplicada (stack real) | Equivalente MERN | ISO/IEC 25010 | Principio GSF | Pauta W3C WSG 1.0 | Evidencia |
|---|---|---|---|---|---|---|
| 1 | SQL con columnas explícitas, filtros en la base (`listar_por_ventana`) e índices compuestos (PostgreSQL/PostGIS) | `.select()`, `.lean()`, índices MongoDB | Eficiencia — utilización de recursos | Eficiencia de energía | 3.1 Transferencia de datos | `postgres_repository.py`, migraciones `20261113_02`, `test_green_it_consultas.py` |
| 2 | Paginación `pagina`/`limite` de 12 en API y en la tabla de pedidos | `skip/limit` + React | Eficiencia — capacidad | Eficiencia de energía | 2.1 Eficiencia de la experiencia de usuario | `router.py`, `PaginaPedidos.tsx`, `medir_api_verde.py` |
| 3 | Imágenes AVIF/WebP/PNG adaptativas con `<picture>` | WebP/AVIF + `<picture>` | Eficiencia — comportamiento temporal | Eficiencia de carbono | 1.2 Optimización de medios | `Logo.tsx`, `public/img/` |
| 4 | `React.lazy`/`Suspense` por vista y build de producción con `NODE_ENV` fijado | Code splitting | Mantenibilidad — modularidad | Eficiencia de hardware | 2.4 Arquitectura de código | `App.tsx`, `scripts/build.mjs` |
| 5 | Auditoría y sustitución de dependencias: Preact (`preact/compat`) en lugar de React en el build, `Intl` nativo | Reemplazo de moment/lodash | Mantenibilidad — analizabilidad | Eficiencia de energía | 2.2 Código limpio y librerías | `package.json`, `vite.config.ts`, `fechas.ts`, `GreenIt.test.ts` |
| 6 | SVG en línea (ilustraciones e íconos), CSS en línea, eliminación de recursos inexistentes y de la solicitud de sesión para quien no tiene sesión | Inlining de SVG | Eficiencia — comportamiento temporal | Eficiencia de carbono | 3.2 Minimización de solicitudes HTTP | `Hero.tsx`, `styles.css`, `index.html` |
| 7 | `ETag`, `Cache-Control` y 304; estáticos `immutable` en hosting | ETag Express + React Query | Eficiencia — comportamiento temporal | Eficiencia de energía | 2.4 Estrategias de caché | `cache_http.py`, `deploy/nginx.conf`, `test_cache_compresion.py` |
| 8 | Compresión Brotli con respaldo Gzip (`BrotliMiddleware`) | `compression` de Express | Eficiencia — capacidad | Eficiencia de carbono | 3.1 Optimización de red | `main.py`, `test_cache_compresion.py` |

Las ocho optimizaciones quedan vinculadas a una subcaracterística de ISO/IEC 25010, a un principio de la GSF y a una pauta WSG.

---

### 2.4 Alcance y limitaciones

- La matriz demuestra **trazabilidad**, no certificación: no se realizó una evaluación formal de conformidad con ISO/IEC 25010 ni con la GSF.
- El indicador SCI (Software Carbon Intensity) no se calculó; se mide el peso transferido con SWDM v4 como aproximación.
- La caché de estáticos inmutable y la compresión Brotli de estáticos dependen del servidor de hosting, aún no definido para el despliegue (`deploy/nginx.conf` es una referencia).

---

## 3. Guía de Comandos Git para Despliegue de Documentación

Secuencia usada para crear la estructura, versionar ambos informes y sincronizarlos con GitHub. Las rutas y los nombres de archivo son los exigidos por la consigna (versión semántica `V_1_0_0`).

```bash
# 1. Verificar el estado actual del repositorio
git status

# 2. Crear las carpetas de destino en la ruta exacta
mkdir -p "docs/03 Implementación/reduccion del impacto ambiental"

# 3. Los dos archivos Markdown quedan en esa carpeta:
#    - 01 Informe de reduccion del impacto ambiental V_1_0_0.md
#    - 02 Estandares Ingeniería de software V_1_0_0.md

# 4. Añadir la carpeta y los documentos al área de preparación (staging)
git add "docs/03 Implementación/reduccion del impacto ambiental/"

# 5. Registrar el commit que formaliza la documentación
git commit -m "docs(green-it): add performance optimization reports and software engineering standards"

# 6. Sincronizar con el repositorio remoto
git push origin sprint-4/green-it-calidad
```

**Variación respecto a la plantilla.** La plantilla termina con `git push origin main`. En este proyecto el flujo es de ramas cortas con Pull Request y CI obligatorio (ver GitFlow del Sprint 03), por lo que el `push` se hace a la rama `sprint-4/green-it-calidad` y la integración a `main` se realiza mediante Pull Request una vez que el CI pasa.

