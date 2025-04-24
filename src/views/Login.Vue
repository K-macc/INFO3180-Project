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


function flashMessage(prompt){
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
            console.error("Error: ",error);
        });
}

onMounted(() => {
    getCsrfToken();
});

function login () {
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
      successMessage.value = data.message;
      username.value = '';
      password.value = '';
      authStore.setFlashMessage('');
      authStore.login(form_data,token.value)
      flashMessage(successMessage);
      setTimeout(() => {
        router.push('/');
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
    <div>
      <h1>Login</h1>

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


      <form @submit.prevent="login" id="loginForm" enctype="multipart/form-data">
        <div>
          <label>Username:</label>
          <input v-model="username" type="text" name="username">
        </div>
        <div>
          <label>Password:</label>
          <input v-model="password" type="password" name="password">
        </div>
        <button type="submit">Login</button>
      </form>
      <p>Don't have an account? <router-link to="/register">Register here</router-link></p>
    </div>
</template>


<style scoped>
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
</style>