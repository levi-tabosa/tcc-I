<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1">
      <!-- Hero -->
      <section class="bg-gradient-to-br from-chart-2/10 via-background to-primary/10 py-12">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-foreground sm:text-4xl">Análises Detalhadas</h1>
          <p class="mt-2 text-muted-foreground max-w-2xl">
            Visualizações baseadas em dados reais processados
          </p>
        </div>
      </section>

      <!-- Gastos por Categoria -->
      <section class="py-12 bg-background">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 class="text-2xl font-bold text-foreground mb-3">Gastos por Categoria</h2>
          <p class="text-muted-foreground mb-8">Distribuição das despesas por tipo de serviço</p>
          <BaseCard>
            <div class="space-y-3 p-6">
              <div v-for="(categoria, index) in categorias" :key="index" class="group">
                <div class="flex items-center justify-between mb-2">
                  <div class="flex-1">
                    <p class="text-sm font-medium text-foreground group-hover:text-primary transition-colors">
                      {{ categoria.nome }}
                    </p>
                  </div>
                  <div class="ml-4 text-right">
                    <p class="text-sm font-bold text-foreground">{{ categoria.valor }}</p>
                  </div>
                </div>
                <div class="h-2 bg-muted rounded-full overflow-hidden">
                  <div
                    class="h-full bg-gradient-to-r from-primary to-chart-2 rounded-full transition-all duration-500 group-hover:from-chart-1 group-hover:to-primary"
                    :style="{ width: `${categoria.percentual}%` }"
                  ></div>
                </div>
              </div>
            </div>
          </BaseCard>
        </div>
      </section>

      <!-- Evolução Mensal de Gastos -->
      <section class="py-12 bg-muted/30">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 class="text-2xl font-bold text-foreground mb-3">Gastos nos Últimos Meses</h2>
          <p class="text-muted-foreground mb-8">Série temporal dos últimos meses registrados</p>
          <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            <BaseCard v-for="mes in mesesGastos" :key="mes.mes" hover>
              <div class="p-6">
                <div class="flex items-start gap-4">
                  <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-primary/10">
                    <TrendingUp class="h-6 w-6 text-primary" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-muted-foreground mb-1">{{ mes.titulo }}</p>
                    <p class="text-3xl font-bold text-foreground">{{ mes.valor }}</p>
                  </div>
                </div>
              </div>
            </BaseCard>
          </div>
        </div>
      </section>

      <!-- Gastos por Estado -->
      <section class="py-12 bg-background">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 class="text-2xl font-bold text-foreground mb-3">Gastos por Estado</h2>
          <p class="text-muted-foreground mb-8">Análise de despesas acumuladas por UF</p>
          <BaseCard>
            <div class="p-6">
              <div class="max-w-3xl mx-auto">
                <Pie :data="chartData" :options="chartOptions" />
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
import { TrendingUp } from 'lucide-vue-next'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Pie } from 'vue-chartjs'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import BaseCard from '@/components/ui/BaseCard.vue'

ChartJS.register(ArcElement, Tooltip, Legend)

const categorias = [
  { nome: 'DIVULGAÇÃO DA ATIVIDADE PARLAMENTAR.', valor: 'R$ 802.081.900', percentual: 100 },
  { nome: 'MANUTENÇÃO DE ESCRITÓRIO DE APOIO À ATIVIDADE PARLAMENTAR', valor: 'R$ 340.822.104', percentual: 42.5 },
  { nome: 'LOCAÇÃO OU FRETAMENTO DE VEÍCULOS AUTOMOTORES', valor: 'R$ 309.383.652', percentual: 38.6 },
  { nome: 'COMBUSTÍVEIS E LUBRIFICANTES.', valor: 'R$ 263.172.035', percentual: 32.8 },
  { nome: 'CONSULTORIAS, PESQUISAS E TRABALHOS TÉCNICOS.', valor: 'R$ 237.330.739', percentual: 29.6 },
  { nome: 'TELEFONIA', valor: 'R$ 104.914.929', percentual: 13.1 },
  { nome: 'LOCAÇÃO DE VEÍCULOS AUTOMOTORES OU FRETAMENTO DE EMBARCAÇÕES', valor: 'R$ 90.951.259', percentual: 11.3 },
  { nome: 'PASSAGEM AÉREA - REEMBOLSO', valor: 'R$ 48.372.000', percentual: 6.0 },
  { nome: 'HOSPEDAGEM ,EXCETO DO PARLAMENTAR NO DISTRITO FEDERAL.', valor: 'R$ 29.794.213', percentual: 3.7 },
  { nome: 'LOCAÇÃO OU FRETAMENTO DE AERONAVES', valor: 'R$ 25.511.421', percentual: 3.2 },
  { nome: 'SERVIÇO DE SEGURANÇA PRESTADO POR EMPRESA ESPECIALIZADA.', valor: 'R$ 19.736.109', percentual: 2.5 },
  { nome: 'FORNECIMENTO DE ALIMENTAÇÃO DO PARLAMENTAR', valor: 'R$ 15.820.379', percentual: 2.0 },
  { nome: 'SERVIÇO DE TÁXI, PEDÁGIO E ESTACIONAMENTO', valor: 'R$ 8.281.050', percentual: 1.0 },
  { nome: 'SERVIÇOS POSTAIS', valor: 'R$ 7.914.879', percentual: 1.0 },
  { nome: 'LOCOMOÇÃO, ALIMENTAÇÃO E HOSPEDAGEM', valor: 'R$ 5.589.553', percentual: 0.7 },
  { nome: 'ASSINATURA DE PUBLICAÇÕES', valor: 'R$ 2.795.812', percentual: 0.35 },
  { nome: 'LOCAÇÃO OU FRETAMENTO DE EMBARCAÇÕES', valor: 'R$ 2.042.053', percentual: 0.25 },
  { nome: 'AQUISIÇÃO OU LOC. DE SOFTWARE; SERV. POSTAIS; ASS.', valor: 'R$ 985.521', percentual: 0.12 },
  { nome: 'PASSAGENS TERRESTRES, MARÍTIMAS OU FLUVIAIS', valor: 'R$ 955.024', percentual: 0.12 },
  { nome: 'PARTICIPAÇÃO EM CURSO, PALESTRA OU EVENTO SIMILAR', valor: 'R$ 657.195', percentual: 0.08 },
  { nome: 'AQUISIÇÃO DE MATERIAL DE ESCRITÓRIO.', valor: 'R$ 564.825', percentual: 0.07 },
  { nome: 'AQUISIÇÃO DE TOKENS E CERTIFICADOS DIGITAIS', valor: 'R$ 22.506', percentual: 0.003 }
]

