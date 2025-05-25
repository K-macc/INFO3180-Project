<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const fav = ref([]);
const top_fav = ref([]);
const authStore = useAuthStore();
const fav_order = ref('');
const top_fav_order = ref('');
const show = ref(false);
const show_fav = ref(false);
const num = ref(0);

function loadFavourites(id) {
  show.value = true;
  fetch(`/api/users/${id}/favourites?order=${fav_order.value}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authStore.token}`
    }
  })
    .then((response) => response.json())
    .then((data) => {
      fav.value = data.favourites;
    })
    .catch((error) => {
      console.error('Error fetching favourites:', error);
    });
}

function sortFavourites() {
  loadFavourites(authStore.user_id);
}

function loadFavouritedNUsers() {
  if (!num.value || num.value < 1) {
    alert('Please enter a valid number greater than 0');
    return;
  }
  show_fav.value = true;
  fetch(`/api/users/favourites/${num.value}?order=${top_fav_order.value}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authStore.token}`
    }
  })
    .then((response) => response.json())
    .then((data) => {
      top_fav.value = data.favourites;
    })
    .catch((error) => {
      console.error('Error fetching favourites:', error);
    });
}

function sortFavourited() {
  loadFavouritedNUsers();
}
</script>

<template>
  <div class="container-bg">
    <section class="controls-section">
      <button class="btn btn-primary" @click="loadFavourites(authStore.user_id)">
        View Your Favourited Users
      </button>

      <div class="top-favourited-control">
        <label for="number">Number of top favourited users to view:</label>
        <input v-model.number="num" type="number" id="number" min="1" />
        <button class="btn btn-primary favourited" @click="loadFavouritedNUsers">
          View Top {{ num }} Favourited Users
        </button>
      </div>
    </section>

    <section v-if="show" class="favourites-section">
      <h3>My Favourite Users</h3>
      <select v-model="fav_order" @change="sortFavourites" class="order-select" aria-label="Sort favourites">
        <option value="">--Sort By--</option>
        <option value="age">Age</option>
        <option value="name">Name</option>
        <option value="parish">Parish</option>
      </select>

      <div class="favourites-list">
        <article v-for="favourite in fav" :key="favourite.id" class="user-card">
          <p><strong>User Name:</strong> {{ favourite.user_name }}</p>
          <p><strong>Parish:</strong> {{ favourite.parish }}</p>
          <p><strong>Age:</strong> {{ favourite.age }}</p>
        </article>
      </div>
    </section>

    <section v-if="show_fav" class="favourites-section">
      <h3>Top Favourited Users</h3>
      <select v-model="top_fav_order" @change="sortFavourited" class="order-select" aria-label="Sort top favourites">
        <option value="">--Sort By--</option>
        <option value="age">Age</option>
        <option value="name">Name</option>
        <option value="parish">Parish</option>
      </select>

      <div class="favourites-list">
        <article v-for="favourite in top_fav" :key="favourite.id" class="user-card">
          <p><strong>User Name:</strong> {{ favourite.user_name }}</p>
          <p><strong>Parish:</strong> {{ favourite.parish }}</p>
          <p><strong>Age:</strong> {{ favourite.age }}</p>
        </article>
      </div>
    </section>
  </div>
</template>

<style scoped>
.container-bg {
  margin: 0;
  padding: 2rem 1rem;
}

.controls-section {
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  gap: 1.5rem;
  justify-content: center;
  margin-bottom: 3rem;
}

.btn {
    padding: 0.75rem 2rem;
    border-radius: 0.7rem;
    font-weight: 600;
    font-size: 1.1rem;
    cursor: pointer;
    border: none;
    color: #fff;
    transition: background 0.3s, color 0.3s;
    box-shadow: 0 2px 8px rgba(138, 0, 71, 0.07);
    width: 350px;
    margin: 0 auto;
}

.favourited {
    margin: 0;
}

.btn:hover {
    transform: translateY(-2px);
    color: #fff;
}

.top-favourited-control {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  width: 100%;
}

.top-favourited-control label {
  font-weight: 600;
  color: #f7d4e6;
  text-shadow: 2px 2px #AD2874;
  min-width: 220px;
}

.top-favourited-control input[type="number"] {
  width: 80px;
  padding: 0.4rem 0.6rem;
  border-radius: 8px;
  border: 2px solid #ad2874;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.top-favourited-control input[type="number"]:focus {
  border-color: #00c8ff;
  outline: none;
  box-shadow: 0 0 6px #00c8ff66;
}

.order-select {
  margin: 1rem 0 1.5rem 0;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: 2px solid #ad2874;
  font-size: 1rem;
  color: #69003D;
  cursor: pointer;
  transition: border-color 0.3s ease;
  width: 10%;
  margin: 1rem auto;
}

.order-select:hover,
.order-select:focus {
  border-color: #00c8ff;
  outline: none;
  box-shadow: 0 0 6px #00c8ff66;
}

.favourites-section {
  padding: 1.5rem 2rem;
  box-shadow: 0 4px 20px rgba(138, 0, 71, 0.1);
  margin-bottom: 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.favourites-section h3 {
  color: #f7d4e6;
  text-shadow: 2px 2px #AD2874;
  margin-bottom: 1rem;
  font-weight: 700;
  font-size: 1.5rem;
  text-align: center;
}

.favourites-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: center;
}

.user-card {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(138, 0, 71, 0.12);
  padding: 1rem 1.2rem;
  width: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: default;
  color: #333;
}

.user-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 200, 255, 0.3);
}

.user-card p {
  margin: 0.3rem 0;
  font-size: 1rem;
}

.user-card strong {
  color: #69003D;
}
</style>
