<template>
  <section class="py-16 bg-muted/30">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-foreground">Números da Câmara</h2>
        <p class="mt-2 text-muted-foreground">Dados da 57ª Legislatura</p>
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
import { Banknote, UserCheck, Shield, Users } from 'lucide-vue-next'
import { useDeputadosStore } from '@/stores/deputados'

const store = useDeputadosStore()

onMounted(() => {
  store.fetchEstatisticasGerais()
})

const metrics = computed(() => [
  {
    id: 1,
    label: "Gastos Totais",
    value: store.generalStats
      ? `R$ ${(store.generalStats.total_gastos_12_meses / 1000000).toFixed(1)}M`
      : "Carregando...",
    description: "Gastos (últimos 12 meses)",
    icon: Banknote,
    color: "text-primary",
    bgColor: "bg-primary/10"
  },
  {
    id: 2,
    label: "Presença Média",
    value: "-", // Requested to be zeroed/dashed
    description: "Sessões plenárias",
    icon: UserCheck,
    color: "text-accent",
    bgColor: "bg-accent/10"
  },
  {
    id: 3,
    label: "Fidelidade Média",
    value: "-", // Requested to be zeroed/dashed
    description: "Alinhamento partidário",
    icon: Shield,
    color: "text-chart-2",
    bgColor: "bg-chart-2/10"
  },
  {
    id: 4,
    label: "Parlamentares",
    value: store.generalStats ? store.generalStats.total_deputados : "...",
    description: "Monitorados",
    icon: Users,
    color: "text-chart-1",
    bgColor: "bg-chart-1/10"
  }
])
</script>
