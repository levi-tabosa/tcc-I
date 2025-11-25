<template>
  <div class="page-wrapper">
    
    <main class="main-content">
      <!-- Dashboard Header -->
      <section class="dashboard-header-section">
        <div class="container">
          <div class="dashboard-header">
            <h1 class="dashboard-title">Dashboard Geral</h1>
            <p class="dashboard-subtitle">Visão consolidada dos indicadores parlamentares</p>
          </div>
        </div>
      </section>

      <!-- KPI Section -->
      <section class="kpis-section">
        <div class="container">
          <div class="stats-grid">
            <StatCard 
              title="Gastos Totais" 
              :value="formatCurrency(totalGastos)" 
              subtitle="Últimos 12 meses"
              icon="DollarSign" 
            />
            <StatCard 
              title="Presença Média" 
              :value="`${presencaMedia.toFixed(1)}%`" 
              subtitle="Sessões plenárias"
              icon="Users" 
            />
            <StatCard 
              title="Fidelidade Média" 
              :value="`${fidelidadeMedia.toFixed(1)}%`" 
              subtitle="Alinhamento partidário"
              icon="Award" 
            />
            <StatCard 
              title="Parlamentares" 
              :value="parlamentares.length.toString()" 
              subtitle="Monitorados"
              icon="TrendingUp" 
            />
          </div>
        </div>
      </section>

      <!-- Charts Section -->
      <section class="charts-section">
        <div class="container">
          <div class="section-title">
            <h2>Análises Detalhadas</h2>
            <p>Visualizações e insights dos dados parlamentares</p>
          </div>
          
          <div class="charts-grid">
            <!-- Gastos por Categoria -->
            <div class="chart-card">
              <div class="chart-header">
                <h3 class="chart-title">Gastos por Categoria</h3>
                <p class="chart-description">Distribuição das despesas parlamentares</p>
              </div>
              <div class="chart-content">
                <div class="simple-chart">
                  <div v-for="(item, index) in gastosPorCategoriaMock" :key="index" class="chart-item">
                    <div class="chart-label">{{ item.categoria }}</div>
                    <div class="chart-bar">
                      <div 
                        class="chart-fill" 
                        :style="{ width: (item.valor / maxGastosCategoria * 100) + '%' }"
                      ></div>
                      <span class="chart-value">{{ formatCurrency(item.valor) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Evolução Mensal -->
            <div class="chart-card">
              <div class="chart-header">
                <h3 class="chart-title">Evolução Mensal de Gastos</h3>
                <p class="chart-description">Série temporal dos últimos 12 meses</p>
              </div>
              <div class="chart-content">
                <div class="simple-chart">
                  <div v-for="(item, index) in gastosMensaisMock" :key="index" class="chart-item">
                    <div class="chart-label">{{ item.mes }}</div>
                    <div class="chart-bar">
                      <div 
                        class="chart-fill" 
                        :style="{ width: (item.valor / maxGastosMensal * 100) + '%' }"
                      ></div>
                      <span class="chart-value">{{ formatCurrency(item.valor) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Top 10 Gastadores -->
            <div class="chart-card">
              <div class="chart-header">
                <h3 class="chart-title">Top 10 Gastadores</h3>
                <p class="chart-description">Parlamentares com maiores despesas</p>
              </div>
              <div class="chart-content">
                <div class="simple-chart">
                  <div v-for="(item, index) in top10Gastadores.slice(0, 10)" :key="index" class="chart-item">
                    <div class="chart-label">{{ item.nome }}</div>
                    <div class="chart-bar">
                      <div 
                        class="chart-fill" 
                        :style="{ width: (item.gastoTotal / maxGastoTotal * 100) + '%' }"
                      ></div>
                      <span class="chart-value">{{ formatCurrency(item.gastoTotal) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Gastos por Estado -->
            <div class="chart-card">
              <div class="chart-header">
                <h3 class="chart-title">Gastos por Estado</h3>
                <p class="chart-description">Top 10 estados com maiores despesas</p>
              </div>
              <div class="chart-content">
                <div class="simple-chart">
                  <div v-for="(item, index) in gastosPorEstadoMock" :key="index" class="chart-item">
                    <div class="chart-label">{{ item.estado }}</div>
                    <div class="chart-bar">
                      <div 
                        class="chart-fill" 
                        :style="{ width: (item.valor / maxGastosEstado * 100) + '%' }"
                      ></div>
                      <span class="chart-value">{{ formatCurrency(item.valor) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Coesão Partidária - Full Width -->
          <div class="chart-card full-width">
            <div class="chart-header">
              <h3 class="chart-title">Coesão Partidária</h3>
              <p class="chart-description">Índice de fidelidade por partido</p>
            </div>
            <div class="chart-content">
              <div class="simple-chart">
                <div v-for="(item, index) in coesaoPartidariaMock" :key="index" class="chart-item">
                  <div class="chart-label">{{ item.partido }}</div>
                  <div class="chart-bar">
                    <div 
                      class="chart-fill" 
                      :style="{ width: item.coesao + '%' }"
                    ></div>
                    <span class="chart-value">{{ item.coesao }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Call to Action Section -->
      <section class="cta-section">
        <div class="container">
          <div class="cta-content">
            <BarChart3 class="cta-icon" />
            <h2 class="cta-title">Explore os Dados</h2>
            <p class="cta-description">
              Acesse perfis individuais dos parlamentares ou explore outras análises detalhadas
            </p>
            <div class="cta-actions">
              <router-link to="/metodologia" class="btn btn-secondary">
                Metodologia
              </router-link>
            </div>
          </div>
        </div>
      </section>
    </main>
    
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import AppFooter from '@/components/AppFooter.vue'
import StatCard from '@/components/StatCard.vue'
import { BarChart3, TrendingUp, Users, DollarSign } from 'lucide-vue-next'

// Minimal reactive list of parlamentares (keep for computed values)
const parlamentares = ref<any[]>([])

// Chart refs
const gastosCategoria = ref<HTMLElement>()
const gastosMensais = ref<HTMLElement>()
const topGastadores = ref<HTMLElement>()
const gastosEstado = ref<HTMLElement>()
const coesaoPartidaria = ref<HTMLElement>()

// Computed values
const totalGastos = computed(() => 
  parlamentares.value.reduce((sum, p) => sum + p.gastoTotal, 0)
)

const presencaMedia = computed(() => 
  parlamentares.value.length > 0 
    ? parlamentares.value.reduce((sum, p) => sum + p.presenca, 0) / parlamentares.value.length 
    : 0
)

const fidelidadeMedia = computed(() =>
  parlamentares.value.length > 0
    ? parlamentares.value.reduce((sum, p) => sum + p.fidelidadePartidaria, 0) / parlamentares.value.length
    : 0
)

const top10Gastadores = computed(() => 
  [...parlamentares.value]
    .sort((a, b) => b.gastoTotal - a.gastoTotal)
    .slice(0, 10)
    .map(p => ({ nome: p.nome_civil, gastoTotal: p.gastoTotal }))
)

// Computed values for chart maximums
const maxGastosCategoria = computed(() => 
  Math.max(...gastosPorCategoriaMock.map(item => item.valor))
)

const maxGastosMensal = computed(() => 
  Math.max(...gastosMensaisMock.map(item => item.valor))
)

const maxGastoTotal = computed(() => 
  top10Gastadores.value.length > 0 
    ? Math.max(...top10Gastadores.value.map(item => item.gastoTotal))
    : 1
)

const maxGastosEstado = computed(() => 
  Math.max(...gastosPorEstadoMock.map(item => item.valor))
)

// Mock data for charts
const gastosPorCategoriaMock = [
  { categoria: 'Passagens', valor: 450000 },
  { categoria: 'Hospedagem', valor: 320000 },
  { categoria: 'Alimentação', valor: 180000 },
  { categoria: 'Combustível', valor: 150000 },
  { categoria: 'Telefonia', valor: 80000 }
]

const gastosMensaisMock = [
  { mes: 'Jan', valor: 120000 },
  { mes: 'Fev', valor: 135000 },
  { mes: 'Mar', valor: 145000 },
  { mes: 'Abr', valor: 125000 },
  { mes: 'Mai', valor: 160000 },
  { mes: 'Jun', valor: 180000 },
  { mes: 'Jul', valor: 155000 },
  { mes: 'Ago', valor: 170000 },
  { mes: 'Set', valor: 165000 },
  { mes: 'Out', valor: 175000 },
  { mes: 'Nov', valor: 185000 },
  { mes: 'Dez', valor: 190000 }
]

const gastosPorEstadoMock = [
  { estado: 'SP', valor: 850000 },
  { estado: 'RJ', valor: 720000 },
  { estado: 'MG', valor: 650000 },
  { estado: 'RS', valor: 580000 },
  { estado: 'PR', valor: 520000 },
  { estado: 'BA', valor: 480000 },
  { estado: 'SC', valor: 420000 },
  { estado: 'GO', valor: 380000 },
  { estado: 'PE', valor: 350000 },
  { estado: 'CE', valor: 320000 }
]

const coesaoPartidariaMock = [
  { partido: 'PT', coesao: 92 },
  { partido: 'PL', coesao: 88 },
  { partido: 'PSDB', coesao: 85 },
  { partido: 'MDB', coesao: 82 },
  { partido: 'PP', coesao: 80 },
  { partido: 'PDT', coesao: 78 },
  { partido: 'PSB', coesao: 75 },
  { partido: 'REPUBLICANOS', coesao: 72 }
]

// Format currency function
const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 0,
  }).format(value)
}

// Chart initialization functions (simplified - no ECharts dependency)
const initGastosCategoriaChart = () => {
  // Chart rendered with CSS bars
}

const initGastosMensaisChart = () => {
  // Chart rendered with CSS bars
}

const initTopGastadoresChart = () => {
  // Chart rendered with CSS bars
}

const initGastosEstadoChart = () => {
  // Chart rendered with CSS bars
}

const initCoesaoPartidaria = () => {
  // Chart rendered with CSS bars
}

onMounted(() => {
  // Inicializar gráficos locais (mock data)
  initGastosCategoriaChart()
  initGastosMensaisChart()
  initTopGastadoresChart()
  initGastosEstadoChart()
  initCoesaoPartidaria()
})
</script>

<style scoped>
/* ======================
   ESTRUTURA GERAL 
   ====================== */
.page-wrapper {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc, #f1f5f9);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: var(--color-gray-900);
}

.main-content {
  margin: 0 auto;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

@media (min-width: 640px) {
  .container {
    padding: 0 1.5rem;
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 0 2rem;
  }
}

/* ======================
   NAVIGATION HEADER 
   ====================== */
.dashboard-header-section {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, transparent 100%);
  padding: 3rem 0;
}

.dashboard-header {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.dashboard-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--color-gray-900);
  margin-bottom: 1rem;
  line-height: 1.2;
  letter-spacing: -0.025em;
}

@media (min-width: 768px) {
  .dashboard-title {
    font-size: 3rem;
  }
}

.dashboard-subtitle {
  font-size: 1.125rem;
  color: var(--color-gray-600);
  margin: 0;
  line-height: 1.6;
}

/* ======================
   SEÇÃO KPIS 
   ====================== */
.kpis-section {
  padding: 3rem 0;
  background-color: var(--color-white);
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

@media (min-width: 640px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* ======================
   SEÇÃO CHARTS 
   ====================== */
.charts-section {
  padding: 4rem 0;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, transparent 100%);
}

.section-title {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title h2 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: 0.75rem;
}

.section-title p {
  color: var(--color-gray-600);
  font-size: 1.125rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

@media (min-width: 768px) {
  .charts-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.chart-card {
  background: var(--color-white);
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid var(--color-gray-200);
  overflow: hidden;
  transition: all 0.2s ease;
}

.chart-card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

.chart-card.full-width {
  grid-column: 1 / -1;
}

.chart-header {
  padding: 1.5rem 1.5rem 0 1.5rem;
}

.chart-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-gray-900);
  margin: 0 0 0.5rem 0;
}

.chart-description {
  color: var(--color-gray-600);
  font-size: 0.875rem;
  margin: 0;
}

.chart-content {
  padding: 1rem 1.5rem 1.5rem 1.5rem;
}

.chart-container {
  width: 100%;
  height: 300px;
}

/* ======================
   SEÇÃO CTA 
   ====================== */
.cta-section {
  padding: 4rem 0;
  background-color: var(--color-white);
}

.cta-content {
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.cta-icon {
  width: 3rem;
  height: 3rem;
  color: var(--color-primary);
  margin: 0 auto 1.5rem;
}

.cta-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: 1rem;
}

.cta-description {
  font-size: 1.125rem;
  color: var(--color-gray-600);
  margin-bottom: 2rem;
  line-height: 1.6;
}

.cta-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

@media (min-width: 640px) {
  .cta-actions {
    flex-direction: row;
    justify-content: center;
  }
}

/* ======================
   BOTÕES 
   ====================== */
.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;
  font-size: 1rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-primary {
  background-color: var(--color-primary);
  color: var(--color-white);
}

.btn-primary:hover {
  background-color: var(--color-primary-dark);
}

.btn-secondary {
  background-color: var(--color-white);
  color: var(--color-gray-700);
  border: 1px solid var(--color-gray-300);
}

.btn-secondary:hover {
  background-color: var(--color-gray-50);
}

/* ======================
   SIMPLE CHARTS STYLES 
   ====================== */
.simple-chart {
  padding: 1rem;
}

.chart-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

.chart-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-gray-700);
  margin-bottom: 0.5rem;
}

.chart-bar {
  position: relative;
  background-color: var(--color-gray-200);
  border-radius: 0.5rem;
  height: 2rem;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.chart-fill {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  height: 100%;
  border-radius: 0.5rem;
  transition: width 0.5s ease;
  min-width: 2px;
}

.chart-value {
  position: absolute;
  right: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-gray-700);
  background-color: rgba(255, 255, 255, 0.9);
  padding: 0.125rem 0.5rem;
  border-radius: 0.25rem;
  backdrop-filter: blur(4px);
}

/* ======================
   RESPONSIVIDADE 
   ====================== */
@media (max-width: 640px) {
  .dashboard-title {
    font-size: 2rem;
  }
  
  .dashboard-header-section {
    padding: 2rem 0;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    height: 250px;
  }
}

@media (max-width: 768px) {
  .charts-section {
    padding: 2rem 0;
  }
  
  .kpis-section {
    padding: 2rem 0;
  }
  
  .cta-section {
    padding: 2rem 0;
  }
}

/* ======================
   THEME VARIABLES OVERRIDE
   ====================== */
.chart-card {
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
</style>
