<template>
    <div>
      <h1>Register</h1>
      <form @submit.prevent="handleRegister">
        <div>
          <label>Username:</label>
          <input v-model="user.username" type="text" required>
        </div>
        <div>
          <label>Password:</label>
          <input v-model="user.password" type="password" required>
        </div>
        <div>
          <label>Full Name:</label>
          <input v-model="user.name" type="text" required>
        </div>
        <div>
          <label>Email:</label>
          <input v-model="user.email" type="email" required>
        </div>
        <button type="submit">Register</button>
      </form>
      <p>Already have an account? <router-link to="/login">Login here</router-link></p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Register',
    data() {
      return {
        user: {
          username: '',
          password: '',
          name: '',
          email: ''
        }
      }
    },
    methods: {
      async handleRegister() {
        try {
          // Call your API register endpoint
          const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.user)
          })
          
          if (response.ok) {
            this.$router.push('/login')
          } else {
            console.error('Registration failed')
          }
        } catch (error) {
          console.error('Error:', error)
        }
      }
    }
  }
  </script>