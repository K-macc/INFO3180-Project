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
};
</script>

<template>
  <div class="login-container">
    <h1 class="brand-title">Jam-Date</h1>

    <div class="login-card">
      <h2 class="card-title">Welcome Back</h2>

      <form @submit.prevent="login" class="form" id="loginForm" enctype="multipart/form-data">
        <input v-model="username" type="text" placeholder="Username" name="username" class="input"/>
        <input v-model="password" type="password" placeholder="Password" name="password" class="input"/>

        <button type="submit" class="btn-primary">Login</button>
      </form>

      <transition name="fade">
        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>
      </transition>

      <transition name="fade">
      <div v-if="errorMessage.length" class="error-message">
        <ul>
          <li v-for="(error, index) in errorMessage" :key="index">{{ error }}</li>
        </ul>
      </div>
    </transition>
      

      <div class="link-group">
        <router-link to="/register" class="link">Register</router-link>
        <router-link to="/view-reports" class="link">View Reports</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  background: linear-gradient(to right, #478bda, #4364f7);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.brand-title {
  font-size: 3rem;
  font-weight: 700;
  color: white;
  margin-bottom: 1rem;
}

.login-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 90%;
  max-width: 350px;
  text-align: center;
}

.card-title {
  font-size: 1.5rem;
  margin-bottom: 1.2rem;
  color: #333;
}

.form {
  display: flex;
  flex-direction: column;
}

.input {
  padding: 12px;
  margin-bottom: 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
  transition: border 0.2s;
}

.input:focus {
  outline: none;
  border-color: #007bff;
}

.btn-primary {
  padding: 12px;
  background-color: #007bff;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.success-message {
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

.error-message {
  color: red;
  background-color: #f8d7da;
  padding: 10px;
  padding-top: 20px;
  padding-left: 0px;
  margin-bottom: 10px;
  border-radius: 5px;
  top: 70px;
  right: 45px;
  position: fixed;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 26%;
  min-height: 8%;
  height: auto;
}

.fade-leave-active {
  transition: opacity 1s ease-in-out;
}

.fade-leave-to {
  opacity: 0;
}

.link-group {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
}

.link {
  color: #007bff;
  text-decoration: none;
  font-size: 0.9rem;
}

.link:hover {
  text-decoration: underline;
}
</style>
