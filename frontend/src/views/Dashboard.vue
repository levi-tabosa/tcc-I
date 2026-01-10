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
              :icon="DollarSign" 
            />
            <StatCard 
              title="Presença Média" 
              :value="`${presencaMedia.toFixed(1)}%`" 
              subtitle="Sessões plenárias"
              :icon="Users" 
            />
            <StatCard 
              title="Fidelidade Média" 
              :value="`${fidelidadeMedia.toFixed(1)}%`" 
              subtitle="Alinhamento partidário"
              :icon="Award" 
            />
            <StatCard 
              title="Parlamentares" 
              :value="totalParlamentares.toString()" 
              subtitle="Monitorados"
              :icon="TrendingUp" 
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

            <!-- Distribuição Regional -->
            <div class="chart-card full-width">
              <div class="chart-header">
                <h3 class="chart-title">Distribuição por Região</h3>
                <p class="chart-description">Percentual de deputados por região do Brasil</p>
              </div>
              <div class="chart-content">
                <RegionalDistributionChart 
                  v-if="!loading && deputados.length > 0"
                  :deputados="deputados" 
                />
                <div v-else-if="loading" class="empty-state">
                  <p>Carregando dados regionais...</p>
                </div>
                <div v-else class="empty-state">
                  <p>Nenhum dado disponível. Verifique se a API está respondendo.</p>
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
import RegionalDistributionChart from '@/components/RegionalDistributionChart.vue'
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
const deputados = ref<any[]>([])

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

    // 5. Buscar lista de deputados para distribuição regional
    try {
      const deputadosResponse = await fetch('http://localhost:8000/api/deputados/')
      if (deputadosResponse.ok) {
        const data = await deputadosResponse.json()
        deputados.value = data
        console.log('Deputados carregados:', data.length)
      } else {
        console.error('Erro ao buscar deputados:', deputadosResponse.status)
      }
    } catch (err) {
      console.error('Erro na requisição de deputados:', err)
    }

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
  background: var(--bg-secondary);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: var(--text-primary);
}

.main-content {
  margin: 0 auto;
}

/* ======================
   DASHBOARD HEADER
   ====================== */
.dashboard-header-section {
  position: relative;
  padding: 3rem 0 2rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, transparent 100%);
}

.dark .dashboard-header-section {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(37, 99, 235, 0.05) 50%, transparent 100%);
}

.dashboard-header {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.dashboard-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
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
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.6;
}

/* ======================
   SEÇÃO DE KPIs
   ====================== */
.kpis-section {
  padding: 3rem 0;
  background-color: var(--bg-secondary);
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

.text-center {
  text-align: center;
}

.py-4 {
  padding-top: 1.5rem;
  padding-bottom: 1.5rem;
}

/* ======================
   SEÇÃO DE GRÁFICOS
   ====================== */
.charts-section {
  padding: 3rem 0 4rem;
  background-color: var(--surface-primary);
}

.dark .charts-section {
  background-color: var(--bg-secondary);
}

.section-title {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title h2 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.section-title p {
  font-size: 1rem;
  color: var(--text-secondary);
  margin: 0;
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* ======================
   CARDS DE GRÁFICOS
   ====================== */
.chart-card {
  background: var(--chart-bg);
  border: 1px solid var(--card-border);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
}

.chart-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.chart-card.full-width {
  grid-column: 1 / -1;
}

.chart-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--card-border);
}

.chart-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
}

.chart-description {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0;
}

.chart-content {
  padding: 0.5rem 0;
}

/* ======================
   GRÁFICOS SIMPLES
   ====================== */
.simple-chart {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chart-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.chart-label {
  min-width: 100px;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--chart-label);
  flex-shrink: 0;
}

@media (min-width: 640px) {
  .chart-label {
    min-width: 150px;
  }
}

.chart-bar {
  position: relative;
  flex: 1;
  height: 2rem;
  background-color: var(--bg-secondary);
  border-radius: 0.5rem;
  overflow: hidden;
  display: flex;
  align-items: center;
}

.dark .chart-bar {
  background-color: var(--bg-secondary);
}

.chart-fill {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  background: linear-gradient(
    90deg,
    var(--chart-fill-gradient-start),
    var(--chart-fill-gradient-end)
  );
  border-radius: 0.5rem;
  transition: width 0.6s ease-out;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.dark .chart-fill {
  box-shadow: 0 2px 4px rgba(96, 165, 250, 0.3);
}

.chart-value {
  position: relative;
  z-index: 1;
  padding: 0 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--chart-text);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* ======================
   CTA SECTION
   ====================== */
.cta-section {
  padding: 4rem 0;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, transparent 100%);
}

.dark .cta-section {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(59, 130, 246, 0.05) 50%, transparent 100%);
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
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
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.cta-description {
  font-size: 1.125rem;
  color: var(--text-secondary);
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

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;
  font-size: 1rem;
  display: inline-block;
}

.btn-secondary {
  background-color: var(--card-bg);
  color: var(--text-primary);
  border: 1px solid var(--card-border);
}

.btn-secondary:hover {
  background-color: var(--card-hover-bg);
  border-color: var(--color-primary);
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
  font-style: italic;
}
</style>