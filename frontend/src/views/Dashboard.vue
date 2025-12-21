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
          <!-- Estado de Carregamento nos KPIs -->
          <div v-if="loading" class="text-center py-4">Sincronizando indicadores...</div>
          
          <div v-else class="stats-grid">
            <StatCard 
              title="Gastos Totais" 
              :value="formatCurrency(totalGastos)" 
              subtitle="Acumulado total"
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
              :value="totalParlamentares.toString()" 
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
            <p v-if="loading">Buscando dados oficiais na base de dados...</p>
            <p v-else>Visualizações baseadas em dados reais processados</p>
          </div>
          
          <div v-if="!loading" class="charts-grid">
            <!-- Gastos por Categoria -->
            <div class="chart-card full-width">
              <div class="chart-header">
                <h3 class="chart-title">Gastos por Categoria</h3>
                <p class="chart-description">Distribuição das despesas por tipo de serviço</p>
              </div>
              <div class="chart-content">
                <div class="simple-chart">
                  <div v-for="(item, index) in gastosPorCategoria" :key="index" class="chart-item">
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

            <!-- Evolução Mensal (Baseado na sua imagem de 12 meses) -->
            <div class="chart-card full-width">
              <div class="chart-header">
                <h3 class="chart-title">Evolução Mensal de Gastos</h3>
                <p class="chart-description">Série temporal dos últimos 12 meses registrados</p>
              </div>
              <div class="chart-content">
                <div class="simple-chart">
                  <div v-for="(item, index) in gastosMensais" :key="index" class="chart-item">
                    <div class="chart-label">{{ item.label }}</div>
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

            <!-- Gastos por Estado -->
            <div class="chart-card full-width">
              <div class="chart-header">
                <h3 class="chart-title">Gastos por Estado</h3>
                <p class="chart-description">Ranking de despesas acumuladas por UF</p>
              </div>
              <div class="chart-content">
                <div class="simple-chart">
                  <div v-for="(item, index) in gastosPorEstado" :key="index" class="chart-item">
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
        </div>
      </section>

      <!-- Call to Action -->
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
import { ref, computed, onMounted } from 'vue'
import AppFooter from '@/components/AppFooter.vue'
import StatCard from '@/components/StatCard.vue'
import { BarChart3, TrendingUp, Users, DollarSign, Award } from 'lucide-vue-next'

// --- ESTADOS REATIVOS ---
const loading = ref(true)
const totalGastos = ref(0)
const totalParlamentares = ref(0)
const presencaMedia = ref(0)
const fidelidadeMedia = ref(0)

const gastosPorCategoria = ref<any[]>([])
const gastosMensais = ref<any[]>([])
const gastosPorEstado = ref<any[]>([])

// --- LÓGICA DE BUSCA DE DADOS ---
const fetchDashboardData = async () => {
  loading.value = true
  try {
    const response = await fetch('http://localhost:8000/api/deputados/estatisticas/geral')
    if (!response.ok) throw new Error('Falha ao buscar dados')
    
    const data = await response.json()

    // 1. Preenchendo KPIs
    totalGastos.value = data.total_gastos
    totalParlamentares.value = data.total_parlamentares
    presencaMedia.value = data.presenca_media || 0
    fidelidadeMedia.value = data.fidelidade_media || 0

    // 2. Gráfico de Categorias
    gastosPorCategoria.value = data.gastos_por_categoria

    // 3. Gráfico de Estados
    gastosPorEstado.value = data.gastos_por_estado

    // 4. Evolução Mensal (Tratando a imagem que você mandou)
    const mesesNomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
    // Invertemos a ordem (reverse) para que o mês 10/2024 apareça antes do mês 09/2025
    gastosMensais.value = data.gastos_por_mes.map((item: any) => ({
      label: `${mesesNomes[item.mes - 1]}/${item.ano}`,
      valor: item.valor
    })).reverse()

  } catch (error) {
    console.error("Erro na integração com backend:", error)
  } finally {
    loading.value = false
  }
}

// --- CÁLCULOS DE PROPORÇÃO PARA AS BARRAS ---
const maxGastosCategoria = computed(() => 
  Math.max(...gastosPorCategoria.value.map(i => i.valor), 1)
)

const maxGastosMensal = computed(() => 
  Math.max(...gastosMensais.value.map(i => i.valor), 1)
)

const maxGastosEstado = computed(() => 
  Math.max(...gastosPorEstado.value.map(i => i.valor), 1)
)

// --- FORMATAÇÃO ---
const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    maximumFractionDigits: 0
  }).format(value)
}

onMounted(() => {
  fetchDashboardData()
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
```