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

function flashMessage(prompt){
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
        filters.value.push({field: selectedFilter.value, operator: 'between', value: ''});
        filterValues.value.push(selectedFilter.value);
        selectedFilter.value = ''; // reset the dropdown
      } else if (!filterValues.value.includes(selectedFilter.value) && selectedFilter.value === 'race') {
        filters.value.push({field: selectedFilter.value, operator: 'among', value: ''});
        filterValues.value.push(selectedFilter.value);
        selectedFilter.value = ''; // reset the dropdown
      } else if (!filterValues.value.includes(selectedFilter.value) && selectedFilter.value !== '') {
        filters.value.push({field: selectedFilter.value, operator: '', value: ''});
        filterValues.value.push(selectedFilter.value);
        selectedFilter.value = ''; // reset the dropdown
      } else {
        errorMessage.value = 'Filter already added!';
        flashMessage(errorMessage);
      }
}
    // Removes the filter from the list
function removeFilter(index) {
      filters.value.splice(index, 1);
      filterValues.value.splice(index, 1);
}

function fetchProfiles(){
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
                recent_profiles.value =  profiles.value.slice(-4).reverse();
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


function filteredProfiles(){
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
      <div class="search-container">
        <input v-model="searchTerm" type="search" class="search-input" placeholder="Enter an item to search" @keyup.enter="filteredProfiles"/>

        <select v-model="selectedFilter" @change="addFilter" class="filter-dropdown">
            <option value="">Select filter</option>
            <option value="birth_year">Birth Year</option>
            <option value="sex">Sex</option>
            <option value="race">Race</option>
            <!-- Add more options as needed -->
        </select>
    
    <!-- Filter Container -->
    <div class="border rounded p-4 mb-4" v-if="filters.length">
      <div v-for="(filter, index) in filters" :key="index" class="flex items-center mb-3 space-x-2">
        <!-- Filter Field Dropdown -->
        

        <!-- Input Fields -->
        <div class="flex space-x-2">
          <input
            v-if="filter.operator === ''"
            v-model="filter.value"
            type="text"
            class="border rounded px-2 py-1 w-24"
            :placeholder="filter.field"
          />
        </div>

        <select v-model="filter.value" v-if="filter.operator === 'between'" class="filter">
            <option value="">--Select one--</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <!-- Add more options as needed -->
        </select>

        <select v-model="filter.value" v-if="filter.operator === 'among'" class="filter">
            <option value="">--Select one--</option>
            <option value="asian">Asian</option>
            <option value="black">Black</option>
            <option value="indigenous">Indigenous</option>
            <option value="mixed">Mixed</option>
            <option value="white">White</option>
            <!-- Add more options as needed -->
        </select>

        <!-- Remove Filter -->
        <button @click="removeFilter(index)" class="text-gray-500 hover:text-red-600">✕</button>
      </div>
      <button @click="filteredProfiles" class="btn btn-primary">Search</button>
    </div>

  </div>
  
      <h2>Recently Added Profiles</h2>
      <div class="profile-list">
        <div v-for="profile in recent_profiles" :key="profile.id" class="profile-item card">
          <h3>{{ profile.sex }}</h3>
          <p>{{ profile.description }}</p>
          <router-link class="btn btn-primary" :to="`/profiles/${profile.id}`" @click="trackProfileView(profile.id)">View more details</router-link>
        </div>
      </div>

    
        <h2 v-if="filtered_profiles.length">Search Results</h2>
        <div class="profile-list">
            <div v-for="profile in filtered_profiles" :key="profile.id" class="profile-item card">
                <h3>{{ profile.sex }}</h3>
                <p>{{ profile.description }}</p>
                <router-link class="btn btn-primary" :to="`/profiles/${profile.id}`" @click="trackProfileView(profile.id)">View more details</router-link>
            </div>
        </div>
    </div>
  </template>

<style scoped>
.search-container {
    text-align: center;
    margin: 2rem 0;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .search-input {
    padding: 0.7rem;
    width: 50%;
    border-radius: 10px;
    font-size: 1rem;
    border: 1px solid #ccc;
  }
  
  .profile-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
  }
  
  .profile-item.card {
    width: 300px;
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid #ccc;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
  }

  .profile-item.card:hover {
    background: white ;
    transform: scale(1.05);
    box-shadow: 0px 0px 10px rgb(146, 144, 144) ;
    border-color: #817e7e96 ;
  }

  h2 {
    align-self: center;
    justify-self: center;
    margin: 70px 0 20px 0;;
  }

  .btn.btn-primary {
    width: 60%;
    align-self: center;
    margin-bottom: 10px;
}

.filter-dropdown { background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 8px 20px 5px 12px;
  font-size: 18px;
  cursor: pointer;
  height: 38px;
  align-self: flex-end;
  margin-right: 395px;
  margin-top: 5px;
  }

  .filter { 
    background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 8px 20px 5px 12px;
  font-size: 18px;
  cursor: pointer;
  height: 38px;
  margin-top: 5px;
  margin-right: 5px;
  }

.error-message {
      color: red;
      background-color: #f8d7da;
      padding: 10px;
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
      width: 12%;
      height: 5%;
  }

  .fade-leave-active {
    transition: opacity 1s ease-in-out;
  }

  .fade-leave-to {
    opacity: 0;
  }

</style>
  