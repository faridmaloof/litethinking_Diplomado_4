import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), 'VITE_')
  const apiOrigin = env.VITE_API_ORIGIN ?? 'http://localhost:8000'
  const appOrigin = env.VITE_APP_ORIGIN ?? 'http://localhost:4173'

  return {
    plugins: [
      react(),
      {
        name: 'replace-app-origin',
        transformIndexHtml(html) {
          return html.replaceAll('__APP_ORIGIN__', appOrigin)
        },
      },
    ],
    server: {
      host: '0.0.0.0',
      port: 4173,
      proxy: {
        '/api': {
          target: apiOrigin,
          changeOrigin: true,
        },
      },
    },
  }
})