const mesesGastos = [
  { mes: 'Dez/2025', titulo: 'Dezembro 2025', valor: 'R$ 42,5M' },
  { mes: 'Nov/2025', titulo: 'Novembro 2025', valor: 'R$ 41,8M' },
  { mes: 'Out/2025', titulo: 'Outubro 2025', valor: 'R$ 44,2M' },
  { mes: 'Set/2025', titulo: 'Setembro 2025', valor: 'R$ 38,9M' },
  { mes: 'Ago/2025', titulo: 'Agosto 2025', valor: 'R$ 40,1M' }
]

const estados = [
  { uf: 'SP', valor: 262638502 },
  { uf: 'MG', valor: 226440719 },
  { uf: 'BA', valor: 184124059 },
  { uf: 'RJ', valor: 178609251 },
  { uf: 'RS', valor: 134913580 },
  { uf: 'PR', valor: 126752432 },
  { uf: 'PE', valor: 112713385 },
  { uf: 'CE', valor: 109887455 },
  { uf: 'MA', valor: 91084619 },
  { uf: 'GO', valor: 89228162 },
  { uf: 'PA', valor: 80188671 },
  { uf: 'PB', valor: 60240034 },
  { uf: 'SC', valor: 58771100 },
  { uf: 'PI', valor: 53242480 },
  { uf: 'RR', valor: 49036509 },
  { uf: 'AC', valor: 46609379 },
  { uf: 'AP', valor: 45999723 },
  { uf: 'AL', valor: 45336123 },
  { uf: 'ES', valor: 44889313 },
  { uf: 'RO', valor: 43428965 },
  { uf: 'TO', valor: 42229409 },
  { uf: 'SE', valor: 41779840 },
  { uf: 'MS', valor: 39833962 },
  { uf: 'AM', valor: 39728252 },
  { uf: 'MT', valor: 38929387 },
  { uf: 'RN', valor: 36422479 },
  { uf: 'DF', valor: 34641369 }
]

// Generate colors for all states
const generateColors = (count: number) => {
  const colors = [
    'rgba(59, 130, 246, 0.8)',   // blue
    'rgba(16, 185, 129, 0.8)',   // green
    'rgba(245, 158, 11, 0.8)',   // amber
    'rgba(239, 68, 68, 0.8)',    // red
    'rgba(139, 92, 246, 0.8)',   // purple
    'rgba(236, 72, 153, 0.8)',   // pink
    'rgba(20, 184, 166, 0.8)',   // teal
    'rgba(251, 146, 60, 0.8)',   // orange
    'rgba(34, 197, 94, 0.8)',    // emerald
    'rgba(168, 85, 247, 0.8)',   // violet
  ]
  const result = []
  for (let i = 0; i < count; i++) {
    result.push(colors[i % colors.length])
  }
  return result
}

const chartData = {
  labels: estados.map(e => e.uf),
  datasets: [
    {
      label: 'Gastos',
      data: estados.map(e => e.valor),
      backgroundColor: generateColors(estados.length),
      borderColor: 'rgba(255, 255, 255, 1)',
      borderWidth: 2,
    }
  ]
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      position: 'right' as const,
      labels: {
        padding: 15,
        font: {
          size: 12
        },
        generateLabels: (chart: any) => {
          const data = chart.data
          if (data.labels.length && data.datasets.length) {
            return data.labels.map((label: string, i: number) => {
              const value = data.datasets[0].data[i]
              const formattedValue = new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
              }).format(value)
              
              return {
                text: `${label}: ${formattedValue}`,
                fillStyle: data.datasets[0].backgroundColor[i],
                hidden: false,
                index: i
              }
            })
          }
          return []
        }
      }
    },
    tooltip: {
      callbacks: {
        label: function(context: any) {
          const label = context.label || ''
          const value = context.parsed
          const formattedValue = new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          }).format(value)
          
          // Calculate percentage
          const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0)
          const percentage = ((value / total) * 100).toFixed(1)
          
          return `${label}: ${formattedValue} (${percentage}%)`
        }
      }
    }
  }
}
</script>
