import type { HttpMethod } from './scenarios'

export interface ApiResponse {
  status: number
  body: unknown
  elapsedMs: number
}

const baseUrl = import.meta.env.VITE_API_BASE_URL ?? ''

export async function callApi(
  method: HttpMethod,
  path: string,
  body?: Record<string, unknown>,
): Promise<ApiResponse> {
  const controller = new AbortController()
  const timeoutId = window.setTimeout(() => controller.abort(), 20000)
  const startedAt = performance.now()

  try {
    const response = await fetch(`${baseUrl}${path}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: method === 'POST' ? JSON.stringify(body ?? {}) : undefined,
      signal: controller.signal,
    })

    const elapsedMs = Math.round(performance.now() - startedAt)
    const responseText = await response.text()
    let parsedBody: unknown = responseText

    if (responseText) {
      try {
        parsedBody = JSON.parse(responseText)
      } catch {
        parsedBody = responseText
      }
    }

    return {
      status: response.status,
      body: parsedBody,
      elapsedMs,
    }
  } finally {
    window.clearTimeout(timeoutId)
  }
}