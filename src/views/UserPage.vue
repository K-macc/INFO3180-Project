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
/* Global Layout */
.profiles {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: linear-gradient(to bottom right, #8A0047, #00C8FF); /* Lavender Blush to Sky Blue */
  padding: 2rem 1rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  gap: 1rem;
  z-index: 5;
}

.profiles h1 {
  font-size: 2.8rem;
  color: #AD2874; /* Fandango */
  background: #F7E1E9;;
  padding: 1rem 2rem;
  border-radius: 12px;
  text-shadow: 2px 2px #f7d4e6; /* lighter Lavender Blush */
  box-shadow: 0 4px 12px rgba(138, 0, 71, 0.15); /* Murrey shadow */
  animation: slideDown 0.8s ease-in-out;
}

/* Error Box */
.error-message {
  color: #69003D; /* Tyrian Purple */
  background-color: #F7E1E9; /* Lavender Blush */
  padding: 12px 24px;
  margin-bottom: 20px;
  border: 1px solid #AD2874; /* Fandango */
  border-radius: 8px;
  position: fixed;
  top: 70px;
  right: 45px;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(138, 0, 71, 0.2); /* Murrey */
  animation: fadeInUp 0.4s ease-in;
}

/* Search Container */
.search-container {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: fadeIn 1s ease;
}

/* Input Field */
.search-input {
  padding: 0.75rem 1rem;
  width: 60%;
  max-width: 500px;
  border-radius: 12px;
  font-size: 1rem;
  border: 1px solid #00C8FF; /* Vivid Sky Blue */
  margin-bottom: 1rem;
  outline-color: #00C8FF;
  background-color: #F7E1E9; /* Lavender Blush */
  transition: 0.3s;
  color: #333;
}

.search-input:focus {
  border-color: #AD2874; /* Fandango */
  box-shadow: 0 0 8px #AD2874aa;
  background-color: #fff;
}

/* Filter Dropdown */
.filter-dropdown {
  display: flex;
  flex-direction: column;
  padding: 0.6rem;
  border-radius: 10px;
  border: 1px solid #AD2874; /* Fandango */
  background-color: #F7E1E9; /* Lavender Blush */
  width: 200px;
  font-size: 1rem;
  margin-bottom: 1.5rem;
  color: #69003D; /* Tyrian Purple */
}

/* Filter Container */
.border.rounded.p-4.mb-4 {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border: 1px solid #AD2874; /* Fandango */
  border-radius: 12px;
  width: 60%;
  max-width: 600px;
  margin: 1rem auto;
  padding: 1rem;
  box-shadow: 0 4px 16px rgba(173, 40, 116, 0.08); /* subtle fandango shadow */
}

/* Filter Inputs and Selects */
.filter input,
.filter select {
  border: 1px solid #00C8FF; /* Vivid Sky Blue */
  border-radius: 8px;
  padding: 0.5rem;
  font-size: 0.95rem;
  background-color: #F7E1E9; /* Lavender Blush */
  color: #69003D; /* Tyrian Purple */
  transition: 0.2s ease-in;
}

.filter input:focus,
.filter select:focus {
  border-color: #AD2874; /* Fandango */
  box-shadow: 0 0 8px #AD2874aa;
  background-color: #fff;
}

/* Remove Button */
button.text-gray-500 {
  font-size: 1.2rem;
  cursor: pointer;
  background: none;
  border: none;
  color: #8A0047; /* Murrey */
  transition: transform 0.2s ease;
}

button.text-gray-500:hover {
  transform: rotate(15deg);
  color: #AD2874; /* Fandango */
}

/* Section Title */
h2 {
  font-size: 1.6rem;
  color: #69003D; /* Tyrian Purple */
  margin: 3rem 0 1rem;
  text-align: center;
}

/* Profile Card Grid */
.profile-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-top: 1rem;
  animation: fadeIn 1s ease-in-out;
}

/* Profile Card */
.profile-item.card {
  width: 300px;
  padding: 1.8rem;
  background: linear-gradient(145deg, #F7E1E9, #ffffff);
  border-radius: 20px;
  border: 1px solid #AD2874; /* Fandango */
  box-shadow: 0 12px 24px rgba(173, 40, 116, 0.06);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  color: #69003D; /* Tyrian Purple */
}

.profile-item.card:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 16px 32px rgba(173, 40, 116, 0.25);
}

/* Profile Text */
.profile-item.card h2 {
  margin: 0;
  color: #AD2874; /* Fandango */
  font-size: 1.3rem;
  font-weight: 600;
}

.profile-item.card p {
  margin: 0.5rem 0 1rem;
  color: #444; /* Jet */
  font-style: italic;
}

/* Button */
.btn.btn-primary {
  background-color: #AD2874; /* Fandango */
  color: #fff;
  padding: 0.7rem 1.2rem;
  border-radius: 10px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.25s ease;
  box-shadow: 0 6px 16px rgba(173, 40, 116, 0.3);
}

.btn.btn-primary:hover {
  background-color: #69003D; /* Tyrian Purple */
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(138, 0, 71, 0.4);
}

/* Fade Animations */
.fade-leave-active {
  transition: opacity 1s ease-in-out;
}

.fade-leave-to {
  opacity: 0;
}

/* Custom Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-30px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

