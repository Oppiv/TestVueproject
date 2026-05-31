import { fileURLToPath, URL } from 'node:url'
import vuetify from "vite-plugin-vuetify"

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    vuetify({ autoImport: true }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    port: 3000, // порт фронтенда (можно изменить)
    proxy: {
      '/labubu': {
        target: 'http://localhost:8000', // бэкенд на порту 8000
        changeOrigin: true,
        rewrite: (path) => path, // оставляет путь без изменений  
      },
    },
  },
})