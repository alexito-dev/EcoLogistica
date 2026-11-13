// Compila para producción fijando NODE_ENV antes de que Vite lea los archivos .env.
// Un NODE_ENV=development heredado de un .env local hacía que React se empaquetara en modo desarrollo
// (477 kB en vez de 288 kB, con jsxDEV fallando al combinarlo con define). Green IT / ISO 25010 (eficiencia).
process.env.NODE_ENV = 'production'
const { build } = await import('vite')
await build({ mode: 'production' })
