<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <RouterLink class="navbar-brand" to="/">Jam Date</RouterLink>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item" v-if="!isAuthenticated">
              <RouterLink class="nav-link" to="/">Home</RouterLink>
            </li>

            <li class="nav-item" v-if="!isAuthenticated">
              <RouterLink class="nav-link" to="/register">Register</RouterLink>
            </li>

            <li class="nav-item" v-if="!isAuthenticated">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>

            <li class="nav-item" v-if="isAuthenticated">
              <RouterLink class="nav-link" :to="`/users/${authStore.user_id}`">My Profile</RouterLink>
            </li>

            <li class="nav-item" v-if="isAuthenticated">
              <RouterLink class="nav-link" to="/profiles/new">Add New Profile</RouterLink>
            </li>

            <li class="nav-item" v-if="isAuthenticated">
              <RouterLink class="nav-link" to="/logout">Logout</RouterLink>
            </li>

            <li class="nav-item" v-if="isAuthenticated">
              <RouterLink class="nav-link" to="/users">View Users</RouterLink>
            </li>

            <li class="nav-item" v-if="isAuthenticated">
              <RouterLink class="nav-link" to="/profiles/check">Check Profiles</RouterLink>
            </li>

            <li class="nav-item" v-if="isAuthenticated">
              <RouterLink class="nav-link" :to="`/profiles/update/${authStore.user_id}`">Update Profile</RouterLink>
            </li>

            <li class="nav-item" v-if="isAuthenticated">
              <RouterLink class="nav-link" :to="`/profiles/${authStore.user_id}`">Profile Details</RouterLink>
            </li>

            <li class="nav-item" v-if="isAuthenticated">
              <RouterLink class="nav-link" to="/profiles/match">Match Profile</RouterLink>
            </li>

            <li class="nav-item" v-if="isAuthenticated">
              <RouterLink class="nav-link" to="/reports">View Reports</RouterLink>
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
/* Optional spacing fix to prevent content from being hidden under fixed header */
body {
  padding-top: 70px;
}
</style>
