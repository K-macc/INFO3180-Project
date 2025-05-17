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

    <div class="user-card card">
      <div class="profile-pic">
        <img v-if="profile.image" :src="profile.image" alt="Profile Picture" />
        <div v-else class="placeholder-pic">{{ profile.user_name?.charAt(0).toUpperCase() }}</div>
      </div>
      <div class="header-info">
      <h3>About {{ profile.user_name }}</h3>

      <div>
          <label for="description">Description:</label>
          <p>{{ profile.description }}</p>

          <label for="biography">Biography:</label>
          <p>{{ profile.biography }}</p>

          <label for="parish">Parish:</label>
          <p>{{ profile.parish }}</p>
      </div>
    </div>

    <hr>
    <div class="user-info">
      <div class="preferences">
      <h3>Preferences</h3>

        <div>
          <label for="fav_cuisine">Favourite Cuisine:</label>
          <p>{{ profile.fav_cuisine }}</p>
        </div>

        <div>
          <label for="fav_colour">Favourite Colour:</label>
          <p>{{ profile.fav_colour }}</p>
        </div>

        <div>
          <label for="fav_school_subject">Favourite School Subject:</label>
          <p>{{ profile.fav_school_subject }}</p>
        </div>
      </div>

      <div class="values">
      <h3>Values</h3>

        <div>
          <label for="political">Political:</label>
          <p>{{ profile.political }}</p>
        </div>

        <div>
          <label for="religious">Religious:</label>
          <p>{{ profile.religious }}</p>
        </div>

        <div>
          <label for="family_oriented">Family Oriented:</label>
          <p>{{ profile.family_oriented }}</p>
        </div>
      </div>
    </div>

    <hr>
    <div class="appearance">
      <h3>Appearance</h3>


      <div>
        <label for="sex">Sex:</label>
        <p>{{ profile.sex }}</p>
      </div>

      <div>
        <label for="race">Race:</label>
        <p>{{ profile.race }}</p>
      </div>

      <div>
        <label for="birth_year">Birth Year:</label>
        <p>{{ profile.birth_year }}</p>
      </div>

      <div>
        <label for="height">Height:</label>
        <p>{{ profile.height }} cm</p>
      </div>
    </div>

    <hr>
    <div class="favourite-users">
      <h3>Favourite Users</h3>
      <div class="favourites">
        <ul>
          <li v-for="favourite in load_fav" :key="favourite.id">
            <router-link :to="`/profiles/${favourite.fav_profile_id}`" class ="btn-favourite">
              {{ favourite.user_name }}
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </div>

    <button class="btn btn-secondary" v-if="profile.user_id !== authStore.user_id">Email User</button>

    <router-link class="btn btn-primary" v-if="profile.user_id === authStore.user_id" :to="`/profiles/match`">Match
      Me</router-link>

    <button class="btn btn-fav" @click="addToFavourites(profile.id)">
      <font-awesome-icon
    :icon="[isFavourited(profile.id) ? 'fas' : 'far', 'heart']"
    :class="{ 'heart-icon': true, 'favourited': isFavourited(profile.id) }"
  /></button>
  </div>
</template>


<style scoped>
/* Core profile picture styles */
.profile-pic {
  width: 150px;
  height: 150px;
  margin: 20px;
}

.main-body {
  background: linear-gradient(to bottom left, #F7E1E9, #8A0047); /* Lavender Blush to Sky Blue */
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding: 2rem 1rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.profile-pic img,
.placeholder-pic {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  border: 4px solid #AD2874; /* Fandango border */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: auto;
  object-fit: cover;
}

/* Placeholder background */
.placeholder-pic {
  font-size: 48px;
  color: white;
  background-color: #69003D; /* Tyrian Purple */
  font-weight: bold;
}

/* Headings */
h1, h2, h3 {
  color: #8A0047; /* Fandango */
  text-shadow: 2px 2px #00C8FF; /* Lavender Blush shadow */
  margin-bottom: 1rem;
}

h1 {
  font-size: 2.5rem;
  font-weight: bold;
}

/* Card container */
.user-card.card {
  background: #F7E1E9; /* Lavender Blush */
  border-radius: 1.5rem;
  box-shadow: 0 6px 20px rgba(105, 0, 61, 0.15); /* Tyrian Purple shadow */
  padding: 2rem;
  max-width: 720px;
  width: 100%;
  margin-bottom: 2rem;
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

/* Sections */
section {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(51, 51, 51, 0.05); /* Jet subtle shadow */
  padding: 1.5rem 2rem;
  width: 100%;
  max-width: 700px;
  transition: transform 0.3s;
}

section:hover {
  transform: translateY(-3px);
}

/* Header area */
.header-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  width: 90%;
  padding: 1rem;
}

/* User details layout */
.user-info {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 90%;
  gap: 2rem;
}

.user-info h3, h2 {
  color: #8A0047; /* Fandango */
}

/* Appearance block */
.appearance {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 90%;
  padding: 1rem;
}

.appearance h2, .appearance h3 {
  color: #8A0047; /* Vivid Sky Blue highlight */
}

.appearance div,
.preferences div,
.values div {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.appearance label,
.preferences label,
.values label {
  width: 180px;
  font-weight: 600;
  color: #333333; /* Jet */
  text-align: left;
}

.appearance p,
.preferences p,
.values p {
  flex: 1;
  color: #333333; /* Jet */
}

/* Preferences & values */
.preferences,
.values {
  flex-direction: column;
  width: 45%;
}

/* Favourites section */
.favourite-users {
  width: 90%;
  text-align: center;
}

.favourite-users h3 {
  color: #8A0047; /* Vivid Sky Blue */
}

.favourite-users ul {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.favourite-users li {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Messages */
.success-message,
.error-message {
  position: fixed;
  top: 70px;
  right: 30px;
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  z-index: 1000;
  animation: fadeOut 2s forwards;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.success-message {
  background-color: #D6F0F9; /* pale blue success */
  color: #0C4A6E; /* dark blue text */
}

.error-message {
  background-color: #F7D6DA; /* pale pink error */
  color: #8A0047; /* Murrey */
}

@keyframes fadeOut {
  0% { opacity: 1; }
  80% { opacity: 1; }
  100% { opacity: 0; }
}

/* Buttons */
.btn {
  padding: 0.6rem 1.2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: background 0.3s;
}

.btn-primary {
  background-color: #6DDBFC; /* Sky Blue */
  color: white;
}

.btn-primary:hover {
  background-color: #00C8FF; /* Vivid Sky Blue */
}

.btn-secondary {
  background-color: #69003D; /* Tyrian Purple */
  color: white;
}

.btn-secondary:hover {
  background-color: #8A0047; /* Murrey */
}

.btn-favourite {
  background-color: #AD2874; /* Fandango */
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s ease;
}

.btn-favourite:hover {
  background-color: #8A0047; /* Murrey */
}

.heart-icon {
  font-size: 2rem;
  color: #333333; /* Jet */
  transition: color 0.3s;
  margin: 1rem;
}

.heart-icon.favourited {
  color: #AD2874; /* Fandango */
}

/* General styles */
label {
  font-weight: 600;
  color: #333333; /* Jet */
}

p {
  margin: 0.2rem 0 1rem;
  color: #333333; /* Jet */
}

hr {
  border: none;
  border-top: 1.5px solid #8A0047; /* Murrey */
  margin: 1.5rem 0;
  width: 90%;
}

/* Responsive */
@media screen and (max-width: 768px) {
  .user-info {
    flex-direction: column;
  }

  .preferences, .values {
    width: 100%;
  }
}
</style>

