<template>
  <div class="mvp-perfil">
    <AppHeader />
    
    <main class="main">
      <div class="container">
        <!-- Loading -->
        <div v-if="isLoading" class="loading">
          <p>Carregando...</p>
        </div>

        <!-- Erro -->
        <div v-else-if="error || !parlamentar" class="error">
          <h2>{{ error || 'Deputado não encontrado' }}</h2>
          <RouterLink to="/parlamentares" class="back-btn">
            ← Voltar para lista
          </RouterLink>
        </div>

        <!-- Perfil -->
        <div v-else>
          <!-- Header -->
          <div class="perfil-header">
            <div class="basic-info">
              <h1>{{ parlamentar.nome }}</h1>
              <p class="subtitle">{{ parlamentar.partido }} - {{ parlamentar.estado }}</p>
            </div>
          </div>

          <!-- Stats -->
          <div class="stats-grid">
            <div class="stat-card">
              <h3>Gastos Totais</h3>
              <p class="value">{{ formatCurrency(parlamentar.gastoTotal) }}</p>
            </div>
            
            <div class="stat-card">
              <h3>Presença</h3>
              <p class="value">{{ parlamentar.presenca }}%</p>
            </div>
            
            <div class="stat-card">
              <h3>Fidelidade</h3>
              <p class="value">{{ parlamentar.fidelidadePartidaria }}%</p>
            </div>
          </div>

          <!-- Informações Básicas -->
          <div class="section">
            <h2>Informações Básicas</h2>
            <div class="info-grid">
              <div class="info-item">
                <strong>Nome Civil:</strong>
                <span>{{ parlamentar.nome_civil || parlamentar.nome }}</span>
              </div>
              <div class="info-item">
                <strong>Cargo:</strong>
                <span>{{ parlamentar.cargo }}</span>
              </div>
              <div class="info-item">
                <strong>Partido:</strong>
                <span>{{ parlamentar.partido }}</span>
              </div>
              <div class="info-item">
                <strong>Estado:</strong>
                <span>{{ parlamentar.estado }}</span>
              </div>
              <div v-if="parlamentar.email" class="info-item">
                <strong>Email:</strong>
                <a :href="'mailto:' + parlamentar.email">{{ parlamentar.email }}</a>
              </div>
            </div>
          </div>

          <!-- Gastos Recentes -->
          <div class="section">
            <h2>Últimos Gastos</h2>
            <div v-if="parlamentar.gastosRecentes && parlamentar.gastosRecentes.length > 0" class="gastos-list">
              <div 
                v-for="gasto in parlamentar.gastosRecentes.slice(0, 5)" 
                :key="gasto.id"
                class="gasto-item"
              >
                <div class="gasto-info">
                  <p class="gasto-desc">{{ gasto.descricao }}</p>
                  <p class="gasto-data">{{ formatDate(gasto.data) }}</p>
                </div>
                <span class="gasto-valor">{{ formatCurrency(gasto.valor) }}</span>
              </div>
            </div>
            <div v-else class="empty-state">
              <p>Nenhum gasto recente encontrado.</p>
            </div>
          </div>

          <!-- Voltar -->
          <div class="actions">
            <RouterLink to="/parlamentares" class="back-btn">
              ← Voltar para lista
            </RouterLink>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import AppHeader from '../components/AppHeader.vue'
import { useMockData } from '../composables/useMockData'

const route = useRoute()
const mockData = useMockData()

const isLoading = ref(true)
const error = ref('')
const parlamentarData = ref(null)

// Tenta buscar da API real, caso falhe usa mock
const parlamentar = computed(() => {
  if (parlamentarData.value) {
    return parlamentarData.value
  }
  const id = parseInt(route.params.id as string)
  return mockData.parlamentares.value.find(p => p.id === id)
})

onMounted(async () => {
  const id = route.params.id
  
  try {
    // Tenta buscar da API real
    const response = await fetch(`http://localhost:8000/api/deputados/${id}`)
    if (response.ok) {
      const data = await response.json()
      parlamentarData.value = {
        id: data.id,
        nome: data.nome_civil,
        nome_civil: data.nome_civil,
        partido: data.partido_sigla,
        estado: data.uf_nascimento,
        cargo: 'Deputado Federal',
        email: data.email,
        gastoTotal: data.gasto_total || 0,
        presenca: data.presenca || 0,
        fidelidadePartidaria: data.fidelidade || 0,
        gastosRecentes: []
      }
    }
  } catch (err) {
    console.log('Usando dados mock (API não disponível)')
  }
  
  setTimeout(() => {
    isLoading.value = false
    if (!parlamentar.value) {
      error.value = 'Deputado não encontrado'
    }
  }, 300)
})

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('pt-BR')
}
</script>

<style scoped>
.mvp-perfil {
  min-height: 100vh;
  background: #f5f5f5;
}

.main {
  padding: 20px;
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

.loading, .error {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  margin: 40px 0;
}

.error h2 {
  color: #dc3545;
  margin-bottom: 20px;
}

.perfil-header {
  background: white;
  padding: 30px;
  border-radius: 12px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.basic-info h1 {
  font-size: 2.2rem;
  margin-bottom: 8px;
  color: #333;
}

.subtitle {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stat-card h3 {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-card .value {
  font-size: 1.8rem;
  font-weight: 700;
  color: #007bff;
}

.section {
  background: white;
  padding: 30px;
  border-radius: 12px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.section h2 {
  font-size: 1.4rem;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item strong {
  color: #555;
  font-weight: 600;
}

.info-item a {
  color: #007bff;
  text-decoration: none;
}

.info-item a:hover {
  text-decoration: underline;
}

.gastos-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.gasto-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #007bff;
}

.gasto-info {
  flex: 1;
}

.gasto-desc {
  font-weight: 600;
  margin-bottom: 4px;
  color: #333;
}

.gasto-data {
  font-size: 0.85rem;
  color: #666;
  margin: 0;
}

.gasto-valor {
  font-weight: 600;
  color: #007bff;
  font-size: 1.1rem;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.actions {
  text-align: center;
  margin-top: 40px;
}

.back-btn {
  display: inline-block;
  padding: 12px 24px;
  background: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: background-color 0.2s;
}

.back-btn:hover {
  background: #0056b3;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .gasto-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .perfil-header .basic-info h1 {
    font-size: 1.8rem;
  }
}
</style>