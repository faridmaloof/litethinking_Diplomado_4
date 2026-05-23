import { Bar } from './Bar'
import { formatNumber } from '../utils/format'
import type { LabState } from '../types/lab'

interface PerformanceSectionProps {
  data: LabState | null
  isLoading: boolean
}

export function PerformanceSection({ data, isLoading }: PerformanceSectionProps) {
  return (
    <article className="card spotlight">
      <div className="section-header">
        <div>
          <p className="eyebrow">Performance</p>
          <h2>{data?.content.headline ?? 'Cargando...'}</h2>
        </div>
        {isLoading ? <span className="pill muted">Actualizando</span> : <span className="pill">Listo</span>}
      </div>

      <p className="supporting-text">{data?.content.subheadline ?? 'Esperando respuesta del backend...'}</p>
      <p className="supporting-text subtle">{data?.content.intro}</p>

      <div className="metrics-grid">
        <div className="metric-card">
          <span>TTFB</span>
          <strong>{formatNumber(data?.performance.ttfbMs ?? 0)} ms</strong>
          <Bar value={data?.performance.ttfbMs ?? 0} max={1000} />
        </div>
        <div className="metric-card">
          <span>p95</span>
          <strong>{formatNumber(data?.performance.p95Ms ?? 0)} ms</strong>
          <Bar value={data?.performance.p95Ms ?? 0} max={1200} />
        </div>
        <div className="metric-card">
          <span>Throughput</span>
          <strong>{formatNumber(data?.performance.throughputRps ?? 0)} req/s</strong>
          <Bar value={data?.performance.throughputRps ?? 0} max={300} />
        </div>
      </div>

      <div className="detail-strip">
        <div>
          <span className="panel-label">Cache</span>
          <strong>{data?.cache.hit ? 'Hit' : 'Miss'}</strong>
        </div>
        <div>
          <span className="panel-label">Delay servidor</span>
          <strong>{formatNumber(data?.performance.serverDelayMs ?? 0)} ms</strong>
        </div>
        <div>
          <span className="panel-label">Fecha</span>
          <strong>{data?.generatedAt ?? '-'}</strong>
        </div>
      </div>

      <p className="note">{data?.performance.note}</p>
    </article>
  )
}
