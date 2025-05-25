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
  <div class="profile-bg">
    <transition name="fade">
      <div v-if="success_message" class="alert success-message">{{ success_message }}</div>
    </transition>
    <transition name="fade">
      <div v-if="error_message" class="alert error-message">{{ error_message }}</div>
    </transition>

    <div class="profile-card" v-if="profile">
      
      <div class="profile-topbar">
        <div class="profile-avatar">
          <img v-if="profile.image" :src="profile.image" alt="Profile Picture" />
          <div v-else class="avatar-placeholder">
            {{ profile.user_name?.charAt(0).toUpperCase() }}
          </div>
        </div>
        <div class="profile-name-btns">
          <div class="profile-name-button">
            <h1>{{ profile.user_name }}</h1>
          <div class="profile-btn-row">
            <button class="btn-fav" @click="addToFavourites(profile.id)"
              :aria-label="isFavourited(profile.id) ? 'Remove from favourites' : 'Add to favourites'"
              v-if="parseInt(profile.user_id) !== parseInt(authStore.user_id)">
              <font-awesome-icon :icon="[isFavourited(profile.id) ? 'fas' : 'far', 'heart']"
                :class="{ 'heart-icon': true, 'favourited': isFavourited(profile.id) }" />
            </button>
          </div>
          </div>
          <button class="btn btn-secondary" v-if="parseInt(profile.user_id) !== parseInt(authStore.user_id)">Email User</button>
            <router-link class="btn btn-primary" v-if="parseInt(profile.user_id) === parseInt(authStore.user_id)" :to="`/profiles/match`">
              Match Me
            </router-link>
        </div>
      </div>

      <div class="profile-grid">
        <section class="about-section grid-about">
          <h2>About</h2>
          <div class="about-list">
            <div>
              <label>Description:</label>
              <p>{{ profile.description }}</p>
            </div>
            <div>
              <label>Biography:</label>
              <p>{{ profile.biography }}</p>
            </div>
            <div>
              <label>Parish:</label>
              <p>{{ profile.parish }}</p>
            </div>
          </div>
        </section>

        
        <section class="appearance-section grid-appearance">
          <h2>Appearance</h2>
          <div class="appearance-list">
            <div><label>Sex:</label><p>{{ profile.sex }}</p></div>
            <div><label>Race:</label><p>{{ profile.race }}</p></div>
            <div><label>Birth Year:</label><p>{{ profile.birth_year }}</p></div>
            <div><label>Height:</label><p>{{ profile.height }}</p></div>
          </div>
        </section>

       
        <section class="preferences-section grid-preferences">
          <h2>Preferences</h2>
          <div class="preferences-list">
            <div><label>Favourite Cuisine:</label><p>{{ profile.fav_cuisine }}</p></div>
            <div><label>Favourite Colour:</label><p>{{ profile.fav_colour }}</p></div>
            <div><label>Favourite School Subject:</label><p>{{ profile.fav_school_subject }}</p></div>
          </div>
        </section>

       
        <section class="values-section grid-values">
          <h2>Values</h2>
          <div class="values-list">
            <div><label>Political:</label><p>{{ profile.political }}</p></div>
            <div><label>Religious:</label><p>{{ profile.religious }}</p></div>
            <div><label>Family Oriented:</label><p>{{ profile.family_oriented }}</p></div>
          </div>
        </section>
      </div>

      
      <section class="favourites-section">
        <h2>Favourite Users</h2>
        <ul>
          <li v-for="favourite in load_fav" :key="favourite.id">
            <router-link :to="`/profiles/${favourite.fav_profile_id}`" class="favourite-link">
              {{ favourite.user_name }}
            </router-link>
          </li>
        </ul>
      </section>
    </div>
  </div>
</template>

<style scoped>
.profile-bg {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem 1rem;
}

.profile-card {
  background: #fff;
  border-radius: 2rem;
  max-width: 900px;
  width: 100%;
  box-shadow: 0 12px 36px rgba(138, 0, 71, 0.12), 0 1.5px 6px rgba(0,0,0,0.04);
  padding: 2.5rem 2rem 2rem 2rem;
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
  animation: fadeIn 0.8s cubic-bezier(.68,-0.55,.27,1.55);
}

