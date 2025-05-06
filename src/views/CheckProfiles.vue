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
    const response = await fetch(`/api/users/${userID}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) throw new Error('Failed to fetch profiles');
    
    const data = await response.json();
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
.title {
  text-align: center;
  margin: 2rem 0 1.5rem;
  font-size: 2rem;
  color: #333;
}

.profile-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
}

.profile-item.card {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  width: 380px;
  padding: 1.5rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.profile-item.card:hover {
  transform: scale(1.03);
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.1);
  border-color: #ccc;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-bottom: 1rem;
  background-color: #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #fff;
  overflow: hidden;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-initials {
  font-weight: bold;
  user-select: none;
}

.profile-details {
  width: 100%;
  text-align: center;
  margin-top: 0.5rem;
}

.profile-details p {
  margin: 0.3rem 0;
  color: #555;
  font-size: 1rem;
}

.btn.btn-primary {
  margin-top: 1rem;
  background-color: #007bff;
  color: #fff;
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  text-decoration: none;
  display: inline-block;
}

.btn.btn-primary:hover {
  background-color: #0056b3;
}

.loading, .error {
  text-align: center;
  margin: 2rem;
  font-size: 1.2rem;
}

.error {
  color: red;
}
</style>
