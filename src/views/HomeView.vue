<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.js';
import profile1 from '@/assets/homepic1.jpg';
import profile2 from '@/assets/homepic2.jpg';
import profile3 from '@/assets/homepic3.jpg';
import profile4 from '@/assets/homepic4.jpg';
import profile5 from '@/assets/homepic5.jpg';
import profile6 from '@/assets/homepic6.jpg';
import profile7 from '@/assets/homepic7.jpg';
import profile8 from '@/assets/homepic8.jpg';
import profile9 from '@/assets/homepic9.jpg';

const authStore = useAuthStore();
const flashMessageText = ref('');
flashMessageText.value = authStore.flashMessage;

const profiles = [
  { image: profile1 },
  { image: profile2 },
  { image: profile3 },
  { image: profile4 },
  { image: profile5 },
  { image: profile6 },
  { image: profile7 },
  { image: profile8 },
  { image: profile9 },
];

setTimeout(() => {
  flashMessageText.value = '';
}, 3000);
</script>

<template>
  <div>
      <transition name="fade">
        <div v-if="flashMessageText" class="flash-message">
          {{ flashMessageText }}
        </div>
      </transition>

    <div class="home-wrapper">
      <!-- Background image grid -->
      <div class="image-grid">
        <div
          v-for="(profile, index) in profiles"
          :key="index"
          class="bg-image"
          :style="{ backgroundImage: `url(${profile.image})` }"
        ></div>
      </div>

      <!-- Overlay elements -->
      <div class="overlay">
        <!-- Top navbar with buttons on the right -->
        <div class="top-bar">
          <div class="left-title">
            <h1 class="title-text">
              Jam Date <span role="img" aria-label="heart">💖</span>
            </h1>
          </div>
          <div class="center-wrapper">
            <div class="card">
              <div class="center-title">
                <h1 class="title-text">
                  Jamaica's 1st dating site<span role="img" aria-label="heart">💖</span>
                </h1>
                <p class="caption">Where hearts meet for a lifetime</p>
                <p class="caption">From profile matching to suit matching</p>
                <p class="caption">Find your loved one right here!</p>
              </div>
            </div>
          </div>
          <div class="right-buttons">
            <router-link
              to="/login"
              class="btn btn-primary me-2 d-flex align-items-center justify-content-center "
              :style="{ height: '50px', width: '90px' }"
              >Login</router-link
            >
            <router-link
              to="/register"
              class="btn btn-primary me-2 d-flex align-items-center justify-content-center"
              :style="{ height: '50px', width: '90px' }"
              >Register</router-link
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');

.image-grid {
  opacity: calc(0.5 + 0.5 * var(--opacity));
  transition: opacity 0.5s ease-in-out;
}

.flash-message {
  background-color: #D6F0F9;
  color: #0C4A6E;
  padding: 10px;
  border-radius: 5px;
  width: 20%;
  top: 100px;
  right: 45px;
  text-align: center;
  position: fixed;
  z-index: 1000;
  font-weight: 600;
}

.flash-message::before {
  content: '✔';
  color: #065f46;
  font-weight: bold;
  font-size: 1.2rem;
  margin-right: 6px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.center-title {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  z-index: 2;
  font-size: 18px;
  width: 100%;
}

.center-title h1 {
  font-family: 'Pacifico', cursive;
  font-size: 3rem;
  color: white;
  text-shadow: 2px 2px 5px #000;
}

.center-title .caption {
  font-family: 'Pacifico', cursive;
  font-size: 2rem;
  color: white;
  text-shadow: 2px 2px 5px #000;
}

.center-wrapper {
  position: absolute;
  top: 380%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
  width: 90%;
  max-width: 800px;
}

.card {
  background-color: rgba(173, 40, 116, 0.85);
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  text-align: center;
  width: 100%;
  min-height: 300px;
}

.home-wrapper {
  height: 100%;
  margin-top: 10px;
  background-color: white;
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(3, 33.33%);
  grid-template-rows: repeat(3, 33.33vh);
  width: 100%;
  height: 100%;
}

.bg-image {
  background-size: cover;
  background-position: center;
  filter: brightness(0.4);
  width: 100%;
  height: 100%;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.top-bar {
  position: absolute;
  top: 0;
  width: 100%;
  z-index: 10;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left-title h1 {
  font-family: 'Pacifico', cursive;
  font-size: 2.5rem;
  color: white;
  text-shadow: 2px 2px 5px #000;
}

.right-buttons {
  display: flex;
  gap: 10px;
}


.register-card {
  width: 100%;
  max-width: 400px;
  border-radius: 12px;
}
</style>
