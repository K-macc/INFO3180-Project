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
    console.log(data.value);
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
  <div class="register-container">
    <!-- Header -->
    <h1 class="title">Jam-Date 💖</h1>

    <!-- Success Message -->
    <transition name="fade">
      <div v-if="successMessage" class="alert success-message">
        {{ successMessage }}
      </div>
    </transition>

    <!-- Error Messages -->
    <transition name="fade">
      <div v-if="errorMessage.length" class="alert error-message">
        <ul>
          <li v-for="(error, index) in errorMessage" :key="index">{{ error }}</li>
        </ul>
      </div>
    </transition>

    <!-- Registration Form -->
    <div class="form-container">
      <form @submit.prevent="register" id="registrationForm" enctype="multipart/form-data">
        <input v-model="username" type="text" name="username" placeholder="Username" class="input-field"/>
        <input v-model="password" type="password" name="password" placeholder="Password" class="input-field" />
        <input v-model="name" type="text" name="name" placeholder="Full Name" class="input-field"/>
        <input v-model="email" type="email" name="email" placeholder="Email Address" class="input-field" />

        <label for="photo" class="upload-label">Upload Profile Picture</label>
        <input id="photo" name="photo" type="file" @change="handleFileChange" accept="image/png, image/jpeg" class="input-field" />

        <button type="submit" class="submit-btn">Register</button>
      </form>

      <p class="switch-auth">
        Already have an account?
        <router-link to="/login" class="link">Login here</router-link>
      </p>
    </div>
  </div>
</template>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Ancizar+Sans:ital,wght@0,100..1000;1,100..1000&family=Poetsen+One&display=swap');
/* Page Background */
.register-container {
  background: linear-gradient(120deg, #8A0047, #AD2874);
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.register-container::before {
  content: "";
  position: absolute;
  width: 200%;
  height: 100vh;
  background: radial-gradient(circle, rgba(173,216,230, 0.2) 20%, transparent 70%);
  animation: ripple 10s infinite linear;
  top: -50%;
  left: -50%;
  z-index: 0;
}

@keyframes ripple {
  0% {
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: scale(1.2) rotate(360deg);
    opacity: 0.7;
  }
}

/* Form Container */
.form-container {
  position: relative; /* same */
  z-index: 5; /* match login-card z-index */
  color: #69003D; /* Tyrian Purple for text */
  padding: 2rem; /* match padding scale */
  border-radius: 16px; /* match login-card rounding */
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 350px;
  background: #F7E1E9; /* Lavender Blush background */
  box-shadow: 0 10px 25px rgba(105, 0, 61, 0.15); /* subtle Tyrian Purple shadow */
  font-family: 'Montserrat', sans-serif;
}

.title {
  position: relative; /* Add this */
  z-index: 2; /* Add this */
  font-size: 40px;
  font-weight: bold;
  color: #FFFFFF;
  margin-bottom: 20px;
  text-align: center;
}


/* Input Fields */
.input-field {
  background-color: #fff; /* white inputs for clean contrast */
  width: 100%;
  padding: 12px 14px; /* slightly more padding */
  margin: 10px 0;
  border: 2px solid #69003D; /* stronger Tyrian Purple border */
  border-radius: 8px; /* softer corners */
  font-size: 16px;
  color: #333333;
  font-family: 'Montserrat', sans-serif;
  transition: border-color 0.3s ease;
}

.input-field:focus {
  border-color: #00C8FF; /* Vivid Sky Blue on focus */
  outline: none;
  box-shadow: 0 0 6px #00C8FFaa;
}

::placeholder {
  color: #69003D;
}

.link {
  color: #333333; /* Fandango */
  text-decoration: underline;
  font-size: 18px;
}

.link:hover {
  color: #00C8FF; /* Darker tone for hover */
  font-size: 18px;
}

/* Submit Button */
.submit-btn {
  background-color: #00C8FF; /* sky blue */
  color: white;
  border: none;
  padding: 10px;
  width: 100%;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
}

.submit-btn:hover {
  background-color: #69003D; /* Darker tone for hover */
}

.switch-auth {
  margin-top: 20px;
  font-size: 18px;
  font-weight: bold;
  color: #333333; /* white */
}

/* Upload Label */
.upload-label {
  font-size: 18px;
  font-weight: bold;
  color: #333333;
  margin-top: 10px;
}

/* Success Message */
.success-message {
  color: #333333;
  background-color: #d4edda;
  padding: 10px;
  border-radius: 5px;
  width: 15%;
  top: 100px;
  right: 45px;
  text-align: center;
  position: fixed;
}

/* Error Message */
.error-message {
  color: #69003D;
  background-color: #f8d7da;
  padding: 10px 10px 10px 0;
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

/* Fade Transition */
.fade-leave-active {
  transition: opacity 1s ease-in-out;
}

.fade-leave-to {
  opacity: 0;
}
</style>


