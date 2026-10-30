import { afterEach, describe, expect, it, vi } from 'vitest'
import { solicitar, ApiError, alHaberActividad, alVencerSesion } from '../src/api/http'
import { iniciarSesion, verificarCodigo, obtenerSesion, cerrarSesion } from '../src/api/auth'
import { crearVehiculo, actualizarVehiculo, guardarDisponibilidad, listarVehiculos } from '../src/api/flota'
import { obtenerRutasGuardadas, obtenerVistaPrevia, guardarRutas } from '../src/api/rutas'
import { obtenerIndicadores } from '../src/api/indicadores'

function respuesta(status: number, body: unknown = {}) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: vi.fn().mockResolvedValue(body),
  }
}
function mockRespuesta(status: number, body: unknown = {}) {
  const fetch = vi.fn().mockResolvedValue(respuesta(status, body))
  vi.stubGlobal('fetch', fetch)
  return fetch
}
afterEach(() => vi.unstubAllGlobals())

describe('Contrato del cliente HTTP compartido', () => {
  it('incorpora credenciales y conserva cabeceras y método personalizado', async () => {
    const fetch = mockRespuesta(200, { confirmado: true })
    expect(await solicitar('/verificar', {
      method: 'PUT', headers: { 'X-Test': 'valor' }, body: JSON.stringify({ ok: 1 }),
    })).toEqual({ confirmado: true })
    expect(fetch).toHaveBeenCalledWith(
      expect.stringMatching(/\/verificar$/),
      expect.objectContaining({
        credentials: 'include', method: 'PUT',
        headers: expect.objectContaining({ 'Content-Type': 'application/json', 'X-Test': 'valor' }),
      }),
    )
  })

  it('notifica actividad tras obtener respuesta 2xx o 204 y cancela la suscripción', async () => {
    const actividad = vi.fn()
    const desuscribir = alHaberActividad(actividad)
    mockRespuesta(200, { ok: true })
    await solicitar('/actividad')
    mockRespuesta(204)
    await solicitar('/logout', { method: 'POST' })
    expect(actividad).toHaveBeenCalledTimes(2)
    desuscribir()
    await solicitar('/logout')
    expect(actividad).toHaveBeenCalledTimes(2)
  })

  it('notifica una sola vez la sesión vencida en 401 y permite desuscribir', async () => {
    const vencida = vi.fn()
    const quitar = alVencerSesion(vencida)
    mockRespuesta(401, { message: 'Sesión vencida' })
    await expect(solicitar('/restringido')).rejects.toMatchObject({ status: 401, message: 'Sesión vencida' })
    expect(vencida).toHaveBeenCalledTimes(1)
    await expect(solicitar('/auth/login', undefined, { avisarSesionVencida: false })).rejects.toMatchObject({ status: 401 })
    expect(vencida).toHaveBeenCalledTimes(1)
    quitar()
    await expect(solicitar('/restringido')).rejects.toThrow(ApiError)
    expect(vencida).toHaveBeenCalledTimes(1)
  })

  it('representa errores sin JSON con un mensaje estable y detalle vacío', async () => {
    const fetch = vi.fn().mockResolvedValue({
      ok: false, status: 502, json: vi.fn().mockRejectedValue(new SyntaxError('HTML')),
    })
    vi.stubGlobal('fetch', fetch)
    await expect(solicitar('/fallo')).rejects.toMatchObject({
      status: 502, message: 'Ocurrió un error inesperado. Intente nuevamente.', errors: {},
    })
  })

  it('convierte errores de conexión de fetch a un ApiError con estado cero', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('NetworkError')))
    await expect(solicitar('/sin-red')).rejects.toMatchObject({
      status: 0, message: expect.stringMatching(/No se pudo conectar/),
    })
  })
})

