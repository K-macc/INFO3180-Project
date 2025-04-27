<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const name = ref('');
const email = ref('');
const router = useRouter();
const errorMessage = ref([]);
const successMessage = ref('');
const csrf_token = ref("");
const photo = ref(null);

const handleFileChange = (event) => {
    photo.value = event.target.files[0];
};

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
 
function register() {
  const registrationForm = document.getElementById('registrationForm');
  const form_data = new FormData(registrationForm);
  successMessage.value = '';
  errorMessage.value = [];


  fetch('/api/register', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'X-CSRFToken': csrf_token.value
    },
    body: form_data
  })
  .then(response => response.json())
  .then(data => {
    if (data.errors) {
      errorMessage.value = data.errors;
      flashMessage(errorMessage);
    } else if (data.error) {
      errorMessage.value.push(data.error);
      flashMessage(errorMessage);
    } else {
      successMessage.value = data.message;
      registrationForm.reset();
      flashMessage(successMessage);
      setTimeout(() => {
        router.push('/profiles/new');
      }, 5000);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    errorMessage.value.push('An error occurred during registration.');
    flashMessage(errorMessage);
  });
     
}
</script>


<template>
  <div>
    <h1>Register</h1>

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


    <form @submit.prevent="register" id="registrationForm" enctype="multipart/form-data">
      <div>
        <label>Username:</label>
        <input v-model="username" type="text" name="username" class="form-control">
      </div>
      <div>
        <label>Password:</label>
        <input v-model="password" type="password" name="password" class="form-control">
      </div>
      <div>
        <label>Name:</label>
        <input v-model="name" type="text" name="name" class="form-control">
      </div>
      <div>
        <label>Email:</label>
        <input v-model="email" type="email" name="email" class="form-control">
      </div>
      <input id="photo" name="photo" type="file" @change="handleFileChange" ref="fileInput" accept="image/png, image/jpeg"  class="form-control"/>
      <button type="submit">Register</button>
    </form>
    <p>Already have an account? <router-link to="/login">Login here</router-link></p>
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
  
