import type { LabState } from '../types/lab'

interface SeoSectionProps {
  data: LabState | null
}

export function SeoSection({ data }: SeoSectionProps) {
  return (
    <article className="card">
      <div className="section-header">
        <div>
          <p className="eyebrow">SEO</p>
          <h2 id="seo-title">Metadatos, canonical y datos estructurados</h2>
        </div>
      </div>

      <dl className="meta-list">
        <div>
          <dt>Title</dt>
          <dd>{data?.seo.title}</dd>
        </div>
        <div>
          <dt>Description</dt>
          <dd>{data?.seo.description}</dd>
        </div>
        <div>
          <dt>Canonical</dt>
          <dd>{data?.seo.canonical}</dd>
        </div>
        <div>
          <dt>Robots</dt>
          <dd>{data?.seo.robots}</dd>
        </div>
      </dl>

      <div className="keyword-row" aria-label="Palabras clave SEO">
        {data?.seo.keywords?.map((keyword) => (
          <span key={keyword} className="pill subtle-pill">
            {keyword}
          </span>
        ))}
      </div>

      <div className="code-box">
        <h3>JSON-LD</h3>
        <pre>{JSON.stringify(data?.seo.jsonLd, null, 2)}</pre>
      </div>
    </article>
  )
}
