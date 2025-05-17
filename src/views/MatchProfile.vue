<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const matches = ref([]);
const profileID = authStore.profile_id;
const success_message = ref('');
const error_message = ref('');

function flashMessage(prompt) {
  setTimeout(() => {
    if (Array.isArray(prompt)) {
      prompt.value = [];
    } else {
      prompt.value = '';
    }
  }, 2000);
}

function trackProfileView(profileID) {
  authStore.setProfileId(profileID);
}

function matchProfile() {
  fetch(`/api/profiles/matches/${profileID}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authStore.token}`
    }
  })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        error_message.value = data.error;
        flashMessage(error_message);
      } else {
        matches.value = data.matches;
        success_message.value = data.message;
        flashMessage(success_message);
      }
    })
    .catch(error => {
      console.error('Error matching profile:', error);
    });
}

onMounted(() => {
  matchProfile();
})
</script>

<template>
  <div class="container">
    <transition name="fade">
      <div v-if="error_message" class="error-message">
        {{ error_message }}
      </div>
    </transition>

    <transition name="fade">
      <div v-if="success_message" class="success-message">
        {{ success_message }}
      </div>
    </transition>

    <h1>Match Report</h1>

    <h5 v-if="matches.value">Matches found to your profile:</h5>
    <h5 v-else="!matches.value">No matches found.</h5>

    <div class="match-results" v-for="match in matches" :key="match.id">
      <h3>{{ match.sex }}</h3>
      <p>{{ match.description }}</p>
      <router-link class="btn btn-primary" :to="`/profiles/${match.id}`" @click="trackProfileView(match.id)">View
        more details</router-link>
    </div>
  </div>
</template>

<style scoped>
/* General Page Styling */
.container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 20px;
  background-color: #F7E1E9; /* Lavender Blush */
  min-height: 100vh;
}

/* Headings */
h1 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #69003D; /* Tyrian Purple */
}

h5 {
  font-size: 1.2rem;
  color: #8A0047; /* Murrey */
  margin-bottom: 20px;
}

/* Match Results Styling */
.match-results {
  background-color: white;
  margin-bottom: 20px;
  padding: 1.5rem;
  border-radius: 16px;
  border: 1px solid #AD2874; /* Fandango border */
  box-shadow: 0px 2px 8px rgba(105, 0, 61, 0.1); /* Tyrian Purple */
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.match-results:hover {
  transform: scale(1.02);
  box-shadow: 0px 4px 12px rgba(0, 200, 255, 0.3); /* Vivid Sky Blue */
}

/* Match Headings */
.match-results h3 {
  margin-top: 0;
  color: #00C8FF; /* Vivid Sky Blue */
}

.match-results p {
  color: #333333; /* Jet */
  margin-bottom: 1rem;
}

/* View More Button */
.match-results .btn {
  background-color: #6DDBFC; /* Sky Blue */
  color: #333333; /* Jet */
  border: none;
  padding: 0.5rem 1rem;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.match-results .btn:hover {
  background-color: #00C8FF; /* Vivid Sky Blue */
}

/* Flash Messages */
.success-message {
  color: #155724;
  background-color: #d4edda;
  padding: 10px;
  border-radius: 8px;
  width: 250px;
  top: 100px;
  right: 45px;
  text-align: center;
  position: fixed;
  box-shadow: 0 2px 8px rgba(0, 128, 0, 0.2);
}

.error-message {
  color: #721c24;
  background-color: #f8d7da;
  padding: 10px;
  border-radius: 8px;
  top: 100px;
  right: 45px;
  position: fixed;
  text-align: center;
  width: 250px;
  box-shadow: 0 2px 8px rgba(255, 0, 0, 0.2);
}

/* Fade Animation */
.fade-leave-active {
  transition: opacity 1s ease-in-out;
}

.fade-leave-to {
  opacity: 0;
}
</style>
