<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const fav = ref([]);
const authStore = useAuthStore();

function loadFavourites(id) {
  favourites.value = [];
  fetch(`/api/users/${id}/favourites?order=name`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authStore.token}`
    }
  })
    .then((response) => response.json())
    .then((data) => {
      fav.value = data.favourites;
      console.log(fav.value);
    })
    .catch((error) => {
      console.error('Error fetching favourites:', error);
    });
}
</script>

<template></template>

<style scoped></style>