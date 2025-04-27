<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const profiles = ref([]);
const searchTerm = ref('');
const recent_profiles = ref([]);
const filtered_profiles = ref([]);
const authStore = useAuthStore();

function trackProfileView(profileID) {
    authStore.setProfileId(profileID);
}

function fetchProfiles(){
  fetch('/api/profiles', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    profiles.value = data.profiles;
    recent_profiles.value =  profiles.value.slice(-4).reverse();
  })
  .catch(error => {
    console.error('Error fetching profiles:', error);
  });
};

onMounted(() => {
  fetchProfiles();
});


function filteredProfiles(){
  const term = searchTerm.value.toLowerCase();
  filtered_profiles.value = profiles.value.filter(profile =>
    profile.birth_year?.toString().includes(term) ||
    profile.sex?.toLowerCase().includes(term) ||
    profile.race?.toLowerCase().includes(term)
  );
};
</script>

<template>
    <div class="profiles">
      <div class="search-container">
        <input v-model="searchTerm" type="search" class="search-input" placeholder="Search name, birth year, sex, race..." @keyup.enter="filteredProfiles"/>
      </div>
  
      <h2>Recently Added Profiles</h2>
      <div class="profile-list">
        <div v-for="profile in recent_profiles" :key="profile.id" class="profile-item card">
          <h3>{{ profile.sex }}</h3>
          <p>{{ profile.description }}</p>
          <router-link class="btn btn-primary" :to="`/profiles/${profile.id}`" @click="trackProfileView(profile.id)">View more details</router-link>
        </div>
      </div>

    
        <h2 v-if="filtered_profiles.length">Search Results</h2>
        <div class="profile-list">
            <div v-for="profile in filtered_profiles" :key="profile.id" class="profile-item card">
                <h3>{{ profile.sex }}</h3>
                <p>{{ profile.description }}</p>
                <router-link class="btn btn-primary" :to="`/profiles/${profile.id}`" @click="trackProfileView(profile.id)">View more details</router-link>
            </div>
        </div>
    </div>
  </template>

<style scoped>
.search-container {
    text-align: center;
    margin: 2rem 0;
  }
  
  .search-input {
    padding: 0.7rem;
    width: 50%;
    border-radius: 10px;
    font-size: 1rem;
    border: 1px solid #ccc;
  }
  
  .profile-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .profile-item.card {
    width: 300px;
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid #ccc;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
  }

  .profile-item.card:hover {
    background: white ;
    transform: scale(1.05);
    box-shadow: 0px 0px 10px rgb(146, 144, 144) ;
    border-color: #817e7e96 ;
  }

  h2 {
    align-self: center;
    justify-self: center;
    margin: 70px 0 20px 0;;
  }

  .btn.btn-primary {
    width: 60%;
    align-self: center;
    margin-bottom: 10px;
}

</style>
  