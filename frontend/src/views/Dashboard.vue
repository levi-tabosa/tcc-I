<template>
  <div class="mvp-dashboard">
    <AppHeader />
    
    <main class="main">
      <div class="container">
        <!-- Header -->
        <div class="header">
          <h1>Dashboard</h1>
          <p>Visão geral dos dados parlamentares</p>
        </div>

        <!-- Stats Grid -->
        <div class="stats-grid">
          <div class="stat-card">
            <h3>Gastos Totais</h3>
            <p class="value">{{ formatCurrency(totalGastos) }}</p>
            <small>Últimos 12 meses</small>
          </div>
          
          <div class="stat-card">
            <h3>Presença Média</h3>
            <p class="value">{{ presencaMedia }}%</p>
            <small>Sessões plenárias</small>
          </div>
          
          <div class="stat-card">
            <h3>Deputados</h3>
            <p class="value">{{ parlamentares.length }}</p>
            <small>Monitorados</small>
          </div>
          
          <div class="stat-card">
            <h3>Partidos</h3>
            <p class="value">{{ partidosUnicos.length }}</p>
            <small>Diferentes</small>
          </div>
        </div>

        <!-- Top Gastos -->
        <div class="section">
          <h2>Maiores Gastos</h2>
          <div class="ranking">
            <div 
              v-for="(deputado, index) in topGastos" 
              :key="deputado.id"
              class="ranking-item"
            >
              <span class="position">{{ index + 1 }}º</span>
              <div class="info">
                <RouterLink :to="'/perfil/' + deputado.id" class="name">
                  {{ deputado.nome }}
                </RouterLink>
                <p class="party">{{ deputado.partido }} - {{ deputado.estado }}</p>
              </div>
              <span class="value">{{ formatCurrency(deputado.gastoTotal) }}</span>
            </div>
          </div>
        </div>

        <!-- Top Presença -->
        <div class="section">
          <h2>Maior Presença</h2>
          <div class="ranking">
            <div 
              v-for="(deputado, index) in topPresenca" 
              :key="deputado.id"
              class="ranking-item"
            >
              <span class="position">{{ index + 1 }}º</span>
              <div class="info">
                <RouterLink :to="'/perfil/' + deputado.id" class="name">
                  {{ deputado.nome }}
                </RouterLink>
                <p class="party">{{ deputado.partido }} - {{ deputado.estado }}</p>
              </div>
              <span class="value">{{ deputado.presenca }}%</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import AppHeader from '../components/AppHeader.vue'
import { useMockData } from '../composables/useMockData'

const mockData = useMockData()
const parlamentares = mockData.parlamentares

// Stats computadas
const totalGastos = computed(() => {
  return parlamentares.value.reduce((total, p) => total + p.gastoTotal, 0)
})

const presencaMedia = computed(() => {
  const total = parlamentares.value.reduce((sum, p) => sum + p.presenca, 0)
  return Math.round(total / parlamentares.value.length)
})

const partidosUnicos = computed(() => {
  return [...new Set(parlamentares.value.map(p => p.partido))]
})

// Rankings
const topGastos = computed(() => {
  return [...parlamentares.value]
    .sort((a, b) => b.gastoTotal - a.gastoTotal)
    .slice(0, 5)
})

const topPresenca = computed(() => {
  return [...parlamentares.value]
    .sort((a, b) => b.presenca - a.presenca)
    .slice(0, 5)
})

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    notation: 'compact'
  }).format(value)
}
</script>

<style scoped>
.mvp-dashboard {
  min-height: 100vh;
  background: #f5f5f5;
}

.main {
  padding: 20px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

.header {
  margin-bottom: 40px;
  text-align: center;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: #333;
}

.header p {
  color: #666;
  font-size: 1.1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 50px;
}

.stat-card {
  background: white;
  padding: 25px 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stat-card h3 {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 10px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-card .value {
  font-size: 1.8rem;
  font-weight: 700;
  color: #007bff;
  margin-bottom: 5px;
}

.stat-card small {
  color: #888;
  font-size: 0.8rem;
}

.section {
  margin-bottom: 50px;
}

.section h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #333;
}

.ranking {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.ranking-item {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
}

.ranking-item:last-child {
  border-bottom: none;
}

.ranking-item:hover {
  background: #f8f9fa;
}

.position {
  width: 40px;
  font-weight: 700;
  color: #007bff;
  font-size: 1.1rem;
}

.info {
  flex: 1;
  margin-left: 15px;
}

.name {
  font-weight: 600;
  color: #007bff;
  text-decoration: none;
  font-size: 1rem;
}

.name:hover {
  text-decoration: underline;
}

.party {
  margin: 2px 0 0 0;
  color: #666;
  font-size: 0.85rem;
}

.value {
  font-weight: 600;
  color: #333;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .ranking-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .position {
    width: auto;
  }
  
  .info {
    margin-left: 0;
  }
}
</style>