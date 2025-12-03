<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const restaurant = ref(null)
const loading = ref(true)

const addToCart = async (produtoId) => {
  try {
    await axios.post('/api/carrinho/adicionar/', { produto_id: produtoId })
    alert('Produto adicionado ao carrinho!')
  } catch (error) {
    if (error.response && error.response.status === 401) {
      alert('Faça login para adicionar ao carrinho')
    } else {
      console.error('Error adding to cart:', error)
    }
  }
}

onMounted(async () => {
  try {
    const response = await axios.get(`/api/restaurantes/${route.params.id}/`)
    restaurant.value = response.data
  } catch (error) {
    console.error('Error fetching restaurant:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div v-if="restaurant" class="pb-20">
    <!-- Header Image -->
    <div class="h-64 md:h-80 w-full relative">
      <img 
        v-if="restaurant.produtos && restaurant.produtos.length > 0 && restaurant.produtos[0].foto_url"
        :src="restaurant.produtos[0].foto_url" 
        class="w-full h-full object-cover"
        alt="Restaurant Cover"
      >
      <div v-else class="w-full h-full bg-gray-800 flex items-center justify-center text-white">
        <span class="text-6xl">🍽️</span>
      </div>
      <div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
      
      <div class="absolute bottom-0 left-0 w-full p-6 md:p-10 text-white">
        <div class="container mx-auto">
          <h1 class="text-3xl md:text-5xl font-bold mb-2">{{ restaurant.nome }}</h1>
          <div class="flex flex-wrap items-center gap-4 text-sm md:text-base opacity-90">
            <span>{{ restaurant.tipo_cozinha }}</span>
            <span>•</span>
            <span class="flex items-center gap-1">⭐ 4.8 (500+)</span>
            <span>•</span>
            <span>30-45 min</span>
          </div>
        </div>
      </div>
    </div>

    <div class="container mx-auto px-4 py-8">
      <!-- Menu Section -->
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Cardápio</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div 
          v-for="produto in restaurant.produtos" 
          :key="produto.id" 
          class="bg-white rounded-xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-all flex justify-between gap-4 group"
        >
          <div class="flex flex-col justify-between flex-1">
            <div>
              <h3 class="font-bold text-gray-800 text-lg mb-1 group-hover:text-primary transition-colors">{{ produto.nome }}</h3>
              <p class="text-gray-500 text-sm line-clamp-2 mb-2">{{ produto.descricao }}</p>
              <p class="font-bold text-gray-800">R$ {{ produto.preco }}</p>
            </div>
            <button 
              @click="addToCart(produto.id)" 
              class="mt-3 self-start text-primary font-bold text-sm hover:bg-red-50 px-3 py-1 rounded-lg transition-colors -ml-3"
            >
              Adicionar
            </button>
          </div>
          
          <div class="w-32 h-32 flex-shrink-0 rounded-lg overflow-hidden bg-gray-100 relative">
            <img 
              v-if="produto.foto_url" 
              :src="produto.foto_url" 
              :alt="produto.nome" 
              class="w-full h-full object-cover"
            >
             <div v-else class="w-full h-full flex items-center justify-center text-gray-300 text-2xl">
              🍔
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <div v-else-if="loading" class="min-h-screen flex items-center justify-center">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
  </div>
</template>
