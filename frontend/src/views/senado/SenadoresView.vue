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

      <!-- Em breve -->
      <section class="section-content">
        <div class="mx-auto max-w-2xl px-4 sm:px-6 lg:px-8">
          <BaseCard class="text-center py-16">
            <div class="relative inline-flex p-5 rounded-full bg-purple-500/10 mb-6">
              <Users class="h-14 w-14 text-purple-500" />
              <span class="absolute top-1 right-1 flex h-4 w-4">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-4 w-4 bg-purple-500"></span>
              </span>
            </div>
            <h2 class="text-2xl font-bold text-foreground mb-3">Em Desenvolvimento</h2>
            <p class="text-muted-foreground max-w-md mx-auto mb-6">
              Estamos trabalhando para trazer os dados do Senado Federal. 
              Em breve você poderá acompanhar os gastos e atividades dos senadores.
            </p>
            <div class="flex items-center justify-center gap-2 text-sm text-muted-foreground">
              <div class="flex gap-1">
                <div class="h-2 w-2 rounded-full bg-purple-500 animate-pulse"></div>
                <div class="h-2 w-2 rounded-full bg-purple-400 animate-pulse animate-delay-100"></div>
                <div class="h-2 w-2 rounded-full bg-purple-300 animate-pulse animate-delay-200"></div>
              </div>
              <span>Integração em andamento</span>
            </div>
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
