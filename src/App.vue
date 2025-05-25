<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'

const authStore = useAuthStore();
authStore.restoreAuth();

onMounted(() => {
  authStore.restoreAuth();
});
const isAuthenticated = authStore.isAuthenticated;


</script>

<template>
  <div class="wrapper">
  <AppHeader :is-authenticated="isAuthenticated" />
  <main class="main-content">
    <RouterView v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </RouterView>
  </main>
  <AppFooter />
</div>
</template>

<style scoped>
html, body {
    height: 100%;
    margin: 0;
}

body, [class$="-bg"] {
    background-image: url('/src/assets/backgroundpic.webp');
    background-repeat: no-repeat;
    background-size: cover;      
    background-position: center; 
    background-attachment: fixed;
    font-family: 'Poppins', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    min-height: 100vh;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background-color: #f7e1e9;
  }

.wrapper {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.main-content {
  flex: 1;
  padding-top: 55px;
  background-color: white;
  margin-bottom: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>