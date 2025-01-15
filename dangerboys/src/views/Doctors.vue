<script setup lang="ts">
import { useRoute } from 'vue-router';
import Doctor from '../components/Doctor.vue';
import DoctorHeader from '../components/DoctorHeader.vue';
import { inject, ref, computed } from 'vue';
import { useFetch } from '@vueuse/core';

// Инъекция BASE_SITE из родительского контекста
const BASE_SITE = inject<string>('BASE_SITE');

// Получаем параметры маршрута
const route = useRoute();
const specialId = route.params.specialId as string; // Убедимся, что specialId обрабатывается как строка

// Запрашиваем врачей по ID специализации
const { data: doctors, isFetching, error } = useFetch(`${BASE_SITE}/doctors/${specialId}`)
    .get()
    .json();

// Используем ref для хранения заголовка для шапки
const label = ref<string>('Наши врачи');

// Вычисляемое свойство для безопасного доступа к метке из данных врачей
const specializationLabel = computed(() => {
    if (doctors.value && doctors.value.length > 0) {
        return doctors.value[0].specialization.label;
    }
    return label.value; // Резервный вариант, если врачи не найдены
});
</script>

<template>
    <DoctorHeader :label="specializationLabel" />
    <div v-if="isFetching" class="text-center">
        <p>Загрузка...</p>
    </div>
    <!-- Ошибка -->
    <div v-else-if="error" class="text-center text-red-500">
        <p>Ошибка: {{ error.message }}</p>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div v-for="doctor in doctors" :key="doctor.id">
            <Doctor :photo="doctor.photo" :description="doctor.description" :experience="doctor.experience"
                :doctorId="doctor.id" :name="`${doctor.first_name} ${doctor.last_name}`" :special="doctor.special"
                :work_experience="doctor.work_experience" />
        </div>
    </div>
</template>