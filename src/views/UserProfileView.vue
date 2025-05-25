<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const userID = authStore.user_id;
const user = ref(null);
const profiles = ref([]);

function fetchUser() {
    fetch(`/api/users/${userID}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            user.value = data.user;
            profiles.value = data.profiles;
        })
        .catch(error => {
            console.error('Failed to parse JSON:', error);
        });
}

function trackProfileView(profileID) {
    authStore.setProfileId(profileID);
}

onMounted(() => {
    fetchUser();
});
</script>

<template>
    <div class="main-body-bg">
        <h1>My Profile</h1>

        <div class="user-card card" v-if="user">
            <img :src="user.photo" alt="Profile Picture" />
            <div class="text-content">
                <h2>My Details</h2>
                <div class="user-info">
                    <label>Name:</label>
                    <p>{{ user.name }}</p>
                </div>
                <div class="user-info">
                    <label>Email:</label>
                    <p>{{ user.email }}</p>
                </div>
                <div class="user-info">
                    <label>Date Joined:</label>
                    <p>{{ user.date_joined }}</p>
                </div>
            </div>
        </div>

        <div class="profiles" v-if="profiles.length">
            <h2>My Profiles</h2>
            <div class="profile-list">
                <div v-for="profile in profiles" :key="profile.id" class="profile-item card">
                    <h3>About Me</h3>
                    <label>Description:</label>
                    <p>{{ profile.description }}</p>
                    <label>Biography:</label>
                    <p>{{ profile.biography }}</p>
                    <router-link
                        class="btn btn-primary"
                        :to="`/profiles/${profile.id}`"
                        @click="trackProfileView(profile.id)"
                    >
                        View Profile
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.main-body-bg {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding: 2rem 1rem;
}

h1 {
  font-size: 3rem;
  color: #f7d4e6;
  text-shadow: 2px 2px #AD2874;
  margin-bottom: 2rem;
}

.user-card.card {
  display: flex;
  align-items: center;
  background-color: #fff;
  border: 1px solid #AD2874;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  max-width: 500px;
  width: 100%;
  margin-bottom: 3rem;
  gap: 24px;
  transition: all 0.3s ease;
  flex-wrap: wrap;
}

.user-card h2 {
  color: #ad1457;
  margin-bottom: 1rem;
  text-align: start;
}

img {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  border: 4px solid #ad1457;
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.3);
}

.text-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.user-info {
  display: flex;
  justify-content: flex-start;
  gap: 8px;
  font-size: 1.1rem;
  color: #444;
  margin-bottom: 0.1rem;
}

label {
  font-weight: bold;
  min-width: 50px;
  color: #555;
}

.profiles {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.profiles h2 {
  font-size: 2.2rem;
  color: #f7d4e6;
  text-shadow: 2px 2px #AD2874;
  margin-bottom: 1.5rem;
}

.profile-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  width: 100%;
}

.profile-item.card {
  background: linear-gradient(145deg, #F7E1E9, #ffffff);
  border: 1px solid #AD2874;
  color: #69003D;
  border-radius: 20px;
  box-shadow: 0 8px 26px rgba(0, 0, 0, 0.12);
  width: 300px;
  padding: 1.5rem;
  text-align: left;
  transition: all 0.3s ease;
}

.profile-item.card:hover {
  transform: scale(1.04);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
}

.profile-item.card h3 {
  font-size: 1.4rem;
  color: #c2185b;
  margin-bottom: 0.75rem;
}

.profile-item.card label {
  display: block;
  font-weight: 600;
  margin-top: 1rem;
  color: #333;
}

.profile-item.card p {
  margin-top: 0.3rem;
  color: #444;
  line-height: 1.5;
}

.btn.btn-primary {
  display: inline-block;
  color: white;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: bold;
  text-decoration: none;
  margin-top: 1rem;
  box-shadow: 0 8px 20px rgba(216, 27, 96, 0.3);
  transition: all 0.3s ease;
}

.btn.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 28px rgba(136, 14, 79, 0.5);
}
</style>
