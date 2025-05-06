<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const profiles = ref([]);
const searchTerm = ref('');
const selectedFilter = ref('');
const recent_profiles = ref([]);
const filtered_profiles = ref([]);
const authStore = useAuthStore();
const errorMessage = ref('');
const router = useRouter();
const filters = ref([])
const filterValues = ref([]);
const filterOptions = ref([]);

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

function addFilter() {
    if (!filterValues.value.includes(selectedFilter.value) && selectedFilter.value === 'sex') {
        filters.value.push({ field: selectedFilter.value, operator: 'between', value: '' });
        filterValues.value.push(selectedFilter.value);
        selectedFilter.value = ''; // reset the dropdown
    } else if (!filterValues.value.includes(selectedFilter.value) && selectedFilter.value === 'race') {
        filters.value.push({ field: selectedFilter.value, operator: 'among', value: '' });
        filterValues.value.push(selectedFilter.value);
        selectedFilter.value = ''; 
    } else if (!filterValues.value.includes(selectedFilter.value) && selectedFilter.value !== '') {
        filters.value.push({ field: selectedFilter.value, operator: '', value: '' });
        filterValues.value.push(selectedFilter.value);
        selectedFilter.value = ''; 
    } else {
        errorMessage.value = 'Filter already added!';
        flashMessage(errorMessage);
    }
}

function removeFilter(index) {
    filters.value.splice(index, 1);
    filterValues.value.splice(index, 1);
}

function fetchProfiles() {
    fetch(`/api/check-profiles/${authStore.user_id}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                errorMessage.value = data.error;
                flashMessage(errorMessage);
                setTimeout(() => {
                    router.push('/profiles/check');
                }, 3000);
            } else {
                fetch('/api/profiles', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${authStore.token}`,
                        'Content-Type': 'application/json'
                    }
                })
                    .then(response => response.json())
                    .then(data => {
                        profiles.value = data.profiles;
                        recent_profiles.value = profiles.value.slice(-4).reverse();
                    })
                    .catch(error => {
                        console.error('Error fetching profiles:', error);
                    });
            }
        })
};

onMounted(() => {
    fetchProfiles();
});


function filteredProfiles() {
    errorMessage.value = '';
    filtered_profiles.value = [];
    filterOptions.value = [];
    filters.value.forEach((filter) => {
        filterOptions.value.push([filter.field, filter.value]);
    });
    const url = `/api/search?search=${encodeURIComponent(searchTerm.value)}&field=${encodeURIComponent(JSON.stringify(filterOptions.value))}`;
    fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.results) {
                const result = data.results;
                result.forEach((item) => {
                    filtered_profiles.value.push(item);
                });
            } else {
                errorMessage.value = data.error;
                flashMessage(errorMessage);
            }
        })
        .catch(error => {
            console.error('Error fetching profiles:', error);
        });
};
</script>

<template>
    <div class="profiles">
        <transition name="fade">
            <div v-if="errorMessage" class="error-message">
                {{ errorMessage }}
            </div>
        </transition>
        <h1>Search Profiles</h1>
        <div class="search-container">
            <input v-model="searchTerm" type="search" class="search-input" placeholder="Enter an item to search"
                @keyup.enter="filteredProfiles" />

            <select v-model="selectedFilter" @change="addFilter" class="filter-dropdown">
                <option value="">Select filter</option>
                <option value="birth_year">Birth Year</option>
                <option value="sex">Sex</option>
                <option value="race">Race</option>
            </select>

            <div class="border rounded p-4 mb-4" v-if="filters.length">
                <div v-for="(filter, index) in filters" :key="index" class="flex items-center mb-3 space-x-2">
                    <div class="flex space-x-2">
                        <input v-if="filter.operator === ''" v-model="filter.value" type="text"
                            class="border rounded px-2 py-1 w-24" :placeholder="filter.field" />
                    </div>

                    <select v-model="filter.value" v-if="filter.operator === 'between'" class="filter">
                        <option value="">--Select one--</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select>

                    <select v-model="filter.value" v-if="filter.operator === 'among'" class="filter">
                        <option value="">--Select one--</option>
                        <option value="asian">Asian</option>
                        <option value="black">Black</option>
                        <option value="indigenous">Indigenous</option>
                        <option value="mixed">Mixed</option>
                        <option value="white">White</option>
                    </select>

                    <button @click="removeFilter(index)" class="text-gray-500 hover:text-red-600">✕</button>
                </div>
                <button @click="filteredProfiles" class="btn btn-primary">Search</button>
            </div>

        </div>

        <h1>Recently Added Profiles</h1>
        <div class="profile-list">
            
            <div v-for="profile in recent_profiles" :key="profile.id" class="profile-item card">
                <h2>{{ profile.user_name }}</h2>
                <p>{{ profile.description }}</p>
                <router-link class="btn btn-primary" :to="`/profiles/${profile.id}`"
                    @click="trackProfileView(profile.id)">View more details</router-link>
            </div>
        </div>


        <h2 v-if="filtered_profiles.length">Search Results</h2>
        <div class="profile-list">
            <div v-for="profile in filtered_profiles" :key="profile.id" class="profile-item card">
                <h3>{{ profile.sex }}</h3>
                <p>{{ profile.description }}</p>
                <router-link class="btn btn-primary" :to="`/profiles/${profile.id}`"
                    @click="trackProfileView(profile.id)">View more details</router-link>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Layout and Container Styling */
