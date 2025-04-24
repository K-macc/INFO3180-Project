<script setup>
import { useRouter } from 'vue-router';
import { onMounted, ref } from 'vue';
import { useAuthStore } from '@/stores/auth.js';

const router = useRouter();
const success_message = ref('');
const errors = ref([]);
const csrf_token = ref('');
const authStore = useAuthStore();



function getCsrfToken() {
    return new Promise((resolve, reject) => {
        fetch('/api/v1/csrf-token')
            .then((response) => response.json())
            .then((data) => {
                csrf_token.value = data.csrf_token;
                resolve();  // Resolve when token is successfully fetched
            })
            .catch((error) => {
                console.error("Error: ", error);
                reject(error);  // Reject if there is an error
            });
    });
}



const logoutUser = async () => {
    success_message.value = '';
    errors.value = [];
    
    if (!csrf_token.value) {
        console.error('CSRF Token is not available');
        return;
    }

    await fetch('/api/auth/logout', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'X-CSRF-Token': csrf_token.value, // Send CSRF token in header
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            success_message.value = data.message;
            authStore.setFlashMessage(success_message.value);
            authStore.logout(); 
            router.push('/'); // Redirect to login page after logout
        } else {
            errors.value = data.errors;
        }
    })
    .catch(error => {
        console.error('Error during logout:', error);
        errors.value.push('An error occurred during logout.');
    });
}


onMounted(async () => {
    try {
        // First, wait for CSRF token to be fetched before logging out
        await getCsrfToken();  // Wait for CSRF token to be fetched
        await logoutUser();     // Now perform the logout after CSRF token is set
    } catch (error) {
        console.error('Error:', error);
    }
});
</script>

<template>
  <div class="logout-message">
    <transition name="fade">
      <div v-if="success_message" class="success-message">
        {{ success_message }}
      </div>
    </transition>

    <transition name="fade">
      <div v-if="errors.length > 0" class="error-message">
        <ul>
          <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
        </ul>
      </div>
    </transition>
  </div>
</template>
