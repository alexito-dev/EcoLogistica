import { fireEvent, render, screen, within } from '@testing-library/react'
import Drawer from '../src/components/Drawer'

const cuerpo = <>
  <label>Referencia<input data-foco-inicial defaultValue="PED-123" /></label>
  <button type="button">Guardar</button>
</>

describe('Drawer: gestión del foco, teclado y cierre accesible', () => {
  it('no inserta un diálogo mientras permanece cerrado', () => {
    const cerrar = vi.fn()
    render(<Drawer abierto={false} titulo="Ejemplo" onCerrar={cerrar}>{cuerpo}</Drawer>)
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    expect(document.body).not.toHaveClass('sin-scroll')
  })

  it('enfoca el primer campo, impide scroll y devuelve el foco al cerrar', () => {
    const previo = document.createElement('button')
    previo.textContent = 'Abrir'
    document.body.appendChild(previo)
    previo.focus()
    const { rerender, unmount } = render(
      <Drawer abierto titulo="Registrar" descripcion="Complete los datos" onCerrar={vi.fn()}>{cuerpo}</Drawer>,
    )
    const panel = screen.getByRole('dialog', { name: 'Registrar' })
    expect(panel).toHaveAttribute('aria-describedby')
    expect(within(panel).getByLabelText('Referencia')).toHaveFocus()
    expect(document.body).toHaveClass('sin-scroll')
    rerender(<Drawer abierto={false} titulo="Registrar" onCerrar={vi.fn()}>{cuerpo}</Drawer>)
    expect(document.body).not.toHaveClass('sin-scroll')
    expect(previo).toHaveFocus()
    unmount()
    previo.remove()
  })

  it('atrapa Tab y Shift+Tab entre los controles del diálogo', () => {
    render(<Drawer abierto titulo="Opciones" onCerrar={vi.fn()}>{cuerpo}</Drawer>)
    const primero = screen.getByRole('button', { name: 'Cerrar panel' })
    const ultimo = screen.getByRole('button', { name: 'Guardar' })
    primero.focus()
    fireEvent.keyDown(document, { key: 'Tab', shiftKey: true })
    expect(ultimo).toHaveFocus()
    fireEvent.keyDown(document, { key: 'Tab' })
    expect(primero).toHaveFocus()
  })

  it('acepta tecla Escape y el click en el fondo para cerrar', () => {
    const cerrar = vi.fn()
    const { container } = render(<Drawer abierto titulo="Detalles" onCerrar={cerrar}>{cuerpo}</Drawer>)
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(cerrar).toHaveBeenCalledTimes(1)
    fireEvent.click(container.querySelector('.drawer__fondo')!)
    expect(cerrar).toHaveBeenCalledTimes(2)
    fireEvent.click(screen.getByRole('button', { name: 'Cerrar panel' }))
    expect(cerrar).toHaveBeenCalledTimes(3)
  })

  it('usa el callback más reciente cuando el panel sigue abierto', () => {
    const anterior = vi.fn()
    const actual = vi.fn()
    const { rerender } = render(<Drawer abierto titulo="Editar" onCerrar={anterior}>{cuerpo}</Drawer>)
    rerender(<Drawer abierto titulo="Editar" onCerrar={actual}>{cuerpo}</Drawer>)
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(anterior).not.toHaveBeenCalled()
    expect(actual).toHaveBeenCalledOnce()
  })

  it('muestra un título accesible sin exigir descripción opcional', () => {
    render(<Drawer abierto titulo="Confirmación" onCerrar={vi.fn()}><p>Solo lectura</p></Drawer>)
    const dialogo = screen.getByRole('dialog', { name: 'Confirmación' })
    expect(dialogo).toHaveAttribute('aria-modal', 'true')
    expect(dialogo).not.toHaveAttribute('aria-describedby')
    expect(screen.getByText('Solo lectura')).toBeInTheDocument()
  })
})
