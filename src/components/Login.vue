<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const successMessage = ref('');
const csrf_token = ref('');
const router = useRouter();

function flashMessage(prompt) {
  setTimeout(() => {
    if (Array.isArray(prompt)) {
      prompt.value = [];
    } else {
      prompt.value = '';
    }
  }, 3000);
}

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    })
    .catch((error) => {
      console.error("Error fetching CSRF token:", error);
    });
}

onMounted(() => {
  getCsrfToken();
});

function loginUser() {
  successMessage.value = '';
  errorMessage.value = '';

  fetch('/api/auth/login', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token.value,
    },
    body: JSON.stringify({
      username: username.value,
      password: password.value,
    }),
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
      errorMessage.value = "⚠️ Something went wrong.";
      flashMessage(errorMessage);
    });
}
</script>

<template>
  <div class="login-container">
    <h1 class="brand-title">Jam-Date</h1>

    <div class="login-card">
      <h2 class="card-title">Welcome Back</h2>

      <form @submit.prevent="loginUser" class="form">
        <input v-model="username" type="text" placeholder="Username" class="input" required/>
        <input v-model="password" type="password" placeholder="Password" class="input" required/>

        <button type="submit" class="btn-primary">Login</button>
      </form>

      <div v-if="errorMessage" class="alert error">{{ errorMessage }}</div>
      <div v-if="successMessage" class="alert success">{{ successMessage }}</div>

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

.alert {
  margin-top: 1rem;
  padding: 10px;
  border-radius: 6px;
  font-size: 0.95rem;
}

.alert.error {
  background-color: #ffe5e5;
  color: #d8000c;
}

.alert.success {
  background-color: #e1f8e6;
  color: #27632a;
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
