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
    <h1 class="title">Jam-Date</h1>

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
  /* Page Background */
  .register-container {
    background-color: #8648d6; /* Light blue background */
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
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

  /* Title Styling */
  .title {
    font-size: 40px;
    font-weight: bold;
    color: white;
    margin-bottom: 20px;
    text-align: center;
  }

  /* Form Container */
  .form-container {
    /* background-color: #99c3e9; */
    color: white;
    padding: 20px;
    border-radius: 10px;
    /*box-shadow: 0px 4px 8px rgba(6, 10, 243, 0.2);*/
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 300px;
  }

  ::placeholder {
    color: white;
  }

  /* Input Fields */
  .input-field {
    background-color: #8cbfeb;
    width: 100%;
    padding: 10px;
    margin: 8px 0;
    border: 1px solid white;
    border-radius: 5px;
    font-size: 16px;
  }

  /* Submit Button */
  .submit-btn {
    background-color: #28a745; /* Green Button */
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
    background-color: #218838;
  }
</style>
