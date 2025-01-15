<script setup lang='ts'>
defineProps(['label']);
</script>


<template>
    <div class="flex justify-between items-center mb-12 ">
        <h1 class="text-3xl font-bold text-indigo-900">{{ label }}</h1>
        <router-link to="/"
            class="inline-flex items-center px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
            <i class="fas fa-home mr-2"></i>
            Главная
        </router-link>
    </div>
</template>