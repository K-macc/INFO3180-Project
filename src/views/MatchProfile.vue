<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const matches = ref([]);
const profileID = authStore.profile_id;
const success_message = ref('');
const error_message = ref('');

function flashMessage(prompt) {
  setTimeout(() => {
    if (Array.isArray(prompt)) {
      prompt.value = [];
    } else {
      prompt.value = '';
    }
  }, 3000);
}

function trackProfileView(profileID) {
  authStore.setProfileId(profileID);
}

function matchProfile() {
  fetch(`/api/profiles/matches/${profileID}`, {
    method: 'GET',
    headers: {
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
        matches.value = data.matches;
        success_message.value = data.message;
        flashMessage(success_message);
      }
    })
    .catch(error => {
      console.error('Error matching profile:', error);
      error_message.value = 'Failed to fetch matches.';
      flashMessage(error_message);
    });
}

onMounted(() => {
  matchProfile();
});
</script>

<template>
  <div class="container-bg">
    <transition name="fade">
      <div v-if="error_message" class="alert error-message" role="alert" aria-live="assertive">
        {{ error_message }}
      </div>
    </transition>

    <transition name="fade">
      <div v-if="success_message" class="alert success-message" role="alert" aria-live="polite">
        {{ success_message }}
      </div>
    </transition>

    <h1 class="page-title">Match Report</h1>

    <h2 v-if="matches.length" class="matches-subtitle">Users matched to your profile:</h2>
    <h2 v-else class="matches-subtitle">No matches found at this time.</h2>

    <section class="match-results-container" v-if="matches.length">
      <article v-for="match in matches" :key="match.id" class="match-card" tabindex="0" aria-label="Matched user profile">
        <div class="profile-avatar">
          <img v-if="match.photo" :src="match.photo" alt="Profile Picture" />
          <div v-else class="avatar-placeholder">
            {{ match.user_name?.charAt(0).toUpperCase() }}
          </div>
        </div>
        <header class="match-header">
          <h3 class="match-name">{{ match.user_name }}</h3>
          <span class="match-sex">{{ match.sex }}</span>
        </header>

        <p class="match-description" v-if="match.description">{{ match.description }}</p>

        <ul class="match-details">
          <li><strong>Parish:</strong> {{ match.parish }}</li>
          <li v-if="match.fav_cuisine"><strong>Favourite Cuisine:</strong> {{ match.fav_cuisine }}</li>
          <li v-if="match.fav_colour"><strong>Favourite Colour:</strong> {{ match.fav_colour }}</li>
        </ul>

        <router-link
          class="btn btn-primary"
          :to="`/profiles/${match.id}`"
          @click="trackProfileView(match.id)"
          aria-label="View more details about this matched user"
        >
          View More Details
        </router-link>
      </article>
    </section>
  </div>
</template>

<style scoped>
.container-bg {
  padding: 2rem 1rem 4rem;
  min-height: 100vh;
  margin: 0 auto;
  box-sizing: border-box;
}

.page-title {
  font-size: 2.8rem;
  font-weight: 700;
  color: #f7d4e6;
  text-shadow: 2px 2px #AD2874;
  text-align: center;
  margin-bottom: 1rem;
  letter-spacing: 1.2px;
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
  justify-self: center;
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

.matches-subtitle {
  font-size: 1.5rem;
  font-weight: 600;
  color: #f7d4e6;
  text-shadow: 2px 2px #AD2874;
  text-align: center;
  margin-bottom: 2rem;
}

.match-results-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-top: 1rem;
  margin-bottom: 6rem;
}

.match-card {
  background-color: #fff;
  border-radius: 16px;
  padding: 1.8rem 1.5rem;
  box-shadow: 0 6px 18px rgba(138, 0, 71, 0.12);
  border: 1px solid #ad2874;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  outline-offset: 4px;
  width: 450px;
}

.match-card:focus,
.match-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 30px rgba(0, 200, 255, 0.3);
  border-color: #00c8ff;
  cursor: pointer;
}

.match-header {
  display: flex;
  justify-content: space-between;
  flex-direction: column;
  align-items: center;
  margin-top: 0.8rem;
  margin-bottom: 0.8rem;
  gap: 1rem;
  width: 100%;
}

.match-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: #69003d;
  margin: 0;
}

.match-sex {
  font-size: 1.1rem;
  font-weight: 600;
  color: #00c8ff;
  background: #e0f7ff;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
}

.match-description {
  color: #333333;
  font-size: 1rem;
  margin-bottom: 1rem;
  line-height: 1.4;
}

.match-details {
  list-style: none;
  padding: 0;
  margin: 0 0 1.5rem 0;
  color: #555555;
  font-size: 0.95rem;
}

.match-details li {
  margin-bottom: 0.3rem;
}

.btn {
    padding: 0.75rem 2rem;
    border-radius: 0.7rem;
    font-weight: 600;
    font-size: 1.1rem;
    cursor: pointer;
    border: none;
    background: #ad2874;
    color: #fff;
    transition: background 0.3s, color 0.3s;
    box-shadow: 0 2px 8px rgba(138, 0, 71, 0.07);
}

.btn:hover {
    background-color: #69003D;
    transform: translateY(-2px);
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
