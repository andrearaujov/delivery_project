<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'

const searchQuery = ref('')
const mobileMenuOpen = ref(false)
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- Navbar -->
    <header class="bg-white shadow-sm sticky top-0 z-50 border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-3 group">
          <div class="w-10 h-10 bg-gradient-to-br from-red-500 to-red-600 rounded-lg flex items-center justify-center text-white font-bold text-xl shadow-md group-hover:shadow-lg transition-shadow">
            🍕
          </div>
          <span class="text-2xl font-bold bg-gradient-to-r from-red-600 to-red-500 bg-clip-text text-transparent tracking-tight hidden sm:inline">DeliveryHub</span>
        </RouterLink>

        <!-- Search Bar (Hidden on mobile) -->
        <div class="hidden md:flex flex-1 max-w-lg mx-8 relative">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 absolute left-3 top-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Buscar pratos ou restaurantes..." 
            class="w-full bg-gray-100 border border-gray-200 rounded-full py-2 pl-10 pr-4 focus:outline-none focus:ring-2 focus:ring-red-500 focus:bg-white transition-all"
          >
        </div>

        <!-- Navigation -->
        <nav class="flex items-center gap-2">
          <!-- Desktop Navigation -->
          <div class="hidden md:flex items-center gap-2">
            <RouterLink 
              to="/" 
              class="text-gray-600 hover:text-red-600 transition-colors p-2 rounded-lg hover:bg-red-50 font-medium"
            >
              Home
            </RouterLink>
            
            <RouterLink 
              to="/carrinho" 
              class="text-gray-600 hover:text-red-600 transition-colors p-2 rounded-lg hover:bg-red-50 relative flex items-center gap-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
              <span>Carrinho</span>
            </RouterLink>

            <RouterLink 
              to="/login" 
              class="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-200"
            >
              Entrar
            </RouterLink>
          </div>

          <!-- Mobile Menu Button -->
          <button 
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden text-gray-600 hover:text-red-600 p-2 rounded-lg hover:bg-red-50 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </nav>
      </div>

      <!-- Mobile Menu -->
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-200 bg-white">
        <div class="px-4 py-4 space-y-2">
          <RouterLink 
            to="/" 
            class="block text-gray-600 hover:text-red-600 hover:bg-red-50 p-3 rounded-lg transition-colors"
          >
            Home
          </RouterLink>
          <RouterLink 
            to="/carrinho" 
            class="block text-gray-600 hover:text-red-600 hover:bg-red-50 p-3 rounded-lg transition-colors"
          >
            🛒 Carrinho
          </RouterLink>
          <RouterLink 
            to="/login" 
            class="block bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors text-center"
          >
            Entrar
          </RouterLink>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-gray-300 mt-12 border-t border-gray-800">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <h3 class="text-white font-bold text-lg mb-4">🍕 DeliveryHub</h3>
            <p class="text-sm text-gray-400">Conectando você aos melhores restaurantes da sua região.</p>
          </div>
          <div>
            <h4 class="text-white font-bold mb-4">Links Rápidos</h4>
            <ul class="text-sm space-y-2">
              <li><RouterLink to="/" class="text-gray-400 hover:text-white transition-colors">Home</RouterLink></li>
              <li><RouterLink to="/carrinho" class="text-gray-400 hover:text-white transition-colors">Carrinho</RouterLink></li>
              <li><RouterLink to="/login" class="text-gray-400 hover:text-white transition-colors">Entrar</RouterLink></li>
            </ul>
          </div>
          <div>
            <h4 class="text-white font-bold mb-4">Contato</h4>
            <p class="text-sm text-gray-400">Email: contato@deliveryhub.com</p>
            <p class="text-sm text-gray-400">Telefone: (11) 9999-9999</p>
          </div>
        </div>
        <div class="border-t border-gray-800 pt-8 text-center text-sm text-gray-400">
          <p>&copy; 2025 DeliveryHub. Todos os direitos reservados.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* Smooth transitions */
:deep(.router-link-active) {
  @apply text-red-600 font-semibold;
}
</style>
