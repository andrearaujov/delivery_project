<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const restaurants = ref([])
const loading = ref(true)
const error = ref(null)

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
  } catch (err) {
    console.error('Erro ao buscar restaurantes:', err)
    error.value = 'Não foi possível carregar os restaurantes. Tente novamente.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-red-600 via-red-500 to-orange-500 rounded-2xl p-8 md:p-16 mb-12 text-white relative overflow-hidden shadow-lg">
      <div class="relative z-10 max-w-2xl">
        <h1 class="text-4xl md:text-5xl font-bold mb-4 leading-tight">Fome de quê?</h1>
        <p class="text-lg opacity-95 mb-8">Os melhores restaurantes da cidade entregando na sua porta. Rápido, fácil e delicioso!</p>
        <div class="flex gap-4">
          <button class="bg-white text-red-600 font-bold py-3 px-8 rounded-full hover:bg-gray-100 transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5">
            Ver Promoções
          </button>
          <button class="border-2 border-white text-white font-bold py-3 px-8 rounded-full hover:bg-white/10 transition-all duration-200">
            Saiba Mais
          </button>
        </div>
      </div>
      <!-- Decorative circle -->
      <div class="absolute -right-32 -top-32 w-64 h-64 bg-white/10 rounded-full blur-3xl"></div>
      <div class="absolute -left-32 -bottom-32 w-80 h-80 bg-white/5 rounded-full blur-3xl"></div>
    </div>

    <!-- Categories Section -->
    <div class="mb-12">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Categorias Populares</h2>
      <div class="flex gap-4 overflow-x-auto pb-4 scrollbar-hide">
        <div 
          v-for="category in categories" 
          :key="category.id" 
          class="flex flex-col items-center min-w-[100px] cursor-pointer group"
        >
          <div class="w-24 h-24 bg-white rounded-2xl shadow-md flex items-center justify-center text-4xl mb-3 group-hover:shadow-lg group-hover:-translate-y-1 transition-all duration-300 border border-gray-100 group-hover:border-red-200">
            {{ category.icon }}
          </div>
          <span class="text-sm font-medium text-gray-700 group-hover:text-red-600 transition-colors text-center">{{ category.name }}</span>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin">
        <svg class="w-12 h-12 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
      <p class="text-red-800 font-medium">{{ error }}</p>
    </div>

    <!-- Restaurants List -->
    <div v-else>
      <h2 class="text-2xl font-bold text-gray-800 mb-8">Restaurantes em Destaque</h2>
      
      <div v-if="restaurants.length === 0" class="bg-blue-50 border border-blue-200 rounded-lg p-8 text-center">
        <p class="text-blue-800 text-lg font-medium">😔 Nenhum restaurante disponível no momento.</p>
        <p class="text-blue-600 mt-2">Volte em breve para descobrir novos estabelecimentos!</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <router-link 
          v-for="restaurant in restaurants" 
          :key="restaurant.id" 
          :to="`/restaurante/${restaurant.id}`"
          class="group"
        >
          <div class="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100 h-full flex flex-col">
            <!-- Image -->
            <div class="relative h-48 overflow-hidden bg-gradient-to-br from-gray-200 to-gray-300">
              <img 
                v-if="restaurant.imagem_url" 
                :src="restaurant.imagem_url" 
                :alt="restaurant.nome" 
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              >
              <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
                <span class="text-6xl opacity-30">🏪</span>
              </div>
              
              <!-- Rating Badge -->
              <div class="absolute top-4 right-4 bg-white/95 backdrop-blur-sm px-3 py-1 rounded-full text-sm font-bold shadow-md flex items-center gap-1">
                <span class="text-yellow-500">⭐</span>
                <span class="text-gray-800">4.8</span>
              </div>
              
              <!-- Overlay -->
              <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
            
            <!-- Content -->
            <div class="p-5 flex-1 flex flex-col">
              <div class="flex justify-between items-start mb-2">
                <h3 class="text-lg font-bold text-gray-800 group-hover:text-red-600 transition-colors">{{ restaurant.nome }}</h3>
              </div>
              
              <p class="text-sm text-gray-600 mb-4">{{ restaurant.tipo_cozinha }}</p>
              
              <!-- Info Footer -->
              <div class="flex items-center justify-between text-xs text-gray-500 border-t pt-4 mt-auto">
                <div class="flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>30-45 min</span>
                </div>
                <div class="flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  </svg>
                  <span>Grátis</span>
                </div>
              </div>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Hide scrollbar for categories */
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>
