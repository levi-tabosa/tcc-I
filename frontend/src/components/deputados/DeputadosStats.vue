<template>
  <section class="py-8 bg-muted/30">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="grid gap-6 lg:grid-cols-2">
        <!-- Gastos nos Últimos Meses -->
        <BaseCard>
          <template #header>
            <h3 class="text-lg font-semibold text-foreground">Gastos nos Últimos Meses</h3>
          </template>
          <div class="space-y-4">
            <div v-for="mes in gastosUltimosMeses" :key="mes.mes" class="flex items-center gap-4">
              <div :class="`w-3 h-3 rounded-full ${mes.color}`" />
              <div class="flex-1">
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-foreground font-medium">{{ mes.mes }}</span>
                  <span class="text-muted-foreground">{{ mes.valor }}</span>
                </div>
                <div class="h-2 bg-muted rounded-full overflow-hidden">
                  <div :class="`h-full rounded-full ${mes.color}`" :style="{ width: `${mes.percentage}%` }" />
                </div>
              </div>
            </div>
          </div>
        </BaseCard>

        <!-- Maiores Bancadas -->
        <BaseCard>
          <template #header>
            <h3 class="text-lg font-semibold text-foreground">Maiores Bancadas</h3>
          </template>
          <div class="space-y-3">
            <div v-for="(partido, index) in topPartidos" :key="partido.sigla" class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <span class="text-muted-foreground text-sm w-6">{{ index + 1 }}º</span>
                <span class="font-medium text-foreground">{{ partido.sigla }}</span>
              </div>
              <div class="flex items-center gap-2">
                <div class="w-24 h-2 bg-muted rounded-full overflow-hidden">
                  <div class="h-full bg-primary rounded-full" :style="{ width: `${(partido.deputados / 99) * 100}%` }" />
                </div>
                <span class="text-sm text-muted-foreground w-8 text-right">{{ partido.deputados }}</span>
              </div>
            </div>
          </div>
        </BaseCard>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import { partidos } from '@/data/mock-data'

const gastosUltimosMeses = [
  { mes: 'Dezembro 2025', valor: 'R$ 42,5M', color: 'bg-chart-1', percentage: 95 },
  { mes: 'Novembro 2025', valor: 'R$ 41,8M', color: 'bg-chart-2', percentage: 92 },
  { mes: 'Outubro 2025', valor: 'R$ 44,2M', color: 'bg-chart-3', percentage: 100 },
  { mes: 'Setembro 2025', valor: 'R$ 38,9M', color: 'bg-chart-4', percentage: 88 },
  { mes: 'Agosto 2025', valor: 'R$ 40,1M', color: 'bg-chart-5', percentage: 90 },
]

const topPartidos = partidos.sort((a, b) => b.deputados - a.deputados).slice(0, 6)
</script>
