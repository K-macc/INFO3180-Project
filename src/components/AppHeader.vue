<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
      <div class="container-fluid">
        <img src="../../public/jam_date_logo.png" alt="Logo" class="logo" :style="{ width: '50px', height: '50px' }" />
        <RouterLink class="navbar-brand" to="/">Jam Date</RouterLink>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <RouterLink class="nav-link" :class="{ active: $route.path === '/' }" to="/" v-if="!isAuthenticated">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :class="{ active: $route.path === '/register' }" to="/register" v-if="!isAuthenticated">Register</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :class="{ active: $route.path === '/login' }" to="/login" v-if="!isAuthenticated">Login</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/users" class="nav-link" :class="{ active: $route.path === '/users' }" v-if="isAuthenticated">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :class="{ active: $route.path === `/users/${authStore.user_id}` }" :to="`/users/${authStore.user_id}`" v-if="isAuthenticated">My Profile</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :class="{ active: $route.path === '/profiles/new' }" to="/profiles/new" v-if="isAuthenticated">Add New Profile</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :class="{ active: $route.path === '/reports' }" to="/reports" v-if="isAuthenticated">View Reports</RouterLink>
            </li>
          </ul>

          <ul class="navbar-nav mb-2 mb-lg-0">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/logout" v-if="isAuthenticated">
                Logout
              </RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { useAuthStore, isAuthenticated } from "@/stores/auth";

const authStore = useAuthStore();
</script>

<style scoped>
nav {
  background-color: #b10ca3;
  
}

.navbar-brand {
  font-weight: bold;
}

.nav-link {
  color: #fff !important;
  font-weight: bold;
}

.nav-link:hover {
  color: #065f7c !important;
}

.nav-link.active {
  color: #00BFFF !important;
}

body {
  padding-top: 70px;
}
</style>
