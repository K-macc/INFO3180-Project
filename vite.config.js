import { fileURLToPath, URL } from 'url'
import path from 'path'

import { defineConfig } from 'vite'

import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/

export default defineConfig({
  plugins: [vue(),{
    name: 'inject-main-js',
    transformIndexHtml(html) {
      return html.replace(/<\/body>/,
          `<script type="module" src="../main.js"></script></body>`)
    }
  }
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    }
  },
  server: {
    proxy: {
    '^/api*': {
    target: 'http://localhost:8080/'
    }
    }
    },
  build: {
    outDir: 'static',
    emptyOutDir: true,
  },
})
