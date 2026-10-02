import { useEffect, useRef, useState, type FormEvent } from 'react'
import { ArrowLeft, CircleAlert, Eye, EyeOff, KeyRound, LogIn, ShieldCheck, Smartphone } from 'lucide-react'
import { iniciarSesion, verificarCodigo, type RespuestaLogin } from '../api/auth'
import { ApiError } from '../api/http'
import ThemeToggle from '../components/ThemeToggle'
import { useAuth } from './useAuth'

type Paso = 'credenciales' | 'mfa' | 'enrolar'

/** "JBSWY3DPEHPK3PXP" -> "JBSW Y3DP EHPK 3PXP" para copiarla a mano sin errores. */
function agrupar(clave: string): string {
  return clave.replace(/(.{4})/g, '$1 ').trim()
}

function CodigoQR({ uri }: { uri: string }) {
  const [svg, setSvg] = useState<string | null>(null)
  useEffect(() => {
    let activo = true
    // La librería del QR se carga solo al enrolar, para no pesar en el resto de la app.
    import('qrcode')
      .then((m) => m.default.toString(uri, { type: 'svg', margin: 1, color: { dark: '#032d2f', light: '#ffffff' } }))
      .then((s) => activo && setSvg(s))
      .catch(() => activo && setSvg(null))
    return () => {
      activo = false
    }
  }, [uri])
  if (!svg) return <div className="qr qr--cargando" aria-hidden="true" />
  return (
    <img
      className="qr"
      src={`data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`}
      alt="Código QR para registrar EcoLogística en su app autenticadora"
      width={184}
      height={184}
    />
  )
}

