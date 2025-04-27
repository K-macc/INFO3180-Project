<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const profiles = ref([]);
const searchTerm = ref('');
const recent_profiles = ref([]);
const filtered_profiles = ref([]);
const authStore = useAuthStore();
const errorMessage = ref('');
const router = useRouter();

function flashMessage(prompt){
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

function fetchProfiles(){
    fetch(`/api/check-profiles/${authStore.user_id}`, {
        method: 'GET',
        headers: {
             'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            errorMessage.value = data.error;
            flashMessage(errorMessage);
            router.push('/profiles/check');
        } else {
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
        }
    })
};

onMounted(() => {
  fetchProfiles();
});


function filteredProfiles(){
    errorMessage.value = '';
    filtered_profiles.value = [];
    fetch(`/api/search?search=${searchTerm.value}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.results) {
            const result = data.results;
            console.log(result);
            result.forEach((item) => {
                filtered_profiles.value.push(item); 
            });
        } else {
            errorMessage.value = data.error;
            flashMessage(errorMessage);
        }
    })
    .catch(error => {
        console.error('Error fetching profiles:', error);
    });
};
</script>

<template>
    <div class="profiles">
      <transition name="fade">
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </transition>
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

.error-message {
      color: red;
      background-color: #f8d7da;
      padding: 10px;
      padding-left: 0px;
      margin-bottom: 10px;
      border-radius: 5px;
      top: 70px;
      right: 45px;
      position: fixed;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      width: 12%;
      height: 5%;
  }

  .fade-leave-active {
    transition: opacity 1s ease-in-out;
  }

  .fade-leave-to {
    opacity: 0;
  }

</style>
  