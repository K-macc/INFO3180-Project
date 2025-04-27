<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const profile = ref(null);
const authStore = useAuthStore();
const profileID = authStore.profile_id; // Assuming you have the profile ID stored in the auth store
const favourites = ref([]);
const success_message = ref('');
const error_message = ref('');
const csrf_token = ref("");

function flashMessage(prompt){
    setTimeout(() => {
        if (Array.isArray(prompt)) {
            prompt.value = [];
        } else {
            prompt.value = '';
        }
  }, 2000);
}

const isFavourited = (id) => {return favourites.value.includes(id)};

function loadFavourites() {
    fetch(`/api/users/${authStore.user_id}/favourites`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`
        }
      })
      .then((response) => response.json())
      .then((data) => {
        const fav = data.favourites;
        fav.forEach((favourite) => {
            favourites.value.push(favourite.fav_user_id);
        });
      })
      .catch((error) => {
        console.error('Error fetching favourites:', error);
      });
}

function getCsrfToken() {
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            csrf_token.value = data.csrf_token;
        })
        .catch((error) => {
            console.error("Error: ",error);
        });
}


function addToFavourites(id){
  if (favourites.value.includes(id)) {
    favourites.value = favourites.value.filter(fav => fav !== id);
    fetch(`/api/profiles/${id}/favourite`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': csrf_token.value,
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
        success_message.value = data.message;
        flashMessage(success_message);
      }
    })
    .catch(error => {
      console.error('Error deleting from favourites:', error);
    });
  } else {
    favourites.value.push(id);
    fetch(`/api/profiles/${id}/favourite`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrf_token.value,
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
        success_message.value = data.message;
        flashMessage(success_message);
      }
    })
    .catch(error => {
      console.error('Error adding to favourites:', error);
    });
  }
}

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
            console.log(data.error);
            console.error('Error fetching profile:', data.error);
            return;
        } else {
            profile.value = data.profile;
            loadFavourites();
            console.log('Fetched favourites:', favourites.value);
        }
    })
    .catch(error => {
            console.error('Failed to parse JSON:', error);
    })

}

onMounted(() => {
    fetchProfile(); 
    getCsrfToken();
});
</script>

<template>
    <div class="main-body" v-if="profile">
        <transition name="fade">
            <div v-if="success_message" class="success-message">
                {{ success_message }}
            </div>
        </transition>

        <transition name="fade">
            <div v-if="error_message" class="error-message">
                {{ error_message }}
            </div>
        </transition>

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

        <button class="btn btn-secondary" v-if="profile.user_id !== authStore.user_id">Email User</button>
        <button class="btn btn-fav" @click="addToFavourites(profile.user_id)"><font-awesome-icon :icon="[isFavourited(profile.user_id) ? 'fas' : 'far', 'heart']" :class="{'heart-icon': true, 'favourited': isFavourited(profile.user_id)}" v-if="profile.user_id !== authStore.user_id"/></button>
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

.heart-icon {
  font-size: 50px;
  cursor: pointer;
  color: grey; /* default for unfavourited */
}

.favourited {
  color: red;
}

.success-message {
    color: green;
    background-color: #d4edda;
    padding: 10px;
    border-radius: 5px;
    width: 15%;
    top: 100px;
    right: 45px;
    text-align: center;
    position: fixed;
  }

  .error-message {
      color: red;
      background-color: #f8d7da;
      padding: 10px;
      padding-top: 20px;
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
      width: 26%;
      min-height: 8%;
      height: auto;
  }

  .fade-leave-active {
    transition: opacity 1s ease-in-out;
  }

  .fade-leave-to {
    opacity: 0;
  }
</style>