<template>
  <div class="min-h-screen flex flex-col">
    <main class="flex-1">
      <!-- Hero -->
      <section class="bg-gradient-to-br from-primary/10 via-background to-accent/10 py-12">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-foreground sm:text-4xl">Projetos Legislativos do Senado</h1>
          <p class="mt-2 text-muted-foreground max-w-2xl">
            Acompanhe os projetos de lei, PECs, medidas provisórias e outros projetos legislativos apresentados no Senado Federal.
          </p>
        </div>
      </section>
      <!-- Global loading is handled via loadingStore in App.vue -->

      <template v-if="!store.loadingProjetosLegislativos || store.projetosLegislativosList.length > 0">
        <!-- Stats -->
        <ProjetosLegislativosStats />

        <!-- Main content -->
        <section class="py-8">
          <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <ProjetosLegislativosFilters />
            <ProjetosLegislativosList />
          </div>
        </section>
      </template>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import ProjetosLegislativosFilters from '@/components/senado/ProjetosLegislativosFilters.vue'
import ProjetosLegislativosList from '@/components/senado/ProjetosLegislativosList.vue'
import ProjetosLegislativosStats from '@/components/senado/ProjetosLegislativosStats.vue'
import { useLoadingStore } from '@/stores/loading'
import { useSenadoStore } from '@/stores/senado'

const store = useSenadoStore()
const loadingStore = useLoadingStore()

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
