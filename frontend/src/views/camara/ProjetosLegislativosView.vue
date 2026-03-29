<template>
  <div class="min-h-screen flex flex-col">
    <main class="flex-1">
      <!-- Hero -->
      <section class="bg-gradient-to-br from-primary/10 via-background to-accent/10 py-12">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-foreground sm:text-4xl">Projetos Legislativos da Câmara</h1>
          <p class="mt-2 text-muted-foreground max-w-2xl">
            Acompanhe os projetos de lei, PECs, medidas provisórias e outros projetos legislativos apresentados na Câmara dos Deputados.
          </p>
        </div>
      </section>
      <!-- Global loading is handled via loadingStore in App.vue -->

      <!-- Stats -->
      <ProjetosLegislativosStats />

      <!-- Main content -->
      <section class="py-8">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <ProjetosLegislativosFilters />
          <ProjetosLegislativosList />
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import ProjetosLegislativosFilters from '@/components/camara/ProjetosLegislativosFilters.vue'
import ProjetosLegislativosList from '@/components/camara/ProjetosLegislativosList.vue'
import ProjetosLegislativosStats from '@/components/camara/ProjetosLegislativosStats.vue'
import { useLoadingStore } from '@/stores/loading'
import { useCamaraStore } from '@/stores/camara'

const store = useCamaraStore()
const loadingStore = useLoadingStore()

import { onMounted } from 'vue'
onMounted(async () => {
  if (store.projetosLegislativosList.length === 0) {
    loadingStore.startLoading('Carregando projetos legislativos...')
    try {
      await store.fetchProjetosLegislativos()
    } finally {
      loadingStore.stopLoading()
    }
  }
})
</script>
