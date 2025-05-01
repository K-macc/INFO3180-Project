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
.profile-pic {
  width: 150px;
  height: 150px;
  margin: 20px;
}

.profile-pic img {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  border: 4px solid #ffd700;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  margin-left: 20px;
  margin-right: 20px;
}

.placeholder-pic {
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
  border: 4px solid #ffd700;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

.main-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(to bottom right, #ffecd2, #fcb69f);
  padding: 2rem 1rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  /* gap: 2rem; */
}

h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #e91e63;
  margin-bottom: 2rem;
  text-shadow: 1px 1px #fff;
}

/* blue */
.user-card.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #fff;
  border-radius: 20px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  padding: 24px;
  max-width: 720px;
  width: 100%;
  margin-bottom: 2rem;
  transition: transform 0.3s ease;
  gap: 1rem;
  flex-wrap: wrap;
}

.user-card.card h2{
  color: #e91e63;
  margin-bottom: 1rem;
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

/* pink */
.header-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  width: 90%;
}
  /* yellow */
  .header-info div {
    display: flex;
    flex-direction: column;
    align-items: left;
    justify-content: left;
    /* gap: 1rem; */
    width: 90%;
    /* background-color: lightgoldenrodyellow; */
  }
  .header-info img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #ccc;
    margin-right: 1.5rem;
  }
  .header-info h3 {
    color: #e91e63;
    margin-bottom: 1rem;
  }

/* .header-info, */
.user-info,
.location,
.appearance,
.favourite-users {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* teal */
.appearance {
  /* background-color: lightseagreen; */
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-content: center;
  width: 90%;
}
  .appearance h3 {
    color: #e91e63;
  }

  .appearance h2 {
    color: #e91e63;
    margin-bottom: 1rem;
  }

  .appearance div {
    display: flex;
    flex-direction: row;
    gap: 1rem;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
    .appearance div label {
      width: 180px; /*Set a fixed width for labels*/
      text-align: left; /* Align label text to the right */
      margin: 0;
      color: black;
      /* padding-top: 6px;;
      padding-bottom: 6px;; */
    }

    .appearance div p {
      margin: 0; /* Remove extra margins */
      flex: 1; /* Allow paragraphs to take up remaining space */
      text-align: left; /* Align paragraph text to the left */
    }

.user-info {
  flex-direction: row;
  justify-content: space-between;
  /* flex-wrap: wrap; */
  width:90%
}
.user-info h3, h2 {
  color: #e91e63;
  margin-bottom: 1rem;
}

/* GREEN */
.preferences,
.values {
  display: flex;
  flex-direction: column;
  align-content: center;
  padding-left: 1rem;
  /* flex: 1 1 45%; */
  /* background-color: lightgreen; */
  width: 45%;
}
  
    .preferences div,
    .values div {
      display: flex;
      flex-direction: row;
      gap: 1rem;      
      justify-content: center;
      align-items: center;
      text-align: center;
    }
      .preferences div label,
      .values div label {
        width: 180px; /*Set a fixed width for labels*/
        text-align: left; /* Align label text to the right */
        margin: 0;
        padding-top: 6px;
        padding-bottom: 6px;
        color: black;
      }

      .preferences div p,
      .values div p {
        margin: 0; /* Remove extra margins */
        flex: 1; /* Allow paragraphs to take up remaining space */
        text-align: left; /* Align paragraph text to the left */
      }

.favourite-users {
  display: flex;
  flex-direction: column;
  align-content: center;
  align-items: center;
  justify-content: center;
  padding-left: 1rem;
  /* background-color: lightcoral; */
  width: 90%;
}
  .favourite-users h3 {
    color: #e91e63;
    margin-bottom: 1rem;
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
    text-align: center;
  }

label {
  font-weight: 600;
  color: black;
  margin-top: 0.5rem;
}

p {
  margin: 0.2rem 0 1rem;
  color: #333;
}

hr {
  border: none;
  border-top: 1.5px solid grey;
  margin: 1.5rem 0;
  width: 90%; /* Adjust width as needed */
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
  background: none; /* Remove the red background */
  border: none; /* Remove the border */
  padding: 0;
  cursor: pointer; /* Make it look clickable */
  display: inline-flex; /* Center the icon */
  align-items: center;
  justify-content: center;
}

.btn-favourite {
  display: inline-block;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  color: white;
  background-color: #e91e63;
  border: none;
  border-radius: 0.5rem;
  text-align: center;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-favourite:hover {
  background-color: #d81b60;
}

.heart-icon {
  font-size: 2rem;
  cursor: pointer;
  color: grey;
  transition: color 0.3s;
  margin: 1rem;
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