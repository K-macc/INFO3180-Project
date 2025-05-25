<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import loginpic from '@/assets/registerpic.jpg';

const username = ref('');
const password = ref('');
const name = ref('');
const email = ref('');
const router = useRouter();
const errorMessage = ref([]);
const successMessage = ref('');
const csrf_token = ref("");
const photo = ref(null);
const bgphoto = [{ image: loginpic }]

const handleFileChange = (event) => {
  photo.value = event.target.files[0];
};

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
  <div class="register-container" :style="{
    backgroundImage: `url(${bgphoto[0].image})`,
    backgroundRepeat: 'no-repeat',
    backgroundSize: 'cover',
    backgroundPosition: 'center center'
  }">
    

    <h1 class="title">Jam-Date</h1>

    <transition name="fade">
      <div v-if="successMessage" class="alert success-message">
        {{ successMessage }}
      </div>
    </transition>

    <transition name="fade">
      <div v-if="errorMessage.length" class="alert error-message">
        <ul>
          <li v-for="(error, index) in errorMessage" :key="index">{{ error }}</li>
        </ul>
      </div>
    </transition>

    <div class="register-card">
      <form @submit.prevent="register" id="registrationForm" enctype="multipart/form-data">
        <input v-model="username" type="text" name="username" placeholder="Username" class="input-field" />
        <input v-model="password" type="password" name="password" placeholder="Password" class="input-field" />
        <input v-model="name" type="text" name="name" placeholder="Full Name" class="input-field" />
        <input v-model="email" type="email" name="email" placeholder="Email Address" class="input-field" />

        <label for="photo" class="upload-label">Upload Profile Picture</label>
        <input id="photo" name="photo" type="file" @change="handleFileChange" accept="image/png, image/jpeg"
          class="input-field" />

        <button type="submit" class="submit-btn">Register</button>
      </form>

      <p class="link-group">
        Already have an account?
        <router-link to="/login" class="link">Login here</router-link>
      </p>
    </div>
  </div>
</template>


<style scoped>
.register-container {
  background: linear-gradient(135deg, #8A0047, #AD2874);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #444;
  margin-bottom: 1rem;
}

.register-card {
  background: #ffffff;
  backdrop-filter: blur(10px);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 450px;
  text-align: center;
  position: relative;
}

.input-field {
  width: 100%;
  padding: 0.75rem 1rem;
  margin: 0.75rem 0;
  border-radius: 0.75rem;
  border: 1px solid #ddd;
  background-color: #e7e5e5f3;
  font-size: 1rem;
  transition: all 0.25s ease;
  box-shadow: inset 0 0 0 2px transparent;
}

.input-field:focus {
  border-color: #007bff;
  outline: none;
}

.input-field::placeholder {
  color: #aaa;
  font-weight: 500;
}

.upload-label {
  display: block;
  margin-top: 1rem;
  font-weight: 600;
  color: #444;
  text-align: left;
  font-size: 0.95rem;
}

.submit-btn {
  width: 60%;
  padding: 0.75rem;
  margin-top: 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  background-color: #007bff;
  border: none;
  border-radius: 0.75rem;
  color: #fff;
  cursor: pointer;
  display: flex;
  justify-self: center;
  justify-content: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.submit-btn:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(105, 0, 61, 0.3);
}

.link-group {
  font-size: 0.95rem;
  justify-content: center;
  margin-top: 1.5rem;
  font-weight: 500;
}

.link {
  color: #007bff;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}


.success-message {
  position: fixed;
  top: 150px;
  right: 300px;
  z-index: 9999;
  padding: 1rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 500;
  font-size: 1rem;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 300px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-align: left;
}

.error-message {
  position: fixed;
  top: 100px;
  right: 100px;
  z-index: 9999;
  padding: 1rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 500;
  font-size: 1rem;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 550px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-align: left;
}

.error-message * {
  margin: 0;
}

.success-message {
  background-color: #d1fae5;
  color: #0C4A6E;
}

.error-message {
  background-color: #fee2e2;
  color: #991b1b;
}

.fade-leave-active {
  transition: opacity 1s ease-in-out;
}

.fade-leave-to {
  opacity: 0;
}
</style>