/* .profiles {
    padding: 2rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f7f9fc;
    min-height: 100vh;
} */

.profiles {
  display: flex;
  flex-direction: column;
  /* align-items: center; */
  min-height: 100vh;
  background: linear-gradient(to bottom right, #ffecd2, #fcb69f);
  padding: 2rem 1rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  gap: 1rem;
}
    .profiles h1 {
        font-size: 2.5rem;
        color: #e91e63;
        text-shadow: 1px 1px #fff;
        background-color: white;
        padding: 1rem;
        border-radius: 10px
    }

/* Error message box */
.error-message {
    color: #721c24;
    background-color: #f8d7da;
    padding: 10px 20px;
    margin-bottom: 20px;
    border: 1px solid #f5c6cb;
    border-radius: 8px;
    position: fixed;
    top: 70px;
    right: 45px;
    z-index: 1000;
}

/* Search container */
.search-container {
    text-align: center;
    margin: .5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* Input field */
.search-input {
    padding: 0.75rem 1rem;
    width: 60%;
    max-width: 500px;
    border-radius: 10px;
    font-size: 1rem;
    border: 1px solid #ccc;
    margin-bottom: 1rem;
    outline-color: #4e73df;
}

/* Filter dropdown */
.filter-dropdown {
    display: flex;
    flex-direction: column;
    padding: 0.5rem;
    border-radius: 8px;
    border: 1px solid #ccc;
    width: 200px;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}

/* Filter container */
.border.rounded.p-4.mb-4 {
    display: flex;
    flex-direction: column;
    background-color: #ffffff;
    border: 1px solid #ddd;
    border-radius: 10px;
    width: 60%;
    max-width: 600px;
    margin: 1rem auto;
    padding: 1rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

/* Filter inputs and selects */
.filter input,
.filter select {
    display: flex;
    flex-direction: column;
    border: 1px solid #ccc;
    border-radius: 6px;
    padding: 0.5rem;
    font-size: 0.95rem;
}

/* Filter remove button */
button.text-gray-500 {
    font-size: 1.2rem;
    cursor: pointer;
    background: none;
    border: none;
}

/* Profile section title */
h2 {
    font-size: 1.5rem;
    color: #333;
    margin: 3rem 0 1rem;
    text-align: center;
}

/* Profile cards layout */
.profile-list {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: 1.5rem;
    margin-top: 1rem;
}

/* Card styling */
.profile-item.card {
    width: 300px;
    align-items: center;
    padding: 1.5rem;
    background-color: #ffffff;
    border-radius: 15px;
    border: 1px solid #e0e0e0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    transition: transform 0.2s, box-shadow 0.2s;
}

.profile-item.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.1);
    border-color: #d0d0d0;
}

/* Profile text */
.profile-item.card h2 {
    margin: 0;
    /* font-size: 1.2rem; */
    color: #e91e63;
    font-weight: bold;
    align-items: left;
}

.profile-item.card p {
    margin: 0.5rem 0 1rem;
    color: #555;
    font-style: italic;
}

/* Primary button */
.btn.btn-primary {
    background-color: #e91e63;
    color: white;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    border: none;
    font-weight: bold;
    cursor: pointer;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    transition: background-color 0.3s;
}

.btn.btn-primary:hover {
    background-color: #d81b60;
}

/* Fade transition for error */
.fade-leave-active {
    transition: opacity 1s ease-in-out;
}

.fade-leave-to {
    opacity: 0;
}
</style>
