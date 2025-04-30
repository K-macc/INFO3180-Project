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
    <div>
        <transition name="fade">
            <div v-if="success_message || error_message" :class="success_message ? 'success-message' : 'error-message'">
                {{ success_message || error_message }}
            </div>
        </transition>

        <h1>Match Report</h1>

        <h5>Matches found to your profile:</h5>

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
div {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 20px;
  background-color: #f4f6f8;
  min-height: 100vh;
}

/* Headings */
h1 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #333;
}

h5 {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 20px;
}

/* Match Results Styling */
.match-results {
  background-color: white;
  margin-bottom: 20px;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.match-results:hover {
  transform: scale(1.02);
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15);
}

/* Match Headings */
.match-results h3 {
  margin-top: 0;
  color: #1a73e8;
}

.match-results p {
  color: #444;
  margin-bottom: 1rem;
}

/* View More Button */
.match-results .btn {
  background-color: #1a73e8;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.match-results .btn:hover {
  background-color: #0c5ed7;
}

/* Flash Messages */
.success-message,
.error-message {
  position: fixed;
  top: 20px;
  right: 30px;
  padding: 12px 20px;
  border-radius: 8px;
  text-align: center;
  font-weight: bold;
  z-index: 999;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
}

.success-message {
  color: #155724;
  background-color: #d4edda;
}

.error-message {
  color: #721c24;
  background-color: #f8d7da;
}

/* Fade Animation */
.fade-leave-active {
  transition: opacity 1s ease-in-out;
}

.fade-leave-to {
  opacity: 0;
}

</style>