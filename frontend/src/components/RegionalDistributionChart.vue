<template>
  <div class="chart-container">
    <Pie :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  Title
} from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend, Title)

interface Props {
  distribuicao: Array<{
    name: string
    value: number
  }>
}

const props = defineProps<Props>()

// Mapa de cores por região
const coresPorRegiao: Record<string, string> = {
  'Sudeste': '#3b82f6',    // Azul
  'Nordeste': '#f97316',   // Laranja
  'Sul': '#1e3a8a',        // Azul escuro
  'Norte': '#10b981',      // Verde
  'Centro-Oeste': '#8b5cf6' // Roxo
}

// Calcula percentuais
const distribuicaoComPercentual = computed(() => {
  const total = props.distribuicao.reduce((sum, item) => sum + item.value, 0)
  
  return props.distribuicao.map(item => ({
    ...item,
    percentual: total > 0 ? ((item.value / total) * 100).toFixed(1) : '0.0'
  }))
})

const chartData = computed(() => ({
  labels: distribuicaoComPercentual.value.map(d => `${d.name}: ${d.percentual}%`),
  datasets: [
    {
      data: distribuicaoComPercentual.value.map(d => d.value),
      backgroundColor: distribuicaoComPercentual.value.map(d => coresPorRegiao[d.name] || '#6b7280'),
      borderColor: '#ffffff',
      borderWidth: 2
    }
  ]
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      position: 'right' as const,
      labels: {
        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary') || '#1f2937',
        padding: 15,
        font: {
          size: 13,
          family: 'Inter, system-ui, sans-serif'
        },
        usePointStyle: true,
        pointStyle: 'circle'
      }
    },
    title: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: function(context: any) {
          const item = distribuicaoComPercentual.value[context.dataIndex]
          return `${item.value} deputados (${item.percentual}%)`
        }
      }
    }
  }
}))
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  padding: 1rem;
}
</style>
