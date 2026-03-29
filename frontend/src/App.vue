<template>
  <div class="min-h-screen flex flex-col relative w-full h-full text-foreground bg-background">
    <AppHeader />
    
    <main class="flex-1 relative flex flex-col z-0">
      <!-- Loading Overlay -->
      <div 
        v-if="loadingStore.isLoading" 
        class="absolute inset-0 z-40 flex items-center justify-center bg-background/80 backdrop-blur-sm"
      >
        <BaseLoading :message="loadingStore.message" />
      </div>

      <!-- Content -->
      <router-view />
    </main>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useLoadingStore } from '@/stores/loading'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import BaseLoading from '@/components/ui/BaseLoading.vue'

const router = useRouter()
const loadingStore = useLoadingStore()

router.beforeEach((to, from, next) => {
  if (to.name !== from.name) {
    loadingStore.setLoading(true)
  }
  next()
})

router.afterEach(() => {
  // Add a small delay for visual feedback, or just hide it immediately
  setTimeout(() => {
    loadingStore.setLoading(false)
  }, 300)
})
</script>
