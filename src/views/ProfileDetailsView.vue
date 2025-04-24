<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const profile = ref(null);
const authStore = useAuthStore();
const profileID = authStore.profile_id; // Assuming you have the profile ID stored in the auth store

function fetchProfile(){
    fetch(`/api/profiles/${profileID}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authStore.token}`
        }
    })
    .then(response => {
    return response.json();     
    })
    .then(data => { 
        if (data.error) {
            console.error('Error fetching profile:', data.error);
            return;
        } else {
            profile.value = data.profile;
        }
    })
    .catch(error => {
            console.error('Failed to parse JSON:', error);
    })

}

onMounted(() => {
    fetchProfile(); 
});
</script>

<template>
    <div class="main-body" v-if="profile">
        <h1>My Profile</h1>

        <div class="header-info">
            <img src="" alt="Profile Picture">

            <h3>About Me</h3>
                    
            <label for="description">Description:</label>
            <p>{{ profile.description }}</p>

    
            <label for="biography">Biography:</label>
            <p>{{ profile.biography }}</p>
        </div>
        
        <div class="user-info">
            <div class="general-info">
                <h3>Preferences</h3>
                    
                <label for="fav_cuisine">Favourite Cuisine:</label>
                <p>{{ profile.fav_cuisine }}</p>
            
            
                <label for="fav_colour">Favourite Colour:</label>
                <p>{{ profile.fav_colour }}</p>

            
                <label for="fav_school_subject">Favourite School Subject:</label>
                <p>{{ profile.fav_school_subject }}</p>
            </div>

            <div class="favourites">
                <h3>Values</h3>
        
                <label for="political">Political:</label>
                <p>{{ profile.political }}</p>
            

                <label for="religious">Religious:</label>
                <p>{{ profile.religious }}</p>
            

                <label for="family_oriented">Family Oriented:</label>
                <p>{{ profile.family_oriented }}</p>
            </div>
        </div>

        <div class="other-info">
            <h3>Location</h3>

            <label for="parish">Parish:</label>
            <p>{{ profile.parish }}</p>
        </div>

        <div class="other-profiles">
            <h3>Appearance</h3>
                    
            <label for="sex">Sex:</label>
            <p>{{ profile.sex }}</p>
        
        
            <label for="race">Race:</label>
            <p>{{ profile.race }}</p>

        
            <label for="birth_year">Birth Year:</label>
            <p>{{ profile.birth_year }}</p>

        
            <label for="height">Height:</label>
            <p>{{ profile.height }}</p>
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

.header-info {
    display: grid;
    grid-template-columns: 190px 1fr; /* Image takes up 190px, text takes the remaining space */
    align-items: flex-start;  /* Align the content to the top */
    justify-content: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    width: 550px;
    height: auto;
    transition: all 0.3s ease-in-out;
    margin-top: 20px;
}

.user-info {
    display: flex;
    justify-content: center;
    width: 100%;
    margin: 20px 0px;
    gap: 40px;
}

.general-info {
    display: grid;
    grid-template-columns: 190px 1fr; /* Image takes up 190px, text takes the remaining space */
    align-items: flex-start;  /* Align the content to the top */
    justify-content: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    width: 400px;
    height: auto;
    transition: all 0.3s ease-in-out;
}

.favourites {
    display: grid;
    grid-template-columns: 190px 1fr; /* Image takes up 190px, text takes the remaining space */
    align-items: flex-start;  /* Align the content to the top */
    justify-content: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    width: 400px;
    height: auto;
    transition: all 0.3s ease-in-out;
}

.other-info {
    display: grid;
    grid-template-columns: 190px 1fr; /* Image takes up 190px, text takes the remaining space */
    align-items: flex-start;  /* Align the content to the top */
    justify-content: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    width: 400px;
    height: auto;
    transition: all 0.3s ease-in-out;
    margin-bottom: 20px;
}

.other-profiles {
    display: grid;
    grid-template-columns: 190px 1fr; /* Image takes up 190px, text takes the remaining space */
    align-items: flex-start;  /* Align the content to the top */
    justify-content: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    width: 550px;
    height: auto;
    transition: all 0.3s ease-in-out;
}

</style>