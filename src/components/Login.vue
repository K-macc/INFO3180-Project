<template>
  <div class="login-container">
    <h1 class="brand-title">Jam-Date</h1>
    <transition name="fade">
        <div v-if="successMessage" class="message success">
          {{ successMessage }}
        </div>
      </transition>

      <transition name="fade">
        <div v-if="errorMessage.length" class="message error">
          <ul>
            <li v-for="(error, index) in errorMessage" :key="index">{{ error }}</li>
          </ul>
        </div>
      </transition>

    <div class="login-card">

      <h2 class="card-title">Welcome Back 👋</h2>

      <form @submit.prevent="login" class="form" id="loginForm" enctype="multipart/form-data">
        <input v-model="username" type="text" placeholder="Username" name="username" class="input"/>
        <input v-model="password" type="password" placeholder="Password" name="password" class="input"/>
        <button type="submit" class="btn-primary">Login</button>
      </form>

      

      <div class="link-group">
        <router-link to="/register" class="link">Create an Account</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth.js';

const router = useRouter();
const username = ref('');
const password = ref('');
const errorMessage = ref([]);
const successMessage = ref('');
const token = ref('');
const csrf_token = ref("");
const authStore = useAuthStore();
const user_id = ref(null);

function flashMessage(prompt) {
  setTimeout(() => {
    if (Array.isArray(prompt)) {
      prompt.value = [];
    } else {
      prompt.value = '';
    }
  }, 2000);
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

onMounted(() => {
  getCsrfToken();
});

function login() {
  const loginForm = document.getElementById('loginForm');
  const form_data = new FormData(loginForm);
  successMessage.value = '';
  errorMessage.value = [];

  fetch('/api/auth/login', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'X-CSRFToken': csrf_token.value
    },
    body: form_data
  })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        errorMessage.value = data.error;
        flashMessage(errorMessage);
      } else {
        token.value = data.token;
        user_id.value = data.id;
        successMessage.value = data.message;
        loginForm.reset();
        authStore.setFlashMessage('');
        authStore.login(form_data, token.value, user_id.value);
        flashMessage(successMessage);
        setTimeout(() => {
          router.push('/users');
        }, 5000);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      errorMessage.value.push('An error occurred. Please try again.');
      flashMessage(errorMessage);
    });
}
</script>

<style scoped>
.login-container {
  background: linear-gradient(120deg, #8A0047, #AD2874);
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  padding: 1rem;
}

.brand-title {
  font-size: 2.5rem;
  color: #fff;
  margin-bottom: 1rem;
  font-weight: bold;
}

.login-card {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  text-align: center;
  position: relative;
}

.card-title {
  font-size: 1.75rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input {
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
  font-size: 1rem;
  transition: border 0.3s ease;
}

.input:focus {
  border-color: #007bff;
  outline: none;
}

.btn-primary {
  padding: 12px;
  background-color: #007bff;
  color: #fff;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(105, 0, 61, 0.3);
}

.message {
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.95rem;
  text-align: left;
  top: 250px;
  right: 450px;
  position: absolute;
  z-index: 10;
}

.success {
  background-color: #d1e7dd;
  color: #0f5132;
}

.error {
  background-color: #f8d7da;
  color: #842029;
}

.link-group {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}

.link {
  font-size: 0.9rem;
  color: #007bff;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
