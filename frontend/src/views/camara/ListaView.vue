<template>
  <div class="min-h-screen flex flex-col">
    <main class="flex-1">
      <!-- Hero -->
      <section class="bg-gradient-to-br from-primary/10 via-background to-accent/10 py-12">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-foreground sm:text-4xl">Deputados</h1>
          <p class="mt-2 text-muted-foreground max-w-2xl">
            Conheça todos os deputados. Filtre por partido, estado ou região.
          </p>
        </div>
      </section>

      <!-- Stats -->
      <Stats />

      <!-- Main Content -->
      <section class="py-12">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <Filters />
          <List />
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import Filters from '@/components/camara/Filters.vue'
import List from '@/components/camara/List.vue'
import Stats from '@/components/camara/Stats.vue'
</script>
