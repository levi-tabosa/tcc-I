<template>
  <section class="py-16 bg-muted/30">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-foreground">Números do Congresso</h2>
        <p class="mt-2 text-muted-foreground">Câmara dos Deputados e Senado Federal</p>
      </div>

      <!-- Métricas Principais -->
      <div class="grid grid-cols-2 gap-6 lg:grid-cols-4">
        <div
          v-for="(metric, index) in metrics"
          :key="metric.id"
          class="relative group bg-card rounded-2xl p-6 shadow-sm border border-border hover:shadow-lg transition-all duration-300 hover:-translate-y-1 animate-fade-in-up"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div :class="`inline-flex p-3 rounded-xl ${metric.bgColor} mb-4`">
            <component :is="metric.icon" :class="`h-6 w-6 ${metric.color}`" />
          </div>
          <div class="text-3xl font-bold text-foreground">{{ metric.value }}</div>
          <p class="mt-1 text-sm text-muted-foreground">{{ metric.label }}</p>
          <p class="text-xs text-muted-foreground mt-1">{{ metric.description }}</p>

          <!-- Decorative corner -->
          <div class="absolute top-0 right-0 w-16 h-16 overflow-hidden rounded-tr-2xl">
            <div :class="`absolute -top-8 -right-8 w-16 h-16 rotate-45 ${metric.bgColor} opacity-50`" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { Banknote, Building2, Landmark, Users } from 'lucide-vue-next'
import { useDeputadosStore } from '@/stores/deputados'
import { useSenadoresStore } from '@/stores/senadores'

const store = useDeputadosStore()
const senadoresStore = useSenadoresStore()

onMounted(() => {
  store.fetchEstatisticasGerais()
  senadoresStore.fetchEstatisticasGerais()
})

const formatCurrency = (value: number) => {
  if (value >= 1000000000) {
    return `R$ ${(value / 1000000000).toFixed(1)}B`
  }
  if (value >= 1000000) {
    return `R$ ${(value / 1000000).toFixed(0)}M`
  }
  return `R$ ${(value / 1000).toFixed(0)}K`
}

const metrics = computed(() => [
  {
    id: 1,
    label: "Deputados Federais",
    value: store.generalStats ? store.generalStats.total_deputados : "--", // Usar dado real ou --
    description: "Câmara dos Deputados",
    icon: Building2,
    color: "text-primary",
    bgColor: "bg-primary/10"
  },
  {
    id: 2,
    label: "Senadores",
    value: "81", // Valor fixo por enquanto, pois não tem endpoint
    description: "Senado Federal",
    icon: Landmark,
    color: "text-purple-500",
    bgColor: "bg-purple-500/10"
  },
  {
    id: 3,
    label: "Gastos Câmara",
    value: store.generalStats
      ? formatCurrency(store.generalStats.total_gastos_12_meses)
      : "--",
    description: "Últimos 12 meses",
    icon: Banknote,
    color: "text-chart-2",
    bgColor: "bg-chart-2/10"
  },
  {
    id: 4,
    label: "Gastos Senado",
    value: senadoresStore.generalStats?.total_gastos_12_meses
      ? formatCurrency(senadoresStore.generalStats.total_gastos_12_meses)
      : "--",
    description: "Últimos 12 meses",
    icon: Banknote,
    color: "text-purple-500",
    bgColor: "bg-purple-500/10"
  }
])
</script>
