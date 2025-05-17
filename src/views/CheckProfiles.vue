<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js';

const authStore = useAuthStore();
const profiles = ref([]);
const userID = authStore.user_id;
const isLoading = ref(true);
const error = ref(null);

function trackProfileView(profileID) {
  authStore.setProfileId(profileID);
}

function getInitials(text) {
  return text ? text.charAt(0).toUpperCase() : '?';
}

function stringToColor(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  return `hsl(${hash % 360}, 70%, 70%)`;
}

async function fetchProfiles() {
  try {
    console.log('Fetching profiles for userID:', userID);
    console.log('Auth token:', authStore.token);
    const response = await fetch(`/api/users/${userID}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) throw new Error('Failed to fetch profiles');
    
    const data = await response.json();
    console.log('Response data:', data);
    profiles.value = data.profiles;
  } catch (err) {
    error.value = 'Failed to load profiles';
    console.error('Error:', err);
  } finally {
    isLoading.value = false;
  }
}

onMounted(async () => { 
  fetchProfiles();
});
</script>

<template>
  <div>
    <h1 class="title">Choose a Profile</h1>

    <div v-if="isLoading" class="loading">Loading profiles...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="profile-list">
      <div v-for="profile in profiles" :key="profile.id" class="profile-item card">
        <div class="profile-avatar" :style="{ backgroundColor: profile.photo ? 'transparent' : stringToColor(profile.description) }">
          <img v-if="profile.photo" :src="profile.photo" alt="Profile" class="avatar-img" />
          <span v-else class="avatar-initials">{{ getInitials(profile.description || profile.sex) }}</span>
        </div>

        <div class="profile-details">
          <p><strong>Description:</strong> {{ profile.description }}</p>
          <p><strong>Sex:</strong> {{ profile.sex }}</p>
          <p><strong>Race:</strong> {{ profile.race }}</p>

          <router-link class="btn btn-primary" :to="`/profiles/update/${profile.id}`"
            @click="trackProfileView(profile.id)">
            Complete this profile
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
body {
  background: linear-gradient(135deg, #00C8FF, #8A0047);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.title {
  text-align: center;
  margin: 2rem 0 1.5rem;
  font-size: 2.8rem;
  font-weight: 700;
  color: #8A0047; /* Murrey */
  letter-spacing: 1px;
  animation: fadeInDown 0.6s ease-in-out;
}

.profile-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2.5rem;
  padding: 0 2rem 3rem;
  max-width: 1200px;
  margin: 0 auto;
  animation: fadeIn 0.8s ease-in-out;
}

.profile-item.card {
  background: linear-gradient(145deg, #F7E1E9, #ffffff);
  border-radius: 20px;
  padding: 1.8rem 1.5rem;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: all 0.35s ease;
  position: relative;
  overflow: hidden;
}

.profile-item.card::before {
  content: "";
  position: absolute;
  top: -40%;
  left: -40%;
  width: 180%;
  height: 180%;
  background: radial-gradient(circle at center, rgba(0, 200, 255, 0.1), transparent 70%);
  transform: rotate(25deg);
  z-index: 0;
}

.profile-item.card:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 18px 36px rgba(0, 0, 0, 0.15);
}

.profile-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin: 0 auto 1rem;
  background-color: #AD2874; /* Fandango */
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 25rem;
  color: #fff;
  overflow: hidden;
  box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.7);
  animation: popIn 0.5s ease;
  position: relative;
  z-index: 1;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.avatar-initials {
  font-weight: bold;
  user-select: none;
  font-size: 2rem;
}

.profile-details {
  margin-top: 0.5rem;
  position: relative;
  z-index: 1;
}

.profile-details p {
  margin: 0.4rem 0;
  color: #333333; /* Jet */
  font-size: 1rem;
}

.btn.btn-primary {
  margin-top: 1rem;
  background-color: #AD2874; /* Fandango */
  color: #fff;
  padding: 0.7rem 1.4rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.25s ease;
  box-shadow: 0 8px 20px rgba(173, 40, 116, 0.4);
}

.btn.btn-primary:hover {
  background-color: #69003D; /* Tyrian Purple */
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(138, 0, 71, 0.5); /* Murrey shadow */
}

.loading,
.error {
  text-align: center;
  margin: 2rem;
  font-size: 1.2rem;
  animation: fadeIn 0.5s ease;
}

.error {
  color: #8A0047; /* Murrey */
  font-weight: 600;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes popIn {
  0% {
    transform: scale(0.8);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>


