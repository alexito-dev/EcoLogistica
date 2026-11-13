import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ImportarPedidos from '../src/components/ImportarPedidos'
import * as api from '../src/api/pedidos'

afterEach(() => vi.restoreAllMocks())

const archivo = (texto: string) => new File([texto], 'pedidos.csv', { type: 'text/csv' })

describe('ImportarPedidos (ECO-18)', () => {
  it('importa el archivo elegido y avisa la cantidad', async () => {
    const importar = vi.spyOn(api, 'importarPedidos').mockResolvedValue({ importados: 2, codigos: ['A', 'B'] })
    const alImportar = vi.fn()
    const user = userEvent.setup()
    render(<ImportarPedidos onImportado={alImportar} onCancelar={() => {}} />)
    expect(screen.getByRole('button', { name: /Importar pedidos/ })).toBeDisabled()
    await user.upload(screen.getByLabelText('Archivo CSV de pedidos'), archivo('direccion,distrito\nA,B\n'))
    expect(await screen.findByText(/Archivo elegido: pedidos.csv/)).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: /Importar pedidos/ }))
    await waitFor(() => expect(alImportar).toHaveBeenCalledWith(2))
    expect(importar).toHaveBeenCalledWith('direccion,distrito\nA,B\n')
  })

  it('muestra cada fila con error y no cierra', async () => {
    vi.spyOn(api, 'importarPedidos').mockRejectedValue(
      new api.ApiError(422, 'No se cumple una regla de negocio', { 'fila 3 · latitud': 'Fuera del ámbito geográfico configurado' }),
    )
    const alImportar = vi.fn()
    const user = userEvent.setup()
    render(<ImportarPedidos onImportado={alImportar} onCancelar={() => {}} />)
    await user.upload(screen.getByLabelText('Archivo CSV de pedidos'), archivo('x'))
    await user.click(screen.getByRole('button', { name: /Importar pedidos/ }))
    const alerta = await screen.findByRole('alert')
    expect(alerta).toHaveTextContent('fila 3 · latitud: Fuera del ámbito geográfico configurado')
    expect(alImportar).not.toHaveBeenCalled()
  })

  it('descarga la plantilla y permite cancelar', async () => {
    vi.spyOn(api, 'obtenerPlantilla').mockResolvedValue('codigo,direccion\n')
    URL.createObjectURL = vi.fn(() => 'blob:x')
    URL.revokeObjectURL = vi.fn()
    vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
    const cancelar = vi.fn()
    const user = userEvent.setup()
    render(<ImportarPedidos onImportado={() => {}} onCancelar={cancelar} />)
    await user.click(screen.getByRole('button', { name: /Descargar plantilla CSV/ }))
    await waitFor(() => expect(api.obtenerPlantilla).toHaveBeenCalled())
    await user.click(screen.getByRole('button', { name: 'Cancelar' }))
    expect(cancelar).toHaveBeenCalled()
  })
})
