import { isoAHoraLima, limaAIso } from '../src/lib/fechas'

describe('limaAIso', () => {
  it('agrega segundos y el desfase de Lima', () => {
    expect(limaAIso('2026-10-05T08:00')).toBe('2026-10-05T08:00:00-05:00')
  })
  it('conserva los segundos si ya vienen', () => {
    expect(limaAIso('2026-10-05T08:00:30')).toBe('2026-10-05T08:00:30-05:00')
  })
  it('devuelve undefined si está vacío', () => {
    expect(limaAIso('')).toBeUndefined()
  })
})

describe('isoAHoraLima', () => {
  it('convierte UTC a hora de Lima (UTC-5)', () => {
    expect(isoAHoraLima('2026-10-05T13:00:00Z')).toContain('08:00')
  })
  it('devuelve el texto original si no es una fecha', () => {
    expect(isoAHoraLima('no-fecha')).toBe('no-fecha')
  })
})
