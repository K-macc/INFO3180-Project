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
    selectedFilter.value = ''; 
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
  <div class="profiles-bg">

    <transition name="fade">
      <div v-if="errorMessage" class="alert error-message">
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

      <div class="filter-container" v-if="filters.length">
        <div v-for="(filter, index) in filters" :key="index" class="filter-body">
          <div class="filter-input">
            <input v-if="filter.operator === ''" v-model="filter.value" type="text" class="filter-option"
              :placeholder="filter.field" />
          </div>

          <select v-model="filter.value" v-if="filter.operator === 'between'" class="filter-option">
            <option value="">--Select one--</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>

          <select v-model="filter.value" v-if="filter.operator === 'among'" class="filter-option">
            <option value="">--Select one--</option>
            <option value="asian">Asian</option>
            <option value="black">Black</option>
            <option value="indigenous">Indigenous</option>
            <option value="mixed">Mixed</option>
            <option value="white">White</option>
          </select>

          <button @click="removeFilter(index)" class="filter-button">✕</button>
        </div>
        <button @click="filteredProfiles" class="btn btn-primary search">Search</button>
      </div>

    </div>

    <h1>Recently Added Profiles</h1>
    <div class="profile-list">

      <div v-for="profile in recent_profiles" :key="profile.id" class="profile-item card">
        <h2>{{ profile.user_name }}</h2>
        <p>{{ profile.description }}</p>
        <router-link class="btn btn-primary" :to="`/profiles/${profile.id}`" @click="trackProfileView(profile.id)">View
          more details</router-link>
      </div>
    </div>


    <h1 v-if="filtered_profiles.length">Search Results</h1>
    <div class="profile-list">
      <div v-for="profile in filtered_profiles" :key="profile.id" class="profile-item card">
        <h2>{{ profile.user_name }}</h2>
        <p>{{ profile.description }}</p>
        <router-link class="btn btn-primary" :to="`/profiles/${profile.id}`" @click="trackProfileView(profile.id)">View
          more details</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>

.profiles-bg {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  padding: 2rem 1rem;
  gap: 1rem;
  z-index: 5;
}

h1 {
  font-size: 2.8rem;
  color: #f7d4e6;
  text-shadow: 2px 2px #AD2874;
  animation: slideDown 0.8s ease-in-out;
  margin-top: 3rem;
  text-align: center;
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
  min-width: 250px;
  max-width: 450px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-align: left;
  animation: fadeInUp 0.4s ease-in;

  background-color: #fee2e2; 
  color: #991b1b; 
}


.search-container {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: fadeIn 1s ease;
}


.search-input {
  padding: 0.75rem 1rem;
  width: 60%;
  max-width: 500px;
  border-radius: 12px;
  font-size: 1rem;
  border: 1px solid #AD2874;
  margin-bottom: 1rem;
  background-color: #F7E1E9;
  transition: 0.3s;
  color: #69003D;
}

.search-input:focus {
  border-color: #00C8FF;
  box-shadow: 0 0 8px #00C8FFaa;
  background-color: #fff;
}


.filter-dropdown {
  display: flex;
  flex-direction: column;
  padding: 0.6rem;
  border-radius: 10px;
  border: 1px solid #AD2874;
  background-color: #F7E1E9;
  width: 200px;
  font-size: 1rem;
  margin-bottom: 1.5rem;
  color: #69003D;
}

.filter-dropdown:focus {
  border-color: #00C8FF;
  box-shadow: 0 0 8px #00C8FFaa;
  background-color: #fff;
}

.filter-container {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border: 1px solid #AD2874;
  border-radius: 12px;
  width: 60%;
  max-width: 600px;
  margin: 1rem auto;
  padding: 1rem;
  box-shadow: 0 4px 16px rgba(173, 40, 116, 0.08);
}

.filter-body {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
  gap: 0;
}

.filter-option {
  border: 2px solid #AD2874;
  border-radius: 8px;
  padding: 0.5rem;
  font-size: 0.95rem;
  background-color: #F7E1E9;
  color: #69003D;
  margin-right: 0;
  width: auto;
}

input.filter-option::placeholder {
  color: #69003D;
  opacity: 0.5;
}

select.filter-option {
  width: 150px;
  padding: 0.5rem;
}

.filter-option:focus {
  border-color: #00C8FF;
  box-shadow: 0 0 8px #00C8FFaa;
  background-color: #fff;
}

.filter-button {
  font-size: 1.2rem;
  cursor: pointer;
  background: none;
  border: none;
  color: #8A0047;
  transition: transform 0.2s ease;
  width: 10px;
  padding: 0.5rem;
}

.filter-button:hover {
  transform: rotate(15deg);
  color: #AD2874;
}

h2 {
  font-size: 1.6rem;
  color: #69003D;
  margin: 3rem 0 1rem;
  text-align: center;
}

.profile-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-top: 1rem;
  margin-bottom: 6rem;
  animation: fadeIn 1s ease-in-out;
}

.profile-item.card {
  width: 350px;
  padding: 1.8rem;
  background: linear-gradient(145deg, #F7E1E9, #ffffff);
  border-radius: 20px;
  border: 1px solid #AD2874;
  box-shadow: 0 12px 24px rgba(173, 40, 116, 0.06);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  color: #69003D;
}

.profile-item.card:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 16px 32px rgba(173, 40, 116, 0.25);
}

.profile-item.card h2 {
  margin: 0;
  color: #AD2874;
  font-size: 1.3rem;
  font-weight: 600;
}

.profile-item.card p {
  margin: 0.5rem 0 1rem;
  color: #444;
  font-style: italic;
  text-align: center;
}


.btn.btn-primary {
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
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(138, 0, 71, 0.4);
}

.search {
  width: 40%;
  margin: 0 auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
