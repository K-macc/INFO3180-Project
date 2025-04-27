<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const userID = authStore.user_id; 
const user = ref(null);
const profiles = ref([]);

function fetchUser(){
    fetch(`/api/users/${userID}`, {
        method: 'GET',
    })
    .then(response => {
    return response.json();     
    })
    .then(data => { 
        user.value = data.user;
        profiles.value = data.profiles;
        console.log(profiles.value);
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

        <div class="header-info" v-if="user">
            <img :src="user.photo" alt="Profile Picture">

            <div class="text-content">
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

                    <router-link class="btn btn-primary" :to="`/profiles/${profile.id}`" @click="trackProfileView(profile.id)">View Profile</router-link>
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
    height: 100vh;
}

img {
    width: 130px;
    height: 130px;
    border-radius: 50%;
    margin: 10px 0px 10px 40px;
}

.header-info {
    display: grid;
    grid-template-columns: 140px 1fr; /* Image takes up 190px, text takes the remaining space */
    align-items: flex-start;  /* Align the content to the top */
    justify-content: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    width: 550px;
    height: 150px;
    transition: all 0.3s ease-in-out;
    margin-top: 20px;
    margin-bottom: 50px;
}

.user-info {
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 10px;
    font-size: large;
}

label {
    font-weight: bold;
}

.text-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
}

.profiles {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2rem;
}

.profile-list {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    width: 100%;
    gap: 2rem;
}


.profile-item.card  {
  margin: 0.5rem 0 0.5rem;
  font-size: 1.1rem;
  color: #333;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  width: 500px;
  height: 300px;
  transition: all 0.3s ease-in-out;
  justify-content: space-around;
  padding: 1px 25px;
}


.profile-item.card:hover {
  background: white ;
  transform: scale(1.05);
  box-shadow: 0px 0px 10px rgb(146, 144, 144) ;
  border-color: #817e7e96 ;
}

.btn.btn-primary {
    width: 30%;
    align-self: center;
    margin-bottom: 10px;
}

</style>