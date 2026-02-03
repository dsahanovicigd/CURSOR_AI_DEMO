import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // Ensure environment variables are available in the app
  envPrefix: 'VITE_',
  // Server configuration for development
  server: {
    port: 5173,
    host: true,
  },
  // Preview configuration (for production preview)
  preview: {
    port: 4173,
    host: true,
  },
})
