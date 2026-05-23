import { useState } from 'react'
import './App.css'
import { ControlsSection } from './components/ControlsSection'
import { AccessibilitySection } from './components/AccessibilitySection'
import { FooterSection } from './components/FooterSection'
import { HeroSection } from './components/HeroSection'
import { PerformanceSection } from './components/PerformanceSection'
import { SeoSection } from './components/SeoSection'
import { useLabData } from './hooks/useLabData'
import type { Locale, Mode } from './types/lab'

function App() {
  const [mode, setMode] = useState<Mode>('cached')
  const [locale, setLocale] = useState<Locale>('es')

  // App funciona como capa de orquestacion visual:
  // estado de filtros + secciones reutilizables.
  const { data, isLoading, statusMessage } = useLabData(mode, locale)

  return (
    <main className="app-shell">
      <a className="skip-link" href="#lab-main">
        Saltar al contenido principal
      </a>

      <nav className="site-nav" aria-label="Navegacion principal">
        <a href="#controls-title">Controles</a>
        <a href="#lab-main">Laboratorio</a>
        <a href="#seo-title">SEO</a>
      </nav>

      <HeroSection mode={mode} locale={locale} statusMessage={statusMessage} />

      <ControlsSection
        mode={mode}
        locale={locale}
        onModeChange={setMode}
        onLocaleChange={setLocale}
      />

      <section id="lab-main" className="grid-layout">
        <PerformanceSection data={data} isLoading={isLoading} />
        <AccessibilitySection data={data} />
        <SeoSection data={data} />
      </section>

      <FooterSection />
    </main>
  )
}

export default App
