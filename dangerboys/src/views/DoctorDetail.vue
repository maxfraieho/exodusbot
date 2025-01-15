<script setup lang="ts">
import DoctorHeader from '../components/DoctorHeader.vue'
import BookingSlot from "../components/BookingSlot.vue";
import { useFetch } from '@vueuse/core'
import { computed, inject, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const BASE_SITE = inject<string>('BASE_SITE')
if (!BASE_SITE) {
    throw new Error('BASE_SITE must be provided')
}

const route = useRoute()
const doctorId = route.params.doctorId as string

// Получаем информацию о докторе
const { data: doctor } = useFetch(`${BASE_SITE}/doctor/${doctorId}`)
    .get()
    .json()

const doctorInfo = computed(() => doctor.value || {})

// Формируем URL изображения доктора
const imageSrc = computed(() => {
    if (!doctorInfo.value.photo) return ''
    return new URL(`${BASE_SITE}/static/images/${doctorInfo.value.photo}`, import.meta.url).href
})

// Формируем полное имя доктора
const name = computed(() => {
    const { first_name = '', patronymic = '', last_name = '' } = doctorInfo.value
    return `${first_name} ${patronymic} ${last_name}`.trim()
})

// Получаем текущую дату для начальных слотов
const today = new Date()
const initialDate = today.toISOString().split('T')[0]
const currentStartDate = ref(initialDate)

// Создаем реактивный запрос для получения слотов
const { data: slotsWeekInfo, execute: fetchSlots } = useFetch(
    computed(() => `${BASE_SITE}/booking/available-slots/${doctorId}?start_date=${currentStartDate.value}`),
    { immediate: true }
).get().json()

const label = "Запись"

// Генерируем строку с текущей неделей
const generateCurrentWeek = computed(() => {
    if (slotsWeekInfo.value?.days?.length) {
        const days = slotsWeekInfo.value.days
        const startDate = days[0].date
        const endDate = days[days.length - 1].date
        return `${startDate} - ${endDate}`
    }
    return "Нет данных"
})

// Функция навигации по неделям
const changeWeek = async (direction: number) => {
    const date = new Date(currentStartDate.value)
    date.setDate(date.getDate() + (direction * 7))

    // Предотвращаем выбор даты ранее текущей
    if (date < today) {
        currentStartDate.value = initialDate
    } else {
        currentStartDate.value = date.toISOString().split('T')[0]
    }

    // Ждем обновления слотов
    await fetchSlots()
}

// Следим за изменениями даты и обновляем слоты
watch(currentStartDate, async () => {
    await fetchSlots()
}, { immediate: true })
</script>

<template>
    <DoctorHeader :label="label" />

    <div class="flex flex-col sm:flex-row items-center mb-8 border-b pb-6 rounded-lg 
                shadow-lg hover:shadow-xl transition-shadow duration-300">
        <img v-if="imageSrc" :src="imageSrc" :alt="`Фото доктора ${name}`"
            class="ml-2 w-32 h-24 sm:w-40 sm:h-32 object-cover rounded-lg mr-4 cursor-pointer" />

        <div class="text-center sm:text-left">
            <h2 class="text-2xl sm:text-3xl font-bold text-indigo-900 mb-2">
                {{ name }}
            </h2>
            <p class="text-indigo-600 text-lg">
                {{ doctorInfo.special }} • Стаж: {{ doctorInfo.work_experience }}
                {{ doctorInfo.experience }}
            </p>
        </div>
    </div>

    <div class="flex items-center space-x-6 mb-6">
        <button class="w-14 h-14 flex items-center justify-center bg-indigo-500 text-white rounded-full 
                   hover:bg-indigo-600 active:bg-indigo-700 transition-all duration-300 shadow-lg 
                   hover:shadow-xl" @click="() => changeWeek(-1)" :disabled="currentStartDate === initialDate">
            <i class="fas fa-chevron-left text-xl"></i>
        </button>
        <h3 class="text-xl font-semibold text-indigo-900 flex-grow text-center">
            {{ generateCurrentWeek }}
        </h3>
        <button class="w-14 h-14 flex items-center justify-center bg-indigo-500 text-white rounded-full 
                   hover:bg-indigo-600 active:bg-indigo-700 transition-all duration-300 shadow-lg 
                   hover:shadow-xl" @click="() => changeWeek(1)">
            <i class="fas fa-chevron-right text-xl"></i>
        </button>
    </div>

    <!-- Слоты для записи -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-6" v-if="slotsWeekInfo && slotsWeekInfo.days">
        <BookingSlot v-for="dayDate in slotsWeekInfo.days" :key="dayDate.date" :doctor-info="doctorInfo"
            :dayDate="dayDate" />
    </div>
</template>