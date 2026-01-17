<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1">
      <HeroSection />
      <StatsSection />
      <MapSection />
      <FeaturesSection />
      <FactsSection />
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import HeroSection from '@/components/home/HeroSection.vue'
import StatsSection from '@/components/home/StatsSection.vue'
import MapSection from '@/components/home/MapSection.vue'
import FeaturesSection from '@/components/home/FeaturesSection.vue'
import FactsSection from '@/components/home/FactsSection.vue'
</script>
