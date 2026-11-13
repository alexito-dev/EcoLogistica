import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'

const leer = (ruta: string) => readFileSync(new URL(ruta, import.meta.url), 'utf8')

describe('Guardas Green IT (W3C WSG 1.0 pautas 1.2, 2.2 y 3.2)', () => {
  it('no incorpora librerías pesadas con alternativa nativa', () => {
    const { dependencies } = JSON.parse(leer('../package.json')) as { dependencies: Record<string, string> }
    for (const pesada of ['moment', 'lodash', 'axios', 'dayjs', 'jquery']) {
      expect(Object.keys(dependencies)).not.toContain(pesada)
    }
  })

  it('el build de producción usa Preact (preact/compat) en lugar de React', () => {
    const configuracion = leer('../vite.config.ts')
    expect(configuracion).toContain("react: 'preact/compat'")
    expect(configuracion).toContain("command === 'build'")
    const { dependencies } = JSON.parse(leer('../package.json')) as { dependencies: Record<string, string> }
    expect(Object.keys(dependencies)).toContain('preact')
  })

  it('el logotipo se sirve en AVIF/WebP mediante <picture> y no como PNG original', () => {
    const logo = leer('../src/components/Logo.tsx')
    expect(logo).toContain('<picture>')
    expect(logo).toContain('image/avif')
    expect(logo).toContain('image/webp')
    for (const archivo of ['../src/components/AppShell.tsx', '../src/auth/LoginPage.tsx', '../src/styles.css']) {
      expect(leer(archivo)).not.toContain('logo_ecologistica.png')
    }
  })

  it('las vistas secundarias se cargan bajo demanda con React.lazy', () => {
    const app = leer('../src/App.tsx')
    for (const pagina of ['PaginaFlota', 'PaginaRutas', 'PaginaIndicadores']) {
      expect(app).toContain(`const ${pagina} = lazy(() => import('./pages/${pagina}'))`)
    }
  })

  it('los listados piden bloques de 12 registros', async () => {
    const { PEDIDOS_POR_PAGINA } = await import('../src/api/pedidos')
    expect(PEDIDOS_POR_PAGINA).toBe(12)
  })
})
