<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1">
      <!-- Hero -->
      <section class="bg-gradient-to-br from-primary/10 via-background to-accent/10 py-12">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-foreground sm:text-4xl">Projetos Legislativos</h1>
          <p class="mt-2 text-muted-foreground max-w-2xl">
            Acompanhe os projetos de lei, PECs, medidas provisórias e outros projetos legislativos apresentados pelos deputados.
          </p>
        </div>
      </section>

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
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import ProjetosLegislativosFilters from '@/components/projetosLegislativos/ProjetosLegislativosFilters.vue'
import ProjetosLegislativosList from '@/components/projetosLegislativos/ProjetosLegislativosList.vue'
import ProjetosLegislativosStats from '@/components/projetosLegislativos/ProjetosLegislativosStats.vue'
</script>
