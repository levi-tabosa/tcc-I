<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1">
      <!-- Hero -->
      <section class="bg-gradient-to-br from-accent/10 via-background to-primary/10 py-12">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-foreground sm:text-4xl">Emendas Parlamentares</h1>
          <p class="mt-2 text-muted-foreground max-w-2xl">
            Acompanhe a distribuição de emendas parlamentares. Veja rankings por deputado, área e município.
          </p>
        </div>
      </section>

      <!-- Overview -->
      <section class="py-8 bg-muted/30">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <BaseCard hover>
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-xl bg-primary/10">
                  <Users class="h-6 w-6 text-primary" />
                </div>
                <div>
                  <p class="text-sm text-muted-foreground">Deputados com Emendas</p>
                  <p class="text-2xl font-bold text-foreground">487</p>
                </div>
              </div>
            </BaseCard>
            <BaseCard hover>
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-xl bg-accent/10">
                  <Landmark class="h-6 w-6 text-accent" />
                </div>
                <div>
                  <p class="text-sm text-muted-foreground">Municípios Beneficiados</p>
                  <p class="text-2xl font-bold text-foreground">4,832</p>
                </div>
              </div>
            </BaseCard>
            <BaseCard hover class="sm:col-span-2 lg:col-span-1">
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-xl bg-chart-2/10">
                  <TrendingUp class="h-6 w-6 text-chart-2" />
                </div>
                <div>
                  <p class="text-sm text-muted-foreground">Áreas Contempladas</p>
                  <p class="text-2xl font-bold text-foreground">12</p>
                </div>
              </div>
            </BaseCard>
          </div>
        </div>
      </section>

      <!-- Áreas -->
      <section class="py-8">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 class="text-2xl font-bold text-foreground mb-6">Distribuição por Área</h2>
          <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            <BaseCard v-for="area in areasEmendas" :key="area.nome" hover>
              <div class="flex items-center justify-between mb-2">
                <span class="font-medium text-foreground">{{ area.nome }}</span>
                <span class="text-lg font-bold text-accent">{{ area.percentual }}%</span>
              </div>
              <div class="h-3 bg-muted rounded-full overflow-hidden mb-2">
                <div class="h-full bg-accent rounded-full" :style="{ width: `${area.percentual}%` }" />
              </div>
              <p class="text-sm text-muted-foreground">R$ {{ (area.valor / 1000000).toFixed(0) }}M</p>
            </BaseCard>
          </div>
        </div>
      </section>

      <!-- Ranking -->
      <section class="py-8 bg-muted/30">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 class="text-2xl font-bold text-foreground mb-6">Top 10 Deputados em Emendas</h2>
          <BaseCard>
            <div class="space-y-4">
              <div
                v-for="(deputado, index) in topDeputadosEmendas"
                :key="deputado.id"
                class="flex items-center gap-4 p-3 rounded-lg hover:bg-muted/50 transition-colors"
              >
                <span class="text-lg font-bold text-muted-foreground w-8">{{ index + 1 }}º</span>
                <div class="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center text-primary font-semibold">
                  {{ deputado.nome.charAt(0) }}
                </div>
                <div class="flex-1">
                  <p class="font-medium text-foreground">{{ deputado.nome }}</p>
                  <p class="text-sm text-muted-foreground">{{ deputado.partido }} - {{ deputado.estado }}</p>
                </div>
                <p class="text-lg font-bold text-accent">R$ {{ (deputado.emendasTotal / 1000000).toFixed(1) }}M</p>
              </div>
            </div>
          </BaseCard>
        </div>
      </section>
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { Landmark, Users, TrendingUp } from 'lucide-vue-next'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import { areasEmendas, deputados } from '@/data/mock-data'

const topDeputadosEmendas = deputados.sort((a, b) => b.emendasTotal - a.emendasTotal).slice(0, 10)
</script>