.profile-topbar {
  display: flex;
  align-items: center;
  gap: 2.5rem;
  margin-bottom: 1.2rem;
  justify-content: flex-start;
}

.profile-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  border: 5px solid #AD2874;
  box-shadow: 0 4px 18px rgba(138,0,71,0.10);
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F7E1E9;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: 700;
  color: #fff;
  background: linear-gradient(135deg, #AD2874 40%, #8A0047 100%);
}

.profile-name-button {
  display: flex;
  flex-direction: row;
  gap: 0.1rem;
  align-items: center;
  margin-bottom: 0.9rem;
}


.profile-name-btns h1 {
  font-size: 2.2rem;
  font-weight: 700;
  color: #8A0047;
  margin: 0;
  letter-spacing: 1px;
}

.profile-btn-row {
  display: flex;
  flex-direction: row;
  gap: 1.1rem;
  align-items: center;
}

.btn-fav {
  background: none;
  border: none;
  outline: none;
  cursor: pointer;
  transition: transform 0.15s;
  width: 50px;
}

.btn-fav:hover {
  transform: scale(1.12);
}

.heart-icon {
  font-size: 2rem;
  color: #AD2874;
  transition: color 0.3s;
}
.heart-icon.favourited {
  color: #e6397e;
}

.btn {
  padding: 0.65rem 1.5rem;
  border-radius: 0.7rem;
  font-weight: 600;
  font-size: 1.05rem;
  cursor: pointer;
  border: none;
  transition: background 0.3s, color 0.3s;
  box-shadow: 0 2px 8px rgba(138,0,71,0.07);
}

.btn-secondary {
  background: #8A0047;
  color: #fff;
}
.btn-secondary:hover {
  background: #AD2874;
  color: #fff;
}

.profile-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 2rem;
  margin-bottom: 2rem;
}

.grid-about {
  grid-column: 1 / 2;
  grid-row: 1 / 2;
}
.grid-appearance {
  grid-column: 2 / 3;
  grid-row: 1 / 2;
}
.grid-preferences {
  grid-column: 1 / 2;
  grid-row: 2 / 3;
}
.grid-values {
  grid-column: 2 / 3;
  grid-row: 2 / 3;
}

section {
  background: #F7E1E9;
  border-radius: 1.2rem;
  box-shadow: 0 2px 12px rgba(138,0,71,0.04);
  padding: 1.5rem 1.2rem;
}

.about-section h2,
.preferences-section h2,
.values-section h2,
.appearance-section h2,
.favourites-section h2 {
  color: #8A0047;
  margin-bottom: 0.7rem;
  font-weight: 700;
}

.about-list > div,
.preferences-list > div,
.values-list > div,
.appearance-list > div {
  display: flex;
  align-items: flex-start;
  margin-bottom: 0.4rem;
}

label {
  min-width: 140px;
  font-weight: 600;
  color: #8A0047;
  margin-right: 0.6rem;
  text-align: left;
}

p {
  margin: 0;
  color: #333;
  font-size: 1rem;
  line-height: 1.5;
}

.favourites-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  margin-top: 1.5rem;
  background: #F7E1E9;
  border-radius: 1.2rem;
  box-shadow: 0 2px 12px rgba(138,0,71,0.04);
  padding: 1.5rem 1.2rem;
  max-width: 500px;
}

.favourites-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  justify-content: center;
}

.favourite-link {
  background: linear-gradient(90deg, #AD2874 0%, #8A0047 100%);
  color: #fff;
  padding: 0.45rem 1.1rem;
  border-radius: 0.7rem;
  font-weight: 500;
  text-decoration: none;
  transition: background 0.2s;
  box-shadow: 0 1px 4px rgba(138,0,71,0.08);
}

.favourite-link:hover {
  background: linear-gradient(90deg, #8A0047 0%, #AD2874 100%);
  color: #fff;
}

.success-message,
.error-message {
  position: fixed;
  top: 130px;
  right: 130px;
  padding: 1rem 1.5rem;
  border-radius: 0.7rem;
  font-weight: 500;
  z-index: 1000;
  animation: fadeOut 2s forwards;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-align: left;
}

.success-message {
  background-color: #D6F0F9;
  color: #0C4A6E;
}
.error-message {
  background-color: #F7D6DA;
  color: #8A0047;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
