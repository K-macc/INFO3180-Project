<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js';

const authStore = useAuthStore();

const flashMessage = ref('');

flashMessage.value = authStore.flashMessage;


setTimeout(() => {
  flashMessage.value = '';
}, 3000);
</script>

<template>
  <div>
    <transition name="fade">
      <div v-if="flashMessage" class="flash-message">
        {{ flashMessage }}
      </div>
    </transition>


    <h1>Welcome to Jam-Date</h1>


    <nav>
      <router-link to="/login">Login</router-link> |
      <router-link to="/register">Register</router-link>
    </nav>
    <!-- Will display latest profiles later -->
  </div>
</template>

<style scoped>
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
</style>