export default function LoginPage() {
  const { entrar, aviso } = useAuth()
  const [paso, setPaso] = useState<Paso>('credenciales')
  const [correo, setCorreo] = useState('')
  const [clave, setClave] = useState('')
  const [verClave, setVerClave] = useState(false)
  const [codigo, setCodigo] = useState('')
  const [enrolamiento, setEnrolamiento] = useState<RespuestaLogin | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)
  const codigoRef = useRef<HTMLInputElement>(null)
  const claveRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (paso !== 'credenciales') codigoRef.current?.focus()
  }, [paso])

  async function enviarCredenciales(e: FormEvent) {
    e.preventDefault()
    setError(null)
    setEnviando(true)
    try {
      const r = await iniciarSesion(correo, clave)
      setClave('')
      setCodigo('')
      setEnrolamiento(r.paso === 'ENROLAR' ? r : null)
      setPaso(r.paso === 'ENROLAR' ? 'enrolar' : 'mfa')
    } catch (err) {
      setClave('') // la contraseña nunca se conserva tras un rechazo
      setError(err instanceof ApiError ? err.message : 'No se pudo iniciar sesión.')
      claveRef.current?.focus()
    } finally {
      setEnviando(false)
    }
  }

  async function enviarCodigo(e: FormEvent) {
    e.preventDefault()
    setError(null)
    setEnviando(true)
    try {
      entrar(await verificarCodigo(codigo))
    } catch (err) {
      setCodigo('')
      if (err instanceof ApiError && err.status === 401 && !err.errors.codigo) {
        // Comprobante vencido o agotado: se vuelve a pedir la contraseña.
        setPaso('credenciales')
        setError(err.message)
      } else {
        setError(err instanceof ApiError ? (err.errors.codigo ?? err.message) : 'No se pudo verificar el código.')
        codigoRef.current?.focus()
      }
    } finally {
      setEnviando(false)
    }
  }

  function volver() {
    setPaso('credenciales')
    setError(null)
    setCodigo('')
  }

  const mensajeError = error && (
    <div role="alert" className="aviso aviso--error">
      <CircleAlert size={20} aria-hidden="true" />
      <div>
        <strong>{error}</strong>
      </div>
    </div>
  )

  return (
    <div className="acceso">
      <section className="acceso__marca" aria-hidden="true">
        <svg className="hero__arte" viewBox="0 0 600 400" preserveAspectRatio="xMidYMax slice">
          <circle cx="470" cy="90" r="40" className="hero__sol" />
          <path d="M0 330 C 140 270, 260 360, 380 310 S 540 260, 600 290 L 600 400 L 0 400 Z" className="hero__colina hero__colina--atras" />
          <path d="M0 370 C 160 320, 300 390, 430 350 S 560 340, 600 355 L 600 400 L 0 400 Z" className="hero__colina hero__colina--frente" />
          <g className="hero__arbol" transform="translate(150 268)">
            <rect x="-3" y="26" width="6" height="32" rx="3" />
            <circle cx="0" cy="16" r="22" />
          </g>
          <g className="hero__arbol hero__arbol--chico" transform="translate(205 292)">
            <rect x="-2" y="16" width="4" height="22" rx="2" />
            <circle cx="0" cy="10" r="14" />
          </g>
        </svg>
        <div className="acceso__marca-texto">
          <img src="/logo_ecologistica.png" alt="" width="56" height="56" />
          <p className="acceso__nombre">EcoLogística Huancayo</p>
          <p className="acceso__lema">Rutas sostenibles de última milla para el valle del Mantaro.</p>
        </div>
      </section>

      <section className="acceso__panel">
        <div className="acceso__tema">
          <ThemeToggle />
        </div>
        <div className="acceso__tarjeta aparecer">
          {paso === 'credenciales' && (
            <form onSubmit={enviarCredenciales} noValidate>
              <span className="acceso__icono">
                <LogIn size={24} aria-hidden="true" />
              </span>
              <h1>Iniciar sesión</h1>
              <p className="subtitulo">Ingrese con su correo institucional.</p>
              {aviso && !error && (
                <p className="aviso aviso--info" role="status">
                  {aviso}
                </p>
              )}
              {mensajeError}
              <div className="campo">
                <label htmlFor="correo">Correo</label>
                <input
                  id="correo"
                  type="email"
                  autoComplete="username"
                  value={correo}
                  onChange={(e) => setCorreo(e.target.value)}
                  required
                  autoFocus
                />
              </div>
              <div className="campo">
                <label htmlFor="clave">Contraseña</label>
                <div className="campo-clave">
                  <input
                    id="clave"
                    ref={claveRef}
                    type={verClave ? 'text' : 'password'}
                    autoComplete="current-password"
                    value={clave}
                    onChange={(e) => setClave(e.target.value)}
                    required
                  />
                  <button
                    type="button"
                    className="icono-boton"
                    onClick={() => setVerClave((v) => !v)}
                    aria-label={verClave ? 'Ocultar contraseña' : 'Mostrar contraseña'}
                    aria-pressed={verClave}
                  >
                    {verClave ? <EyeOff size={18} aria-hidden="true" /> : <Eye size={18} aria-hidden="true" />}
                  </button>
                </div>
              </div>
              <button type="submit" className="boton boton--primario boton--bloque" disabled={enviando || !correo || !clave}>
                {enviando ? 'Verificando…' : 'Continuar'}
              </button>
            </form>
          )}

          {paso !== 'credenciales' && (
            <form onSubmit={enviarCodigo} noValidate>
              <span className="acceso__icono">
                {paso === 'enrolar' ? <Smartphone size={24} aria-hidden="true" /> : <ShieldCheck size={24} aria-hidden="true" />}
              </span>
              <h1>{paso === 'enrolar' ? 'Active la verificación en dos pasos' : 'Verificación en dos pasos'}</h1>
              {paso === 'mfa' && (
                <p className="subtitulo">Ingrese el código de 6 dígitos de su app autenticadora.</p>
              )}
              {paso === 'enrolar' && enrolamiento?.otpauthUri && enrolamiento.claveMfa && (
                <ol className="pasos-enrolar">
                  <li>Abra una app autenticadora (Google Authenticator, Microsoft Authenticator u otra).</li>
                  <li>
                    Escanee este código QR:
                    <CodigoQR uri={enrolamiento.otpauthUri} />
                  </li>
                  <li>
                    O ingrese la clave manualmente:
                    <span className="clave-mfa">
                      <KeyRound size={16} aria-hidden="true" />
                      <code aria-label="Clave para ingreso manual">{agrupar(enrolamiento.claveMfa)}</code>
                    </span>
                  </li>
                  <li>Escriba el código de 6 dígitos que muestra la app.</li>
                </ol>
              )}
              {mensajeError}
              <div className="campo">
                <label htmlFor="codigo">Código de verificación</label>
                <input
                  id="codigo"
                  ref={codigoRef}
                  className="input-codigo"
                  inputMode="numeric"
                  autoComplete="one-time-code"
                  pattern="[0-9]{6}"
                  maxLength={6}
                  value={codigo}
                  onChange={(e) => setCodigo(e.target.value.replace(/\D/g, '').slice(0, 6))}
                  aria-describedby="codigo-ayuda"
                />
                <p id="codigo-ayuda" className="ayuda">
                  El código cambia cada 30 segundos.
                </p>
              </div>
              <button type="submit" className="boton boton--primario boton--bloque" disabled={enviando || codigo.length !== 6}>
                {enviando ? 'Verificando…' : paso === 'enrolar' ? 'Activar y entrar' : 'Verificar y entrar'}
              </button>
              <button type="button" className="boton boton--secundario boton--bloque" onClick={volver}>
                <ArrowLeft size={18} aria-hidden="true" />
                Volver
              </button>
            </form>
          )}
        </div>
        <p className="acceso__pie">Taller de Proyectos 2 · Ingeniería de Sistemas e Informática · 2026</p>
      </section>
    </div>
  )
}
