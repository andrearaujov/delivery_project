<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const restaurants = ref([])
const categories = ref([
  { id: 1, name: 'Lanches', icon: '🍔' },
  { id: 2, name: 'Pizza', icon: '🍕' },
  { id: 3, name: 'Japonesa', icon: '🍣' },
  { id: 4, name: 'Brasileira', icon: '🍛' },
  { id: 5, name: 'Saudável', icon: '🥗' },
  { id: 6, name: 'Doces', icon: '🍰' },
])

onMounted(async () => {
  try {
    const response = await axios.get('/api/restaurantes/')
    restaurants.value = response.data
  } catch (error) {
    console.error('Error fetching restaurants:', error)
  }
})
</script>

<template>
  <div>
    <!-- Hero Section -->
    <div class="bg-primary rounded-2xl p-6 md:p-10 mb-8 text-white relative overflow-hidden shadow-lg">
      <div class="relative z-10 max-w-lg">
        <h1 class="text-3xl md:text-5xl font-bold mb-4">Fome de quê?</h1>
        <p class="text-lg opacity-90 mb-6">Os melhores restaurantes da cidade entregando na sua porta.</p>
        <div class="flex gap-4">
          <button class="bg-white text-primary font-bold py-3 px-6 rounded-full hover:bg-gray-100 transition-colors">
            Ver Promoções
          </button>
        </div>
      </div>
      <!-- Decorative circle -->
      <div class="absolute -right-20 -bottom-40 w-80 h-80 bg-white/10 rounded-full blur-3xl"></div>
    </div>

    <!-- Categories -->
    <div class="mb-10">
      <h2 class="text-xl font-bold text-gray-800 mb-4">Categorias</h2>
      <div class="flex gap-4 overflow-x-auto pb-4 scrollbar-hide">
        <div v-for="category in categories" :key="category.id" class="flex flex-col items-center min-w-[80px] cursor-pointer group">
          <div class="w-20 h-20 bg-white rounded-2xl shadow-sm flex items-center justify-center text-3xl mb-2 group-hover:shadow-md group-hover:-translate-y-1 transition-all border border-gray-100">
            {{ category.icon }}
          </div>
          <span class="text-sm font-medium text-gray-600 group-hover:text-primary transition-colors">{{ category.name }}</span>
        </div>
      </div>
    </div>

    <!-- Restaurants List -->
    <div>
      <h2 class="text-xl font-bold text-gray-800 mb-6">Restaurantes</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <router-link 
          v-for="restaurant in restaurants" 
          :key="restaurant.id" 
          :to="`/restaurante/${restaurant.id}`"
          class="bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden group border border-gray-100"
        >
          <div class="relative h-48 overflow-hidden">
            <img 
              v-if="restaurant.imagem_url" 
              :src="restaurant.imagem_url" 
              :alt="restaurant.nome" 
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            >
            <div v-else class="w-full h-full bg-gray-200 flex items-center justify-center text-gray-400">
              <span class="text-4xl">🏪</span>
            </div>
            <div class="absolute top-3 right-3 bg-white/90 backdrop-blur-sm px-2 py-1 rounded-lg text-xs font-bold shadow-sm flex items-center gap-1">
              <span>⭐ 4.8</span>
            </div>
          </div>
          
          <div class="p-4">
            <div class="flex justify-between items-start mb-1">
              <h3 class="text-lg font-bold text-gray-800">{{ restaurant.nome }}</h3>
            </div>
            <p class="text-sm text-gray-500 mb-3">{{ restaurant.tipo_cozinha }} • 2.5 km</p>
            
            <div class="flex items-center gap-4 text-xs text-gray-500 border-t pt-3">
              <div class="flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                30-45 min
              </div>
              <div class="flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Grátis
              </div>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>
