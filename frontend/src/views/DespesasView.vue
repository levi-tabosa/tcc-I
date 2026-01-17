<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1">
      <!-- Hero -->
      <section class="bg-gradient-to-br from-primary/10 via-background to-accent/10 py-12">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-foreground sm:text-4xl">Despesas e Gastos</h1>
          <p class="mt-2 text-muted-foreground max-w-2xl">
            Acompanhe como os deputados federais utilizam a cota parlamentar. Totais, rankings e análises por bloco ideológico.
          </p>
        </div>
      </section>

      <!-- Overview -->
      <section class="py-8 bg-muted/30">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <BaseCard v-for="stat in overviewStats" :key="stat.label" hover>
              <div class="flex items-center gap-4">
                <div :class="`p-3 rounded-xl ${stat.bgColor}`">
                  <component :is="stat.icon" :class="`h-6 w-6 ${stat.color}`" />
                </div>
                <div>
                  <p class="text-sm text-muted-foreground">{{ stat.label }}</p>
                  <p class="text-2xl font-bold text-foreground">{{ stat.value }}</p>
                </div>
              </div>
            </BaseCard>
          </div>
        </div>
      </section>

      <!-- Gastos por Bloco -->
      <section class="py-8">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 class="text-2xl font-bold text-foreground mb-6">Gastos por Bloco Ideológico</h2>
          <div class="grid gap-6 lg:grid-cols-2">
            <BaseCard>
              <div class="h-[300px] flex items-center justify-center">
                <div class="w-48 h-48 relative">
                  <svg viewBox="0 0 100 100" class="transform -rotate-90">
                    <circle cx="50" cy="50" r="40" fill="none" stroke="currentColor" stroke-width="20" class="text-chart-3" stroke-dasharray="125.6 251.2" />
                    <circle cx="50" cy="50" r="40" fill="none" stroke="currentColor" stroke-width="20" class="text-chart-2" stroke-dasharray="94.2 251.2" stroke-dashoffset="-125.6" />
                    <circle cx="50" cy="50" r="40" fill="none" stroke="currentColor" stroke-width="20" class="text-chart-4" stroke-dasharray="31.4 251.2" stroke-dashoffset="-219.8" />
                  </svg>
                  <div class="absolute inset-0 flex items-center justify-center">
                    <div class="text-center">
                      <p class="text-2xl font-bold text-foreground">R$ 647M</p>
                      <p class="text-xs text-muted-foreground">Total</p>
                    </div>
                  </div>
                </div>
              </div>
              <div class="flex justify-center gap-6 mt-4">
                <div class="flex items-center gap-2">
                  <div class="w-3 h-3 rounded-full bg-chart-3" />
                  <span class="text-sm text-muted-foreground">Direita (48%)</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-3 h-3 rounded-full bg-chart-2" />
                  <span class="text-sm text-muted-foreground">Centro (29%)</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-3 h-3 rounded-full bg-chart-4" />
                  <span class="text-sm text-muted-foreground">Esquerda (23%)</span>
                </div>
              </div>
            </BaseCard>

            <div class="space-y-4">
              <BaseCard v-for="(bloco, index) in gastosPorBloco" :key="bloco.bloco" hover>
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-4">
                    <div class="w-4 h-12 rounded" :style="{ backgroundColor: ['#2563eb', '#ffd700', '#dc2626'][index] }" />
                    <div>
                      <h3 class="font-semibold text-foreground">{{ bloco.bloco }}</h3>
                      <p class="text-sm text-muted-foreground">{{ ((bloco.valor / 647000000) * 100).toFixed(1) }}% do total</p>
                    </div>
                  </div>
                  <p class="text-2xl font-bold text-foreground">R$ {{ (bloco.valor / 1000000).toFixed(0) }}M</p>
                </div>
              </BaseCard>
            </div>
          </div>
        </div>
      </section>

      <!-- Categorias -->
      <section class="py-8 bg-muted/30">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 class="text-2xl font-bold text-foreground mb-6">Gastos por Categoria</h2>
          <div class="grid gap-4 md:grid-cols-2">
            <BaseCard v-for="categoria in categoriasDespesas" :key="categoria.nome">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-medium text-foreground">{{ categoria.nome }}</span>
                <span class="text-sm text-muted-foreground">R$ {{ (categoria.total / 1000000).toFixed(0) }}M</span>
              </div>
              <div class="h-2 bg-muted rounded-full overflow-hidden">
                <div
                  class="h-full bg-primary rounded-full"
                  :style="{ width: `${(categoria.total / 127000000) * 100}%` }"
                />
              </div>
            </BaseCard>
          </div>
        </div>
      </section>
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { Banknote, Users, Building2, TrendingUp } from 'lucide-vue-next'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import { statsGerais, gastosPorBloco, categoriasDespesas } from '@/data/mock-data'

const overviewStats = [
  { label: "Total de Gastos", value: `R$ ${(statsGerais.totalGastos / 1000000).toFixed(0)}M`, icon: Banknote, color: "text-primary", bgColor: "bg-primary/10" },
  { label: "Média por Deputado", value: `R$ ${(statsGerais.mediaGastoDeputado / 1000).toFixed(0)}K`, icon: Users, color: "text-accent", bgColor: "bg-accent/10" },
  { label: "Empresas Contratadas", value: statsGerais.totalEmpresas.toLocaleString(), icon: Building2, color: "text-chart-2", bgColor: "bg-chart-2/10" },
  { label: "Deputados c/ Auxílio", value: statsGerais.deputadosComAuxilio.toString(), icon: TrendingUp, color: "text-chart-4", bgColor: "bg-chart-4/10" },
]
</script>
