export type Mode = 'cached' | 'nocache'
export type Locale = 'es' | 'de'

export interface LabState {
  mode: Mode
  locale: Locale
  generatedAt: string
  cache: {
    hit: boolean
    ttlSeconds: number
    ageSeconds: number
  }
  performance: {
    cacheHit: boolean
    serverDelayMs: number
    ttfbMs: number
    p95Ms: number
    throughputRps: number
    note: string
  }
  accessibility: {
    landmarks: string[]
    signals: string[]
    testing: string[]
  }
  seo: {
    title: string
    description: string
    canonical: string
    robots: string
    keywords: string[]
    jsonLd: Record<string, unknown>
  }
  content: {
    headline: string
    subheadline: string
    intro: string
    localeLabel: string
    cacheModeLabel: string
  }
}
