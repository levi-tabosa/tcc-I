<template>
  <div class="min-h-screen flex flex-col">
    <main class="flex-1">
      <HeroSection />
      <StatsSection />

      <FeaturesSection />

    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useLoadingStore } from '@/stores/loading'
import HeroSection from '@/components/home/HeroSection.vue'
import StatsSection from '@/components/home/StatsSection.vue'
import FeaturesSection from '@/components/home/FeaturesSection.vue'

const loadingStore = useLoadingStore()

onMounted(() => {
  loadingStore.startLoading('Bem-vindo ao Fiscaliza Brasil...')
  setTimeout(() => {
    loadingStore.stopLoading()
  }, 1000) // Visual feedback for home load
})

</script>
