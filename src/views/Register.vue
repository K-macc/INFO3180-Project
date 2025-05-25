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
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap');

.register-container {
  font-family: 'Montserrat', sans-serif;
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

.register-container::before {
  content: "";
  position: absolute;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.08) 20%, transparent 70%);
  animation: ripple 18s linear infinite;
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
    opacity: 0.3;
  }
}

.title {
  z-index: 2;
  font-size: 2.8rem;
  font-weight: 600;
  color: #fff;
  text-align: center;
  margin-bottom: 2rem;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
}

.form-container {
  z-index: 2;
  background: #ffffff;
  backdrop-filter: blur(10px);
  padding: 2rem;
  border-radius: 1.25rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 420px;
  transition: all 0.3s ease;
}

.input-field {
  width: 100%;
  padding: 0.75rem 1rem;
  margin: 0.75rem 0;
  border-radius: 0.75rem;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
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

.link {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.link:hover {
  text-decoration: underline;
}

.switch-auth {
  margin-top: 1.5rem;
  font-size: 0.95rem;
  font-weight: 500;
  justify-self: center;
}

.success-message,
.error-message {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  padding: 1rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 500;
  font-size: 1rem;
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
  width: 320px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-align: left;
}

.success-message::before {
  content: '✔';
  color: #065f46;
  font-weight: bold;
  font-size: 1.2rem;
}

.error-message::before {
  content: '⚠';
  color: #991b1b;
  font-weight: bold;
  font-size: 1.2rem;
}

.success-message {
  background-color: #d1fae5;
  color: #065f46;
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

/* Responsive optimization */
@media (max-width: 480px) {
  .title {
    font-size: 2rem;
  }

  .form-container {
    padding: 1.5rem;
  }
}


</style>


