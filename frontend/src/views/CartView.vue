<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const cart = ref({ itens: [], total: 0 })
const router = useRouter()

const fetchCart = async () => {
  try {
    const response = await axios.get('/api/carrinho/')
    cart.value = response.data
  } catch (error) {
    console.error('Error fetching cart:', error)
  }
}

const checkout = async () => {
  try {
    const response = await axios.post('/api/checkout/')
    if (response.data.success) {
      alert('Pedido realizado com sucesso!')
      cart.value = { itens: [], total: 0 }
      router.push('/')
    }
  } catch (error) {
    console.error('Error checkout:', error)
    alert('Erro ao finalizar pedido.')
  }
}

onMounted(() => {
  fetchCart()
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-gray-800 mb-8">Seu Carrinho</h1>
    
    <div v-if="cart.itens.length > 0" class="flex flex-col lg:flex-row gap-8">
      <!-- Cart Items -->
      <div class="flex-1 space-y-4">
        <div 
          v-for="item in cart.itens" 
          :key="item.produto_id" 
          class="bg-white p-4 rounded-xl border border-gray-100 shadow-sm flex items-center justify-between"
        >
          <div class="flex items-center gap-4">
            <div class="w-16 h-16 bg-gray-100 rounded-lg flex items-center justify-center text-xl">
              📦
            </div>
            <div>
              <h3 class="font-bold text-gray-800">{{ item.nome }}</h3>
              <p class="text-sm text-gray-500">R$ {{ item.preco }} / un</p>
            </div>
          </div>
          
          <div class="flex items-center gap-6">
            <div class="flex items-center border rounded-lg">
              <button class="px-3 py-1 text-gray-500 hover:bg-gray-50">-</button>
              <span class="px-2 font-medium">{{ item.quantidade }}</span>
              <button class="px-3 py-1 text-primary hover:bg-red-50 font-bold">+</button>
            </div>
            <p class="font-bold text-gray-800 min-w-[80px] text-right">R$ {{ item.subtotal }}</p>
          </div>
        </div>
      </div>
      
      <!-- Summary -->
      <div class="lg:w-96">
        <div class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm sticky top-24">
          <h2 class="text-lg font-bold text-gray-800 mb-4">Resumo do Pedido</h2>
          
          <div class="space-y-2 mb-4">
            <div class="flex justify-between text-gray-600">
              <span>Subtotal</span>
              <span>R$ {{ cart.total }}</span>
            </div>
            <div class="flex justify-between text-gray-600">
              <span>Taxa de entrega</span>
              <span>Grátis</span>
            </div>
          </div>
          
          <div class="border-t pt-4 mb-6">
            <div class="flex justify-between items-center">
              <span class="font-bold text-lg text-gray-800">Total</span>
              <span class="font-bold text-xl text-primary">R$ {{ cart.total }}</span>
            </div>
          </div>
          
          <button 
            @click="checkout" 
            class="w-full bg-primary text-white py-4 rounded-xl font-bold hover:bg-red-700 transition-colors shadow-lg shadow-red-200"
          >
            Finalizar Pedido
          </button>
          
          <router-link to="/" class="block text-center text-primary font-medium mt-4 hover:underline">
            Continuar comprando
          </router-link>
        </div>
      </div>
    </div>
    
    <!-- Empty State -->
    <div v-else class="text-center py-20 bg-white rounded-2xl border border-gray-100 shadow-sm">
      <div class="text-6xl mb-4">🛒</div>
      <h2 class="text-xl font-bold text-gray-800 mb-2">Seu carrinho está vazio</h2>
      <p class="text-gray-500 mb-6">Parece que você ainda não escolheu nada.</p>
      <router-link 
        to="/" 
        class="inline-block bg-primary text-white px-8 py-3 rounded-full font-bold hover:bg-red-700 transition-colors"
      >
        Ver Restaurantes
      </router-link>
    </div>
  </div>
</template>
