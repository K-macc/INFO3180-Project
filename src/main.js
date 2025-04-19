import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// Set base URL for API requests
axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

const app = createApp(App)

// Initialize Pinia for state management
const pinia = createPinia()
app.use(pinia)

// Use Vue Router
app.use(router)

// Global error handler
app.config.errorHandler = (err) => {
  console.error('Global Vue error:', err)
}

// Add axios to global properties for access in components
app.config.globalProperties.$axios = axios

// Mount the app
app.mount('#app')

// Interceptor for adding JWT to requests
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('jwt')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

// Interceptor for handling 401 responses
axios.interceptors.response.use(response => response, error => {
  if (error.response?.status === 401) {
    localStorage.removeItem('jwt')
    router.push('/login')
  }
  return Promise.reject(error)
})