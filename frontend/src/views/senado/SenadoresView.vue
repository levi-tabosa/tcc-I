<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1">
      <!-- Hero -->
      <section class="bg-gradient-to-br from-purple-500/10 via-background to-accent/10 py-12">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-foreground sm:text-4xl">Senadores</h1>
          <p class="mt-2 text-muted-foreground max-w-2xl">
            Conheça os 81 senadores da República. Filtre por partido, estado ou região.
          </p>
        </div>
      </section>

      <!-- Em breve -->
      <section class="py-16">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <BaseCard class="text-center py-12">
            <div class="inline-flex p-4 rounded-full bg-purple-500/10 mb-4">
              <Users class="h-12 w-12 text-purple-500" />
            </div>
            <h2 class="text-2xl font-bold text-foreground mb-2">Em Breve</h2>
            <p class="text-muted-foreground max-w-md mx-auto">
              Estamos trabalhando para trazer os dados do Senado Federal. 
              Em breve você poderá acompanhar os gastos e atividades dos senadores.
            </p>
          </BaseCard>
        </div>
      </section>
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { Users } from 'lucide-vue-next'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
</script>
