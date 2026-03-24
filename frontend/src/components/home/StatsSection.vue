<template>
  <section class="py-12 bg-muted/30">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-2 gap-4 lg:grid-cols-4 lg:gap-6">
        <BaseCard
          v-for="metric in metrics"
          :key="metric.id"
          variant="flat"
          class="hover:border-primary/20"
        >
          <p class="text-sm text-muted-foreground">{{ metric.label }}</p>
          <p class="mt-1 text-2xl font-bold text-foreground">{{ metric.value }}</p>
          <p class="text-xs text-muted-foreground mt-1">{{ metric.description }}</p>
        </BaseCard>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import BaseCard from '@/components/ui/BaseCard.vue'

const deputadosTotal = ref<number | null>(null)
const senadoresTotal = ref<number | null>(null)
const gastosCamara = ref<number | null>(null)
const gastosSenado = ref<number | null>(null)

onMounted(async () => {
  const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"
  
  try {
    const [depRes, senRes, camaraGastosRes, senadoGastosRes] = await Promise.all([
      fetch(`${apiUrl}/api/camara/estatisticas`),
      fetch(`${apiUrl}/api/senado/estatisticas`),
      fetch(`${apiUrl}/api/camara/despesas/estatisticas`),
      fetch(`${apiUrl}/api/senado/despesas/estatisticas`)
    ])
    
    if (depRes.ok) {
      const depData = await depRes.json()
      deputadosTotal.value = depData.total_deputados
    }
    
    if (senRes.ok) {
      const senData = await senRes.json()
      senadoresTotal.value = senData.total_senadores
    }

    if (camaraGastosRes.ok) {
      const camaraData = await camaraGastosRes.json()
      gastosCamara.value = camaraData.total_12_meses
    }

    if (senadoGastosRes.ok) {
      const senadoData = await senadoGastosRes.json()
      gastosSenado.value = senadoData.total_12_meses
    }
  } catch (err) {
    console.error("Erro ao buscar estatísticas globais:", err)
  }
})

const formatCurrency = (value: number | undefined | null) => {
  if (value === undefined || value === null || isNaN(value)) return "--"
  
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
    value: deputadosTotal.value !== null ? deputadosTotal.value : "--",
    description: "Câmara dos Deputados",
  },
  {
    id: 2,
    label: "Senadores",
    value: senadoresTotal.value !== null ? senadoresTotal.value : "--",
    description: "Senado Federal",
  },
  {
    id: 3,
    label: "Gastos Câmara",
    value: formatCurrency(gastosCamara.value),
    description: "Últimos 12 meses",
  },
  {
    id: 4,
    label: "Gastos Senado",
    value: formatCurrency(gastosSenado.value),
    description: "Últimos 12 meses",
  }
])
</script>
