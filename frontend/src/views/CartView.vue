<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const cart = ref({ itens: [], total: 0 })
const router = useRouter()
const loading = ref(false)
const checkoutLoading = ref(false)
const notification = ref(null)

const fetchCart = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/carrinho/')
    cart.value = response.data
  } catch (error) {
    console.error('Erro ao buscar carrinho:', error)
    notification.value = { type: 'error', message: 'Erro ao carregar o carrinho' }
  } finally {
    loading.value = false
  }
}

const updateQuantity = async (itemId, newQuantity) => {
  if (newQuantity < 1) return
  try {
    await axios.patch(`/api/carrinho/item/${itemId}/`, { quantidade: newQuantity })
    await fetchCart()
  } catch (error) {
    console.error('Erro ao atualizar quantidade:', error)
    notification.value = { type: 'error', message: 'Erro ao atualizar quantidade' }
  }
}

const removeItem = async (itemId) => {
  try {
    await axios.delete(`/api/carrinho/item/${itemId}/`)
    await fetchCart()
    notification.value = { type: 'success', message: 'Produto removido do carrinho' }
    setTimeout(() => {
      notification.value = null
    }, 2000)
  } catch (error) {
    console.error('Erro ao remover item:', error)
    notification.value = { type: 'error', message: 'Erro ao remover item' }
  }
}

const checkout = async () => {
  checkoutLoading.value = true
  try {
    const response = await axios.post('/api/checkout/')
    if (response.data.success) {
      notification.value = { type: 'success', message: 'Pedido realizado com sucesso!' }
      setTimeout(() => {
        cart.value = { itens: [], total: 0 }
        router.push('/')
      }, 2000)
    }
  } catch (error) {
    console.error('Erro ao finalizar pedido:', error)
    notification.value = { type: 'error', message: 'Erro ao finalizar pedido. Tente novamente.' }
  } finally {
    checkoutLoading.value = false
  }
}

const subtotal = computed(() => {
  return cart.value.itens.reduce((sum, item) => sum + (item.preco * item.quantidade), 0)
})

const deliveryFee = computed(() => 0)

const total = computed(() => subtotal.value + deliveryFee.value)

onMounted(() => {
  fetchCart()
})
</script>

