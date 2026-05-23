import { locales } from '../constants/locales'
import type { Locale, Mode } from '../types/lab'

interface ControlsSectionProps {
  mode: Mode
  locale: Locale
  onModeChange: (mode: Mode) => void
  onLocaleChange: (locale: Locale) => void
}

export function ControlsSection({ mode, locale, onModeChange, onLocaleChange }: ControlsSectionProps) {
  return (
    <section className="controls card" aria-labelledby="controls-title">
      <div className="section-header">
        <div>
          <p className="eyebrow">Controles</p>
          <h2 id="controls-title">Cambiar el comportamiento del taller</h2>
        </div>
      </div>

      <div className="toggle-row" role="tablist" aria-label="Modo de rendimiento">
        <button
          type="button"
          className={mode === 'cached' ? 'toggle active' : 'toggle'}
          onClick={() => onModeChange('cached')}
          aria-pressed={mode === 'cached'}
        >
          Modo cache
        </button>
        <button
          type="button"
          className={mode === 'nocache' ? 'toggle active' : 'toggle'}
          onClick={() => onModeChange('nocache')}
          aria-pressed={mode === 'nocache'}
        >
          Modo sin cache
        </button>
      </div>

      <div className="locale-row" aria-label="Selector de localizacion">
        {locales.map((item) => (
          <button
            key={item.code}
            type="button"
            className={locale === item.code ? 'locale-chip active' : 'locale-chip'}
            onClick={() => onLocaleChange(item.code)}
            aria-pressed={locale === item.code}
          >
            {item.label}
          </button>
        ))}
      </div>
    </section>
  )
}
