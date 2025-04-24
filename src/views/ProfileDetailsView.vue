<script setup>
import { ref, onMounted } from 'vue'


</script>

<template>
    <div class="main-body">
        <h1>My Profile</h1>

        <div class="header-info">
            <img src="" alt="Profile Picture">

            <h3></h3>

            <p></p>
        </div>
        
        <div class="user-info">
            <div class="general-info">
            <h3></h3>

            <h3></h3>

            <h3></h3>

            <h3></h3>

            <h3></h3>

            <h3></h3>
            </div>

            <div class="favourites">
                <h3></h3>

                <h3></h3>

                <h3></h3>
            </div>
        </div>

        <div class="other-info">
            <h3></h3>

            <h3></h3>

            <h3></h3>
        </div>

        <div class="other-profiles">
            <h2>Other Profiles</h2>

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

.header-info {
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
    margin-top: 20px;
}

.user-info {
    display: flex;
    justify-content: center;
    width: 100%;
    margin: 20px 0px;
    gap: 40px;
}

.general-info {
    display: grid;
    grid-template-columns: 190px 1fr; /* Image takes up 190px, text takes the remaining space */
    align-items: flex-start;  /* Align the content to the top */
    justify-content: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    width: 400px;
    height: auto;
    transition: all 0.3s ease-in-out;
}

.favourites {
    display: grid;
    grid-template-columns: 190px 1fr; /* Image takes up 190px, text takes the remaining space */
    align-items: flex-start;  /* Align the content to the top */
    justify-content: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    width: 400px;
    height: auto;
    transition: all 0.3s ease-in-out;
}

.other-info {
    display: grid;
    grid-template-columns: 190px 1fr; /* Image takes up 190px, text takes the remaining space */
    align-items: flex-start;  /* Align the content to the top */
    justify-content: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    width: 400px;
    height: auto;
    transition: all 0.3s ease-in-out;
    margin-bottom: 20px;
}

.other-profiles {
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