<template>
  <div class="min-h-screen">
    <!-- Notification Toast -->
    <transition name="fade">
      <div 
        v-if="notification" 
        :class="[
          'fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 flex items-center gap-2 text-white',
          notification.type === 'success' ? 'bg-green-500' : 'bg-red-500'
        ]"
      >
        <svg v-if="notification.type === 'success'" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
        </svg>
        <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
        </svg>
        {{ notification.message }}
      </div>
    </transition>

    <!-- Header -->
    <div class="bg-gradient-to-r from-red-600 to-red-500 text-white py-8 mb-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center gap-4 mb-4">
          <router-link 
            to="/" 
            class="bg-white/20 hover:bg-white/30 rounded-full p-2 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </router-link>
          <h1 class="text-3xl md:text-4xl font-bold">🛒 Seu Carrinho</h1>
        </div>
        <p class="text-white/90">{{ cart.itens.length }} item{{ cart.itens.length !== 1 ? 's' : '' }} no carrinho</p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="text-center">
        <div class="inline-block animate-spin mb-4">
          <svg class="w-12 h-12 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <p class="text-gray-600 font-medium">Carregando carrinho...</p>
      </div>
    </div>

    <!-- Cart Content -->
    <div v-else-if="cart.itens.length > 0" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Cart Items -->
        <div class="lg:col-span-2">
          <div class="space-y-4">
            <div 
              v-for="(item, index) in cart.itens" 
              :key="item.produto_id" 
              class="bg-white rounded-xl border border-gray-200 shadow-md hover:shadow-lg transition-all duration-300 p-5"
            >
              <div class="flex gap-4">
                <!-- Product Image -->
                <div class="w-24 h-24 flex-shrink-0 rounded-lg overflow-hidden bg-gray-100">
                  <div class="w-full h-full flex items-center justify-center text-gray-400 text-3xl">
                    📦
                  </div>
                </div>

                <!-- Product Info -->
                <div class="flex-1">
                  <h3 class="font-bold text-lg text-gray-800 mb-1">{{ item.nome }}</h3>
                  <p class="text-sm text-gray-600 mb-3">R$ {{ item.preco.toFixed(2) }} / unidade</p>
                  
                  <!-- Quantity Controls -->
                  <div class="flex items-center gap-4">
                    <div class="flex items-center border border-gray-300 rounded-lg overflow-hidden bg-gray-50">
                      <button 
                        @click="updateQuantity(item.produto_id, item.quantidade - 1)"
                        class="px-3 py-2 text-gray-600 hover:bg-gray-100 transition-colors font-medium"
                      >
                        −
                      </button>
                      <span class="px-4 py-2 font-semibold text-gray-800 min-w-[40px] text-center">{{ item.quantidade }}</span>
                      <button 
                        @click="updateQuantity(item.produto_id, item.quantidade + 1)"
                        class="px-3 py-2 text-red-600 hover:bg-red-50 transition-colors font-bold"
                      >
                        +
                      </button>
                    </div>
                    <button 
                      @click="removeItem(item.produto_id)"
                      class="text-red-600 hover:text-red-700 font-medium text-sm hover:bg-red-50 px-3 py-2 rounded-lg transition-colors"
                    >
                      Remover
                    </button>
                  </div>
                </div>

                <!-- Subtotal -->
                <div class="text-right flex flex-col justify-between">
                  <p class="font-bold text-lg text-gray-800">R$ {{ (item.preco * item.quantidade).toFixed(2) }}</p>
                  <p class="text-xs text-gray-500">Subtotal</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Summary Sidebar -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-xl border border-gray-200 shadow-md p-6 sticky top-24">
            <h2 class="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
              <svg class="w-5 h-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3 1a1 1 0 000 2h1.22l.305 1.222a.997.997 0 00.01.042l1.358 5.43-.893.892C3.74 11.846 4.632 14 6.414 14H15a1 1 0 000-2H6.414l1-1H14a1 1 0 00.894-.553l3-6A1 1 0 0017 6H6.28l-.31-1.243A1 1 0 005 4H3z"></path>
              </svg>
              Resumo do Pedido
            </h2>
            
            <div class="space-y-3 mb-6 pb-6 border-b border-gray-200">
              <div class="flex justify-between text-gray-700">
                <span>Subtotal</span>
                <span class="font-semibold">R$ {{ subtotal.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-gray-700">
                <span>Taxa de entrega</span>
                <span class="font-semibold text-green-600">Grátis</span>
              </div>
            </div>
            
            <div class="mb-6">
              <div class="flex justify-between items-center">
                <span class="font-bold text-lg text-gray-800">Total</span>
                <span class="font-bold text-2xl text-red-600">R$ {{ total.toFixed(2) }}</span>
              </div>
            </div>
            
            <button 
              @click="checkout"
              :disabled="checkoutLoading"
              class="w-full bg-gradient-to-r from-red-600 to-red-500 hover:from-red-700 hover:to-red-600 disabled:from-gray-400 disabled:to-gray-400 text-white font-bold py-4 rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <svg v-if="!checkoutLoading" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"></path>
              </svg>
              <span v-if="checkoutLoading" class="inline-block animate-spin">⏳</span>
              <span v-else>Finalizar Pedido</span>
            </button>
            
            <router-link 
              to="/" 
              class="block text-center text-red-600 hover:text-red-700 font-medium mt-4 py-2 hover:bg-red-50 rounded-lg transition-colors"
            >
              ← Continuar Comprando
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty Cart State -->
    <div v-else class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div class="bg-white rounded-2xl border border-gray-200 shadow-md p-12 text-center">
        <div class="text-8xl mb-6 opacity-50">🛒</div>
        <h2 class="text-2xl font-bold text-gray-800 mb-3">Seu carrinho está vazio</h2>
        <p class="text-gray-600 mb-8 text-lg">Parece que você ainda não escolheu nada. Que tal explorar nossos restaurantes?</p>
        <router-link 
          to="/" 
          class="inline-block bg-gradient-to-r from-red-600 to-red-500 hover:from-red-700 hover:to-red-600 text-white font-bold py-3 px-8 rounded-full transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 flex items-center gap-2"
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path>
          </svg>
          Ver Restaurantes
        </router-link>
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
