import type { ReactNode } from 'react'
import type { Pedido } from '../api/pedidos'
import { isoAHoraLima } from '../lib/fechas'
import { ETIQUETA_ESTADO, ETIQUETA_PRIORIDAD, formatoNumero } from '../lib/estados'

function Dato({ etiqueta, children }: { etiqueta: string; children: ReactNode }) {
  return (
    <div className="dato">
      <dt>{etiqueta}</dt>
      <dd>{children}</dd>
    </div>
  )
}

export default function PedidoDetalle({ pedido: p }: { pedido: Pedido }) {
  return (
    <div className="drawer__cuerpo">
      <div className="detalle-cabecera">
        <span className={`insignia insignia--${p.estado.toLowerCase()}`}>{ETIQUETA_ESTADO[p.estado]}</span>
        <span className={`prioridad prioridad--${p.prioridad}`}>Prioridad {ETIQUETA_PRIORIDAD[p.prioridad]}</span>
      </div>

      <h3 className="detalle-titulo">Destino</h3>
      <dl className="datos">
        <Dato etiqueta="Dirección">{p.direccion}</Dato>
        <Dato etiqueta="Distrito">{p.distrito}</Dato>
        <Dato etiqueta="Coordenadas">
          {p.latitud}, {p.longitud}
        </Dato>
        <Dato etiqueta="Destinatario">{p.destinatarioAlias ?? '—'}</Dato>
      </dl>

      <h3 className="detalle-titulo">Carga y servicio</h3>
      <dl className="datos">
        <Dato etiqueta="Peso">{formatoNumero(p.demandaKg)} kg</Dato>
        <Dato etiqueta="Volumen">{formatoNumero(p.demandaM3)} m³</Dato>
        <Dato etiqueta="Tiempo de servicio">{p.tiempoServicioMin} min</Dato>
      </dl>

      <h3 className="detalle-titulo">Ventana horaria (hora de Lima)</h3>
      <dl className="datos">
        <Dato etiqueta="Inicio">{isoAHoraLima(p.ventanaInicio)}</Dato>
        <Dato etiqueta="Fin">{isoAHoraLima(p.ventanaFin)}</Dato>
      </dl>

      <h3 className="detalle-titulo">Registro</h3>
      <dl className="datos">
        <Dato etiqueta="Observación">{p.observacionOperativa ?? '—'}</Dato>
        <Dato etiqueta="Creado">{isoAHoraLima(p.creadoEn)}</Dato>
        <Dato etiqueta="Identificador">
          <code>{p.id}</code>
        </Dato>
      </dl>
    </div>
  )
}
