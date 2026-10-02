import { useEffect, useState } from 'react'
import { Moon, Sun } from 'lucide-react'

type Tema = 'claro' | 'oscuro'

function temaInicial(): Tema {
  try {
    const guardado = localStorage.getItem('tema')
    if (guardado === 'claro' || guardado === 'oscuro') return guardado
  } catch {
    /* almacenamiento no disponible */
  }
  return window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'oscuro' : 'claro'
}

export default function ThemeToggle() {
  const [tema, setTema] = useState<Tema>(temaInicial)

  useEffect(() => {
    document.documentElement.dataset.tema = tema
    try {
      localStorage.setItem('tema', tema)
    } catch {
      /* sin persistencia */
    }
  }, [tema])

  const siguiente: Tema = tema === 'claro' ? 'oscuro' : 'claro'
  return (
    <button
      type="button"
      className="icono-boton icono-boton--borde"
      onClick={() => setTema(siguiente)}
      aria-label={`Cambiar a tema ${siguiente}`}
      title={`Tema ${siguiente}`}
    >
      {tema === 'claro' ? <Moon size={20} aria-hidden="true" /> : <Sun size={20} aria-hidden="true" />}
    </button>
  )
}
