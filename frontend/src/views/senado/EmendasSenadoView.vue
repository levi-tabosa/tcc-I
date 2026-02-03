<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1">
      <!-- Hero -->
      <section class="bg-gradient-to-br from-purple-500/10 via-background to-accent/10 py-12">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-foreground sm:text-4xl">Emendas do Senado</h1>
          <p class="mt-2 text-muted-foreground max-w-2xl">
            Acompanhe as emendas parlamentares dos senadores.
          </p>
        </div>
      </section>

      <!-- Em breve -->
      <section class="py-16">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <BaseCard class="text-center py-12">
            <div class="inline-flex p-4 rounded-full bg-purple-500/10 mb-4">
              <Landmark class="h-12 w-12 text-purple-500" />
            </div>
            <h2 class="text-2xl font-bold text-foreground mb-2">Em Breve</h2>
            <p class="text-muted-foreground max-w-md mx-auto">
              Os dados de emendas do Senado Federal estarão disponíveis em breve.
            </p>
          </BaseCard>
        </div>
      </section>
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { Landmark } from 'lucide-vue-next'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
</script>
