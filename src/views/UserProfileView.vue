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
        .then(response => {
            return response.json();
        })
        .then(data => {
            user.value = data.user;
            profiles.value = data.profiles;
        })
        .catch(error => {
            console.error('Failed to parse JSON:', error);
        })

}

function trackProfileView(profileID) {
    authStore.setProfileId(profileID);
}


onMounted(() => {
    fetchUser();
});

</script>

<template>
    <div class="main-body">
        <h1>My Profile</h1>

<div class="user-card card" v-if="user">
    <img :src="user.photo" alt="Profile Picture" />
    <div class="text-content">
        <h2>My Details</h2>
        <div class="user-info">
            <label for="name">Name:</label>
            <p>{{ user.name }} </p>
        </div>
        <div class="user-info">
            <label for="email">Email:</label>
            <p>{{ user.email }}</p>
        </div>
        <div class="user-info">
            <label for="date_joined">Date Joined:</label>
            <p>{{ user.date_joined }}</p>
        </div>
    </div>
</div>

        <div class="profiles">
            <h2>Profiles</h2>

            <div class="profile-list">
                <div v-for="profile in profiles" :key="profile.id" class="profile-item card">
                    <h3>About Me</h3>

                    <label for="description">Description:</label>
                    <p>{{ profile.description }}</p>


                    <label for="biography">Biography:</label>
                    <p>{{ profile.biography }}</p>

                    <router-link class="btn btn-primary" :to="`/profiles/${profile.id}`"
                        @click="trackProfileView(profile.id)">View Profile</router-link>
                </div>
            </div>
        </div>
    </div>
</template>


<style scoped>
.main-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(to bottom right, #ffecd2, #fcb69f);
  padding: 2rem 1rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
  font-size: 2.5rem;
  color: #e91e63;
  margin-bottom: 2rem;
  text-shadow: 1px 1px #fff;
}

.user-card.card {
  display: flex;
  flex-direction: row;
  align-items: center;
  background-color: #fff;
  border-radius: 20px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  padding: 24px;
  max-width: 720px;
  width: 100%;
  margin-bottom: 2rem;
  transition: transform 0.3s ease;
  gap: 20px;
  flex-wrap: wrap;
}

.user-card.card:hover {
  transform: scale(1.02);
}

.user-card h2 {
  color: #e91e63;
  margin-bottom: 1rem;
}

img {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  border: 4px solid #ffd700;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  margin-left: 20px;
  margin-right: 20px;
}

.user-info {
  display: flex;
  flex-direction: row;
  gap: 10px;
  font-size: 1rem;
  color: #333;
  margin: 6px 0;
}

label {
  font-weight: 600;
  color: #444;
  min-width: 90px;
}

.text-content {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  flex: 1;
}

.profiles {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  width: 100%;
}

.profiles h2 {
  font-size: 2rem;
  color: #d81b60;
  margin-bottom: 0.5rem;
}

.profile-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  width: 100%;
}

.profile-item.card {
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  width: 320px;
  padding: 20px;
  text-align: left;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
}

.profile-item.card:hover {
  transform: scale(1.03);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.profile-item.card h3 {
  font-size: 1.4rem;
  color: #e91e63;
  margin-bottom: 12px;
}

.profile-item.card label {
  display: block;
  font-weight: bold;
  margin-top: 12px;
  color: #444;
}

.profile-item.card p {
  margin-top: 4px;
  color: #333;
  line-height: 1.4;
}

.btn.btn-primary {
  display: inline-block;
  background: #e91e63;
  color: white;
  text-align: center;
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
  text-decoration: none;
  margin-top: 16px;
}

.btn.btn-primary:hover {
  background: #d81b60;
}

/* Responsive tweaks */
@media (max-width: 768px) {
  .user-card.card {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 20px;
  }

  .text-content {
    align-items: center;
    margin-left: 0;
  }

  .user-info {
    justify-content: center;
    text-align: left;
    flex-wrap: wrap;
  }

  img {
    margin: 0 auto 20px auto;
  }
}
</style>
