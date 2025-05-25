<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <img src="../../public/jam_date_logo.png" alt="Logo" class="logo" :style="{ width: '50px' , height: '50px' }" />
        <RouterLink class="navbar-brand" to="/">Jam Date</RouterLink>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/">Home</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/register">Register</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" :to="`/users/${authStore.user_id}`" v-if="isAuthenticated">My Profile
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/profiles/new" v-if="isAuthenticated">Add New Profile</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/logout" v-if="isAuthenticated">Logout</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/users" v-if="isAuthenticated">View Users</RouterLink>
              <RouterLink to="/users" class="nav-link active" v-if="isAuthenticated">Home</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/profiles/check" v-if="isAuthenticated">Check Profiles</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" :to="`/profiles/update/${authStore.user_id}`" v-if="isAuthenticated">Update
                Profile</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" :to="`/profiles/${authStore.user_id}`" v-if="isAuthenticated">Profile Details
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/profiles/match" v-if="isAuthenticated">Match Profile</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/reports" v-if="isAuthenticated">View Reports</RouterLink>
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
body {
  padding-top: 70px;
}
</style>
