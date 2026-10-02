/// <reference types="vitest/config" />
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Puerto 3000 = CORS_ORIGIN de .env.example
export default defineConfig({
  plugins: [react()],
  envDir: '..', // usa el .env de la raíz del repositorio (VITE_API_URL)
  server: { port: 3000 },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './tests/setup.ts',
    include: ['tests/**/*.test.{ts,tsx}'],
  },
})
