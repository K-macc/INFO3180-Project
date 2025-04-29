<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const fav = ref([]);
const top_fav = ref([]);
const authStore = useAuthStore();
const order = ref('');
const show = ref(false);
const show_fav = ref(false);
const num = ref(0)

function loadFavourites(id) {
    show.value = true;
    fetch(`/api/users/${id}/favourites?order=${order.value}`, {
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
    show_fav.value  = true;
    fetch(`/api/users/favourites/${num.value}?order=${order.value}`, {
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
    <div>
        <div class="view-users">
            <button class="btn btn-primary" @click="loadFavourites(authStore.user_id)">View Your Favourited Users</button>

            <div class="top-favourited">
                <label for="number">Enter the number of top favourited users you want to view</label>
                <input v-model="num" type="number" id="number">
                <button class="btn btn-primary" @click="loadFavouritedNUsers">View the top {{ num }} favourited users</button>
            </div>  
        </div>
        

        <div class="favourite-users" v-if="show">
            <h3>My Favourite Users</h3>

            <select v-model="order" name="order" id="order" class="order-options"  @change="sortFavourites">
                <option value="">--Select--</option>
                <option value="age">Age</option>
                <option value="name">Name</option>
                <option value="parish">Parish</option>
            </select>

            <div class="favourites">
                <div v-for="favourite in fav" :key="favourite.id" class="user-fav">
                    <div>
                        <label for="user_name">User Name:</label>
                        {{ favourite.user_name }}
                    </div>

                    <div>
                        <label for="parish">Parish:</label>
                        {{ favourite.parish }}
                    </div>

                    <div>
                        <label for="age">Age:</label>
                        {{ favourite.age }}
                    </div>
                </div>
            </div>
        </div>

        <div class="top-favourited-users" v-if="show_fav">
            <h3>Top Favourited Users</h3>

            <select v-model="order" name="order" id="order" class="order-options"  @change="sortFavourited">
                <option value="">--Select--</option>
                <option value="age">Age</option>
                <option value="name">Name</option>
                <option value="parish">Parish</option>
            </select>

            <div class="favourites">
                <div v-for="favourite in top_fav" :key="favourite.id" class="user-fav">
                    <div>
                        <label for="user_name">User Name:</label>
                        {{ favourite.user_name }}
                    </div>

                    <div>
                        <label for="parish">Parish:</label>
                        {{ favourite.parish }}
                    </div>

                    <div>
                        <label for="age">Age:</label>
                        {{ favourite.age }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.view-users {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
    gap: 2rem;
    margin-bottom: 120px;
}

.top-favourited {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
    gap: 1rem;
}

.favourite-users {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
    margin-bottom: 120px
}

.top-favourited-users {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
    margin-bottom: 120px
}

.order-options {
    margin-bottom: 1rem;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 8px 20px 5px 12px;
    font-size: 16px;
    cursor: pointer;
    height: 38px;
}

.favourites {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
}

.user-fav{
    width: 300px;
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid #ccc;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
}

.user-fav:hover {
    background: white;
    transform: scale(1.05);
    box-shadow: 0px 0px 10px rgb(146, 144, 144);
    border-color: #817e7e96;
}
</style>