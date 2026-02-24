<template>
  <section class="py-12 bg-muted/30">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-2 gap-6 lg:grid-cols-4">
        <div
          v-for="metric in metrics"
          :key="metric.id"
          class="bg-card rounded-lg p-5 border border-border"
        >
          <p class="text-sm text-muted-foreground">{{ metric.label }}</p>
          <p class="mt-1 text-2xl font-bold text-foreground">{{ metric.value }}</p>
          <p class="text-xs text-muted-foreground mt-1">{{ metric.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
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
    label: "Deputados",
    value: store.generalStats ? store.generalStats.total_deputados : "--",
    description: "Câmara dos Deputados",
  },
  {
    id: 2,
    label: "Senadores",
    value: senadoresStore.generalStats ? senadoresStore.generalStats.total_senadores : "--",
    description: "Senado Federal",
  },
  {
    id: 3,
    label: "Gastos Câmara",
    value: store.generalStats
      ? formatCurrency(store.generalStats.total_gastos_12_meses)
      : "--",
    description: "Últimos 12 meses",
  },
  {
    id: 4,
    label: "Gastos Senado",
    value: senadoresStore.generalStats?.total_gastos_12_meses
      ? formatCurrency(senadoresStore.generalStats.total_gastos_12_meses)
      : "--",
    description: "Últimos 12 meses",
  }
])
</script>
