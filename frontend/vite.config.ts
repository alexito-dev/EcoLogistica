/// <reference types="vitest/config" />
import react from '@vitejs/plugin-react'
import { defineConfig, type Plugin } from 'vite'

/**
 * Incrusta la hoja de estilos principal en el HTML del build: elimina una solicitud que bloquea el primer pintado
 * (un viaje de ida y vuelta menos en redes lentas).
 */
function cssEnLinea(): Plugin {
  return {
    name: 'css-en-linea',
    apply: 'build',
    enforce: 'post',
    transformIndexHtml(html, { bundle }) {
      if (!bundle) return html
      let resultado = html
      for (const [nombre, pieza] of Object.entries(bundle)) {
        if (pieza.type !== 'asset' || !nombre.startsWith('assets/index-') || !nombre.endsWith('.css')) continue
        const enlace = new RegExp(`<link[^>]*href="[^"]*${nombre.split('/').pop()}"[^>]*>`)
        if (!enlace.test(resultado)) continue
        resultado = resultado.replace(enlace, `<style>${String(pieza.source)}</style>`)
        delete bundle[nombre]
      }
      return resultado
    },
  }
}

// Puerto 3000 = CORS_ORIGIN de .env.example
// Preact en el build de producción: misma API (preact/compat) con ~100 kB menos de JavaScript inicial.
const alias = {
  react: 'preact/compat',
  'react-dom/client': 'preact/compat/client',
  'react-dom': 'preact/compat',
  'react/jsx-runtime': 'preact/jsx-runtime',
}

export default defineConfig(({ command }) => ({
  plugins: [react(), cssEnLinea()],
  resolve: command === 'build' ? { alias } : {},
  envDir: '..', // usa el .env de la raíz del repositorio (VITE_API_URL)
  server: { port: 3000 },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './tests/setup.ts',
    include: ['tests/**/*.test.{ts,tsx}'],
    // lcov lo consume SonarQube (sonar-project.properties)
    coverage: { provider: 'v8', include: ['src/**'], reporter: ['text-summary', 'lcov'] },
  },
}))
