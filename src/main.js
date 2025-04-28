import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from '@/router'
import axios from 'axios'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faHeart as fasHeart } from '@fortawesome/free-solid-svg-icons'
import { faHeart as farHeart } from '@fortawesome/free-regular-svg-icons'

library.add(fasHeart, farHeart)

// Set base URL for API requests
axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL

// Interceptor for adding JWT to requests
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('jwt')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  console.log('Outgoing Request:', config.method.toUpperCase(), config.url);
  console.log('Request Headers:', config.headers);
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

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)

// Initialize Pinia for state management
const pinia = createPinia()
app.use(pinia)

// Use Vue Router
app.use(router)


// Add axios to global properties for access in components
app.config.globalProperties.$axios = axios

// Mount the app
app.mount('#app')

