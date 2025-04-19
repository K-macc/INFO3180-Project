<template>
    <div>
      <h1>Login</h1>
      <form @submit.prevent="handleLogin">
        <div>
          <label>Username:</label>
          <input v-model="credentials.username" type="text" required>
        </div>
        <div>
          <label>Password:</label>
          <input v-model="credentials.password" type="password" required>
        </div>
        <button type="submit">Login</button>
      </form>
      <p>Don't have an account? <router-link to="/register">Register here</router-link></p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Login',
    data() {
      return {
        credentials: {
          username: '',
          password: ''
        }
      }
    },
    methods: {
      async handleLogin() {
        try {
          const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.credentials)
          })
          
          if (response.ok) {
            const data = await response.json()
            // Store the token 
            localStorage.setItem('jwt', data.token)
            this.$router.push('/')
          } else {
            console.error('Login failed')
          }
        } catch (error) {
          console.error('Error:', error)
        }
      }
    }
  }
  </script>