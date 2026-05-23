import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiOrigin = env.VITE_API_ORIGIN ?? 'http://localhost:8000'

  return {
    plugins: [react()],
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
