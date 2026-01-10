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
  deputados: Array<{
    uf: string
    [key: string]: any
  }>
}

const props = defineProps<Props>()

// Mapeamento de estados para regiões
const estadosPorRegiao: Record<string, string[]> = {
  'Sudeste': ['SP', 'RJ', 'MG', 'ES'],
  'Nordeste': ['BA', 'CE', 'PE', 'MA', 'PB', 'RN', 'AL', 'SE', 'PI'],
  'Sul': ['RS', 'SC', 'PR'],
  'Norte': ['AM', 'PA', 'AC', 'RO', 'RR', 'AP', 'TO'],
  'Centro-Oeste': ['GO', 'MT', 'MS', 'DF']
}

// Calcula a distribuição por região
const distribuicaoPorRegiao = computed(() => {
  const contagem: Record<string, number> = {
    'Sudeste': 0,
    'Nordeste': 0,
    'Sul': 0,
    'Norte': 0,
    'Centro-Oeste': 0
  }

  props.deputados.forEach(deputado => {
    for (const [regiao, estados] of Object.entries(estadosPorRegiao)) {
      if (estados.includes(deputado.uf)) {
        contagem[regiao]++
        break
      }
    }
  })

  const total = Object.values(contagem).reduce((sum, val) => sum + val, 0)
  
  return Object.entries(contagem).map(([regiao, quantidade]) => ({
    regiao,
    quantidade,
    percentual: total > 0 ? ((quantidade / total) * 100).toFixed(1) : '0.0'
  }))
})

const chartData = computed(() => ({
  labels: distribuicaoPorRegiao.value.map(d => `${d.regiao}: ${d.percentual}%`),
  datasets: [
    {
      data: distribuicaoPorRegiao.value.map(d => d.quantidade),
      backgroundColor: [
        '#3b82f6', // Sudeste - Azul
        '#f97316', // Nordeste - Laranja
        '#1e3a8a', // Sul - Azul escuro
        '#10b981', // Norte - Verde
        '#8b5cf6'  // Centro-Oeste - Roxo
      ],
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
          const regiao = distribuicaoPorRegiao.value[context.dataIndex]
          return `${regiao.quantidade} deputados (${regiao.percentual}%)`
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
