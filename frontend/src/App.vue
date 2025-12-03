<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'

const searchQuery = ref('')
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <!-- Navbar -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
      <div class="container mx-auto px-4 h-16 flex items-center justify-between">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-2">
          <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-white font-bold text-xl">
            D
          </div>
          <span class="text-xl font-bold text-gray-800 tracking-tight">DeliveryApp</span>
        </RouterLink>

        <!-- Search Bar (Hidden on mobile) -->
        <div class="hidden md:flex flex-1 max-w-lg mx-8 relative">
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Buscar pratos ou restaurantes..." 
            class="w-full bg-gray-100 border-none rounded-lg py-2 pl-10 pr-4 focus:ring-2 focus:ring-primary/20 focus:bg-white transition-all"
          >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 absolute left-3 top-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>

        <!-- Navigation -->
        <nav class="flex items-center gap-4">
          <RouterLink to="/" class="text-gray-500 hover:text-primary transition-colors p-2 rounded-full hover:bg-gray-50">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
          </RouterLink>
          
          <RouterLink to="/carrinho" class="text-gray-500 hover:text-primary transition-colors p-2 rounded-full hover:bg-gray-50 relative">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
            <!-- Badge placeholder -->
            <!-- <span class="absolute top-1 right-1 w-2 h-2 bg-primary rounded-full"></span> -->
          </RouterLink>

          <RouterLink to="/login" class="text-gray-500 hover:text-primary transition-colors p-2 rounded-full hover:bg-gray-50">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </RouterLink>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 container mx-auto px-4 py-6">
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t py-8 mt-auto">
      <div class="container mx-auto px-4 text-center text-gray-400 text-sm">
        <p>&copy; 2025 DeliveryApp. Feito com ❤️ e Vue.js.</p>
      </div>
    </footer>
  </div>
</template>
