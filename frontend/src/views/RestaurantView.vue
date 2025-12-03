<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const restaurant = ref(null)
const loading = ref(true)
const error = ref(null)
const cartNotification = ref(null)

const addToCart = async (produtoId) => {
  try {
    await axios.post('/api/carrinho/adicionar/', { produto_id: produtoId })
    // Show notification instead of alert
    cartNotification.value = 'Produto adicionado ao carrinho!'
    setTimeout(() => {
      cartNotification.value = null
    }, 3000)
  } catch (error) {
    if (error.response && error.response.status === 401) {
      cartNotification.value = 'Faça login para adicionar ao carrinho'
    } else {
      console.error('Erro ao adicionar ao carrinho:', error)
      cartNotification.value = 'Erro ao adicionar ao carrinho'
    }
    setTimeout(() => {
      cartNotification.value = null
    }, 3000)
  }
}

onMounted(async () => {
  try {
    const response = await axios.get(`/api/restaurantes/${route.params.id}/`)
    restaurant.value = response.data
  } catch (err) {
    console.error('Erro ao buscar restaurante:', err)
    error.value = 'Não foi possível carregar o restaurante. Tente novamente.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div v-if="loading" class="min-h-screen flex items-center justify-center">
    <div class="text-center">
      <div class="inline-block animate-spin mb-4">
        <svg class="w-12 h-12 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
      </div>
      <p class="text-gray-600 font-medium">Carregando restaurante...</p>
    </div>
  </div>

  <div v-else-if="error" class="min-h-screen flex items-center justify-center">
    <div class="bg-red-50 border border-red-200 rounded-lg p-8 text-center max-w-md">
      <p class="text-red-800 font-medium text-lg mb-4">{{ error }}</p>
      <router-link to="/" class="inline-block bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded-lg transition-colors">
        ← Voltar para Restaurantes
      </router-link>
    </div>
  </div>

  <div v-else-if="restaurant" class="pb-20">
    <!-- Notification Toast -->
    <transition name="fade">
      <div v-if="cartNotification" class="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 flex items-center gap-2">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
        </svg>
        {{ cartNotification }}
      </div>
    </transition>

    <!-- Header Image with Overlay -->
    <div class="relative h-64 md:h-96 w-full overflow-hidden">
      <img 
        v-if="restaurant.produtos && restaurant.produtos.length > 0 && restaurant.produtos[0].foto_url"
        :src="restaurant.produtos[0].foto_url" 
        class="w-full h-full object-cover"
        alt="Restaurant Cover"
      >
      <div v-else class="w-full h-full bg-gradient-to-br from-gray-300 to-gray-400 flex items-center justify-center text-white">
        <span class="text-8xl opacity-30">🍽️</span>
      </div>
      
      <!-- Gradient Overlay -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"></div>
      
      <!-- Back Button -->
      <router-link 
        to="/" 
        class="absolute top-6 left-6 bg-white/90 hover:bg-white text-gray-800 rounded-full p-2 transition-all shadow-md hover:shadow-lg z-10"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
        </svg>
      </router-link>
      
      <!-- Restaurant Info Overlay -->
      <div class="absolute bottom-0 left-0 w-full p-6 md:p-10 text-white">
        <div class="max-w-7xl mx-auto">
          <h1 class="text-4xl md:text-5xl font-bold mb-3">{{ restaurant.nome }}</h1>
          <div class="flex flex-wrap items-center gap-4 text-sm md:text-base opacity-95">
            <div class="flex items-center gap-2">
              <span class="text-lg">🍽️</span>
              <span class="font-medium">{{ restaurant.tipo_cozinha }}</span>
            </div>
            <span class="text-white/60">•</span>
            <div class="flex items-center gap-2">
              <span>⭐</span>
              <span class="font-medium">4.8 (500+ avaliações)</span>
            </div>
            <span class="text-white/60">•</span>
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v3.586L7.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 10.586V7z" clip-rule="evenodd"></path>
              </svg>
              <span class="font-medium">30-45 min</span>
            </div>
            <span class="text-white/60">•</span>
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.5 13a3.5 3.5 0 01-.369-6.98 4 4 0 117.753-1.3A4.5 4.5 0 1113.5 13H11V9.413l1.293 1.293a1 1 0 001.414-1.414l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13H5.5z" clip-rule="evenodd"></path>
              </svg>
              <span class="font-medium">Entrega Grátis</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Menu Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-800 mb-2">Cardápio</h2>
        <p class="text-gray-600">Escolha entre nossos deliciosos pratos</p>
      </div>
      
      <div v-if="restaurant.produtos && restaurant.produtos.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="produto in restaurant.produtos" 
          :key="produto.id" 
          class="bg-white rounded-xl border border-gray-200 shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden group flex flex-col h-full"
        >
          <!-- Product Image -->
          <div class="relative h-48 overflow-hidden bg-gray-100">
            <img 
              v-if="produto.foto_url" 
              :src="produto.foto_url" 
              :alt="produto.nome" 
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
            >
            <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
              <span class="text-6xl opacity-30">🍔</span>
            </div>
            <!-- Overlay on hover -->
            <div class="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors duration-300"></div>
          </div>
          
          <!-- Product Info -->
          <div class="p-5 flex-1 flex flex-col">
            <h3 class="font-bold text-lg text-gray-800 group-hover:text-red-600 transition-colors mb-2">{{ produto.nome }}</h3>
            <p class="text-gray-600 text-sm line-clamp-2 mb-4 flex-1">{{ produto.descricao }}</p>
            
            <!-- Price and Button -->
            <div class="flex items-center justify-between pt-4 border-t border-gray-100">
              <p class="font-bold text-xl text-red-600">R$ {{ produto.preco }}</p>
              <button 
                @click="addToCart(produto.id)" 
                class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5 flex items-center gap-2"
              >
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M3 1a1 1 0 000 2h1.22l.305 1.222a.997.997 0 00.01.042l1.358 5.43-.893.892C3.74 11.846 4.632 14 6.414 14H15a1 1 0 000-2H6.414l1-1H14a1 1 0 00.894-.553l3-6A1 1 0 0017 6H6.28l-.31-1.243A1 1 0 005 4H3z"></path>
                </svg>
                Adicionar
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="bg-blue-50 border border-blue-200 rounded-lg p-8 text-center">
        <p class="text-blue-800 text-lg font-medium">Nenhum produto disponível no momento.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
