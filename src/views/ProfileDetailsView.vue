<script setup>
import { ref, onMounted, watch } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRoute } from 'vue-router';

const profile = ref(null);
const authStore = useAuthStore();
const profileID = ref(null); 
const favourites = ref([]);
const check_fav = ref([]);
const load_fav = ref([])
const success_message = ref('');
const error_message = ref('');
const csrf_token = ref("");
const route = useRoute();


profileID.value = authStore.profile_id;

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
  authStore.setProfileId(profileID.value);
}

const isFavourited = (id) => { return favourites.value.includes(id) };

function loadFavourites(id) {
  favourites.value = [];
  fetch(`/api/users/${id}/favourites`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authStore.token}`
    }
  })
    .then((response) => response.json())
    .then((data) => {
      load_fav.value = data.favourites;
    })
    .catch((error) => {
      console.error('Error fetching favourites:', error);
    });
}

function checkFavourites() {
  favourites.value = [];
  fetch(`/api/users/${authStore.user_id}/favourites`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authStore.token}`
    }
  })
    .then((response) => response.json())
    .then((data) => {
      check_fav.value = data.favourites;
      check_fav.value.forEach((favourite) => {
        favourites.value.push(favourite.fav_profile_id);
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
      console.error("Error: ", error);
    });
}

function addToFavourites(id) {
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

function fetchProfile() {
  fetch(`/api/profiles/${profileID.value}`, {
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
        checkFavourites();
        loadFavourites(profile.value.user_id);
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

watch(() => route.params.profile_id, (newId) => {
  if (newId) {
    trackProfileView(route.params.profile_id);
    profileID.value = route.params.profile_id;
    fetchProfile();
  }
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
      <div class="profile-pic">
  <img v-if="profile.photo" :src="profile.photo" alt="Profile Picture" />
  <div v-else class="placeholder-pic">{{ profile.user_name?.charAt(0).toUpperCase() }}</div>
</div>

      <h3>About Me</h3>

      <label for="user_name">Name:</label>
      <p>{{ profile.user_name   }}</p>

      <label for="description">Description:</label>
      <p>{{ profile.description }}</p>


      <label for="biography">Biography:</label>
      <p>{{ profile.biography }}</p>
    </div>

    <div class="user-info">
      <div class="preferences">
        <h3>Preferences</h3>

        <label for="fav_cuisine">Favourite Cuisine:</label>
        <p>{{ profile.fav_cuisine }}</p>


        <label for="fav_colour">Favourite Colour:</label>
        <p>{{ profile.fav_colour }}</p>


        <label for="fav_school_subject">Favourite School Subject:</label>
        <p>{{ profile.fav_school_subject }}</p>
      </div>

      <div class="values">
        <h3>Values</h3>

        <label for="political">Political:</label>
        <p>{{ profile.political }}</p>


        <label for="religious">Religious:</label>
        <p>{{ profile.religious }}</p>


        <label for="family_oriented">Family Oriented:</label>
        <p>{{ profile.family_oriented }}</p>
      </div>
    </div>

    <div class="location">
      <h3>Location</h3>

      <label for="parish">Parish:</label>
      <p>{{ profile.parish }}</p>
    </div>

    <div class="appearance">
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

    <div class="favourite-users">
      <h3>Favourite Users</h3>
      <div class="favourites">
        <ul>
          <li v-for="favourite in load_fav" :key="favourite.id">
            <router-link :to="`/profiles/${favourite.fav_profile_id}`">
              {{ favourite.user_name }}
            </router-link>
          </li>
        </ul>
      </div>
    </div>

    <button class="btn btn-secondary" v-if="profile.user_id !== authStore.user_id">Email User</button>

    <router-link class="btn btn-primary" v-if="profile.user_id === authStore.user_id" :to="`/profiles/match`">Match
      Me</router-link>

    <button class="btn btn-fav" @click="addToFavourites(profile.id)"><font-awesome-icon
        :icon="[isFavourited(profile.id) ? 'fas' : 'far', 'heart']"
        :class="{ 'heart-icon': true, 'favourited': isFavourited(profile.id) }"
        v-if="profile.user_id !== authStore.user_id" /></button>
  </div>
</template>


<style scoped>
.profile-pic {
  width: 150px;
  height: 150px;
  margin: 20px;
}

.profile-pic img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  color: white;
  background-color: #6c63ff; /* Example color */
  font-weight: bold;
  border: 2px solid #ccc;
}

.placeholder-pic img{
  width: 100%;
  height: 100%;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  color: white;
  background-color: #6c63ff; /* Example color */
  font-weight: bold;
  border: 2px solid #ccc;
}

.main-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  gap: 2rem;
}

h1 {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

section {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  padding: 1.5rem 2rem;
  width: 100%;
  max-width: 700px;
  transition: transform 0.3s;
}

section:hover {
  transform: translateY(-3px);
}

.header-info img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ccc;
  margin-right: 1.5rem;
}

.header-info,
.user-info,
.location,
.appearance,
.favourite-users {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.user-info {
  flex-direction: row;
  justify-content: space-between;
  flex-wrap: wrap;
}

.preferences,
.values {
  flex: 1 1 45%;
}

label {
  font-weight: 600;
  color: #555;
  margin-top: 0.5rem;
}

p {
  margin: 0.2rem 0 1rem;
  color: #333;
}

.success-message,
.error-message {
  position: fixed;
  top: 70px;
  right: 30px;
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  animation: fadeOut 2s forwards;
  z-index: 1000;
}

.success-message {
  background-color: #d1e7dd;
  color: #0f5132;
}

.error-message {
  background-color: #f8d7da;
  color: #842029;
}

@keyframes fadeOut {
  0% { opacity: 1; }
  80% { opacity: 1; }
  100% { opacity: 0; }
}

.btn {
  padding: 0.6rem 1.2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: background 0.3s;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.btn-fav {
  background: none;
  border: none;
  padding: 0;
  margin-top: 1rem;
}

.heart-icon {
  font-size: 2rem;
  cursor: pointer;
  color: grey;
  transition: color 0.3s;
}

.heart-icon.favourited {
  color: red;
}

.favourites ul {
  list-style: none;
  padding: 0;
}

.favourites li {
  margin-bottom: 0.5rem;
}

@media screen and (max-width: 768px) {
  .user-info {
    flex-direction: column;
    gap: 1.5rem;
  }
}

</style>