<template>
  <div> 
    <div v-if="flashMessage">
      <transition name="fade">
        <div class="flash-message">
          {{ flashMessage }}
        </div>
      </transition>
    </div>

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
          <div class="center-title">
            <h1 class="title-text">
              Jam Date <span role="img" aria-label="heart">💖</span>
            </h1>
            <p class="caption">Where hearts meet for a lifetime</p>
          </div>
          <div class="right-buttons">
            <router-link to="/login" class="btn btn-outline-light me-2">Login</router-link>
            <router-link to="/register" class="btn btn-outline-light me-2">Register</router-link>
            <router-link to="/view-reports" class="btn btn-outline-light">View Reports</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import profile1 from "@/assets/homepic1.jpg"
import profile2 from "@/assets/homepic2.jpg"
import profile3 from "@/assets/homepic3.jpg"
import profile4 from "@/assets/homepic4.jpg"
import profile5 from "@/assets/homepic5.jpg"
import profile6 from "@/assets/homepic6.jpg"
import profile7 from "@/assets/homepic7.jpg"
import profile8 from "@/assets/homepic8.jpg"
import profile9 from "@/assets/homepic9.jpg"

const authStore = useAuthStore()

const flashMessage = ref(authStore.flashMessage)

const form = ref({
  name: '',
  email: '',
  password: '',
})

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
]

const registerUser = () => {
  console.log("Registering:", form.value)
  // TODO: Add your API call
}

onMounted(() => {
  setTimeout(() => {
    flashMessage.value = ''
  }, 3000)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');


.flash-message {
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

  .fade-leave-active {
    transition: opacity 1s ease-in-out;
  }

  .fade-leave-to {
    opacity: 0;
  }

.home-wrapper {
  height: 100%;
  margin: 0;
  background-color: yellow;
}

.home-wrapper {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(3, 33.33%); /* 3 columns for the images */
  grid-template-rows: repeat(3, 33.33vh); /* Each image takes up 1/3 of the viewport height */
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
}

.left-title h1 {
  font-family: 'Pacifico', cursive;
  font-size: 2.5rem;
  color: white;
  text-shadow: 2px 2px 5px #000;
}

.right-buttons {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.right-buttons button {
  font-family: 'Montserrat', sans-serif;
  font-size: 1rem;
  color: white;
}

.center-card {
  height: 100%;
}

.btn:hover {
  background-color: rgb(173, 22, 47);
  color: white;
  font-weight: 5px;
}

.center-title {
  margin: 60px auto;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  z-index: 5; /* Ensure it's above the background */
}

.center-title h1 {
  font-family: 'Pacifico', cursive;
  font-size: 3rem;
  color: white;
  text-shadow: 2px 2px 5px #000;
}

.center-title .caption {
  font-family: 'Montserrat', sans-serif;
  font-size: 1rem;
  color: white;
  margin-top: 10px;
  font-style: italic;
}

.register-card {
  width: 100%;
  max-width: 400px;
  border-radius: 12px;
}
</style>
