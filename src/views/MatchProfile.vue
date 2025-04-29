<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const matches = ref([]);
const profileID = authStore.profile_id;
const success_message = ref('');
const error_message = ref('');

function flashMessage(prompt) {
    setTimeout(() => {
        if (Array.isArray(prompt)) {
            prompt.value = [];
        } else {
            prompt.value = '';
        }
    }, 2000);
}

function trackProfileView(profileID) {
    authStore.setProfileId(profileID);
}

function matchProfile() {
    fetch(`/api/profiles/matches/${profileID}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authStore.token}`
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                error_message.value = data.error;
                flashMessage(error_message);
            } else {
                matches.value = data.matches;
                success_message.value = data.message;
                flashMessage(success_message);
            }
        })
        .catch(error => {
            console.error('Error matching profile:', error);
        });
}

onMounted(() => {
    matchProfile();
})
</script>

<template>
    <div>
        <transition name="fade">
            <div v-if="success_message || error_message" :class="success_message ? 'success-message' : 'error-message'">
                {{ success_message || error_message }}
            </div>
        </transition>

        <h1>Match Report</h1>

        <h5>Matches found to your profile:</h5>

        <div class="match-results" v-for="match in matches" :key="match.id">
            <h3>{{ match.sex }}</h3>
            <p>{{ match.description }}</p>
            <router-link class="btn btn-primary" :to="`/profiles/${match.id}`" @click="trackProfileView(match.id)">View
                more details</router-link>
        </div>
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

.match-results{
    width: 300px;
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid #ccc;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
}

.match-results:hover {
    background: white;
    transform: scale(1.05);
    box-shadow: 0px 0px 10px rgb(146, 144, 144);
    border-color: #817e7e96;
}
</style>