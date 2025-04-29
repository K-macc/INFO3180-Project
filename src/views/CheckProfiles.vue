<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js';

const authStore = useAuthStore();
const profiles = ref([]);
const userID = authStore.user_id;

function trackProfileView(profileID) {
    authStore.setProfileId(profileID);
}

function fetchProfiles() {
    fetch(`/api/users/${userID}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            return response.json();
        })
        .then(data => {
            profiles.value = data.profiles;
        })
        .catch(error => {
            console.error('Failed to parse JSON:', error);
        })

}

onMounted(() => {
    fetchProfiles();
});
</script>

<template>
    <div>
        <h1 class="title">Choose a Profile</h1>

        <div class="profile-list">
            <div v-for="profile in profiles" :key="profile.id" class="profile-item card">
                <label for="description">Description:</label>
                <p>{{ profile.description }}</p>

                <label for="sex">Sex:</label>
                <p>{{ profile.sex }}</p>

                <label for="race">Race:</label>
                <p>{{ profile.race }}</p>
                <router-link class="btn btn-primary" :to="`/profiles/update/${profile.id}`"
                    @click="trackProfileView(profile.id)">Complete this profile</router-link>
            </div>
        </div>
    </div>
</template>

<style scoped>
.title {
    text-align: center;
    margin-top: 2rem;
}

label {
    font-weight: bold;
}

.profile-list {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    width: 100%;
    gap: 2rem;
}


.profile-item.card {
    margin: 0.5rem 0 0.5rem;
    font-size: 1.1rem;
    color: #333;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    width: 500px;
    height: 300px;
    transition: all 0.3s ease-in-out;
    justify-content: space-around;
    padding: 10px 25px;
}


.profile-item.card:hover {
    background: white;
    transform: scale(1.05);
    box-shadow: 0px 0px 10px rgb(146, 144, 144);
    border-color: #817e7e96;
}

.btn.btn-primary {
    width: 40%;
    align-self: center;
    margin-bottom: 5px;
}
</style>
