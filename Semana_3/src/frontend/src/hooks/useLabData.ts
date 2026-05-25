import { useEffect, useState } from 'react'
import type { LabState, Locale, Mode } from '../types/lab'

export interface UseLabDataResult {
  data: LabState | null
  isLoading: boolean
  statusMessage: string
}

export function useLabData(mode: Mode, locale: Locale): UseLabDataResult {
  const [data, setData] = useState<LabState | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [statusMessage, setStatusMessage] = useState('Cargando laboratorio...')

  useEffect(() => {
    const controller = new AbortController()

    async function loadLabState() {
      setIsLoading(true)
      setStatusMessage('Consultando backend del laboratorio...')

      try {
        // El frontend consume una sola ruta de agregacion para mantener
        // la UI desacoplada de los detalles internos del backend.
        const response = await fetch(`/api/lab?mode=${mode}&locale=${locale}`, {
          signal: controller.signal,
        })

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`)
        }

        const payload = (await response.json()) as LabState
        setData(payload)
        setStatusMessage(
          payload.cache.hit
            ? 'Cache activa. La ruta rapida esta disponible.'
            : 'Sin cache. El laboratorio esta midiendo la ruta lenta.',
        )
      } catch (error) {
        if (!controller.signal.aborted) {
          setStatusMessage(`No se pudo consultar el laboratorio: ${String(error)}`)
        }
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false)
        }
      }
    }

    void loadLabState()

    return () => controller.abort()
  }, [mode, locale])

  return { data, isLoading, statusMessage }
}
