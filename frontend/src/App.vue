<template>
  <div class="min-h-screen flex flex-col relative w-full h-full text-foreground bg-background">
    <AppHeader />
    
    <main class="flex-1 relative flex flex-col z-0">
      <!-- Loading Overlay -->
      <div 
        v-if="isLoading && $route.name !== 'home'" 
        class="absolute inset-0 z-[100] flex items-center justify-center bg-background/80 backdrop-blur-sm"
      >
        <BaseLoading message="Carregando..." />
      </div>

      <!-- Content -->
      <router-view />
    </main>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import BaseLoading from '@/components/ui/BaseLoading.vue'

const router = useRouter()
const isLoading = ref(false)

router.beforeEach((to, from, next) => {
  if (to.name !== from.name) {
    isLoading.value = true
  }
  next()
})

router.afterEach(() => {
  // Add a small delay for visual feedback, or just hide it immediately
  setTimeout(() => {
    isLoading.value = false
  }, 300)
})
</script>
