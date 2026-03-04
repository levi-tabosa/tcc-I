<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1">
      <!-- Hero -->
      <section class="bg-gradient-to-br from-purple-500/10 via-background to-accent/10 py-12">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-foreground sm:text-4xl">Senadores</h1>
          <p class="mt-2 text-muted-foreground max-w-2xl">
            Conheça os senadores da República. Filtre por partido, estado ou região.
          </p>
        </div>
      </section>

      <!-- Main content -->
      <section class="py-8">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <SenadoresFilters />
          <SenadoresList />
        </div>
      </section>
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import SenadoresFilters from '@/components/senado/SenadoresFilters.vue'
import SenadoresList from '@/components/senado/SenadoresList.vue'
</script>
