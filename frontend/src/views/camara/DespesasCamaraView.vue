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

      <!-- Gastos por Partido -->
      <section class="py-8">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 class="text-2xl font-bold text-foreground mb-6">Gastos por Partido</h2>
          
          <div class="grid gap-6 lg:grid-cols-2">
            <!-- Gráfico de pizza com todos os partidos -->
            <BaseCard>
              <div class="h-[400px] flex items-center justify-center">
                <div class="w-56 h-56 relative">
                  <svg viewBox="0 0 100 100" class="transform -rotate-90">
                    <circle 
                      v-for="(segment, index) in allPieSegments" 
                      :key="index"
                      cx="50" 
                      cy="50" 
                      r="40" 
                      fill="none" 
                      stroke="currentColor" 
                      stroke-width="20" 
                      :class="segment.colorClass" 
                      :stroke-dasharray="`${segment.dashArray} 251.2`"
                      :stroke-dashoffset="segment.dashOffset"
                    />
                  </svg>
                  <div class="absolute inset-0 flex items-center justify-center">
                    <div class="text-center">
                      <p class="text-2xl font-bold text-foreground">{{ totalGastosFormatado }}</p>
                      <p class="text-xs text-muted-foreground">Total</p>
                    </div>
                  </div>
                </div>
              </div>
              <div class="mt-4 max-h-32 overflow-y-auto">
                <div class="grid grid-cols-2 gap-2">
                  <div v-for="(partido, index) in todosPartidos.slice(0, 10)" :key="partido.partido" class="flex items-center gap-2">
                    <div :class="`w-2 h-2 rounded-full ${getBgColorClass(index)}`" />
                    <span class="text-xs text-muted-foreground truncate">{{ partido.partido }} ({{ partido.percentual }}%)</span>
                  </div>
                </div>
              </div>
            </BaseCard>

            <!-- Lista de todos os partidos -->
            <div class="space-y-3 max-h-[500px] overflow-y-auto pr-2">
              <BaseCard v-for="(partido, index) in todosPartidos" :key="partido.partido" hover class="transition-all">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3 flex-1">
                    <div :class="`w-3 h-10 rounded ${getBgColorClass(index)}`" />
                    <div class="flex-1 min-w-0">
                      <h3 class="font-semibold text-foreground truncate">{{ partido.partido }}</h3>
                      <p class="text-xs text-muted-foreground">{{ partido.percentual }}% do total</p>
                    </div>
                  </div>
                  <p class="text-lg font-bold text-foreground ml-2">{{ partido.valorFormatado }}</p>
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
                <span class="text-sm text-muted-foreground">R$ {{ (categoria.total / 1000000).toFixed(1) }}M</span>
              </div>
              <div class="h-2 bg-muted rounded-full overflow-hidden">
                <div
                  class="h-full bg-primary rounded-full"
                  :style="{ width: `${categoria.percentual}%` }"
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
import { onMounted, computed } from 'vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import { useDeputadosStore } from '@/stores/deputados'

const store = useDeputadosStore()

onMounted(() => {
  store.fetchEstatisticasGerais()
  store.fetchCategorias()
})

const todosPartidos = computed(() => {
  if (!store.generalStats?.gastos_por_partido) return []
  
  const totalGeral = store.generalStats.gastos_por_partido.reduce((sum, p) => sum + p.valor, 0)
  
  return store.generalStats.gastos_por_partido.map(p => ({
    partido: p.partido,
    valor: p.valor,
    valorFormatado: p.valor >= 1000000 
      ? `R$ ${(p.valor / 1000000).toFixed(1)}M`
      : `R$ ${(p.valor / 1000).toFixed(0)}K`,
    percentual: ((p.valor / totalGeral) * 100).toFixed(1)
  }))
})

const allPieSegments = computed(() => {
  if (!todosPartidos.value.length) return []
  
  const circumference = 251.2
  let currentOffset = 0
  
  return todosPartidos.value.map((partido, index) => {
    const percentage = parseFloat(partido.percentual)
    const dashArray = (percentage / 100) * circumference
    const segment = {
      colorClass: getStrokeColorClass(index),
      dashArray: dashArray.toFixed(1),
      dashOffset: -currentOffset
    }
    currentOffset += dashArray
    return segment
  })
})

const getBgColorClass = (index: number) => {
  const colors = [
    'bg-chart-1', 'bg-chart-2', 'bg-chart-3', 'bg-chart-4', 'bg-chart-5',
    'bg-primary', 'bg-accent', 'bg-red-500', 'bg-blue-500', 'bg-green-500',
    'bg-yellow-500', 'bg-purple-500', 'bg-pink-500', 'bg-indigo-500', 'bg-teal-500',
    'bg-orange-500', 'bg-cyan-500', 'bg-lime-500', 'bg-amber-500', 'bg-emerald-500'
  ]
  return colors[index % colors.length]
}

const getStrokeColorClass = (index: number) => {
  const textColors = [
    'text-chart-1', 'text-chart-2', 'text-chart-3', 'text-chart-4', 'text-chart-5',
    'text-primary', 'text-accent', 'text-red-500', 'text-blue-500', 'text-green-500',
    'text-yellow-500', 'text-purple-500', 'text-pink-500', 'text-indigo-500', 'text-teal-500',
    'text-orange-500', 'text-cyan-500', 'text-lime-500', 'text-amber-500', 'text-emerald-500'
  ]
  return textColors[index % textColors.length]
}


const totalGastosFormatado = computed(() => {
  if (!store.generalStats?.gastos_por_partido) return 'R$ 0'
  const total = store.generalStats.gastos_por_partido.reduce((sum, p) => sum + p.valor, 0)
  return `R$ ${(total / 1000000).toFixed(0)}M`
})

const categoriasDespesas = computed(() => {
  if (!store.categorias.length) return []
  
  const maxValor = Math.max(...store.categorias.map(c => c.valor))
  
  return store.categorias.map(c => ({
    nome: c.categoria,
    total: c.valor,
    percentual: (c.valor / maxValor) * 100
  }))
})

const overviewStats = computed(() => [
  { 
    label: "Total de Gastos", 
    value: store.generalStats 
      ? `R$ ${(store.generalStats.total_gastos / 1000000).toFixed(0)}M` 
      : "Carregando...", 
    icon: Banknote, 
    color: "text-primary", 
    bgColor: "bg-primary/10" 
  },
  { 
    label: "Média por Deputado", 
    value: store.generalStats && store.generalStats.total_deputados > 0
      ? `R$ ${(store.generalStats.total_gastos / store.generalStats.total_deputados / 1000).toFixed(0)}K`
      : "Carregando...", 
    icon: Users, 
    color: "text-accent", 
    bgColor: "bg-accent/10" 
  },
  { 
    label: "Empresas Contratadas", 
    value: store.generalStats 
      ? store.generalStats.total_empresas_contratadas.toLocaleString()
      : "Carregando...", 
    icon: Building2, 
    color: "text-chart-2", 
    bgColor: "bg-chart-2/10" 
  },
  { 
    label: "Deputados c/ Auxílio", 
    value: '--', 
    icon: TrendingUp, 
    color: "text-chart-4", 
    bgColor: "bg-chart-4/10" 
  },
])
</script>
