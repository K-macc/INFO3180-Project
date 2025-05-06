<template>
    <footer>
        <div class="container">
            <p>Copyright &copy {{ year }} Jam Date</p>
        </div>
    </footer>
</template>

<script setup>
const year = (new Date).getFullYear();
</script>

<style>
footer {
    background-color: #333;
    color: #fff;
    padding: 20px 0 5px 0;
}

.container {
    max-width: 960px;
    margin: 0 auto;
    text-align: center;
}
</style>