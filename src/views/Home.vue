<template>
    <div>
      <h1>Welcome to Jam-Date</h1>
      <nav>
        <router-link to="/login">Login</router-link> |
        <router-link to="/register">Register</router-link>
      </nav>
      <!-- Will display latest profiles later -->
    </div>
  </template>
  
  <script>
  export default {
    name: 'Home'
  }
  </script>