describe('Contratos API de autenticación', () => {
  it('el inicio de sesión envía contraseña y nunca avisa sesión caducada al recibir 401', async () => {
    const vencida = vi.fn()
    const quitar = alVencerSesion(vencida)
    const fetch = mockRespuesta(401, { message: 'Correo o contraseña incorrectos' })
    await expect(iniciarSesion('p@e.test', 'clave')).rejects.toMatchObject({ status: 401 })
    expect(fetch.mock.calls[0][1].method).toBe('POST')
    expect(JSON.parse(fetch.mock.calls[0][1].body)).toEqual({ correo: 'p@e.test', clave: 'clave' })
    expect(vencida).not.toHaveBeenCalled()
    quitar()
  })
  it('verifica el código MFA y recibe el perfil del usuario', async () => {
    const u = { nombre: 'Ejemplo', correo: 'p@e.test', rol: 'PLANIFICADOR' }
    const fetch = mockRespuesta(200, u)
    expect(await verificarCodigo('123456')).toEqual(u)
    expect(JSON.parse(fetch.mock.calls[0][1].body)).toEqual({ codigo: '123456' })
    expect(fetch.mock.calls[0][0]).toMatch(/\/auth\/mfa$/)
  })
  it('devuelve null solo si la consulta de sesión responde 401', async () => {
    mockRespuesta(401)
    await expect(obtenerSesion()).resolves.toBeNull()
    mockRespuesta(503, { message: 'Error temporal' })
    await expect(obtenerSesion()).rejects.toMatchObject({ status: 503 })
    const usuario = { nombre: 'A', correo: 'a@e.test', rol: 'ADMIN' }
    mockRespuesta(200, usuario)
    await expect(obtenerSesion()).resolves.toEqual(usuario)
  })
  it('cierra sesión mediante POST y acepta 204 sin interpretar un JSON', async () => {
    const fetch = mockRespuesta(204)
    await expect(cerrarSesion()).resolves.toBeUndefined()
    expect(fetch.mock.calls[0][0]).toMatch(/\/auth\/logout$/)
    expect(fetch.mock.calls[0][1].method).toBe('POST')
  })
})

describe('Rutas y disponibilidad en los clientes REST', () => {
  it('codifica fechas y obtiene disponibilidad de vehículos', async () => {
    const fetch = mockRespuesta(200, { items: [] })
    await listarVehiculos('2026-11-01 & otra')
    expect(fetch.mock.calls[0][0]).toContain('fecha=2026-11-01%20%26%20otra')
  })
  it('crea y edita vehículos sin perder el cuerpo JSON', async () => {
    const fetch = mockRespuesta(201, { id: 'v-1' })
    const datos = { placa: 'W3A-123', tipo: 'Furgón', capacidadKg: 350, capacidadM3: 4,
      combustible: 'DIESEL' as const, consumoBasePor100km: 10,
      factorEmisionKgco2eUnidad: null, anio: null, estado: 'DISPONIBLE' as const }
    await crearVehiculo(datos)
    await actualizarVehiculo('v-1', datos)
    expect(fetch.mock.calls.map((c) => c[1].method)).toEqual(['POST', 'PUT'])
    expect(fetch.mock.calls[1][0]).toMatch(/\/vehiculos\/v-1$/)
    expect(JSON.parse(fetch.mock.calls[1][1].body)).toEqual(datos)
  })
  it('guarda turnos mediante PUT y transmite la restricción', async () => {
    const fetch = mockRespuesta(200, { id: 'v-1' })
    const turno = { fecha: '2026-10-30', turnoInicio: '08:00', turnoFin: '16:00',
      disponible: false, restriccionCirculacion: 'Mantenimiento' }
    await guardarDisponibilidad('v-1', turno)
    expect(fetch.mock.calls[0][0]).toMatch(/\/vehiculos\/v-1\/disponibilidad$/)
    expect(fetch.mock.calls[0][1].method).toBe('PUT')
    expect(JSON.parse(fetch.mock.calls[0][1].body)).toEqual(turno)
  })
  it('consulta y guarda rutas usando fecha codificada', async () => {
    const fetch = mockRespuesta(200, { rutas: [] })
    await obtenerVistaPrevia('2026-10-30')
    await guardarRutas('2026-10-30')
    expect(fetch.mock.calls[0][0]).toContain('/rutas/vista-previa?fecha=2026-10-30')
    expect(fetch.mock.calls[1][0]).toContain('/rutas/guardar?fecha=2026-10-30')
    expect(fetch.mock.calls[1][1].method).toBe('POST')
  })
  it('interpreta 404 de rutas guardadas como ausencia, sin ocultar otros errores', async () => {
    mockRespuesta(404, { message: 'No encontrada' })
    await expect(obtenerRutasGuardadas('2026-10-30')).resolves.toBeNull()
    mockRespuesta(403, { message: 'Acceso denegado' })
    await expect(obtenerRutasGuardadas('2026-10-30')).rejects.toMatchObject({ status: 403 })
    mockRespuesta(200, { fecha: '2026-10-30', vista: { rutas: [] } })
    await expect(obtenerRutasGuardadas('2026-10-30')).resolves.toHaveProperty('fecha', '2026-10-30')
  })
  it('pide indicadores de una fecha y conserva el resultado esperado', async () => {
    const fetch = mockRespuesta(200, { fecha: '2026-10-30', dia: { pedidos: 0 } })
    expect(await obtenerIndicadores('2026-10-30')).toHaveProperty('dia.pedidos', 0)
    expect(fetch.mock.calls[0][0]).toMatch(/\/indicadores\?fecha=2026-10-30$/)
  })
})
