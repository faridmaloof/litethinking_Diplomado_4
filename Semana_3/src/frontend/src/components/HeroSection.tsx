import type { Locale, Mode } from '../types/lab'

interface HeroSectionProps {
  mode: Mode
  locale: Locale
  statusMessage: string
}

export function HeroSection({ mode, locale, statusMessage }: HeroSectionProps) {
  return (
    <header className="hero">
      <div className="hero-copy">
        <p className="eyebrow">Semana 3 / Dia 3</p>
        <h1>PulseLab QA Studio</h1>
        <p className="hero-text">
          Laboratorio en React, Vite y FastAPI para probar rendimiento con cache y sin cache,
          accesibilidad real y SEO visible en el DOM.
        </p>
        <p className="status" aria-live="polite">
          {statusMessage}
        </p>
      </div>

      <div className="hero-panel" aria-label="Resumen del laboratorio">
        <div>
          <span className="panel-label">Modo actual</span>
          <strong>{mode === 'cached' ? 'Cache' : 'Sin cache'}</strong>
        </div>
        <div>
          <span className="panel-label">Idioma</span>
          <strong>{locale === 'es' ? 'Español' : 'Deutsch'}</strong>
        </div>
        <div>
          <span className="panel-label">Origen</span>
          <strong>Frontend + backend + qa</strong>
        </div>
      </div>
    </header>
  )
}
