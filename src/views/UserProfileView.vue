<script setup>
import { ref, onMounted } from 'vue'

const user = ref(null);

const fetchUser = () => {
    fetch('/api/users/1', {
        method: 'GET',
    })
    .then(response => {
    return response.json();     
    })
    .then(data => { 
        user.value = data;
        console.log(user.value);
    })
    .catch(error => {
            console.error('Failed to parse JSON:', error);
    })


}


onMounted(() => {
    fetchUser(); 
});

</script>

<template>
    <div class="main-body">
        <h1>My Profile</h1>

        <div class="header-info" v-if="user">
            <img :src="user.photo" alt="Profile Picture">

            <div class="text-content">
                <div class="label-info">
                    <label for="name">Name:</label>
                    <p>{{ user.name }} </p>
                </div>
                
                <div class="label-info">
                    <label for="email">Email:</label>
                    <p>{{ user.email }}</p>
                </div>
                
                <div class="label-info">
                    <label for="date_joined">Date Joined:</label>
                    <p>{{ user.date_joined }}</p>
                </div>
            </div>
            
        </div>

        <div class="profiles">
            <h2>Profiles</h2>

            <div></div>
        </div>
    </div>
</template>


<style scoped>

.main-body {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100vh;
}

img {
    width: 130px;
    height: 130px;
    border-radius: 50%;
    margin: 10px 0px 10px 40px;
}

.header-info {
    display: grid;
    grid-template-columns: 140px 1fr; /* Image takes up 190px, text takes the remaining space */
    align-items: flex-start;  /* Align the content to the top */
    justify-content: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    width: 550px;
    height: 150px;
    transition: all 0.3s ease-in-out;
    margin-top: 20px;
    margin-bottom: 50px;
}

.label-info {
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 10px;
    font-size: large;
}

label {
    font-weight: bold;
}

.text-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
}

.profiles {
    display: grid;
    grid-template-columns: 190px 1fr; /* Image takes up 190px, text takes the remaining space */
    align-items: flex-start;  /* Align the content to the top */
    justify-content: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    width: 550px;
    height: auto;
    transition: all 0.3s ease-in-out;
}

</style>