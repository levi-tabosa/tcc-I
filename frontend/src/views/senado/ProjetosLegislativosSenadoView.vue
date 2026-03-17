<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
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

      <!-- Stats -->
      <ProjetosLegislativosSenadoStats />

      <!-- Main content -->
      <section class="py-8">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <ProjetosLegislativosSenadoFilters />
          <ProjetosLegislativosSenadoList />
        </div>
      </section>
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import ProjetosLegislativosSenadoFilters from '@/components/senado/ProjetosLegislativosSenadoFilters.vue'
import ProjetosLegislativosSenadoList from '@/components/senado/ProjetosLegislativosSenadoList.vue'
import ProjetosLegislativosSenadoStats from '@/components/senado/ProjetosLegislativosSenadoStats.vue'
import { useSenadoresStore } from '@/stores/senadores'

const store = useSenadoresStore()

onMounted(() => {
  if (store.projetosLegislativosList.length === 0) {
    store.fetchProjetosLegislativos()
  }
})
</script>
